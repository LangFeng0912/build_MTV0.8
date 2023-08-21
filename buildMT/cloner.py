import time
import pandas as pd
import os
from git.repo import Repo

# clone the repos from Github
def clone(path, filename, l):
    df = pd.read_json(filename, encoding="utf-8", orient='records')
    df = df[:l]
    rows = df.shape[0]
    print("%d repositoies from the json file have been readed" % rows)
    orient_dir = path
    print("The oriented folder is: " + orient_dir)
    print("start cloning...")
    i = 1
    for row in df.itertuples():
        print("The %d repositary" % i)
        author_name = getattr(row, 'author')
        repo_name = getattr(row, 'repo')
        author_path = os.path.join(orient_dir, author_name)
        repo_path = os.path.join(author_path, repo_name)
        if os.path.exists(repo_path):
            print("This repo has been cloned before... skipping")
            i = i + 1
            continue
        url = getattr(row, 'repoUrl') + '.git'
        print("Current downloading: " + url)
        print(repo_path)
        Repo.clone_from(url, to_path=repo_path)
        print('Download Succeed')
        time.sleep(1)
        i = i + 1

# clean the non-py file
def preprocess(path):
    def clean_nopy(file):
        for root, dirs, files in os.walk(file):
            # traverse the files
            for f in files:
                curfile = os.path.join(root, f)
                suffix = os.path.splitext(curfile)[-1]
                if not suffix == '.py' and not os.path.isdir(curfile):
                    os.remove(curfile)

            # traverse the directories
            for d in dirs:
                curfile = os.path.join(root, d)
                suffix = os.path.splitext(curfile)[-1]
                if not suffix == '.py' and not os.path.isdir(curfile):
                    os.remove(curfile)

    clean_nopy(path)

def clone_projects(jsonfile, path, limit):
    clone(path, jsonfile, limit)
    preprocess(path)