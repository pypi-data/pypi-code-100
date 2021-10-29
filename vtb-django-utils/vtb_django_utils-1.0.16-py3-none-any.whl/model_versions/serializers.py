from abc import ABCMeta

from django.db import transaction
from rest_framework import serializers


class VersionedModelSerializer(serializers.ModelSerializer):
    __metaclass__ = ABCMeta
    version = serializers.CharField(required=False, allow_blank=True, allow_null=True, default='')
    last_version = serializers.SerializerMethodField()
    version_list = serializers.SerializerMethodField()

    class Meta:
        model = None

    @staticmethod
    def get_last_version(obj):
        return obj.last_version.version if obj.last_version else ''

    @staticmethod
    def get_version_list(obj):
        return obj.version_list

    @transaction.atomic()
    def create(self, validated_data):
        version = validated_data.pop('version', None)
        instance = self.Meta.model.objects.create(**validated_data)
        instance.create_or_update_version(version)
        return instance

    @transaction.atomic()
    def update(self, instance, validated_data):
        version = validated_data.pop('version', None)
        save_as_next_version = self.context['request'].query_params.get('save_as_next_version') == 'true'
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if save_as_next_version:
            version = instance.next_version_str
        instance.create_or_update_version(version)
        return instance
