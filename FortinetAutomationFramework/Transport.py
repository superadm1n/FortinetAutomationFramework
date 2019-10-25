from abc import ABC, abstractmethod
from paramiko import SSHClient, AutoAddPolicy
from socket import timeout as SocketTimeout


class BaseTransportEngine(ABC):

    '''
    This class implements the API for all transport engines, In order to implement a new transport engine
    other than what is already implemented, inherit from this class and override the methods with the
    @abstractmethod decorator adding logic for sending commands, getting output, and closing the connection.
    Connection to the server should be handled via __init__()
    '''

    def __new__(cls, *args, **kwargs):
        cls = super().__new__(cls)
        cls.hostname = None
        cls.prompt = None
        return cls

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

    def _extract_hostname(self, output):
        """Extracts the hostname from the output of the firewall and caching that data, This method is run every time
        the framework grabs output from the server

        :param output: Output that was just returned
        :return: Nothing
        """
        if type(output) == list:
            pass
        else:
            output = output.splitlines()

        self.hostname = output[-1].split()[0]

    def _extract_full_prompt(self, output):
        """Extracts the prompt from the output of the firewall and caching that data, This method is run every time
       the framework grabs output from the server

       :param output: Output that was just returned
       :return: Nothing
       """
        if type(output) == list:
            pass
        else:
            output = output.splitlines()

        self.prompt = output[-1]

    def send_command(self, command, end='\n'):
        """Sends a command to the server

        :param command: Command to send
        :param end: End character to send after command (default: return '\n')
        :return: None
        """
        self._send_command(command, end)

    def send_command_get_output(self, command, end='\n', return_as_list=True, buffer_size=1024):
        """Sends a command to the server and immeadeatly gathers the output

        :param command: Command to send
        :param end: End character to send after the command (default: return '\n')
        :param return_as_list: Flag to return data as a list or as a string (Default: True, will return as list)
        :param buffer_size: Size of buffer to return data (default: 1024) This should not need modification
        :return: Data from Firewall
        """
        self.send_command(command, end)
        return self.get_output(return_as_list=return_as_list, buffer_size=buffer_size)

    def get_output(self,  buffer_size, return_as_list):
        """Method to handle getting output from server, this method should be called when trying to get data
        as it will utilize all of the callbacks required to keep various data up to date for the framework.
        This is what is called by send_command_get_output()

        :param buffer_size: Size of buffer to return data (default: 1024) This should not need modification
        :param return_as_list: Flag to return data as a list or as a string (Default: True, will return as list)
        :return: Data from Firewall
        """
        output = self._get_output(buffer_size=buffer_size, return_as_list=return_as_list)
        self._extract_hostname(output)
        self._extract_full_prompt(output)
        return output

    @abstractmethod
    def _send_command(self, command, end):
        '''Callback that handles actually gathering the data from the server. Override this to
        implement a specific transport engine

        :param command: Command to issue
        :param end: End character to send along with the command (Dont specify default when overriding)
        :return:
        '''
        pass

    @abstractmethod
    def _get_output(self, buffer_size, return_as_list):
        """Callback that handles actually gathering the data from the server. Override this to
        implement a specific transport engine

        :param buffer_size:
        :param return_as_list:
        :return:
        """
        pass

    @abstractmethod
    def close_connection(self):
        """Method to close connection to server

        :return:
        """
        pass


class SSHEngine(BaseTransportEngine):

    def __init__(self, hostname, username, password, timeout=.5):
        self._client = SSHClient()
        self._client.set_missing_host_key_policy(AutoAddPolicy())
        self._client.connect(hostname, username=username, password=password)
        self._shell = self._client.invoke_shell()
        self._shell.settimeout(timeout)
        self.send_command_get_output(' ')

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