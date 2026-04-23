from dataclasses import dataclass, field
import uuid
from uuid import UUID


@dataclass
class Genre:
    name: str
    is_active: bool = True
    categories: set[UUID] = field(default_factory=set)
    id: UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        self.validate()

    def validate(self):
        if len(self.name) == 0:
            raise ValueError("name cannot be empty")

        if len(self.name) > 255:
            raise ValueError("name cannot be longer than 255 characters")

    def __str__(self):
        return f"{self.name} ({self.is_active})"

    def __repr__(self):
        return f"<Genre {self.name} ({self.id})>"

    def __eq__(self, other):
        if not isinstance(other, Genre):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def change_name(self, name: str):
        self.name = name
        self.validate()

    def add_category(self, category_id: UUID):
        self.categories.add(category_id)

    def remove_category(self, category_id: UUID):
        self.categories.discard(category_id)

    def activate(self):
        self.is_active = True
        self.validate()

    def deactivate(self):
        self.is_active = False
        self.validate()
