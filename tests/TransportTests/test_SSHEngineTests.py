from tests.BaseClasses import TestableSSHEngine
from tests.helper_functions import read_command_file_contents
from unittest import TestCase


class TestSendingCommands(TestCase):

    def test_sends_command_default_with_newline(self):
        engine = TestableSSHEngine([])
        engine.send_command('test')
        self.assertEqual(['test\n'], engine.commands_sent)

    def test_modifying_end_character(self):
        engine = TestableSSHEngine([])
        engine.send_command('test', end='')
        self.assertEqual(['test'], engine.commands_sent)


class TestGettingOutput(TestCase):

    def setUp(self) -> None:
        self.output_from_server = read_command_file_contents('/command_outputs/get_system_status')

    def test_gets_all_output_from_server(self):
        engine = TestableSSHEngine(self.output_from_server)
        output_gathered_from_server = engine.get_output(buffer_size=1, return_as_list=True)
        self.assertEqual(self.output_from_server, output_gathered_from_server)

    def test_gathers_correct_hostname_from_prompt(self):
        engine = TestableSSHEngine(self.output_from_server)
        _ = engine.get_output(buffer_size=1, return_as_list=True)
        self.assertEqual(engine.hostname, 'my_hostname')

    def test_gathers_correct_prompt_from_prompt(self):
        engine = TestableSSHEngine(self.output_from_server)
        _ = engine.get_output(buffer_size=1, return_as_list=True)
        self.assertEqual(engine.prompt, 'my_hostname #')


