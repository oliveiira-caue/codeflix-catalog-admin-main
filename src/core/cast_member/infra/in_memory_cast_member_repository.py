from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class InMemoryCastMemberRepository(CastMemberRepository):
    def __init__(self, cast_members=None):
        self.cast_members = cast_members or []

    def save(self, cast_member: CastMember) -> None:
        self.cast_members.append(cast_member)

    def get_by_id(self, id: UUID) -> CastMember | None:
        for cm in self.cast_members:
            if cm.id == id:
                return cm
        return None

    def delete(self, id: UUID) -> None:
        cm = self.get_by_id(id)
        if cm:
            self.cast_members.remove(cm)

    def update(self, cast_member: CastMember) -> None:
        old = self.get_by_id(cast_member.id)
        if old:
            self.cast_members.remove(old)
        self.cast_members.append(cast_member)

    def list(self) -> list[CastMember]:
        return list(self.cast_members)
