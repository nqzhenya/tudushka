import click
import lib

def list_print(data, length_name):
    if len(data) == 0:
        print('No filtered tasks in the list.')
        return
    
    if length_name > 30:
        length_name = 30
    
    print(f"{'id':<38}"
          f"{'name':<{(length_name + 2)}}"
          f"{'status':<5}")
    for task in data:
        if len(task['name']) > 30:
            print(f"{task['id']:<38}"
                  f"{task['name'][:(length_name - 3)] + '...  ':<{length_name}}"
                  f"{task['status']:<5}")
        else:
            print(f"{task['id']:<38}"
                  f"{task['name'] + '  ':<{length_name}}"
                  f"{task['status']:<5}")


@click.group()
def task_cli():
    pass

@task_cli.command()
@click.argument('name', nargs=1)
@click.option('--format', type=click.Choice(['json']))
def create(name, format):
    out = lib.create(name)
    if format:
        print(out)
    else:
        print(out['description'])

@task_cli.command()
@click.argument('del_id_list', nargs=-1)
def delete(del_id_list):
    lib.delete(del_id_list)

@task_cli.command()
@click.option('--filter', 
              type=click.Choice(['all', 'completed', 'uncompleted']), 
              default='uncompleted')
@click.option('--format', type=click.Choice(['json']))
def list(filter, format):        
    data, length_name = lib.list(filter)
    if format:
        lib.save_json(data, json_path)
    else:
        list_print(data, length_name)

@task_cli.command()
@click.argument('id', nargs=1)
@click.option('--status', 
              type=click.Choice(['new', 'done']))
def change(id, status):
    lib.change_status(id, status)

task_cli()