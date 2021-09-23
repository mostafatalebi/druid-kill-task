# Druid Task Killer
This (python) script can send Kill-Task requests to a druid overlord server (coordinator).
Kill-Task is a type of task that removes entries of metadata in a database as well
as the actual files on deep storage, for the list of segments which are "unused" for the given
period of time. 

This script is important if your server needs automated deletion of data without 
manual interference.

You can read more about this on druid documentation.
https://druid.apache.org/docs/latest/tutorials/tutorial-delete-data.html#run-a-kill-task

#### Configuration
You can pass a .json config file. The `config.sample.json` contains the schema required
for the configuration. Just make sure you include user:pass in the server URL value in case
your druid server is password protected.

*Data Sources* You can pass as many datasources as you want, and specify the number of days separately.

### Usage
```python
python main.py ./config.json
```

