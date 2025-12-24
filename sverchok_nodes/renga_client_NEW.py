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
ПЕРЕПИСАННАЯ ВЕРСИЯ БЕЗ ОТНОСИТЕЛЬНЫХ ИМПОРТОВ
"""

import socket
import json
import struct
import os
import sys

# Добавить путь к папке для импорта connection_protocol
_current_dir = os.path.dirname(os.path.abspath(__file__))
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)

# Импорт connection_protocol
try:
    import connection_protocol
except ImportError:
    # Если не работает, определяем функции здесь
    def send_message(sock, message_dict):
        if not sock:
            raise ValueError("Socket is None")
        json_str = json.dumps(message_dict)
        data = json_str.encode('utf-8')
        length = len(data)
        length_bytes = struct.pack('>I', length)
        sock.sendall(length_bytes)
        sock.sendall(data)
    
    def receive_message(sock, timeout=10.0):
        if not sock:
            raise ValueError("Socket is None")
        sock.settimeout(timeout)
        length_bytes = b''
        while len(length_bytes) < 4:
            chunk = sock.recv(4 - len(length_bytes))
            if not chunk:
                raise ConnectionError("Connection closed while reading message length")
            length_bytes += chunk
        length = struct.unpack('>I', length_bytes)[0]
        if length < 0 or length > 10 * 1024 * 1024:
            raise ValueError(f"Invalid message length: {length}")
        buffer = b''
        while len(buffer) < length:
            chunk = sock.recv(length - len(buffer))
            if not chunk:
                raise ConnectionError("Connection closed while reading message data")
            buffer += chunk
        return json.loads(buffer.decode('utf-8'))
    
    # Создать объект connection_protocol
    class _ConnectionProtocol:
        send_message = staticmethod(send_message)
        receive_message = staticmethod(receive_message)
    connection_protocol = _ConnectionProtocol()


class RengaConnectionClient:
    """
    TCP client for Renga plugin communication
    """
    
    def __init__(self, host="127.0.0.1", port=50100, timeout=10.0):
        self.host = host
        self.port = port
        self.timeout = timeout
    
    def send(self, message):
        """Send a message and receive response"""
        client = None
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(self.timeout)
            client.connect((self.host, self.port))
            
            connection_protocol.send_message(client, message)
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
        """Check if server is reachable"""
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(2.0)
            client.connect((self.host, self.port))
            client.close()
            return True
        except:
            return False

