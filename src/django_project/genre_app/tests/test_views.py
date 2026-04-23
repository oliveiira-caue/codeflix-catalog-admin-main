from uuid import UUID, uuid4

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository


@pytest.fixture
def category_movie():
    return Category(
        name="Movie",
        description="Movie description",
    )


@pytest.fixture
def category_documentary():
    return Category(
        name="Documentary",
        description="Documentary description",
    )


@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()


@pytest.fixture
def genre_romance(category_movie, category_documentary) -> Genre:
    return Genre(
        name="Romance",
        is_active=True,
        categories={category_movie.id, category_documentary.id},
    )


@pytest.fixture
def genre_drama() -> Genre:
    return Genre(
        name="Drama",
        is_active=True,
        categories=set(),
    )


@pytest.fixture
def genre_repository() -> DjangoORMGenreRepository:
    return DjangoORMGenreRepository()


@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_request_data_is_valid_then_update_genre(
        self,
        category_repository: DjangoORMCategoryRepository,
        category_movie: Category,
        category_documentary: Category,
        genre_repository: DjangoORMGenreRepository,
        genre_romance: Genre,
    ) -> None:
        category_repository.save(category_movie)
        category_repository.save(category_documentary)
        genre_repository.save(genre_romance)

        url = f"/api/genres/{str(genre_romance.id)}/"
        data = {
            "name": "Drama",
            "is_active": True,
            "categories": [category_documentary.id],
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        updated_genre = genre_repository.get_by_id(genre_romance.id)
        assert updated_genre.name == "Drama"
        assert updated_genre.is_active is True
        assert updated_genre.categories == {category_documentary.id}

    def test_when_request_data_is_invalid_then_return_400(
        self,
        genre_repository: DjangoORMGenreRepository,
        genre_drama: Genre,
    ) -> None:
        genre_repository.save(genre_drama)

        url = f"/api/genres/{str(genre_drama.id)}/"
        data = {
            "name": "",
            "is_active": True,
            "categories": [],
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"name": ["This field may not be blank."]}

    def test_when_related_categories_do_not_exist_then_return_400(
        self,
        category_repository: DjangoORMCategoryRepository,
        category_movie: Category,
        category_documentary: Category,
        genre_repository: DjangoORMGenreRepository,
        genre_romance: Genre,
    ) -> None:
        category_repository.save(category_movie)
        category_repository.save(category_documentary)
        genre_repository.save(genre_romance)

        url = f"/api/genres/{str(genre_romance.id)}/"
        data = {
            "name": "Romance",
            "is_active": True,
            "categories": [uuid4()],
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Categories with provided IDs not found" in response.data["error"]

    def test_when_genre_does_not_exist_then_return_404(self) -> None:
        url = f"/api/genres/{str(uuid4())}/"
        data = {
            "name": "Romance",
            "is_active": True,
            "categories": [],
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_404_NOT_FOUND
