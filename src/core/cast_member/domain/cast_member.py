from dataclasses import dataclass, field
import uuid
from enum import StrEnum
from uuid import UUID


class CastMemberType(StrEnum):
    ACTOR = "ACTOR"
    DIRECTOR = "DIRECTOR"


@dataclass
class CastMember:
    name: str
    type: CastMemberType
    id: UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        self.validate()

    def validate(self):
        if not self.name:
            raise ValueError("name cannot be empty")

        if len(self.name) > 255:
            raise ValueError("name cannot be longer than 255 characters")

        if self.type not in CastMemberType:
            raise ValueError(f"type must be one of {list(CastMemberType)}")

    def __eq__(self, other):
        if not isinstance(other, CastMember):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def update(self, name: str, type: CastMemberType) -> None:
        self.name = name
        self.type = type
        self.validate()
