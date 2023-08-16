'''
This script use to build dataset for libsa4py
'''
from buildMT.collector import collect
from buildMT.cloner import clone_projects
from buildMT.deduplicate import deduplicate_files


def build(org_path, limit = 200):
    json_name = "dataset.json"
    collect(json_name, limit)
    clone_projects(json_name, org_path)
    deduplicate_files(org_path)


# if __name__ == '__main__':
#     build()