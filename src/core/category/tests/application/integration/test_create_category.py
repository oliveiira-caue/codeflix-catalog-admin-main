from uuid import UUID
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.category.application.create_category import CreateCategory, CreateCategoryRequest

class TestCreateCategory:
    def test_create_category_With_valid_data(self):
        repository = InMemoryCategoryRepository()
        use_case = CreateCategory(repository=repository)
        request = CreateCategoryRequest(
            name= "Filme",   
            description= "Categoria para filmes",
            is_active= True, # default
        )

        response = use_case.execute(request)


        assert response is not None
        assert isinstance(response.id, UUID)
        assert len(repository.categories) == 1

        persisted_category = repository.categories[0]
        assert persisted_category.id == response.id
        assert persisted_category.name == "Filme"
        assert persisted_category.description == "Categoria para filmes"
        assert persisted_category.is_active == True