'''
This script use to build dataset for libsa4py
'''
from collector import collect
from cloner import clone_projects
from deduplicate import deduplicate_files


def build():
    json_name = "dataset.json"
    org_path = "raw_projects"
    collect(json_name)
    clone_projects(json_name, org_path)
    deduplicate_files(org_path)


if __name__ == '__main__':
    build()