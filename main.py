import os
import datetime
import humanfriendly
import json
import csv
import matplotlib.pyplot as plt
import re

LOG_CMD = "log show --style syslog  --predicate 'senderImagePath contains[cd] \"TimeMachine\"' --info --last {time}"

class TimeMachineLogEntry:
    def __init__(self, line):
        self.date_time = None
        self.bytes_copied = 0
        self.bytes_to_copy = 0
        self.items_copied = 0
        self.items_to_copy = 0
        self.bytes_per_second = 0
        self.items_per_second = 0
        self.last_path_seen = ""
        # Regex Documentation: https://regex101.com/r/dLQn9W/latest
        self.regex = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(?:\.\d{6})?).*Copied (\d+(?:[,|.]\d+)? [kmgtp]?b).* of (\d+(?:[,|.]\d+)? [kmgtp]?b), (\d+).*of (\d+) items \(~((?:-|\d+(?:[,|.]\d+)?) [kmgtp]?b[/]s), (-|\d+(?:[,|.]\d+)?) items[/]s\).*- (.*)", re.IGNORECASE)
        self.parse_log_line(line)

    def __repr__(self) -> str:
        return json.dumps(vars(self), indent=4, sort_keys=True, default=str)

    def parse_log_line(self, line) -> None:
        groups = self.regex.match(line).groups()
        self.date_time = datetime.datetime.strptime(groups[0], '%Y-%m-%d %H:%M:%S.%f')
        self.bytes_copied = humanfriendly.parse_size(groups[1].replace(',', '.'))
        self.bytes_to_copy = humanfriendly.parse_size(groups[2].replace(',', '.'))
        self.items_copied = int(groups[3])
        self.items_to_copy = int(groups[4])
        self.bytes_per_second = humanfriendly.parse_size("0" if "-" in groups[5] else groups[5].replace(',', '.'))
        self.items_per_second = float("0" if "-" in groups[6] else groups[6].replace(',', '.'))
        self.last_path_seen = groups[7]

class TimeMachineAnalyzer:
    def __init__(self, time_range):
        print(f'Starting Time Machine Analyzer')
        self.time_range = time_range
        self.timeMachineLogEntries: [TimeMachineLogEntry] = []
        self.parse_logs()

    def get_log_files(self, time: str) -> str:
        return os.popen(LOG_CMD.format(time=time)).read()

    def print_logs(self):
        logs = self.get_log_files(self.time_range)
        print(logs)

    def parse_logs(self) -> None:
        logs = self.get_log_files(self.time_range)
        for line in logs.splitlines():
            if "MB/s" in line:
                self.timeMachineLogEntries.append(TimeMachineLogEntry(line))

    def plot_graph(self, attribute: str, scaling: int, y_label: str, title: str, axhline: int) -> None:
        dates = []
        values = []
        for log_entry in self.timeMachineLogEntries:
            dates.append(log_entry.date_time)
            values.append(vars(log_entry)[attribute] / scaling)
        plt.plot_date(dates, values, ls = '-')
        plt.ylabel(y_label)
        plt.xlabel('Date')
        plt.title(title)
        if axhline > 0:
            plt.axhline(axhline / scaling, color='red', ls='--')
        plt.show()

    def plot_graphs(self, attributes: [str], scalings: [int], y_labels: [str], titles: [str], axhlines: [int]) -> None:
        fig, axs = plt.subplots(len(attributes))
        for i in range(len(attributes)):
            dates = []
            values = []
            for log_entry in self.timeMachineLogEntries:
                dates.append(log_entry.date_time)
                values.append(vars(log_entry)[attributes[i]] / scalings[i])
            axs[i].plot_date(dates, values, ls = '-')
            axs[i].set_ylabel(y_labels[i])
            axs[i].set_xlabel('Date')
            axs[i].set_title(titles[i])
            axs[i].grid(which='major', axis='both', linestyle='--')
            if axhlines[i] > 0:
                axs[i].axhline(axhlines[i] / scalings[i], color='red', ls='--')
        plt.tight_layout()
        plt.show()

    def export_to_csv(self) -> None:
        with open('time_machine_log_entries.csv', mode='w') as time_machine_log_entries:
            employee_writer = csv.writer(time_machine_log_entries, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            employee_writer.writerow(['Date', 'Bytes Copied', 'Bytes to Copy', 'Items Copied', 'Items to Copy', 'Bytes per Second', 'Items per Second', 'Last Path Seen'])
            for log_entry in self.timeMachineLogEntries:
                employee_writer.writerow(
                    [
                        log_entry.date_time,
                        log_entry.bytes_copied,
                        log_entry.bytes_to_copy,
                        log_entry.items_to_copy,
                        log_entry.items_copied,
                        log_entry.bytes_per_second,
                        log_entry.items_per_second,
                        log_entry.last_path_seen
                    ])

    def export_to_json(self) -> None:
        with open('time_machine_log_entries.json', mode='w') as time_machine_log_entries:
            log_entries = []
            for log_entry in self.timeMachineLogEntries:
                dict = log_entry.__dict__
                del dict["regex"]
                log_entries.append(dict)
            time_machine_log_entries.write(json.dumps(log_entries, indent=4, sort_keys=True, default=str))

if __name__ == '__main__':
    val = input("Enter time range <num>[m|h|d]: ")
    seconds = humanfriendly.parse_timespan(val)
    timeMachineAnalyzer = TimeMachineAnalyzer(str(int(seconds / 60)) + "m")
    #timeMachineAnalyzer.plot_graph(log_entries, "bytes_per_second", 1000000, 'MB/s', 'Time Machine Backup Copy Speed (MB/s)', 0)
    timeMachineAnalyzer.plot_graphs(["bytes_per_second", "items_per_second"], [1000000, 1], ['MB/s', 'items/s'], ['Time Machine Backup Copy Speed (MB/s)', 'Time Machine Backup Copy Speed (items/s)'], [0, 0])
    timeMachineAnalyzer.plot_graphs(["bytes_copied", "bytes_to_copy"], [1000000000, 1000000000], ['GB', 'GB'], ['Time Machine Backup Copied (GB)', 'Time Machine Backup Total (GB)'], [0, 0])
    timeMachineAnalyzer.plot_graphs(["items_copied", "items_to_copy"], [1, 1], ['items', 'items'], ['Time Machine Backup Items Copied (items)', 'Time Machine Backup Items Total (items)'], [0, 0])
    timeMachineAnalyzer.export_to_csv()
    timeMachineAnalyzer.export_to_json()