import pytest

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType


class TestCastMember:
    def test_create_cast_member_with_valid_data(self):
        cm = CastMember(name="John Doe", type=CastMemberType.ACTOR)
        assert cm.name == "John Doe"
        assert cm.type == CastMemberType.ACTOR
        assert cm.id is not None

    def test_cast_member_name_cannot_be_empty(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            CastMember(name="", type=CastMemberType.ACTOR)

    def test_cast_member_name_cannot_exceed_255_chars(self):
        with pytest.raises(ValueError, match="name cannot be longer than 255 characters"):
            CastMember(name="x" * 256, type=CastMemberType.ACTOR)

    def test_cast_member_type_must_be_valid(self):
        with pytest.raises(ValueError):
            CastMember(name="John", type="INVALID")

    def test_cast_member_equality_by_id(self):
        cm1 = CastMember(name="John", type=CastMemberType.ACTOR)
        cm2 = CastMember(name="John", type=CastMemberType.ACTOR)
        assert cm1 != cm2

    def test_update_cast_member(self):
        cm = CastMember(name="John", type=CastMemberType.ACTOR)
        cm.update(name="Jane", type=CastMemberType.DIRECTOR)
        assert cm.name == "Jane"
        assert cm.type == CastMemberType.DIRECTOR
