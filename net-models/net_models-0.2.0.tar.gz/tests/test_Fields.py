import unittest

import yaml

from net_models.fields import DoubleQoutedString, Jinja2String, IosInterfaceName, BaseInterfaceName
from net_models.utils.CustomYamlDumper import CustomYamlDumper
from net_models.models.interfaces import InterfaceServicePolicy

class TestDoubleQuotedString(unittest.TestCase):

    def test_01(self):

        test_value = "Foo"
        self.assertIsInstance(DoubleQoutedString(test_value), DoubleQoutedString)


class TestJinja2String(unittest.TestCase):

    TESTED_CLASS = Jinja2String

    def test_01(self):
        test_value = "{{ i_am_jinja_var }}"
        for validator in self.TESTED_CLASS.__get_validators__():
            validated = validator(test_value)
            self.assertIsInstance(validated, self.TESTED_CLASS)


    def test_dump_01(self):

        test_data = {
            "foo": self.TESTED_CLASS("{{ bar }}")
        }
        have_yaml = yaml.dump(data=test_data, Dumper=CustomYamlDumper)
        want_yaml = 'foo: "{{ bar }}"\n'
        self.assertEqual(have_yaml, want_yaml)

    def test_dump_02(self):
        test_data = {
            "foo": {
                "bar": self.TESTED_CLASS("{{ bar }}")
            }
        }
        have_yaml = yaml.dump(data=test_data, Dumper=CustomYamlDumper)
        want_yaml = 'foo:\n  bar: "{{ bar }}"\n'
        self.assertEqual(have_yaml, want_yaml)


    def test_model_dump(self):

        model = InterfaceServicePolicy(input=self.TESTED_CLASS("{{ PM_TEMPLATE_01 }}"))
        # print(type(model.input))
        # print(model.yaml())
        self.assertIsInstance(model.input, self.TESTED_CLASS)

class TestIosInterfaceName(unittest.TestCase):

    def test_init(self):
        instance = IosInterfaceName('Gi1/0/1')
        with self.subTest(msg="Is instance of BaseInterfaceName"):
            self.assertIsInstance(instance, BaseInterfaceName)
        with self.subTest(msg="Is instance of IosInterfaceName"):
            self.assertIsInstance(instance, IosInterfaceName)
        with self.subTest(msg="Can be __eq__ with plain string"):
            self.assertEqual('GigabitEthernet1/0/1', instance)
        with self.subTest(msg="Can be JSON serialized"):
            pass
        with self.subTest(msg="Can be YAML serialized"):
            yaml.dump(data={})


if __name__ == '__main__':
    unittest.main()