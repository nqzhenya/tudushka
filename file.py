import sys
import json
import uuid
import copy

def open_file():
    with open('data.json', 'r') as file:
        return json.load(file)

def save_file(data):
    with open('data.json', 'w') as file:
        json.dump(data, file, ensure_ascii=False)

def help(): 
    print('This is task manager')
    print('Available commands:')
    for i in available_commands.keys():
        print(i)

def delete(data):
    if len(args) < 3:
        print("Fill ids to be deleted like: python file.py 'id1' 'id2' ... ")
    del_id_list = args[2:]
    
    changed_data = copy.deepcopy(data)

    for del_task_id in del_id_list:
        if del_task_id in changed_data['tasks'].keys():
            del changed_data['tasks'][del_task_id]
        else:
            print(f"Task id: {del_task_id} does not exist")

    return changed_data

def list(data):
    if len(data['tasks']) == 0:
        print('no tasks in the list')
    else:
        print('id', 'name')             
        for i in data['tasks'].keys():
            print(i, data['tasks'][i]['name'])
    
    return data

def create(data):
    if len(args) != 3:
        print("Fill name like: python file.py 'name'")
        
    else:
        task_name = args[2]
        
        changed_data = copy.deepcopy(data)
        
        id_task = str(uuid.uuid4())
        
        changed_data['tasks'][id_task] = {
            'name': task_name
            }
        
        return changed_data

available_commands = {
        'create': create,
        'list': list,
        'delete': delete,
        'help': help,
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
        data = {}
        data['tasks'] = {}
        
    command = args[1]
    command_runner = available_commands.get(command)
    if not command_runner or command == 'help':
        help()
    else:
        changed_data = command_runner(data)
        
        save_file(changed_data)



main()