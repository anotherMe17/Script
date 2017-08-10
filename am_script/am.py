import argparse
import os, sys
import json

# this file path of setting
SETTING_FILE_PATH = sys.path[0]
# the name of application setting file
APPLICATION_SETTING_FILE = 'application_setting.txt'

APPLICATION_FILE_PATH = '{}\{}'.format(SETTING_FILE_PATH, APPLICATION_SETTING_FILE)


def read_file(path):
    """
    get file content. if file not exit return ''
    :param path: filePath + fileName
    :return: file content if empty return ''
    """
    try:
        with open(path, 'r') as f:
            return f.read()
    except OSError:
        return ''


def write_file(path, text):
    """
    write text into file. if not exit create file
    :param path: filePath + fileName
    :param text: content
    """
    with open(path, 'w') as f:
        f.write(text)


def read_file_as_json(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except OSError:
        return {}


def write_file_as_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f)


def get_parser():
    parser = argparse.ArgumentParser(description='instant the command we do next')
    parser.add_argument('open', metavar='OPEN', type=str, nargs='*',
                        help='open application')
    parser.add_argument('-s', '--save', help='save application path')
    parser.add_argument('-show', '--show', help='displays the current version of howdoi',
                        action='store_true')
    return parser


def command_line_runner():
    # the path of application key-application_name value-application_path
    application_path = read_file_as_json(APPLICATION_FILE_PATH)
    parser = get_parser()
    args = parser.parse_args()

    if args.show:
        for a, p in application_path.items():
            print('App: {0:10}  ==>  Path: {1:10}'.format(a, p))
        return

    if args.open:
        if args.save:
            application_path[args.open[0]] = args.save
            application_path = sorted(application_path.items())
            write_file_as_json(APPLICATION_FILE_PATH, application_path)
            print("save {} Path {}".format(args.open[0], args.save))
        else:
            os.system('start "" "{}" '.format(application_path[args.open[0]]))
            print("Open '{}' Success!!!".format(args.open[0]))
    else:
        parser.print_help()


if __name__ == '__main__':
    command_line_runner()
    # print(file.write_file_as_json(APPLICATION_FILE_PATH, application_path))
    # print(file.read_file_as_json(APPLICATION_FILE_PATH))
