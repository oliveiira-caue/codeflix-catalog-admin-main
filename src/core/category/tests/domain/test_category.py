import pytest
from uuid import UUID
import uuid   

from src.core.category.domain.category import Category

class TestCategory:
    def test_name_is_required(self):
        with pytest.raises(TypeError, match="missing 1 required positional argument: 'name'"):
            Category()

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="name cannot be longer than 255 characters"):
            Category(name="a"*256)

    def test_category_must_be_created_with_id_as_uuid(self):
        category = Category(name="filme")
        assert isinstance(category.id, UUID)

    def test_created_category_with_default_values(self):
        category = Category(name="filme")
        assert category.name == "filme"
        assert category.description == ""
        assert category.is_active is True

    def test_category_is_created_as_active_by_default(self):
        category = Category(name="filme")
        assert category.is_active is True  

    def test_category_is_created_with_provided_values(self):
        cat_id = uuid.uuid4()
        category = Category(name="filme",description="Filmes em geral", id=cat_id, is_active=False)
        assert category.id == cat_id
        assert category.name == "filme"
        assert category.description == "Filmes em geral"
        assert category.is_active is False

    def test_cannot_create_category_with_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            Category(name="")

    def test_str_with_provided_values(self):
        category = Category(name="Filme", description="Genero terror", is_active=True,)
        self

    def test_str_representation(self):
        # Criamos uma categoria com dados fixos
        category = Category(name="Filmes", description="Categoria de teste", is_active=True)
        expected_str = "Filmes - Categoria de teste (True)"
        assert str(category) == expected_str

    def test_repr_representation(self):
        # Criamos uma categoria e pegamos o ID dela
        category = Category(name="Filmes")
        cat_id = category.id
        
        # O que esperamos que o repr(category) retorne:
        # Note que aqui incluí o ">" no final, caso você tenha corrigido no seu código
        expected_repr = f"<Category Filmes ({cat_id})>" 
        
        # Verificamos se o repr() do objeto é igual ao esperado
        assert repr(category) == expected_repr



class TestUpdateCategory:
    def test_update_category_with_name_and_description(self):
        category = Category(name="Filme", description="Filmes em geral")

        category.update_category(name="Séries", description="Séries em geral")

        assert category.name == "Séries"
        assert category.description == "Séries em geral"

    def test_update_category_with_invalid_name_raises_exception(self):
        category = Category(name="Filme", description="Filmes em geral")

        with pytest.raises(ValueError, match="name cannot be longer than 255 characters"):
            category.update_category(name="a" * 256, description="Séries em geral")

    def test_cannot_update_category_with_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            Category(name="")

    
class TestActivate:
    def test_activate_inactive_category(self):
        category = Category(
            name="Filme", 
            description="Filmes em geral",
            is_active=False,
            )

        category.activate()

        assert category.is_active is True

    def test_activate_active_catgory(self):
        category = Category(
            name="Filme", 
            description="Filmes em geral",
            is_active=False,
        )

        category.activate()

        assert category.is_active is True

    def test_deactivate_active_category(self):
        category = Category(
            name="Filme",
            description="Filmes em geral",
            is_active=True,
        )

        category.deactivate()

        assert category.is_active is False


class TestEquality:
    def test_when_categories_have_same_id_they_are_equal(self):
        common_id = uuid.uuid4()
        category_1 = Category(name="Filme", id=common_id)
        category_2 = Category(name="Filme", id=common_id)

        assert category_1 == category_2

    def test_equality_different_classes(self):
        class Dummy:
            pass

        common_id = uuid.uuid4()
        category = Category(name="Filme", id=common_id)
        dummy = Dummy()
        dummy.id = common_id

        assert category != dummy





