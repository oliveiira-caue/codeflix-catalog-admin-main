from uuid import UUID

from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from django_project.category_app.repository import DjangoORMCategoryRepository
from django_project.category_app.serializers import UpdateCategoryRequestSerializer
from src.core.category.application.list_category import ListCategory, ListCategoryRequest
from src.core.category.application.update_category import UpdateCategory, UpdateCategoryRequest
from src.core.category.application.exceptions import CategoryNotFound


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        input = ListCategoryRequest()

        use_case = ListCategory(repository=DjangoORMCategoryRepository())
        output = use_case.execute(input)

        categories = [
            {
                "id": str(category.id),
                "name": category.name,
                "description": category.description,
                "is_active": category.is_active,
            } for category in output.data
        ]

        return Response(
            status=HTTP_200_OK,
            data=categories,
        )

    def update(self, request: Request, pk: UUID = None) -> Response:
        serializer = UpdateCategoryRequestSerializer(data={
            **request.data,
            "id": pk,
        })

        serializer.is_valid(raise_exception=True)

        try:
            use_case = UpdateCategory(repository=DjangoORMCategoryRepository())
            use_case.execute(UpdateCategoryRequest(
                id=serializer.validated_data["id"],
                name=serializer.validated_data.get("name"),
                description=serializer.validated_data.get("description"),
                is_active=serializer.validated_data.get("is_active"),
            ))
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_200_OK)

    def partial_update(self, request: Request, pk: UUID = None) -> Response:
        serializer = UpdateCategoryRequestSerializer(data={
            **request.data,
            "id": pk,
        }, partial=True)

        serializer.is_valid(raise_exception=True)

        try:
            use_case = UpdateCategory(repository=DjangoORMCategoryRepository())
            use_case.execute(UpdateCategoryRequest(
                id=serializer.validated_data["id"],
                name=serializer.validated_data.get("name"),
                description=serializer.validated_data.get("description"),
                is_active=serializer.validated_data.get("is_active"),
            ))
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_200_OK)