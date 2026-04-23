from src.core.category.application.delete_category import DeleteCategory, DeleteCategoryRequest
from src.core.category.application.get_category import GetCategory, GetCategoryRequest
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.category.domain.category import Category


class TestDeleteCategory:
    def test_delete_category_from_repository(self):
        category_filme = Category(
            name="Filme",
            description="Categoria para filmes",
            is_active=True,
        )
        category_serie = Category(
            name="Série",
            description="Categoria para séries",
            is_active=True,
        )
        repository = InMemoryCategoryRepository(
            categories = [
                category_filme,
                category_serie]
        )


        use_case = DeleteCategory(repository=repository)
        request = DeleteCategoryRequest(id=category_filme.id,)
        
        assert repository.get_by_id(category_filme.id) is not None
        response = use_case.execute(request)

        
        assert repository.get_by_id(category_filme.id) is None
        assert response is None