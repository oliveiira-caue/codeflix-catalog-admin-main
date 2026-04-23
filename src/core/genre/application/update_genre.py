from dataclasses import dataclass, field
from uuid import UUID

from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.exceptions import GenreNotFound, InvalidGenre, RelatedCategoriesNotFound
from src.core.genre.domain.genre_repository import GenreRepository


@dataclass
class UpdateGenreRequest:
    id: UUID
    name: str
    is_active: bool = True
    categories: set[UUID] = field(default_factory=set)


class UpdateGenre:
    def __init__(self, repository: GenreRepository, category_repository: CategoryRepository):
        self.repository = repository
        self.category_repository = category_repository

    def execute(self, request: UpdateGenreRequest) -> None:
        genre = self.repository.get_by_id(request.id)

        if genre is None:
            raise GenreNotFound(f"Genre with id {request.id} not found")

        if request.categories:
            existing_category_ids = {
                category.id
                for category in self.category_repository.list()
            }
            missing = request.categories - existing_category_ids
            if missing:
                raise RelatedCategoriesNotFound(
                    f"Categories with ids {missing} not found"
                )

        try:
            genre.change_name(request.name)

            genre.categories = set(request.categories)

            if request.is_active:
                genre.activate()
            else:
                genre.deactivate()
        except ValueError as err:
            raise InvalidGenre(err)

        self.repository.update(genre)
