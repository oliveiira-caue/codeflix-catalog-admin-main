
import pytest
from django_project.category_app.models import Category
from django_project.category_app.repository import DjangoORMCategoryRepository
from django_project.category_app.models import Category as CategoryModel

@pytest.mark.django_db
class TestSave:
    def test_save_category_in_database(self):
        category = Category(
            name="Movie",
            description="Movie description",
        )
        repository = DjangoORMCategoryRepository()

        assert CategoryModel.objects.count() == 0
        repository.save(category)
        assert CategoryModel.objects.count() == 1

        category.db = CategoryModel.objects.get()
        assert category.db.id == category.id
        assert category.db.name == category.name
        assert category.db.description == category.description
        assert category.db.is_active == category.is_active
