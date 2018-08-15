import requests, json, datetime
import click

ENDPOINT = "https://api.clockify.me/api/"
headers = {"X-Api-Key": None}

def set_api(api):
    headers["X-Api-Key"] = api

def get_token(email, password):
    body = {"email": "***REMOVED***", "password": "***REMOVED***"}
    r = requests.post(ENDPOINT+'auth/token', headers=headers, json=body)
    return r.json()

def get_workspaces():
    r = requests.get(ENDPOINT+'workspaces/', headers=headers)
    return {workspace["name"]:workspace["id"] for workspace in r.json()}

def get_projects(workspace):
    r = requests.get(ENDPOINT+f'workspaces/{workspace}/projects/', headers=headers)
    return {project["name"]:project["id"] for project in r.json()}

def print_json(inputjson):
    print(json.dumps(inputjson, indent=2))

def get_current_time():
    return str(datetime.datetime.utcnow().isoformat())+'Z'

def start_time_entry(workspace, description, billable="false", project=None, task=None, tags=None):
    start = get_current_time()
    body = {"start": start, "billable": billable, "description": description,
            "projectId": project, "taskId": task, "tagIds": tags}
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

"""
@click.command()
@click.option('--count', default=1, help='Number of greetings')
@click.option('--name', prompt='Your name', help='The person to greet')
def hello(count, name):
    for x in range(count):
        click.echo(f'Hello {name}')
"""

@click.group()
def cli():
    pass

@click.command()
@click.argument('workspace')
@click.argument('description')
def start(workspace, description):
    print(start_time_entry(workspace, description))

@click.command()
@click.argument('workspace')
def finish(workspace):
    print(finish_time_entry(workspace))

cli.add_command(start)
cli.add_command(finish)

if __name__ == "__main__":
    set_api("W3NIM7B5h3SUokJc")
    workspaces = get_workspaces()
    print(workspaces)
    cli()
