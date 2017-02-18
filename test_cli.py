
__author__ = "Felix Simkovic"
__date__ = "01 Nov 2016"

from cli import _GenericArgument
from cli import Argument
from cli import ArgumentList
from cli import CommandLine
from cli import Option
from cli import OptionList
from cli import Switch

import unittest


class Test__GenericArgument(unittest.TestCase):

    def test_names(self):
        arg = _GenericArgument()
        arg.names = ['Hello']
        self.assertEqual(['Hello'], arg.names)

        arg = _GenericArgument()
        arg.names = ['-Hello']
        self.assertEqual(['-Hello'], arg.names)

        arg = _GenericArgument()
        arg.names = ['Hello', 'World']
        self.assertEqual(['Hello', 'World'], arg.names)

    def test_description(self):
        arg = _GenericArgument()
        arg.description = 'Foo bar'
        self.assertEqual('Foo bar', arg.description)

    def test_equate(self):
        arg = _GenericArgument()
        arg.equate = True
        self.assertTrue(arg.equate)

        arg = _GenericArgument()
        arg.equate = False
        self.assertFalse(arg.equate)

    def test_is_filename(self):
        arg = _GenericArgument()
        arg.is_filename = True
        self.assertTrue(arg.is_filename)

        arg = _GenericArgument()
        arg.is_filename = False
        self.assertFalse(arg.is_filename)

    def test_is_set(self):
        arg = _GenericArgument()
        arg.is_set = True
        self.assertTrue(arg.is_set)

        arg = _GenericArgument()
        arg.is_set = False
        self.assertFalse(arg.is_set)

    def test_is_required(self):
        arg = _GenericArgument()
        arg.is_required = True
        self.assertTrue(arg.is_required)

        arg = _GenericArgument()
        arg.is_required = False
        self.assertFalse(arg.is_required)

    def test__escape_spaces(self):
        filename = 'foo_bar'
        self.assertEqual('foo_bar', _GenericArgument._escape_spaces(filename))

        filename = 'foo bar'
        self.assertEqual('"foo bar"', _GenericArgument._escape_spaces(filename))

        filename = '"foo bar"'
        self.assertEqual('"foo bar"', _GenericArgument._escape_spaces(filename))

        filename = ' "foo bar"'
        self.assertEqual('"foo bar"', _GenericArgument._escape_spaces(filename))

        filename = '"foo bar" '
        self.assertEqual('"foo bar"', _GenericArgument._escape_spaces(filename))

        filename = ' "foo bar" '
        self.assertEqual('"foo bar"', _GenericArgument._escape_spaces(filename))


class Test_Argument(unittest.TestCase):

    def test___str__(self):
        argument = Argument(['argument'], 'description')
        argument.value = 'value'
        argument.is_set = True
        self.assertEqual('value ', str(argument))

        argument = Argument(['argument'], 'description', is_filename=True)
        argument.value = 'val ue'
        argument.is_set = True
        self.assertEqual('"val ue" ', str(argument))

    def test_value(self):
        argument = Argument(['argument'], 'description')
        argument.value = 'value'
        self.assertEqual('value', argument.value)

        argument = Argument(['argument'], 'description')
        argument.value = 5
        self.assertEqual(5, argument.value)

        argument = Argument(['argument'], 'description')
        argument.value = 3.1
        self.assertEqual(3.1, argument.value)

        argument = Argument(['argument'], 'description', is_filename=True)
        argument.value = 'value'
        self.assertEqual('value', argument.value)

        argument = Argument(['argument'], 'description', is_filename=True)
        argument.value = 'val ue'
        self.assertEqual('"val ue"', argument.value)

        argument = Argument(['argument'], 'description', is_filename=True)
        argument.value = 3
        self.assertEqual('3', argument.value)

        try:
            argument = Argument(['argument'], 'description')
            argument.value = ['test']
            self.assertTrue(False)
        except TypeError:
            self.assertTrue(True)


class Test_ArgumentList(unittest.TestCase):

    def test___str__(self):
        argument_list = ArgumentList(['argument_list'], 'description')
        argument_list.value = ['value1', 'value2']
        argument_list.is_set = True
        self.assertEqual('value1 value2 ', str(argument_list))

        argument_list = ArgumentList(['argument_list'], 'description', is_filename=True)
        argument_list.value = ['val ue1', 'value2']
        argument_list.is_set = True
        self.assertEqual('"val ue1" value2 ', str(argument_list))

    def test_value(self):
        argument_list = ArgumentList(['argument_list'], 'description')
        argument_list.value = ['value1', 'value2']
        self.assertEqual(['value1', 'value2'], argument_list.value)

        argument_list = ArgumentList(['argument_list'], 'description')
        argument_list.value = ('value1', 'value2')
        self.assertEqual(('value1', 'value2'), argument_list.value)

        argument_list = ArgumentList(['argument_list'], 'description', is_filename=True)
        argument_list.value = ['value1', 'value2']
        self.assertEqual(['value1', 'value2'], argument_list.value)

        argument_list = ArgumentList(['argument_list'], 'description', is_filename=True)
        argument_list.value = ['val ue1', 'value2']
        self.assertEqual(['"val ue1"', 'value2'], argument_list.value)

        argument_list = ArgumentList(['argument_list'], 'description', is_filename=True)
        argument_list.value = ['"val ue1"', 'value2']
        self.assertEqual(['"val ue1"', 'value2'], argument_list.value)

        try:
            argument_list = ArgumentList(['argument_list'], 'description')
            argument_list.value = 'test'
            self.assertTrue(False)
        except TypeError:
            self.assertTrue(True)


