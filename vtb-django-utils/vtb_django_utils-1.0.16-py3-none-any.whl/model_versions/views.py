from rest_framework import viewsets
from rest_framework.response import Response


class VersionMixin(viewsets.ModelViewSet):
    def _json_by_version(self, obj=None) -> dict:
        instance = obj or self.get_object()
        version = self.request.query_params.get('version')
        compare_with_version = self.request.query_params.get('compare_with_version')
        json_field_name = 'raw_json' if self.request.query_params.get('is_raw_json') == 'true' else 'json'
        instance_json = instance.get_json_by_version(version, json_field_name, compare_with_version)
        instance_json['version_list'] = instance.version_list
        return instance_json

    def retrieve(self, request, *args, **kwargs):
        return Response(self._json_by_version())
