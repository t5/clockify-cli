# Clockify-Cli
A command line interface for the time tracker app [Clockify](https://clockify.me/). 
## Usage 
```
Usage: clockify [OPTIONS] COMMAND [ARGS]...

Options:
  --verbose  Enable verbose output
  --help     Show this message and exit.

Commands:
  add_project    Add a project
  add_workspace  Add a workspace
  entries        Show previous 10 time entries
  finish         Finish an on-going time entry
  projects       Show all projects
  remove_entry   Remove entry
  start          Start a new time entry
  workspaces     Show all workspaces
```
To access the usage help for the various subcommands:
```
> clockify start --help
Usage: clockify start [OPTIONS] WORKSPACE DESCRIPTION

Options:
  --billable
  -p, --project TEXT
  -g, --tag TEXT      Multiple tags permitted
  --help              Show this message and exit.
```
## Installation
Move to the main directory that contains setup.py
```
pip install -e .
```
## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
