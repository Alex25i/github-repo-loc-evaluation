import json
import os
from json.decoder import JSONDecodeError

DATA_DIRECTORY = os.path.join("..", "data", "results")
LANGUAGES = ['Cpp', 'Go', 'Java', 'JavaScript', 'Objective-C', 'Perl', 'PHP', 'Python', ]


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

        repo_result = {'language': data['repo']['language'],
                       "old_repo": data['repo']['old_repo'],
                       "name": data['repo']['name'],
                       'n_code': data['analysis']['code'],
                       'n_comment': data['analysis']['comment'],
                       'n_blank': data['analysis']['blank'],
                       'n_files': data['analysis']['nFiles']}

        output.append(repo_result)
    return output


if __name__ == '__main__':
    data = import_files(os.path.abspath(DATA_DIRECTORY))
    pass
