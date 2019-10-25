
class GenericInterfaceClass:

    def __init__(self, transport_engine):
        self.transport = transport_engine
        self._system_status = None

    @property
    def current_prompt(self):
        return self.transport.prompt

    @property
    def system_status(self):
        if not self._system_status:
            self.return_cli_to_root()
            return self.transport.send_command_get_output('get system status', return_as_list=True)
        else:
            return self._system_status

    def return_cli_to_root(self):
        '''Method to issue the 'end' command until the CLI is at the root prompt. This is usefull when issuing
        a series of commands that you need to gaurintee a common place in the CLI structure. All methods
        that abstract data from the firewall should run this prior to any commands, via ssh it only takes about
        1 second to run and will prevent any errors if a user brings the prompt somewhere the framework is not
        expecting.

        :return:
        '''
        while '(' in self.transport.prompt:
            self.send_command_get_output('end')

    def send_command_get_output(self, command, end='\n', return_as_list=True, buffer_size=1024):
        '''This method opens up to the user to send commands and get output directly via the transport they are
        connected with

        :param command: command to issue
        :param end:
        :param return_as_list:
        :param buffer_size:
        :return:
        '''
        return self.transport.send_command_get_output(command=command, end=end,
                                                      return_as_list=return_as_list, buffer_size=buffer_size)


class Interface(GenericInterfaceClass):

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.transport.close_connection()

    def _extract_from_system_status(self, startswith_keyword):
        for line in self.system_status:
            if line.lower().startswith(startswith_keyword):
                return ' '.join(line.split(':')[1:]).strip()

    @property
    def local_users(self):
        self.return_cli_to_root()
        users = []
        self.transport.send_command_get_output('config global')
        self.transport.send_command_get_output('config system admin')
        for line in self.transport.send_command_get_output('show'):
            if line.lstrip().startswith('edit'):
                users.append(line.lstrip().split()[-1].strip('"'))
        return users

    @property
    def hostname(self):
        return self.transport.hostname

    @property
    def serial_number(self):
        return self._extract_from_system_status('serial')

    @property
    def bios_version(self):
        return self._extract_from_system_status('bios')

    @property
    def virus_database_version(self):
        return self._extract_from_system_status('virus-db')

    @property
    def operation_mode(self):
        return self._extract_from_system_status('operation mode')

