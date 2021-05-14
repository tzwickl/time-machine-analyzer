# Time Machine Analyzer

Time Machine Analyzer is a Python Application for analyzing the Time Machine Performance by parsing the log files and extracting the backup speed, size and amount of items to copy.
With this Python Application you can draw different graphs to visualize the performance of your Time Machine and analyze why and when the Backup gets stuck or takes longer than usual.

## Installation

1. Create a virtual environment by running the following command:

```bash
python3 -m venv env
```

2. Activate virtual environment

```bash
source env/bin/activate
```

3. Install needed requirements inside the virtual environment by running the following command:

```bash
python3 -m pip install -r requirements.txt
```

## Usage

To start the Application run the following command after activating the virtual environment:

```bash
python3 main.py
```

After starting the Application you need to enter the time range the analyzer should take into account when parsing the log file:

```bash
Enter time range <num>[m|h|d]:
```

Following input can be given to the Application:

| Input        | Meaning    | Description  |
|:-------------|:-------------|:-----|
| 1m     | 1 minute | Analyze all logs of the last minute |
| 1h     | 1 hour   | Analyze all logs of the last hour |
| 1d     | 1 day    | Analyze all logs of the last day |

After you are done you can leave the virtual environment by running the command

```bash
deactivate
```
## Example Output
After the Application was running successfully the following three graphs are produced for analyzing the Time Machine:

1. The first graph shows the Copy Speed of the Time Machine in MB/s and items/s to the Time Capsule or any other external drive:

![alt text](./examples/copy_speed.png "Time Machine Backup Copy Speed (MB/s)")

2. The second graph shows how many GBs were already copied to the Backup drive and how much in total needs to be copied:

![alt text](./examples/backup_size.png "Time Machine Backup Size (GB)")

3. The third graph shows how many items were already copied to the Backup drive and how much items in total needs to be copied:

![alt text](./examples/backup_items.png "Time Machine Backup Items")

Besides the three graphs an additional CSV and JSON file is created containing all log entries in the following format:

#### CSV
Date | Bytes Copied | Bytes to Copy | Items Copied | Items to Copy | Bytes per Second | Items per Second | Last Path Seen
|:---|:-------------|:--------------|:-------------|:--------------|:-----------------|:-----------------|:-------------|
| The date this log entry was created | Number of bytes copied to backup drive | Total number of Bytes to copy to backup drive | Number of items to copy to backup drive | Total number of items to copy to backup drive | Copy speed in bytes per second | Copy speed in items per second | Last path backed up while this log file was created |

#### JSON
Type: `array`

<i id="#">path: #</i>

&#36;schema: [https://json-schema.org/draft/2020-12/schema](https://json-schema.org/draft/2020-12/schema)

 - **_Items_**
 - Type: `object`
 - <i id="#/items">path: #/items</i>
 - This schema <u>does not</u> accept additional properties.
 - **_Properties_**
	 - <b id="#/items/properties/date_time">date_time</b> `required`
		 - Type: `string`
		 - <i id="#/items/properties/date_time">path: #/items/properties/date_time</i>
	 - <b id="#/items/properties/bytes_copied">bytes_copied</b> `required`
		 - _Number of bytes copied to backup drive_
		 - Type: `integer`
		 - <i id="#/items/properties/bytes_copied">path: #/items/properties/bytes_copied</i>
	 - <b id="#/items/properties/bytes_to_copy">bytes_to_copy</b> `required`
		 - _Total number of Bytes to copy to backup drive_
		 - Type: `integer`
		 - <i id="#/items/properties/bytes_to_copy">path: #/items/properties/bytes_to_copy</i>
	 - <b id="#/items/properties/items_copied">items_copied</b> `required`
		 - _Number of items to copy to backup drive_
		 - Type: `integer`
		 - <i id="#/items/properties/items_copied">path: #/items/properties/items_copied</i>
	 - <b id="#/items/properties/items_to_copy">items_to_copy</b> `required`
		 - _Total number of items to copy to backup drive_
		 - Type: `integer`
		 - <i id="#/items/properties/items_to_copy">path: #/items/properties/items_to_copy</i>
	 - <b id="#/items/properties/bytes_per_second">bytes_per_second</b> `required`
		 - _Copy speed in bytes per second_
		 - Type: `integer`
		 - <i id="#/items/properties/bytes_per_second">path: #/items/properties/bytes_per_second</i>
	 - <b id="#/items/properties/items_per_second">items_per_second</b> `required`
		 - _Copy speed in items per second_
		 - Type: `number`
		 - <i id="#/items/properties/items_per_second">path: #/items/properties/items_per_second</i>
	 - <b id="#/items/properties/last_path_seen">last_path_seen</b> `required`
		 - _Last path backed up while this log file was created_
		 - Type: `string`
		 - <i id="#/items/properties/last_path_seen">path: #/items/properties/last_path_seen</i>

<details>
  <summary>JSON Schema</summary>

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "TimeMachineLogEntries",
  "type": "array",
  "items": {
    "type": "object",
    "additionalProperties": false,
    "required": [
      "date_time",
      "bytes_copied",
      "bytes_to_copy",
      "items_copied",
      "items_to_copy",
      "bytes_per_second",
      "items_per_second",
      "last_path_seen"
    ],
    "properties": {
      "date_time": {
        "type": "string"
      },
      "bytes_copied": {
        "type": "integer",
        "description": "Number of bytes copied to backup drive"
      },
      "bytes_to_copy": {
        "type": "integer",
        "description": "Total number of Bytes to copy to backup drive"
      },
      "items_copied": {
        "type": "integer",
        "description": "Number of items to copy to backup drive"
      },
      "items_to_copy": {
        "type": "integer",
        "description": "Total number of items to copy to backup drive"
      },
      "bytes_per_second": {
        "type": "integer",
        "description": "Copy speed in bytes per second"
      },
      "items_per_second": {
        "type": "number",
        "description": "Copy speed in items per second"
      },
      "last_path_seen": {
        "type": "string",
        "description": "Last path backed up while this log file was created"
      }
    }
  }
}
```
</details>

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