class Test_CommandLine(unittest.TestCase):

    def test___init__(self):

        class NewCli(CommandLine):
            def __init__(self):
                self.clflags = [
                    Switch(['--on', 'onswitch'], 'on-switch'),
                    Argument(['fname'], 'a file name')
                ]
                kwargs = {'onswitch': True, 'fname': 'foo_bar'}
                super(NewCli, self).__init__('go', **kwargs)

        cli = NewCli()
        raise RuntimeError


class Test_Option(unittest.TestCase):

    def test___str__(self):
        option = Option(['-flag', 'option'], 'description')
        option.value = 'value'
        option.is_set = True
        self.assertEqual('-flag value ', str(option))

        option = Option(['-flag', 'option'], 'description', is_filename=True)
        option.value = 'val ue'
        option.is_set = True
        self.assertEqual('-flag "val ue" ', str(option))

        option = Option(['-flag', 'option'], 'description', equate=True, is_filename=True)
        option.value = 'val ue'
        option.is_set = True
        self.assertEqual('-flag="val ue" ', str(option))

    def test_value(self):
        option = Option(['-flag', 'option'], 'description')
        option.value = 'value'
        self.assertEqual('value', option.value)

        option = Option(['-flag', 'option'], 'description')
        option.value = 5
        self.assertEqual(5, option.value)

        option = Option(['-flag', 'option'], 'description')
        option.value = 3.1
        self.assertEqual(3.1, option.value)

        option = Option(['-flag', 'option'], 'description', is_filename=True)
        option.value = 'value'
        self.assertEqual('value', option.value)

        option = Option(['-flag', 'option'], 'description', is_filename=True)
        option.value = 'val ue'
        self.assertEqual('"val ue"', option.value)

        option = Option(['-flag', 'option'], 'description', is_filename=True)
        option.value = 3
        self.assertEqual('3', option.value)

        try:
            option = Option(['-flag', 'option'], 'description')
            option.value = ['test']
            self.assertTrue(False)
        except TypeError:
            self.assertTrue(True)


class Test_OptionList(unittest.TestCase):

    def test___str__(self):
        option_list = OptionList(['-flag', 'argument_list'], 'description')
        option_list.value = ['value1', 'value2']
        option_list.is_set = True
        self.assertEqual('-flag value1 value2 ', str(option_list))

        option_list = OptionList(['-flag', 'argument_list'], 'description', is_filename=True)
        option_list.value = ['val ue1', 'value2']
        option_list.is_set = True
        self.assertEqual('-flag "val ue1" value2 ', str(option_list))

        option_list = OptionList(['-flag', 'argument_list'], 'description', equate=True, is_filename=True)
        option_list.value = ['val ue1', 'value2']
        option_list.is_set = True
        self.assertEqual('-flag="val ue1",value2 ', str(option_list))

    def test_value(self):
        option_list = OptionList(['-flag', 'argument_list'], 'description')
        option_list.value = ['value1', 'value2']
        self.assertEqual(['value1', 'value2'], option_list.value)

        option_list = OptionList(['-flag', 'argument_list'], 'description')
        option_list.value = ('value1', 'value2')
        self.assertEqual(('value1', 'value2'), option_list.value)

        option_list = OptionList(['-flag', 'argument_list'], 'description', is_filename=True)
        option_list.value = ['value1', 'value2']
        self.assertEqual(['value1', 'value2'], option_list.value)

        option_list = OptionList(['-flag', 'argument_list'], 'description', is_filename=True)
        option_list.value = ['val ue1', 'value2']
        self.assertEqual(['"val ue1"', 'value2'], option_list.value)

        option_list = OptionList(['-flag', 'argument_list'], 'description', is_filename=True)
        option_list.value = ['"val ue1"', 'value2']
        self.assertEqual(['"val ue1"', 'value2'], option_list.value)

        try:
            option_list = OptionList(['-flag', 'argument_list'], 'description')
            option_list.value = 'test'
            self.assertTrue(False)
        except TypeError:
            self.assertTrue(True)


class Test_Switch(unittest.TestCase):

    def test___str__(self):
        switch = Switch(['-switch'], 'description')
        switch.is_set = True
        self.assertEqual('-switch ', str(switch))

        switch = Switch(['--switch'], 'description')
        switch.is_set = True
        self.assertEqual('--switch ', str(switch))

        switch = Switch(['--switch'], 'description')
        self.assertEqual('', str(switch))


if __name__ == "__main__":
    unittest.main(verbosity=2)
