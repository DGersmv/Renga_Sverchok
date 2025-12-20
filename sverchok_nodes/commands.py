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
Commands for Renga communication
Compatible with C# Renga plugin commands
"""

import json
import uuid
from datetime import datetime

# Global mapping for point GUIDs (similar to C# implementation)
_point_guid_map = {}
_point_to_guid_map = {}
_guid_counter = 0


def _get_point_guid(point, tolerance=0.001):
    """
    Get or create GUID for a point
    Similar to CreateColumnsCommand.GetPointGuid in C#
    """
    global _point_to_guid_map, _guid_counter
    
    # Check if point already has a GUID
    for existing_point, guid in _point_to_guid_map.items():
        if (abs(existing_point[0] - point[0]) < tolerance and
            abs(existing_point[1] - point[1]) < tolerance and
            abs(existing_point[2] - point[2]) < tolerance):
            return guid
    
    # Create new GUID
    new_guid = f"SV_Point_{_guid_counter}_{uuid.uuid4().hex[:8]}"
    _point_to_guid_map[tuple(point)] = new_guid
    _guid_counter += 1
    return new_guid


def create_update_points_message(points, heights=None):
    """
    Create update_points command message
    Similar to CreateColumnsCommand.CreateMessage in C#
    
    Args:
        points: List of points as tuples (x, y, z) or lists [x, y, z]
        heights: List of heights (one per point, or single value for all, default: 3000.0)
    
    Returns:
        dict: Message dictionary ready for JSON serialization
    """
    global _point_guid_map
    
    if heights is None:
        heights = [3000.0]
    
    # Normalize heights list
    if len(heights) < len(points):
        last_height = heights[-1] if heights else 3000.0
        heights.extend([last_height] * (len(points) - len(heights)))
    
    point_data = []
    for i, point in enumerate(points):
        # Convert point to list if needed
        if isinstance(point, tuple):
            point = list(point)
        
        x, y, z = point[0], point[1], point[2]
        height = heights[i] if i < len(heights) else heights[-1]
        
        # Validate height
        if height <= 0:
            height = 3000.0
        
        point_guid = _get_point_guid(point)
        renga_column_guid = _point_guid_map.get(point_guid)
        
        point_obj = {
            "x": float(x),
            "y": float(y),
            "z": float(z),
            "height": float(height),
            "grasshopperGuid": point_guid,
            "rengaColumnGuid": renga_column_guid if renga_column_guid else None
        }
        point_data.append(point_obj)
    
    message = {
        "id": str(uuid.uuid4()),
        "command": "update_points",
        "data": {
            "points": point_data
        },
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    }
    
    return message


def create_get_walls_message():
    """
    Create get_walls command message
    Similar to GetWallsCommand.CreateMessage in C#
    
    Returns:
        dict: Message dictionary ready for JSON serialization
    """
    message = {
        "id": str(uuid.uuid4()),
        "command": "get_walls",
        "data": {},
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    }
    
    return message


def update_mapping(point_guid, column_id):
    """
    Update mapping between point GUID and column ID
    Similar to CreateColumnsCommand.UpdateMapping in C#
    
    Args:
        point_guid: GUID of the point
        column_id: ID of the column in Renga
    """
    global _point_guid_map
    
    if column_id:
        _point_guid_map[point_guid] = str(column_id)

