# -*- coding: utf-8 -*-
from pip_services3_commons.commands import CommandSet, Command
from pip_services3_commons.convert import TypeCode
from pip_services3_commons.data import FilterParams, PagingParams
from pip_services3_commons.validate import ObjectSchema, FilterParamsSchema, PagingParamsSchema

from example.data.DummySchema import DummySchema
from example.logic.IDummyController import IDummyController


class DummyCommandSet(CommandSet):

    def __init__(self, controller: IDummyController):
        super(DummyCommandSet, self).__init__()

        self._controller = controller

        self.add_command(self.__make_get_page_by_filter_command())
        self.add_command(self.__make_get_one_by_id_command())
        self.add_command(self.__make__create_command())
        self.add_command(self.__make__update_command())
        self.add_command(self.__make_delete_by_id_command())

    def __make_get_page_by_filter_command(self):
        def callback(correlation_id, args):
            filter = FilterParams.from_value(args.get('filter'))
            paging = PagingParams.from_value(args.get('paging'))
            return self._controller.get_page_by_filter(correlation_id, filter, paging)

        return Command(
            'get_dummies',
            ObjectSchema(True)
                .with_optional_property("filter", FilterParamsSchema())
                .with_optional_property("paging", PagingParamsSchema()),
            callback
        )

    def __make_get_one_by_id_command(self):
        def callback(correlation_id, args):
            id = args.get_as_string('dummy_id')
            return self._controller.get_one_by_id(correlation_id, id)

        return Command(
            'get_dummy_by_id',
            ObjectSchema(True).with_required_property('dummy_id', TypeCode.String),
            callback
        )

    def __make__create_command(self):
        def callback(correlation_id, args):
            entity = args.get('dummy')
            return self._controller.create(correlation_id, entity)

        return Command(
            'create_dummy',
            ObjectSchema(True).with_required_property('dummy', DummySchema()),
            callback
        )

    def __make__update_command(self):
        def callback(correlation_id, args):
            entity = args.get('dummy')
            return self._controller.update(correlation_id, entity)

        return Command(
            'update_dummy',
            ObjectSchema(True).with_required_property('dummy', DummySchema()),
            callback
        )

    def __make_delete_by_id_command(self):
        def callback(correlation_id, args):
            id = args.get('id')
            return self._controller.delete_by_id(correlation_id, id)

        return Command(
            'delete_dummy',
            ObjectSchema(True).with_required_property('dummy_id', TypeCode.String),
            callback
        )
