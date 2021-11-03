from . import events
from unittest import TestCase
from unittest.mock import MagicMock


class TestEvent(TestCase):
    def setUp(self):
        self.target = MagicMock()
        self.event = events.Event(self.target, "click", {"type": "mouse"})

    def test_props(self):
        self.assertEqual(self.event.target, self.target)
        self.assertEqual(self.event.name, "click")
        self.assertEqual(self.event.data, {"type": "mouse"})


class TestEventHandlerProperty(TestCase):
    def setUp(self):
        self.handler = MagicMock()
        self.decorated = events.EventHandlerProperty(
            event_names=("click",), handler=self.handler
        )

    def test_match_success(self):
        event = MagicMock()
        event.name = "click"
        self.assertTrue(self.decorated.match(event))

    def test_match_fail(self):
        event = MagicMock()
        event.name = "resize"
        self.assertFalse(self.decorated.match(event))

    def test_get_non_instance(self):
        result = self.decorated.__get__(None, None)
        self.assertIs(result, self.decorated)

    def test_get_handler(self):
        instance = MagicMock()
        result = self.decorated.__get__(instance, None)
        result(1, 2, 3)
        self.handler.assert_called_with(instance, 1, 2, 3)


class TestHandle(TestCase):
    def test_handle(self):
        function = MagicMock()
        decorated = events.handle("foo")(function)
        self.assertIsInstance(decorated, events.EventHandlerProperty)
        self.assertEqual(decorated.event_names, ("foo",))
        self.assertEqual(decorated.handler, function)


class TestEventsBehaviour(TestCase):
    def setUp(self):

        self.resize_handler = resize_handler = MagicMock(return_value="from resize")
        self.click_handler = click_handler = MagicMock(return_value="from click")

        class Parent(object):

            event = None
            not_click_event = None

            @events.handle("click")
            def on_click(self, event):
                self.event = event
                return "from parent click"

            @events.handle("not-click")
            def on_not_click(self, event):
                self.not_click_event = event
                return "from parent not-click"

        self.parent = Parent()

        class Context(object):
            handle_resize = events.handle("resize")(resize_handler)
            handle_click = events.handle("click", priority=1)(click_handler)

        self.context = Context()
        self.context.__parent__ = self.parent

    def test_event_handlers(self):
        handlers = list(events.get_event_handlers(self.context))
        handler_name_matches = [d.event_names[0] for d, h in handlers]
        handler_results = [h("event") for d, h in handlers]
        self.assertEqual(
            handler_name_matches, ["click", "resize", "click", "not-click"]
        )
        self.assertEqual(
            handler_results,
            ["from click", "from resize", "from parent click", "from parent not-click"],
        )

    def test_emit_handled(self):
        events.emit(self.context, "click", {"foo": "bar"})
        self.assertEqual(self.parent.event.data, {"foo": "bar"})
        self.assertIsNone(self.parent.not_click_event)
