import csv
import json
import os
from json.decoder import JSONDecodeError

DATA_RESULTS_DIRECTORY = os.path.join("..", "data", "results")
DATA__DIRECTORY = os.path.join("..", "data")
LANGUAGES = ['Cpp', 'Go', 'Java', 'JavaScript', 'Objective-C', 'Perl', 'PHP', 'Python']
SCRIPT_LANGUAGES = ['JavaScript', 'PHP', 'Python', 'Perl']
COMPILED_LANGUAGES = ['Cpp', 'Java', 'Go', 'Objective-C']


def import_files(dir_path):
    # Create a dict with an empty list for each language
    output = []  # output for old repos

    for file in os.scandir(dir_path):
        try:
            data = json.loads(open(file.path).read())
        except JSONDecodeError:
            raise (
                BaseException("Error while parsing file \"" + file.name + "\". See JSONDecodeError above for details."))

        # skip files which are not results
        if not data['_class'] == 'Result':
            continue

        # skip failed analyses
        if not data['success']:
            continue

        if not data['repo']['language'] in LANGUAGES:
            raise ValueError("The language \"" + data['repo']['language']
                             + "\" of Result of \"" + file.name + "\" is not a valid language.")

        if data['repo']['language'] in COMPILED_LANGUAGES:
            is_compiled = True
        elif data['repo']['language'] in SCRIPT_LANGUAGES:
            is_compiled = False
        else:
            raise ValueError("The language \"" + data['repo']['language']
                             + "\" of Result of \"" + file.name + "\" is not a compiled nor a interpreted language.")

        repo_result = {'language': data['repo']['language'],
                       'compiled_language': is_compiled,
                       'old_repo': data['repo']['old_repo'],
                       'name': data['repo']['name'],
                       'n_code': data['analysis']['code'],
                       'n_comment': data['analysis']['comment'],
                       'n_blank': data['analysis']['blank'],
                       'n_files': data['analysis']['nFiles']}

        output.append(repo_result)
    return output


def export_csv(data, output_file):
    column_names = data[0].keys()
    try:
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=column_names)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
    except IOError:
        raise IOError("Something went wrong")


if __name__ == '__main__':
    data = import_files(os.path.abspath(DATA_RESULTS_DIRECTORY))
    export_csv(data, os.path.join(DATA__DIRECTORY, "results.csv"))
