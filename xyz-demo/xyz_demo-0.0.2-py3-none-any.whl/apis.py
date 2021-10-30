# -*- coding:utf-8 -*-
from __future__ import division, unicode_literals
from rest_framework.response import Response

__author__ = 'denishuang'

from rest_framework import viewsets, decorators
from xyz_restful.decorators import register_raw


@register_raw(path='demo/object')
class ObjectSet(viewsets.ViewSet):
    permission_classes = []

    @decorators.action(['get'], detail=False)
    def read(self, request):
        from .stores import ObjectLog
        ol = ObjectLog()
        qs = request.query_params
        key = qs.get('key')
        rs = ol.collection.find_one({'key': key}, {'_id': 0})
        return Response(rs or {})

    @decorators.action(['post'], detail=False)
    def write(self, request):
        from .stores import ObjectLog
        ol = ObjectLog()
        print(request.data)
        key = request.data.get('key')
        value = request.data.get('value')
        ol.upsert({'key': key}, {'value': value})
        rs = ol.collection.find_one({'key': key}, {'_id': 0})
        return Response(rs)

    @decorators.action(['post'], detail=False)
    def add_to_set(self, request):
        from .stores import ObjectLog
        ol = ObjectLog()
        key = request.data.get('key')
        value = request.data.get('value')
        ol.add_to_set({'key': key}, {'value': value})
        rs = ol.collection.find_one({'key': key}, {'_id': 0})
        return Response(rs)
