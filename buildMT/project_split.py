'''
project-based split file
'''
import pandas as pd
import os
from os.path import join, isdir
from sklearn.model_selection import train_test_split
import sys

def find_repos_list(projects_path):
    repos_list = []
    for author in os.listdir(projects_path):
        if not author.startswith(".") and isdir(join(projects_path, author)):
            for repo in os.listdir(join(projects_path, author)):
                if isdir(join(projects_path, author, repo)):
                    repos_list.append(author + "/" + repo)
    return repos_list

def list_files(directory, file_ext = ".py"):
    filenames = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(file_ext):
                filenames.append(os.path.join(root, filename))

    return filenames

def split_repo_dataframe(df, test_size, valid_size):
    # Split dataframe into train and test
    train_df, test_df = train_test_split(df, test_size=test_size, random_state=42)

    # Split test dataframe into test and validation
    train_df, valid_df = train_test_split(train_df, test_size=valid_size, random_state=42)

    return train_df, test_df, valid_df

def label_file(p_dir, df, label):
    file_list = []
    for index, row in df.iterrows():
        repo_path = join(p_dir, row['project'].split("/")[0], row['project'].split("/")[1])
        file_list_repo = list_files(repo_path)
        file_list.extend(file_list_repo)
    files_df = pd.DataFrame(file_list, columns=['file'])
    files_df.insert(0, "type", label)
    return files_df


def split_projects(p_dir, csv_path):
    project_list = find_repos_list(p_dir)
    repo_df = pd.DataFrame(project_list, columns=['project'])
    # repo-based split
    print("Splitting Python code projects to train, test & validation sets")
    repo_df_train, repo_df_test, repo_df_valid = split_repo_dataframe(repo_df, 0.2, 0.1)

    # base on repo split, give files with label
    df_train = label_file(p_dir, repo_df_train, "train")
    df_valid = label_file(p_dir, repo_df_valid, "valid")
    df_test = label_file(p_dir, repo_df_test, "test")


    # Write recombined output
    print("Combining train, test & validation into dataframe")
    result_df = pd.concat([df_train, df_test, df_valid])

    print("Writing dataframe to:", csv_path)
    result_df.to_csv(csv_path, header=False, index=False, encoding=sys.getfilesystemencoding())
    repo_df_test.to_csv("test_repo.csv", header=False, index=False, encoding=sys.getfilesystemencoding())



