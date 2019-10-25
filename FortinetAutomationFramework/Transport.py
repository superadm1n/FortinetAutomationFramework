from abc import ABC, abstractmethod
from paramiko import SSHClient, AutoAddPolicy
from socket import timeout as SocketTimeout


class BaseTransportEngine(ABC):

    def __new__(cls, *args, **kwargs):
        cls = super().__new__(cls)
        cls.hostname = None
        cls.prompt = None
        return cls

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

    def send_command(self, command, end='\n'):
        self._send_command(command, end)

    def _extract_hostname(self, output):
        if type(output) == list:
            pass
        else:
            output = output.splitlines()

        self.hostname = output[-1].split()[0]

    def _extract_full_prompt(self, output):
        if type(output) == list:
            pass
        else:
            output = output.splitlines()

        self.prompt = output[-1]

    def send_command_get_output(self, command, end='\n', return_as_list=True, buffer_size=1024):
        self.send_command(command, end)
        return self.get_output(return_as_list=return_as_list, buffer_size=buffer_size)

    def get_output(self,  buffer_size, return_as_list):
        output = self._get_output(buffer_size=buffer_size, return_as_list=return_as_list)
        self._extract_hostname(output)
        self._extract_full_prompt(output)
        return output

    @abstractmethod
    def _send_command(self, command, end):
        pass

    @abstractmethod
    def _get_output(self, buffer_size, return_as_list):
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
        self. send_command_get_output(' ')

    def _send_command(self, command, end):
        self._shell.send(command + end)

    def _get_output(self, buffer_size, return_as_list):
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