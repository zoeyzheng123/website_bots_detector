import re
import pandas as pd
from datetime import datetime
import statistics


def ReadFile(log_file_path):
    """
    :param log_file_path: path to the logs.txt file
    :return: pandas dataframe
    """

    logs = pd.DataFrame({'ip': [], 'timestamp': [], 'returned_ob': []})
    with open(log_file_path, "r") as file:
        for line in file:
            line = line.strip('\n')
            ip = line.split(' ')[0]
            timestamp = re.search(r'\[[\s\S]*\]', line).group()
            return_ob = line.split(' ')[-1]
            row = {'ip': ip, 'timestamp': timestamp, 'returned_ob': return_ob}
            logs = logs.append(row, ignore_index=True)
    return(logs)


def UniqueIntervals(alist):
    #calculate the time interval between rides in days
    alist = list(alist)
    l = []
    if(len(alist) > 1):
        for i in range(len(alist)-1, 0, -1):
            minutes = (alist[i] - alist[i-1]).seconds/60
            if minutes not in l:
                l.append(minutes)
        return(len(l))
    return(1)


def Convert(logs):
    """
    summarize logs by IP
    :param logs: logs dataframe with all log records
    :return: summarize log record by ip, output reuqest counts per IP, average object size and interval variety ratio
    """
    logs['timestamp'] = logs['timestamp'].apply(lambda x: datetime.strptime(x[1:-7], '%d/%b/%Y:%H:%M:%S'))
    logs['returned_ob'] = logs['returned_ob'].apply(lambda x: 0 if x == '-' else x)
    logs['returned_ob'] = pd.to_numeric(logs['returned_ob'])
    request_counts = logs.groupby('ip')['timestamp'].count().reset_index(name='hits')
    avg_returned_ob = logs.groupby('ip')['returned_ob']. \
        apply(lambda x: statistics.mean(x)).reset_index(name='avg_returned_ob')
    logs_summary_per_ip = pd.merge(avg_returned_ob, request_counts)

    ip_interval = logs.sort_values(['ip', 'timestamp']).groupby('ip')['timestamp']. \
        apply(UniqueIntervals).reset_index(name='unique_no_intervals')
    logs_summary_per_ip = pd.merge(logs_summary_per_ip, ip_interval)
    logs_summary_per_ip['interval_variety_ratio'] = logs_summary_per_ip['unique_no_intervals'] / logs_summary_per_ip['hits']
    return(logs_summary_per_ip)
