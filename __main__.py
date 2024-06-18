import click
import lib

def list_print(data):
    if len(data) == 0:
        print('No filtered tasks in the list')
        return
    
    print("{:<37} {:<15} {:<10}".format('id', 'name', 'status'))
    for task in data:
        print("{:<37} {:<15} {:<10}".format(task['id'], task['name'], task['status']))


@click.group()
def task_cli():
    pass

@task_cli.command()
@click.argument('name')
def create(name):
    lib.create(name)
    print(f"Task {name} created.")

@task_cli.command()
@click.argument('id', nargs=-1)
def delete(id):
    return id

@task_cli.command()
@click.option('--filter', type=click.Choice(['all', 'completed', 'uncompleted']), default='uncompleted')
def list(filter):
    
    data = lib.list(filter)
    list_print(data)



task_cli()