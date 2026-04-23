from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestInMemoryCategoryRepository:
    def test_can_save_category(self):
        repository = InMemoryCategoryRepository()
        category = Category(
            name="Filme",
            description="Categoria para filmes"
        )

        repository.save(category)

        assert len(repository.categories) == 1
        assert repository.categories[0] == category

    def test_can_get_category_by_id(self):
        # 1. Crio a Estante (Repositório)
        repository = InMemoryCategoryRepository()
        
        # 2. Crio o Livro (Categoria)
        category = Category(
            name="Filme",
            description="Categoria para filmes"
        )
        
        # 3. O PULO DO GATO: Guardo o livro na estante primeiro!
        repository.save(category)

        # 4. AÇÃO: Busco o livro usando o ID dele
        response = repository.get_by_id(category.id)

        # 5. VERIFICAÇÃO: O livro que voltou é o mesmo que eu guardei?
        assert response == category