# coding=utf-8

#####################################################################
# Used to: compare plugins in new formula that generated by jcli in #
#          jenkins with updated plugins                             #
# How To Run: python diff-plugins.py formula.yaml new_formula.yaml  #
# ( First: remove {} in formula.yaml or new_formula.yaml )          #
#####################################################################


import argparse
import yaml

STATUS_ADD = 'add'
STATUS_DELETE = 'delete'
STATUS_UPDATE = 'update'
STATUS_NO_CHANGE = 'no_change'

add_plugins = []
delete_plugins = []
update_plugins = []


# check if exist by artifactId and groupId
def check(old_plugin_list, new_plugin_list):
    for new_p in new_plugin_list:
        status = STATUS_ADD
        for old_p in old_plugin_list:
            if new_p["artifactId"] == old_p["artifactId"] and new_p["groupId"] == old_p["groupId"]:
                status = STATUS_UPDATE
                if str(new_p["source"]["version"]) == str(old_p["source"]["version"]):
                    status = STATUS_NO_CHANGE
                else:
                    new_p["source"]["old_version"] = old_p["source"]["version"]
                break

        if status == STATUS_ADD:
            add_plugins.append(new_p)
        elif status == STATUS_UPDATE:
            update_plugins.append(new_p)

    check_deleted(old_plugin_list, new_plugin_list)


def check_deleted(old_plugin_list, new_plugin_list):
    for p in old_plugin_list:
        flag = True
        for new_p in new_plugin_list:
            if p["artifactId"] == new_p["artifactId"] and p["groupId"] == new_p["groupId"]:
                flag = False
                break
        if flag:
            delete_plugins.append(p)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convert two yaml files to dict and compare equality. Allows comparison of differently ordered keys.')
    parser.add_argument('file_paths', type=str, nargs=2,
                        help='Full paths to yaml documents')
    args = parser.parse_args()

    with open(args.file_paths[0], 'r') as rdr:
        data1 = rdr.read()

    with open(args.file_paths[1], 'r') as rdr:
        data2 = rdr.read()

    data1_dict = yaml.load(data1, Loader=yaml.FullLoader)
    data2_dict = yaml.load(data2, Loader=yaml.FullLoader)

    old_plugins = data1_dict["plugins"]
    new_plugins = data2_dict["plugins"]

    check(old_plugins, new_plugins)

    print "Add plugins: "
    print yaml.dump(add_plugins)

    print "\nupdate plugins: "
    print yaml.dump(update_plugins)

    print "\ndelete plugins: "
    print yaml.dump(delete_plugins)