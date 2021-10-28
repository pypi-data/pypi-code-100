# -*- coding: utf-8 -*-
import json
import pathlib

import bottle
from pip_services3_commons.convert import TypeCode
from pip_services3_commons.data import FilterParams, PagingParams
from pip_services3_commons.refer import Descriptor
from pip_services3_commons.validate import ObjectSchema
from pip_services3_rpc.services import RestService

from example.data.DummySchema import DummySchema
from example.logic.IDummyController import IDummyController


class DummyRestService(RestService):
    def __init__(self):
        super(DummyRestService, self).__init__()
        self._dependency_resolver.put('controller',
                                      Descriptor("pip-services-dummies", "controller", "default", "*", "*"))

        self._controller: IDummyController = None

    def configure(self, config):
        super().configure(config)

    def set_references(self, references):
        super().set_references(references)
        self._controller = self._dependency_resolver.get_one_required('controller')

    def __get_page_by_filter(self):
        paging = PagingParams(bottle.request.query.get('skip'),
                              bottle.request.query.get('take'),
                              bottle.request.query.get('total'))
        filter = FilterParams(bottle.request.query.dict)

        return self.send_result(
            self._controller.get_page_by_filter(bottle.request.query.get('correlation_id'), filter, paging))

    def __get_one_by_id(self, id):
        return self.send_result(self._controller.get_one_by_id(
            bottle.request.query.get('correlation_id'),
            bottle.request.query.get('dummy_id'),
        ))

    def __create(self):
        return self.send_created_result(self._controller.create(
            bottle.request.query.get('correlation_id'),
            json.loads(bottle.request.json).get('body'),
        ))

    def __update(self):
        return self.send_result(self._controller.update(
            bottle.request.query.get('correlation_id'),
            json.loads(bottle.request.json).get('body'),
        ))

    def __delete_by_id(self, id):
        return self.send_deleted_result(self._controller.delete_by_id(
            bottle.request.query.get('correlation_id'),
            bottle.request.query.get('dummy_id'),
        ))

    def register(self):
        self.register_route('get', '/dummies',
                            ObjectSchema(True)
                            .with_optional_property("skip", TypeCode.String)
                            .with_optional_property("take", TypeCode.String)
                            .with_optional_property("total", TypeCode.String),
                            self.__get_page_by_filter
                            )

        self.register_route('get', '/dummies/<dummy_id>',
                            ObjectSchema(True)
                            .with_required_property("dummy_id", TypeCode.String),
                            self.__get_one_by_id)

        self.register_route('post', '/dummies', ObjectSchema(True)
                            .with_required_property("body", DummySchema()),
                            self.__create)

        self.register_route('put', '/dummies/<dummy_id>',
                            ObjectSchema(True)
                            .with_required_property("body", DummySchema()),
                            self.__update)

        self.register_route('delete', '/dummies/<dummy_id>',
                            ObjectSchema(True)
                            .with_required_property("dummy_id", TypeCode.String),
                            self.__delete_by_id)

        self._swagger_route = '/dummies/swagger'
        self._register_open_api_spec_from_file(
            str(pathlib.Path(__file__).parent) + '/../../example/services/dummy.yml')
