
class GenericInterfaceClass:

    def __init__(self, transport_engine):
        self.transport = transport_engine

    @property
    def cli_tracker(self):
        return self.transport.cli_tracker

    def send_command_get_output(self, command, end='\n', return_as_list=True, buffer_size=1024):
        return self.transport.send_command_get_output(command=command, end=end,
                                                      return_as_list=return_as_list, buffer_size=buffer_size)


class Interface(GenericInterfaceClass):

    @property
    def local_users(self):
        users = []
        self.transport.send_command_get_output('config global')
        self.transport.send_command_get_output('config system admin')
        for line in self.transport.send_command_get_output('show'):
            if line.lstrip().startswith('edit'):
                users.append(line.lstrip().split()[-1].strip('"'))
        return users