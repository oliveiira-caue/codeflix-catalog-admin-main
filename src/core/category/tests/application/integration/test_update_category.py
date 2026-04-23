from unittest.mock import create_autospec
import uuid 
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from core.category.domain.category_repository import CategoryRepository
from src.core.category.application.update_category import UpdateCategory, UpdateCategoryRequest
from src.core.category.domain.category import Category


class TestUpdateCategory:
    def test_can_update_category_name_and_description(self):
        category = Category(    
            name="Filme",
            description="Categoria para filmes",
            is_active=True,
        )   

        repository = InMemoryCategoryRepository()
        repository.save(category)

        use_case = UpdateCategory(repository=repository)
        request = UpdateCategoryRequest(
            id=category.id,
            name="Filme",
            description="Categoria para séries",
        )

        use_case.execute(request)
        
        updated_category = repository.get_by_id(category.id)
        assert updated_category.name == "Filme"
        assert updated_category.description == "Categoria para séries"