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
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except OSError:
        return {}


def write_file_as_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f)


def get_parser():
    parser = argparse.ArgumentParser(description='instant the command we do next')
    parser.add_argument('open', metavar='OPEN', type=str, nargs='*',
                        help='open application')
    parser.add_argument('-d', '--desc', help='save application path')
    parser.add_argument('-save', '--save', help='save application path')
    parser.add_argument('-del', '--delete', help='save application path')
    parser.add_argument('-s', '--show', help='displays the current version of howdoi',
                        action='store_true')
    return parser


def command_line_runner():
    # the path of application key-application_name value-application_path
    application_path = read_file_as_json(APPLICATION_FILE_PATH)
    parser = get_parser()
    args = parser.parse_args()

    if args.show:
        sort = sorted(application_path.items(), key=lambda item: item[0])
        for a, p in sort:
            print('App: {0:10}  ==>  Desc: {1:10}'.format(a, p['Desc']))
        return

    if args.delete:
        del application_path[args.delete]
        write_file_as_json(APPLICATION_FILE_PATH, application_path)
        print('delete success!!!')
        return

    if args.open:
        if args.save:
            application_path[args.open[0]] = {'Path': args.save, "Desc": args.desc}
            write_file_as_json(APPLICATION_FILE_PATH, application_path)
            print("save {} Path {}".format(args.open[0], args.save))
        else:
            print(application_path[args.open[0]]['Path'])
            os.system('start "" "{}" '.format(application_path[args.open[0]]['Path']))
            print("Open '{}' Success!!!".format(args.open[0]))
    else:
        parser.print_help()


if __name__ == '__main__':
    command_line_runner()
    # application_path = read_file_as_json(APPLICATION_FILE_PATH)
    # t = {}
    # for key in application_path:
    #     t[key] = {'Path': application_path[key], "Desc": ''}
    # write_file_as_json(APPLICATION_FILE_PATH, t)#

    # print(file.write_file_as_json(APPLICATION_FILE_PATH, application_path))
    # print(file.read_file_as_json(APPLICATION_FILE_PATH))
