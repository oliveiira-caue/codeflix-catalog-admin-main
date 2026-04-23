from uuid import UUID

from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from src.core.cast_member.application.create_cast_member import CreateCastMember
from src.core.cast_member.application.delete_cast_member import DeleteCastMember
from src.core.cast_member.application.exceptions import CastMemberNotFound, InvalidCastMember
from src.core.cast_member.application.list_cast_member import ListCastMember
from src.core.cast_member.application.update_cast_member import UpdateCastMember
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.cast_member_app.serializers import (
    CreateCastMemberInputSerializer,
    CreateCastMemberOutputSerializer,
    DeleteCastMemberInputSerializer,
    ListCastMemberOutputSerializer,
    UpdateCastMemberInputSerializer,
)


class CastMemberViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        use_case = ListCastMember(repository=DjangoORMCastMemberRepository())
        output = use_case.execute(ListCastMember.Input())
        serializer = ListCastMemberOutputSerializer(output)
        return Response(status=HTTP_200_OK, data=serializer.data)

    def create(self, request: Request) -> Response:
        serializer = CreateCastMemberInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = CreateCastMember(repository=DjangoORMCastMemberRepository())
        try:
            output = use_case.execute(CreateCastMember.Input(**serializer.validated_data))
        except InvalidCastMember as error:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={"error": str(error)},
            )

        return Response(
            status=HTTP_201_CREATED,
            data=CreateCastMemberOutputSerializer(output).data,
        )

    def update(self, request: Request, pk: UUID = None) -> Response:
        serializer = UpdateCastMemberInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = UpdateCastMember(repository=DjangoORMCastMemberRepository())
        try:
            use_case.execute(UpdateCastMember.Input(
                id=pk,
                name=serializer.validated_data["name"],
                type=serializer.validated_data["type"],
            ))
        except CastMemberNotFound:
            return Response(status=HTTP_404_NOT_FOUND)
        except InvalidCastMember as error:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={"error": str(error)},
            )

        return Response(status=HTTP_204_NO_CONTENT)

    def destroy(self, request: Request, pk: UUID = None) -> Response:
        serializer = DeleteCastMemberInputSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        use_case = DeleteCastMember(repository=DjangoORMCastMemberRepository())
        try:
            use_case.execute(DeleteCastMember.Input(**serializer.validated_data))
        except CastMemberNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_204_NO_CONTENT)
