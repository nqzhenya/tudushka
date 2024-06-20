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
    
def save_json(data, json_path):
    with open(json_path, 'w') as file:
        json.dump(data, file)

def delete(del_id_list):
    data = get_storage()
    
    deleted_ids = []
    
    for del_task_id in del_id_list:
        if del_task_id in data['tasks'].keys():
            del data['tasks'][del_task_id]
            deleted_ids.append(del_task_id)
        else:
            print(f"Task id: {del_task_id} does not exist")
            
    if len(deleted_ids) > 0:
        print(f"Tasks with ids # {deleted_ids} deleted")
    
    save_file(data)


def list(filter):
    data = get_storage()
    
    result = []
    length_name = 0
    
    if filter == 'all':
        for task in data['tasks'].keys():
            result.append(data['tasks'][task])
            if length_name < len(data['tasks'][task]['name']):
                length_name = len(data['tasks'][task]['name'])
        return result, length_name

    filter_to_status = {'completed': TASK_STATUS['done'],
                        'uncompleted': TASK_STATUS['new']}
    
           
    for task in data['tasks'].keys():
        if data['tasks'][task]['status'] == filter_to_status[filter]:
            result.append(data['tasks'][task])
            if length_name < len(data['tasks'][task]['name']):
                length_name = len(data['tasks'][task]['name'])
    
    return result, length_name


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


def change_status(task_id, new_status):

    data = get_storage()
    changed_data = copy.deepcopy(data)
    
    if task_id not in changed_data['tasks'].keys():
        print(f"Task id: {task_id} does not exist")
        return

    changed_data['tasks'][task_id]['status'] = new_status
    
    print(f"Task with id # {task_id} change status on '{new_status}'")
    
    save_file(changed_data)


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