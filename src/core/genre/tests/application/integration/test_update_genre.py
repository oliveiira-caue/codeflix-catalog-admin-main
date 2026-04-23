import uuid

import pytest

from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.genre.application.exceptions import RelatedCategoriesNotFound
from src.core.genre.application.update_genre import UpdateGenre, UpdateGenreRequest
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


class TestUpdateGenreIntegration:
    def test_update_genre_with_valid_data_and_existing_categories(self):
        category_movie = Category(name="Movie")
        category_series = Category(name="Series")
        category_docs = Category(name="Doc")

        category_repo = InMemoryCategoryRepository(
            categories=[category_movie, category_series, category_docs]
        )

        genre = Genre(
            name="Romance",
            is_active=True,
            categories={category_movie.id, category_series.id, category_docs.id},
        )
        genre_repo = InMemoryGenreRepository(genres=[genre])

        use_case = UpdateGenre(
            repository=genre_repo,
            category_repository=category_repo,
        )

        use_case.execute(UpdateGenreRequest(
            id=genre.id,
            name="Drama",
            is_active=False,
            categories={category_movie.id, category_series.id},
        ))

        updated = genre_repo.get_by_id(genre.id)
        assert updated.name == "Drama"
        assert updated.is_active is False
        assert updated.categories == {category_movie.id, category_series.id}

    def test_update_genre_with_nonexistent_categories_raises_error(self):
        category_repo = InMemoryCategoryRepository()
        genre = Genre(name="Romance")
        genre_repo = InMemoryGenreRepository(genres=[genre])

        use_case = UpdateGenre(
            repository=genre_repo,
            category_repository=category_repo,
        )

        with pytest.raises(RelatedCategoriesNotFound):
            use_case.execute(UpdateGenreRequest(
                id=genre.id,
                name="Drama",
                categories={uuid.uuid4()},
            ))
