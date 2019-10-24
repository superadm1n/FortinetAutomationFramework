from FortinetAutomationFramework.Interface import Interface
from FortinetAutomationFramework.Transport import SSHEngine

__version__ = '0.1'

def connect_ssh(hostname, username, password):
    transport = SSHEngine(hostname=hostname, username=username, password=password)
    return Interface(transport_engine=transport)