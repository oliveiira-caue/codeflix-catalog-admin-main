import uuid
from unittest.mock import create_autospec

import pytest

from src.core.cast_member.application.create_cast_member import CreateCastMember
from src.core.cast_member.application.delete_cast_member import DeleteCastMember
from src.core.cast_member.application.exceptions import CastMemberNotFound, InvalidCastMember
from src.core.cast_member.application.list_cast_member import ListCastMember
from src.core.cast_member.application.update_cast_member import UpdateCastMember
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository


class TestCreateCastMember:
    def test_create_with_valid_data(self):
        repo = InMemoryCastMemberRepository()
        use_case = CreateCastMember(repository=repo)
        output = use_case.execute(CreateCastMember.Input(name="John Doe", type=CastMemberType.ACTOR))
        assert output.id is not None
        assert repo.get_by_id(output.id) is not None

    def test_create_with_invalid_name_raises_invalid_cast_member(self):
        repo = InMemoryCastMemberRepository()
        use_case = CreateCastMember(repository=repo)
        with pytest.raises(InvalidCastMember):
            use_case.execute(CreateCastMember.Input(name="", type=CastMemberType.ACTOR))


class TestListCastMember:
    def test_list_returns_empty_when_no_cast_members(self):
        repo = InMemoryCastMemberRepository()
        use_case = ListCastMember(repository=repo)
        output = use_case.execute(ListCastMember.Input())
        assert output.data == []

    def test_list_returns_existing_cast_members(self):
        cm = CastMember(name="John", type=CastMemberType.ACTOR)
        repo = InMemoryCastMemberRepository(cast_members=[cm])
        use_case = ListCastMember(repository=repo)
        output = use_case.execute(ListCastMember.Input())
        assert len(output.data) == 1
        assert output.data[0].id == cm.id
        assert output.data[0].name == "John"
        assert output.data[0].type == CastMemberType.ACTOR


class TestUpdateCastMember:
    def test_update_existing_cast_member(self):
        cm = CastMember(name="John", type=CastMemberType.ACTOR)
        repo = InMemoryCastMemberRepository(cast_members=[cm])
        use_case = UpdateCastMember(repository=repo)
        use_case.execute(UpdateCastMember.Input(id=cm.id, name="Jane", type=CastMemberType.DIRECTOR))
        updated = repo.get_by_id(cm.id)
        assert updated.name == "Jane"
        assert updated.type == CastMemberType.DIRECTOR

    def test_update_nonexistent_cast_member_raises_not_found(self):
        repo = InMemoryCastMemberRepository()
        use_case = UpdateCastMember(repository=repo)
        with pytest.raises(CastMemberNotFound):
            use_case.execute(UpdateCastMember.Input(
                id=uuid.uuid4(), name="Jane", type=CastMemberType.DIRECTOR
            ))

    def test_update_with_invalid_name_raises_invalid_cast_member(self):
        cm = CastMember(name="John", type=CastMemberType.ACTOR)
        repo = InMemoryCastMemberRepository(cast_members=[cm])
        use_case = UpdateCastMember(repository=repo)
        with pytest.raises(InvalidCastMember):
            use_case.execute(UpdateCastMember.Input(id=cm.id, name="", type=CastMemberType.ACTOR))


class TestDeleteCastMember:
    def test_delete_existing_cast_member(self):
        cm = CastMember(name="John", type=CastMemberType.ACTOR)
        repo = InMemoryCastMemberRepository(cast_members=[cm])
        use_case = DeleteCastMember(repository=repo)
        use_case.execute(DeleteCastMember.Input(id=cm.id))
        assert repo.get_by_id(cm.id) is None

    def test_delete_nonexistent_cast_member_raises_not_found(self):
        repo = InMemoryCastMemberRepository()
        use_case = DeleteCastMember(repository=repo)
        with pytest.raises(CastMemberNotFound):
            use_case.execute(DeleteCastMember.Input(id=uuid.uuid4()))
