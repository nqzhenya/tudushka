#!/usr/bin/env python

import sys
import json
import uuid
import copy

TASK_STATUS = {'new': 'new',
               'done': 'done'}

def create_file():
    data = {'tasks':{}}
    with open('data.json', 'w') as file:
        json.dump(data, file)

def open_file():
    with open('data.json', 'r') as file:
        return json.load(file)

def save_file(data):
    with open('data.json', 'w') as file:
        json.dump(data, file, ensure_ascii=False)
        
def get_storage():
    try:
        return open_file()
    except:
        create_file()
        return open_file()


def help(): 
    print('This is task manager')
    print('Available commands:')
    for i in available_commands.keys():
        print(i)

def delete(del_id_list):

    data = get_storage()
    for del_task_id in del_id_list:
        if del_task_id in data['tasks'].keys():
            del data['tasks'][del_task_id]
        else:
            print(f"Task id: {del_task_id} does not exist")
    
    save_file(data)
    return data



def list(filter):
    data = get_storage()
    
    result = []
    
    if filter == 'all':
        for i in data['tasks'].keys():
            result.append(data['tasks'])
        return result

    filter_to_status = {'completed': TASK_STATUS['done'],
                        'uncompleted': TASK_STATUS['new']}
    
           
    for i in data['tasks'].keys():
        if data['tasks'][i]['status'] == filter_to_status[filter]:
            result.append(data['tasks'][i])
            
    return result


def create(name):
    
    data = get_storage()
    
    task_name = name

    changed_data = copy.deepcopy(data)

    id_task = str(uuid.uuid4())

    changed_data['tasks'][id_task] = {
        'name': task_name,
        'status': TASK_STATUS['new'],
        'id': id_task
        }
    
    save_file(changed_data)
    
    return changed_data


def change_status(task_id):

    data = get_storage()
    changed_data = copy.deepcopy(data)
    
    if task_id not in changed_data['tasks'].keys():
        print(f"Task id: {task_id} does not exist")
        return data

    new_status = args[3]
    
    if new_status not in (TASK_STATUS['new'], TASK_STATUS['done']):
        print(f"Available statuses: completed, to_do")
        return data
    
    changed_data['tasks'][task_id]['status'] = new_status
    
    save_file(changed_data)
    
    return changed_data


available_commands = {
        'create': create,
        'list': list,
        'delete': delete,
        'help': help,
        'change_status': change_status
        }

def main():
    global args
    args = sys.argv

    if len(args) == 1:
        help()
        return
    
    try:
        data = open_file()
    except:
        create_file()
        data = open_file()
        
    command = args[1]
    command_runner = available_commands.get(command)
    
    if not command_runner or command == 'help':
        help()
    else:
        changed_data = command_runner(data)
    
    if changed_data != data:
        save_file(changed_data)


# main()