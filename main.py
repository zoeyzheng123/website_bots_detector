import sys
from pre_process_data import ReadFile, UniqueIntervals, Convert
from robots_detector import *

def main(file):
    """
    :param file: Input file path
    :return: list of robots ip
    """
    if (len(sys.argv) < 1):
        print("Not enough Arguments")
        exit(-1)
    file = sys.argv[0]
    try:
        logs = ReadFile(file)
    except:
        print("file doesn't exist, or wrong format")
        exit(-1)

    logs_summary = Convert(logs)
    logs_summary['if_robots'] = logs_summary.apply(lambda row: IfRobot(row['hits'], \
                       row['interval_variety_ratio'], row['avg_returned_ob']), axis=1)
    robots = logs_summary[logs_summary['if_robots']==True]['ip']
    return(robots)


if __name__ == '__main__':
    main()
