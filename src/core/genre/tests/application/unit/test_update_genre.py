import uuid
from unittest.mock import create_autospec

import pytest

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.exceptions import GenreNotFound, InvalidGenre, RelatedCategoriesNotFound
from src.core.genre.application.update_genre import UpdateGenre, UpdateGenreRequest
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


class TestUpdateGenre:
    def test_when_genre_does_not_exist_then_raise_genre_not_found(self):
        mock_genre_repo = create_autospec(GenreRepository)
        mock_genre_repo.get_by_id.return_value = None

        mock_category_repo = create_autospec(CategoryRepository)

        use_case = UpdateGenre(
            repository=mock_genre_repo,
            category_repository=mock_category_repo,
        )

        with pytest.raises(GenreNotFound, match="not found"):
            use_case.execute(UpdateGenreRequest(
                id=uuid.uuid4(),
                name="Drama",
            ))

    def test_when_genre_name_is_invalid_then_raise_invalid_genre(self):
        existing_genre = Genre(name="Romance")

        mock_genre_repo = create_autospec(GenreRepository)
        mock_genre_repo.get_by_id.return_value = existing_genre

        mock_category_repo = create_autospec(CategoryRepository)
        mock_category_repo.list.return_value = []

        use_case = UpdateGenre(
            repository=mock_genre_repo,
            category_repository=mock_category_repo,
        )

        with pytest.raises(InvalidGenre):
            use_case.execute(UpdateGenreRequest(
                id=existing_genre.id,
                name="",
            ))

    def test_when_related_categories_do_not_exist_then_raise_related_categories_not_found(self):
        existing_genre = Genre(name="Romance")
        non_existent_category_id = uuid.uuid4()

        mock_genre_repo = create_autospec(GenreRepository)
        mock_genre_repo.get_by_id.return_value = existing_genre

        mock_category_repo = create_autospec(CategoryRepository)
        mock_category_repo.list.return_value = []

        use_case = UpdateGenre(
            repository=mock_genre_repo,
            category_repository=mock_category_repo,
        )

        with pytest.raises(RelatedCategoriesNotFound):
            use_case.execute(UpdateGenreRequest(
                id=existing_genre.id,
                name="Drama",
                categories={non_existent_category_id},
            ))

    def test_when_genre_is_valid_then_update_is_called(self):
        existing_genre = Genre(name="Romance")
        category = Category(name="Movie")

        mock_genre_repo = create_autospec(GenreRepository)
        mock_genre_repo.get_by_id.return_value = existing_genre

        mock_category_repo = create_autospec(CategoryRepository)
        mock_category_repo.list.return_value = [category]

        use_case = UpdateGenre(
            repository=mock_genre_repo,
            category_repository=mock_category_repo,
        )

        use_case.execute(UpdateGenreRequest(
            id=existing_genre.id,
            name="Drama",
            is_active=False,
            categories={category.id},
        ))

        mock_genre_repo.update.assert_called_once_with(existing_genre)
        assert existing_genre.name == "Drama"
        assert existing_genre.is_active is False
        assert existing_genre.categories == {category.id}
