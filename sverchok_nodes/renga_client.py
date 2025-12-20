# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

"""
Reliable TCP client for communicating with Renga plugin
Uses length-prefixed protocol for reliable message delivery
Compatible with C# RengaConnectionClient
"""

import socket
import json
from . import connection_protocol


class RengaConnectionClient:
    """
    TCP client for Renga plugin communication
    Similar to RengaConnectionClient in C#
    """
    
    def __init__(self, host="127.0.0.1", port=50100, timeout=10.0):
        """
        Initialize client
        
        Args:
            host: Server host (default: 127.0.0.1)
            port: Server port (default: 50100)
            timeout: Connection timeout in seconds (default: 10.0)
        """
        self.host = host
        self.port = port
        self.timeout = timeout
    
    def send(self, message):
        """
        Send a message and receive response
        Creates a new connection for each request
        Similar to RengaConnectionClient.Send in C#
        
        Args:
            message: Message dictionary (will be converted to JSON)
        
        Returns:
            dict: Response dictionary
        """
        client = None
        try:
            # Create connection
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(self.timeout)
            client.connect((self.host, self.port))
            
            # Send message (connection_protocol expects dict, not JSON string)
            connection_protocol.send_message(client, message)
            
            # Receive response
            response = connection_protocol.receive_message(client, self.timeout)
            
            return response
        
        except socket.timeout:
            return {
                "id": message.get("id", ""),
                "success": False,
                "error": "Connection timeout"
            }
        except ConnectionRefusedError:
            return {
                "id": message.get("id", ""),
                "success": False,
                "error": "Connection refused. Make sure Renga plugin is running and server is started."
            }
        except socket.error as e:
            return {
                "id": message.get("id", ""),
                "success": False,
                "error": f"Socket error: {str(e)}"
            }
        except Exception as e:
            return {
                "id": message.get("id", ""),
                "success": False,
                "error": f"Error: {str(e)}"
            }
        finally:
            if client:
                try:
                    client.close()
                except:
                    pass
    
    def is_server_reachable(self):
        """
        Check if server is reachable (quick connection test)
        Similar to RengaConnectionClient.IsServerReachable in C#
        
        Returns:
            bool: True if server is reachable
        """
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(2.0)
            client.connect((self.host, self.port))
            client.close()
            return True
        except:
            return False

