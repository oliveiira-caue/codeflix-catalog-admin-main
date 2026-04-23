from rest_framework.test import APITestCase

from src.core.category.domain.category import Category
from django_project.category_app.repository import DjangoORMCategoryRepository


class TestListCategoryApi(APITestCase):
    def test_list_categories(self):
        category_movie = Category(
            name="Movie",
            description="Movie description",
        )
        category_documentary = Category(
            name="Documentary",
            description="Documenatry description",
        )

        repository = DjangoORMCategoryRepository()
        repository.save(category_movie)
        repository.save(category_documentary)

        url = "/api/categories/"
        response = self.client.get(url)

        expected_data = [
            {
                "id": str(category_movie.id),
                "name": category_movie.name,
                "description": category_movie.description,
                "is_active": category_movie.is_active
            },
            {
                "id": str(category_documentary.id),
                "name": category_documentary.name,
                "description": category_documentary.description,
                "is_active": category_documentary.is_active
            }
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)


class TestPartialUpdateCategoryApi(APITestCase):
    def setUp(self):
        self.repository = DjangoORMCategoryRepository()
        self.category = Category(
            name="Movie",
            description="Movie description",
            is_active=True,
        )
        self.repository.save(self.category)

    def test_partial_update_only_name(self):
        url = f"/api/categories/{self.category.id}/"
        response = self.client.patch(url, data={"name": "Series"}, format="json")

        self.assertEqual(response.status_code, 200)

        updated = self.repository.get_by_id(self.category.id)
        self.assertEqual(updated.name, "Series")
        self.assertEqual(updated.description, "Movie description")
        self.assertEqual(updated.is_active, True)

    def test_partial_update_only_description(self):
        url = f"/api/categories/{self.category.id}/"
        response = self.client.patch(url, data={"description": "Updated desc"}, format="json")

        self.assertEqual(response.status_code, 200)

        updated = self.repository.get_by_id(self.category.id)
        self.assertEqual(updated.name, "Movie")
        self.assertEqual(updated.description, "Updated desc")
        self.assertEqual(updated.is_active, True)

    def test_partial_update_only_is_active(self):
        url = f"/api/categories/{self.category.id}/"
        response = self.client.patch(url, data={"is_active": False}, format="json")

        self.assertEqual(response.status_code, 200)

        updated = self.repository.get_by_id(self.category.id)
        self.assertEqual(updated.name, "Movie")
        self.assertEqual(updated.description, "Movie description")
        self.assertEqual(updated.is_active, False)

    def test_partial_update_returns_404_for_nonexistent_category(self):
        import uuid
        url = f"/api/categories/{uuid.uuid4()}/"
        response = self.client.patch(url, data={"name": "Ghost"}, format="json")

        self.assertEqual(response.status_code, 404)
