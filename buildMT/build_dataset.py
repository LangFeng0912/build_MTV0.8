'''
This script use to build dataset for libsa4py
'''
from buildMT.collector import collect
from buildMT.cloner import clone_projects
from buildMT.deduplicate import deduplicate_files


def build(org_path, collect_repo, limit = 200):

    if collect_repo:
        print("Not using default dataset json, collecting dataset list...")
        json_name = "dataset.json"
        collect(json_name, limit)
        clone_projects(json_name, org_path, limit)
        deduplicate_files(org_path)
    else:
        print("Using default dataset json: dataset_list")
        clone_projects("dataset_list.json", org_path, limit)
        deduplicate_files(org_path)



# if __name__ == '__main__':
#     build()