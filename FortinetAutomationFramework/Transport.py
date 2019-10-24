from abc import ABC, abstractmethod
from paramiko import SSHClient, AutoAddPolicy
from socket import timeout as SocketTimeout


class BaseTransportEngine(ABC):

    def __new__(cls, *args, **kwargs):
        cls = super().__new__(cls)
        cls.cli_tracker = []
        return cls

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

    def send_command(self, command, end='\n'):
        self._update_cli_tracker(command)
        self._send_command(command, end)

    def _update_cli_tracker(self, command) -> None:
        if len(command) > 0:
            tmp = command.split()[0].lower()
            if tmp == 'config' or tmp == 'edit':
                self.cli_tracker.append(' '.join(command.split()[1:]))
            elif tmp == 'end':
                self.cli_tracker.pop()

    def send_command_get_output(self, command, end='\n', return_as_list=True, buffer_size=1024):
        self.send_command(command, end)
        return self.get_output(return_as_list=return_as_list, buffer_size=buffer_size)

    @abstractmethod
    def _send_command(self, command, end='\n'):
        pass

    @abstractmethod
    def get_output(self, buffer_size=1024, return_as_list=True):
        pass



    @abstractmethod
    def close_connection(self):
        pass


class SSHEngine(BaseTransportEngine):

    def __init__(self, hostname, username, password, timeout=.5):
        self._client = SSHClient()
        self._client.set_missing_host_key_policy(AutoAddPolicy())
        self._client.connect(hostname, username=username, password=password)
        self._shell = self._client.invoke_shell()
        self._shell.settimeout(timeout)

    def _send_command(self, command, end='\n'):
        self._shell.send(command + end)

    def get_output(self, buffer_size=1024, return_as_list=True):
        data = ''
        while True:
            try:
                data += bytes.decode(self._shell.recv(buffer_size))
            except SocketTimeout:
                break

        if return_as_list:
            return data.splitlines()
        else:
            return data

    def close_connection(self):
        self._client.close()