import requests, json, datetime
import os
import click

ENDPOINT = "https://api.clockify.me/api/"
VERBOSE = False
CLOCKIFY_API_EMAIL = os.environ['CLOCKIFY_API_EMAIL']
CLOCKIFY_API_PASSWORD = os.environ['CLOCKIFY_API_PASSWORD']
headers = {"X-Api-Key": None}

def set_api(api):
    headers["X-Api-Key"] = api

def get_token(email, password):
    body = {"email": CLOCKIFY_API_EMAIL, "password": CLOCKIFY_API_PASSWORD}
    r = requests.post(ENDPOINT+'auth/token', headers=headers, json=body)
    return r.json()

def get_workspaces():
    r = requests.get(ENDPOINT+'workspaces/', headers=headers)
    return {workspace["name"]:workspace["id"] for workspace in r.json()}

def get_projects(workspace):
    r = requests.get(ENDPOINT+f'workspaces/{workspace}/projects/', headers=headers)
    return {project["name"]:project["id"] for project in r.json()}

def print_json(inputjson):
    click.echo(json.dumps(inputjson, indent=2))

def get_current_time():
    return str(datetime.datetime.utcnow().isoformat())+'Z'

def start_time_entry(workspace, description, billable="false", project=None, tag=None):
    start = get_current_time()
    body = {"start": start, "billable": billable, "description": description,
            "projectId": project, "taskId": None, "tagIds": tag}
    r = requests.post(ENDPOINT+f'workspaces/{workspace}/timeEntries/',
            headers=headers, json=body) 
    return r.json()

def get_in_progress(workspace):
    r = requests.get(ENDPOINT+f'workspaces/{workspace}/timeEntries/inProgress',
            headers=headers)
    return r.json()

def finish_time_entry(workspace):
    current = get_in_progress(workspace)
    current_id = current["id"]
    body = {"start": current["timeInterval"]["start"], 
            "billable": current["billable"], "description": current["description"], 
            "projectId": current["projectId"], "taskId": current["taskId"], 
            "tagIds": current["tagIds"], "end": get_current_time()}
    r = requests.put(ENDPOINT+f'workspaces/{workspace}/timeEntries/{current_id}',
            headers=headers, json=body)
    return r.json()

def get_time_entries(workspace):
    r = requests.get(ENDPOINT+f'workspaces/{workspace}/timeEntries/',
            headers=headers) 
    return r.json()[:10]

def remove_time_entry(workspace, tid):
    r = requests.delete(ENDPOINT+f'workspaces/{workspace}/timeEntries/{tid}',
            headers=headers) 
    return r.json()

def add_workspace(name):
    body = {"name": name}
    r = requests.post(ENDPOINT+f'workspaces/',
            headers=headers, json=body)
    return r.json()

def add_project(workspace, name):
    body = {"name": name, "clientId": "", "isPublic": "false", "estimate": None,
            "color": None, "billable": None}
    r = requests.post(ENDPOINT+f'workspaces/{workspace}/projects/',
            headers=headers, json=body)
    return r.json()

@click.group()
@click.option('--verbose', is_flag=True, help="Enable verbose output")
def cli(verbose):
    global VERBOSE
    VERBOSE = verbose 

    config_file = os.path.expanduser('~/.clockify.cfg')
    if os.path.exists(config_file):
        with open(config_file) as f:
            api = f.read()
            set_api(api)
    else:
        new = click.prompt("Your API key")
        with open(config_file, 'w') as f:
            f.write(new)
        set_api(new)

@click.command('start', short_help='Start a new time entry')
@click.argument('workspace') 
@click.argument('description')
@click.option('--billable', is_flag=True, default=False, help="Set if entry is billable")
@click.option('--project', '-p', default=None, help="Project ID")
@click.option('--tag', '-g', multiple=True, help='Multiple tags permitted')
def start(workspace, description, billable, project, tag):
    ret = start_time_entry(workspace, description, billable, project, list(tag))
    if VERBOSE:
        print_json(ret)

@click.command('finish', short_help='Finish an on-going time entry')
@click.argument('workspace')
def finish(workspace):
    ret = finish_time_entry(workspace)
    if VERBOSE:
        print_json(ret)

@click.command('projects', short_help='Show all projects')
@click.argument('workspace')
def projects(workspace):
    data = get_projects(workspace)
    if VERBOSE:
        print_json(data)
    else:
        for name in data:
            id = data[name]
            click.echo(f'{id}: {name}')

@click.command('workspaces', short_help='Show all workspaces')
def workspaces():
    data = get_workspaces()
    if VERBOSE:
        print_json(data)
    else:
        for name in data:
            id = data[name]
            click.echo(f'{id}: {name}')

@click.command('entries', short_help='Show previous 10 time entries')
@click.argument('workspace')
def entries(workspace):
    data = get_time_entries(workspace)
    if VERBOSE:
        print_json(data)
    else:
        for entry in data:
            click.echo(f'{entry["id"]}: {entry["description"]}')

@click.command('remove_entry', short_help='Remove entry')
@click.argument('workspace')
@click.argument('time entry ID')
def remove_entry(workspace, tid):
    ret = remove_time_entry(workspace, tid)
    if VERBOSE:
        print_json(ret)
    
@click.command('add_workspace', short_help='Add a workspace')
@click.argument('name')
def add_w(name):
    ret = add_workspace(name)
    if VERBOSE:
        print_json(ret)

@click.command('add_project', short_help='Add a project')
@click.argument('workspace')
@click.argument('name')
def add_p(workspacename):
    ret = add_project(workspace, name)
    if VERBOSE:
        print_json(ret)

cli.add_command(start)
cli.add_command(finish)
cli.add_command(projects)
cli.add_command(workspaces)
cli.add_command(entries)
cli.add_command(remove_entry)
cli.add_command(add_w)
cli.add_command(add_p)

def main():
    cli(obj={})

if __name__ == "__main__":
    main()
