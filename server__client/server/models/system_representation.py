from sys_database.database import create_db_object

from server__client.server.models.room import Room
from server__client.server.models.group import Group
from server__client.server.models.visual_element import *

from common.sys_types import rt, et
from common.relations.regulation import Regulation

def load_system_representation():
    db = create_db_object() #database object
    rooms_data = db.get_table(Room)
    for room_data in rooms_data:
        room_data = list(room_data) #room data is returned from db as tuple
        room = Room(*room_data[:Room.COL_ELS])
        
        room_data[Room.COL_ELS] = [db.read(Visual_element, 'id', int(el_num)) for el_num in room_data[Room.COL_ELS].split(',')] # tworzy wizualizacje
        room_data[Room.COL_TYPE] = rt( room_data[Room.COL_TYPE])

        if room_data[Room.COL_REGS]:    # jesi w pokoju sa regulacje
            for reg_id in room_data[Room.COL_REGS].split(','):
                reg_data = db.read_simple(Regulation.table_name, 'id', int(reg_id))
                reg_data[0] = 'r'+str(reg_data[0]) #dodanie litery r do id zeby bylo wiadomo ze chodzi o wartosc nastawy regulacji
                room_data[Room.COL_ELS].append(Visual_element(*reg_data[:3]))

        for el in room_data[Room.COL_ELS]: # Adds elements to groups and groups to rooms
            group_type = Group.el_to_group_map[el.type]
            group = Group(group_type)
            if group_type not in room.groups.keys():
                room.groups[group_type] = group
                group.elements.append(el)
            else:
                room.groups[group_type].elements.append(el)

        #room.add_element(*room_data[Room.COL_ELS])
    pass


if __name__ == "__main__":
    load_system_representation()