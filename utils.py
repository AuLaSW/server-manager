"""
utils.py
--------

Utility functions and classes for server-manage
"""
from abc import ABC, abstractmethod
import subprocess as sp
from json import dump, load
from pathlib import Path


class Server(ABC):
    """An abstract class for implementing the server components."""
    
    def start(self, *progs):
        """Start the servers"""
        self._server_op(self, self._start_server, *progs)

    def restart(self, *progs):
        """Restart the servers"""
        self._server_op(self, self._restart_server, *progs)
    
    def update(self, *progs):
        """Update the servers"""
        self._server_op(self, self._update_server, *progs)
    
    def save_servers(self, path=None):
        """Save servers to path in json format"""
        if path is not None:
            path = self._path
        with open(path, 'wb') as fp:
            dump(self, fp)
        
    def load_servers(self, path=None):
        """Load server dictionary from path"""
        if path is not None:
            path = self._path
        with open(path, 'rb') as fp:
            servers = load(self, fp)
        
        # make sure all of the paths are Path objects and not strings
        for key in servers:
            self._servers[key] = Path(servers[key])
    
    def add_servers(self, **servers):
        """Append servers to server dictionary, does not allow overwriting"""
        for server in servers:
            if server in self._servers:
                raise AttributeError("Cannot overwrite an existing server.")
        
        self.update_servers(**servers)
    
    def update_servers(self, **servers):
        """Append servers to server dictionary, allows overwriting"""
        self._servers.update(servers)
    
    def remove_servers(self, *servers):
        """Remove listed servers from server dictionary"""
        for server in servers:
            try:
                self._servers.pop(server)
            except KeyError:
                continue
    
    def new_servers(self, **servers)
        """Update servers with new servers, removes old servers"""
        self._server = servers.copy()
    
    def _server_op(self, func, *progs):
        if progs:
            for server in progs:
                if server not in self.servers:
                    continue
                else:
                    func(self.servers[server])
            
            return
        
        for _, server in self._servers.items():
            func(server)
    
    @abstractmethod
    def _start_server(self, server):
        pass
    
    @abstractmethod
    def _restart_server(self, server):
        pass
    
    @abstractmethod
    def _update_server(self, server):
        pass
        

class BotFarm(Server):
    """A class for managing a discord bot server, where all operations are handled by bin files"""
    
    def __init__(self, servers={}, path=None):
        self._servers = servers
        
        if path is None:
            self._path = Path('.') / '.servers' / 'servers.json'
        else:
            self._path = path

    def _start_server(self, server):
        sp.run([server.parent / (server.name + '.start')])
    
    def _restart_server(self, server):
        sp.run([server.parent / (server.name + '.restart')])
    
    def _update_server(self, server):
        sp.run([server.parent / (server.name + '.update')])