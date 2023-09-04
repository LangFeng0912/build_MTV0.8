import time
import pandas as pd
import os
from git.repo import Repo
from libsa4py.utils import ParallelExecutor
from joblib import delayed

# clone the repos from Github
def clone(repo_data, orient_dir):
    author_name = repo_data['author']
    repo_name = repo_data['repo']
    author_path = os.path.join(orient_dir, author_name)
    repo_path = os.path.join(author_path, repo_name)

    if os.path.exists(repo_path):
        print(f"This repo '{repo_name}' has been cloned before... skipping")
        return

    url = repo_data['repoUrl'] + '.git'
    print(f"Current downloading: {url}")
    print(repo_path)
    Repo.clone_from(url, to_path=repo_path)
    # print('Download Succeeded')
    time.sleep(1)

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

def clone_projects(jsonfile, path, jobs, limit):
    df = pd.read_json(jsonfile, encoding="utf-8", orient='records')
    df = df[:limit]
    rows = df.shape[0]
    print(f"{rows} repositories from the JSON file have been read")
    print("The oriented folder is:", path)
    print("Start cloning...")

    ParallelExecutor(n_jobs=jobs)(total=rows)(
        delayed(clone)(row._asdict(), path) for i, row in enumerate(df.itertuples(), start=1))

    preprocess(path)