import datetime
import os
import re
import statistics
import time

FILE_ENDING_RESULT = '.result'
FILE_ENDING_SUMMARIZED = '.summarized'
FILE_ENDING_ANALYZED = '.analyzed'
RESULTS_FOLDER = 'time_measurements'


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()

        _write_time_measure_result_to_file(time1, time2)

        return ret

    def _write_time_measure_result_to_file(time1, time2):
        date = _get_timestamp(time2)
        result = '%s.%s, %0.3f' % (f.__module__, f.__qualname__, (time2 - time1) * 1000.0)
        _append_line_to_file(date + FILE_ENDING_RESULT, result)

    return wrap


def _append_line_to_file(filename, result):
    with open(os.path.join(RESULTS_FOLDER, filename), 'a+', encoding='utf8') as file:
        file.write(result + '\n')


def _get_timestamp(time2):
    return datetime.datetime.fromtimestamp(time2).strftime('%Y-%m-%d_%H:%M')


def export_analyzed_results_as_csv():
    results_map = _get_results_from_files()

    date = _get_timestamp(time.time())
    csv_header = 'func, MAX, MIN, AVG, MED, STD, VAR'
    _append_line_to_file(date + FILE_ENDING_ANALYZED, csv_header)

    for key in sorted(results_map, key=lambda k: statistics.mean(results_map[k]), reverse=True):
        csv_line = key + ',' + \
                   str(max(results_map[key])) + ',' + \
                   str(min(results_map[key])) + ',' + \
                   str(statistics.mean(results_map[key])) + ',' + \
                   str(statistics.median(results_map[key])) + ',' + \
                   str(statistics.stdev(results_map[key])) + ',' + \
                   str(statistics.variance(results_map[key]))
        _append_line_to_file(date + FILE_ENDING_ANALYZED, csv_line)


def export_results_as_csv():
    results_map = _get_results_from_files()
    date = _get_timestamp(time.time())

    for key in sorted(results_map, key=lambda k: statistics.mean(results_map[k]), reverse=True):
        values_as_csv = ",".join([str(v) for v in results_map[key]])
        csv_line = key + ',' + values_as_csv
        _append_line_to_file(date + FILE_ENDING_SUMMARIZED, csv_line)


def _get_results_from_files():
    results_map = {}
    result_files = [f for f in os.listdir(RESULTS_FOLDER)
                    if os.path.isfile(os.path.join(RESULTS_FOLDER, f)) and re.match(r'.*' + FILE_ENDING_RESULT, f)]

    for f in result_files:
        _read_results_from_file_to_map(f, results_map)

    return results_map


def _read_results_from_file_to_map(f, results_map):
    file = open(os.path.join(RESULTS_FOLDER, f))
    results = file.readlines()
    for r in results:
        _put_result_line_to_map(r, results_map)


def _put_result_line_to_map(r, results_map):
    function_name, function_time = r.split(',')
    if function_name not in results_map.keys():
        results_map[function_name] = []
    results_map[function_name].append(float(function_time))
