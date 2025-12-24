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
Protocol for reliable TCP communication with Renga plugin
Uses length-prefixed messages (4 bytes big-endian + JSON data)
Compatible with C# Renga plugin protocol
"""

import struct
import socket
import json


def send_message(sock, message_dict):
    """
    Send a message with length prefix (4 bytes big-endian + JSON data)
    
    Args:
        sock: socket object
        message_dict: Message dictionary (will be converted to JSON)
    """
    if not sock:
        raise ValueError("Socket is None")
    
    # Convert to JSON
    json_str = json.dumps(message_dict)
    data = json_str.encode('utf-8')
    length = len(data)
    
    # Send length (4 bytes, big-endian)
    length_bytes = struct.pack('>I', length)
    sock.sendall(length_bytes)
    
    # Send data
    sock.sendall(data)


def receive_message(sock, timeout=10.0):
    """
    Receive a message with length prefix
    
    Args:
        sock: socket object
        timeout: timeout in seconds (default: 10.0)
    
    Returns:
        dict: Parsed JSON message as dictionary
    """
    if not sock:
        raise ValueError("Socket is None")
    
    # Set timeout
    sock.settimeout(timeout)
    
    # Read length (4 bytes)
    length_bytes = b''
    while len(length_bytes) < 4:
        chunk = sock.recv(4 - len(length_bytes))
        if not chunk:
            raise ConnectionError("Connection closed while reading message length")
        length_bytes += chunk
    
    length = struct.unpack('>I', length_bytes)[0]
    
    if length < 0 or length > 10 * 1024 * 1024:  # Max 10MB
        raise ValueError(f"Invalid message length: {length}")
    
    # Read JSON data
    buffer = b''
    while len(buffer) < length:
        chunk = sock.recv(length - len(buffer))
        if not chunk:
            raise ConnectionError("Connection closed while reading message data")
        buffer += chunk
    
    # Parse JSON and return as dict
    return json.loads(buffer.decode('utf-8'))

