import sys
import json
import uuid
import copy

def create_file():
    data = {'tasks':{}}
    with open('data.json', 'w') as file:
        json.dump(data, file, ensure_ascii=False)

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
        print("Fill ids to be deleted like: python file.py delete 'id1' 'id2' ... ")
        return data
    
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
        return data
    
    if len(args) == 2:
        print('id', 'name')             
        for i in data['tasks'].keys():
            if data['tasks'][i]['status'] == 'to_do':
                print(i,
                    data['tasks'][i]['name'],
                    data['tasks'][i]['status']
                    )
        return data
    
    option = args[2]

    if option == '-all':
        print('id', 'name', 'status')             
        for i in data['tasks'].keys():
            print(i,
                data['tasks'][i]['name'],
                data['tasks'][i]['status']
                )
            
    elif option == '-created':
        print('id', 'name', 'status')             
        for i in data['tasks'].keys():
            if data['tasks'][i]['status'] == 'created':
                print(i,
                    data['tasks'][i]['name'],
                    data['tasks'][i]['status']
                    )

    return data

def create(data):
    if len(args) != 3:
        print("Fill name like: python file.py create 'name'")
        return

    task_name = args[2]
    
    changed_data = copy.deepcopy(data)
    
    id_task = str(uuid.uuid4())
    
    changed_data['tasks'][id_task] = {
        'name': task_name,
        'status': 'to_do'
        }
    
    return changed_data

def change_status(data):
    if len(args) != 4:
        print("Fill new status like: python file.py status 'task_id' 'completed'")
        return data
    
    changed_data = copy.deepcopy(data)
    
    task_id = args[2]
    
    if task_id not in changed_data['tasks'].keys():
        print(f"Task id: {task_id} does not exist")
        return data

    new_status = args[3]
    
    if new_status not in ('completed', 'to_do'):
        print(f"Available statuses: completed, to_do")
        return data
    
    changed_data['tasks'][task_id]['status'] = new_status
    
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


main()