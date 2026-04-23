from uuid import UUID, uuid4

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository


@pytest.fixture
def cast_member_actor() -> CastMember:
    return CastMember(
        name="John Doe",
        type=CastMemberType.ACTOR,
    )


@pytest.fixture
def cast_member_director() -> CastMember:
    return CastMember(
        name="Jane Doe",
        type=CastMemberType.DIRECTOR,
    )


@pytest.fixture
def repository() -> DjangoORMCastMemberRepository:
    return DjangoORMCastMemberRepository()


@pytest.mark.django_db
class TestListAPI:
    def test_list_cast_members(
        self,
        repository: DjangoORMCastMemberRepository,
        cast_member_actor: CastMember,
        cast_member_director: CastMember,
    ) -> None:
        repository.save(cast_member_actor)
        repository.save(cast_member_director)

        url = "/api/cast_members/"
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 2
        assert response.data["data"][0]["id"] == str(cast_member_actor.id)
        assert response.data["data"][0]["name"] == "John Doe"
        assert response.data["data"][0]["type"] == "ACTOR"


@pytest.mark.django_db
class TestCreateAPI:
    def test_when_request_data_is_valid_then_create_cast_member(
        self,
        repository: DjangoORMCastMemberRepository,
    ) -> None:
        url = "/api/cast_members/"
        data = {
            "name": "John Doe",
            "type": "ACTOR",
        }
        response = APIClient().post(url, data=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"]

        saved_cast_member = repository.get_by_id(UUID(response.data["id"]))
        assert saved_cast_member is not None
        assert saved_cast_member.name == "John Doe"
        assert saved_cast_member.type == CastMemberType.ACTOR

    def test_when_request_data_is_invalid_then_return_400(self) -> None:
        url = "/api/cast_members/"
        data = {
            "name": "",
            "type": "INVALID",
        }
        response = APIClient().post(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_request_data_is_valid_then_update_cast_member(
        self,
        repository: DjangoORMCastMemberRepository,
        cast_member_actor: CastMember,
    ) -> None:
        repository.save(cast_member_actor)

        url = f"/api/cast_members/{str(cast_member_actor.id)}/"
        data = {
            "name": "Jane Doe",
            "type": "DIRECTOR",
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        updated = repository.get_by_id(cast_member_actor.id)
        assert updated.name == "Jane Doe"
        assert updated.type == CastMemberType.DIRECTOR

    def test_when_cast_member_does_not_exist_then_return_404(self) -> None:
        url = f"/api/cast_members/{str(uuid4())}/"
        data = {
            "name": "Jane Doe",
            "type": "DIRECTOR",
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_when_request_data_is_invalid_then_return_400(
        self,
        repository: DjangoORMCastMemberRepository,
        cast_member_actor: CastMember,
    ) -> None:
        repository.save(cast_member_actor)

        url = f"/api/cast_members/{str(cast_member_actor.id)}/"
        data = {
            "name": "",
            "type": "DIRECTOR",
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestDeleteAPI:
    def test_when_cast_member_exists_then_delete(
        self,
        repository: DjangoORMCastMemberRepository,
        cast_member_actor: CastMember,
    ) -> None:
        repository.save(cast_member_actor)

        url = f"/api/cast_members/{str(cast_member_actor.id)}/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert repository.get_by_id(cast_member_actor.id) is None

    def test_when_cast_member_does_not_exist_then_return_404(self) -> None:
        url = f"/api/cast_members/{str(uuid4())}/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
