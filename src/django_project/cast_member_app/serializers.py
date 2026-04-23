from rest_framework import serializers

from src.core.cast_member.domain.cast_member import CastMemberType


class CastMemberTypeField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        choices = [(type.name, type.value) for type in CastMemberType]
        super().__init__(choices=choices, **kwargs)

    def to_internal_value(self, data):
        return CastMemberType(super().to_internal_value(data))

    def to_representation(self, value):
        return str(super().to_representation(value))


class CastMemberOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    type = CastMemberTypeField()


class ListCastMemberOutputSerializer(serializers.Serializer):
    data = CastMemberOutputSerializer(many=True)


class CreateCastMemberInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    type = CastMemberTypeField()


class CreateCastMemberOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class UpdateCastMemberInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    type = CastMemberTypeField()


class DeleteCastMemberInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
