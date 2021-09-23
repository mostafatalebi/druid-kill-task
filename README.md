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

Here is a sample entry for a data source:
```json
{
        "numberOfPastDays" : 7,
        "dataSourceName" : "sample"
}
```
`numberOfPastDays` is the number of past days to keep data. A value of `7` means all segments which are flagged `unused` 
and belong to a period before the past 7 days, are targeted. In other words, the data of past week is kept and the rest 
targeted.

### Usage
```python
python main.py ./config.json
```

You can run it via cronjob and having it delete your unused segments on a daily basis.
