'''
This file used to collect the repos from github and save as the json format
'''
import requests
import re
import time
import pandas as pd
from pandas import Series, DataFrame


def save_json(j_name, df):
    df.to_json(j_name, orient='records', force_ascii=False, indent=4)


def get_dependency_list(url):
    response = requests.get(url)
    page_source = response.text

    # get repository list
    reg = r'<span class="f5 color-fg-muted" data-repository-hovercards-enabled>([\s\S]+?)</span>'
    pattern = re.compile(reg)
    tags = re.findall(pattern, page_source)
    str0 = " ".join(tags)
    reg0 = r'"repository" data-hovercard-url="(.*?)/hovercard"'
    pattern0 = re.compile(reg0)
    repos = pattern0.findall(str0)
    print(repos)

    # get url for next page
    reg_next = r'Previous([\s\S]+?)>Next'
    pattern_next = re.compile(reg_next)
    str1 = "".join(pattern_next.findall(page_source))
    reg_url = r'href="([\s\S]+?)"'
    pattern1 = re.compile(reg_url)
    url_next = "".join(pattern1.findall(str1))
    print(url_next)

    # get stars
    reg_A = r'<svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-star">([\s\S]+?)/span>'
    p_A = re.compile(reg_A)
    str_A = "".join(p_A.findall(page_source)).replace(' ', '').replace('\n', '')
    reg_B = r'</svg>([\s\S]+?)<'
    p_B = re.compile(reg_B)
    stars = p_B.findall(str_A)
    print(stars)

    # get folks
    reg_C = r'<svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-repo-forked">([\s\S]+?)/span>'
    p_C = re.compile(reg_C)
    str_C = "".join(p_C.findall(page_source)).replace(' ', '').replace('\n', '')
    reg_D = r'</svg>([\s\S]+?)<'
    p_D = re.compile(reg_D)
    forks = p_D.findall(str_C)
    print(forks)

    return url_next, repos, stars, forks


def deduplicate():
    # read the rough dataframe from cvs
    repo_df = pd.read_csv('dataset_rough.csv', header=None)
    origin_row = repo_df.shape[0]
    print("%d repositoies from the orginal csv file have been readed" % origin_row)

    # drop the duplicated repos and save the clean dataset to csv
    repo_clean = repo_df.drop_duplicates(subset=None, keep='first', inplace=False)
    clean_row = repo_clean.shape[0]
    repo_clean.to_csv('dataset_clean.csv', index=False, header=False)
    print("%d repositoies have been saved to csv file after deduplivation" % clean_row)


def csv_to_json():
    def mk_url(s):
        return "https://github.com" + s

    def get_author(s):
        return s.split("/", 2)[1]

    def get_repo(s):
        return s.split("/", 2)[2]

    # convert csv into json format
    frame = pd.read_csv("dataset_clean.csv", header=None)
    frame.drop(0, axis=0, inplace=True)
    rows = frame.shape[0]
    print("%d repositoies from the csv file have been readed" % rows)
    frame.columns = Series(['temp', 'stars', 'forks'])
    frame['repoUrl'] = frame['temp'].map(mk_url)
    frame['author'] = frame['temp'].map(get_author)
    frame['repo'] = frame['temp'].map(get_repo)
    frame.drop(columns=['temp'])
    order = ['author', 'repo', 'repoUrl', 'stars', 'forks']
    frame = frame[order]

    save_json("dataset_clean.json", frame)


def repo_filter(filename, rule = "f50"):
    df = pd.read_json("dataset_clean.json", encoding="utf-8", orient='records')
    rows = df.shape[0]
    print("%d repositoies from the csv file have been readed" % rows)

    star_contains_str = df['stars'].apply(lambda x: isinstance(x, str)).any()
    fork_contains_str = df['forks'].apply(lambda x: isinstance(x, str)).any()

    if star_contains_str:
        df['stars'] = df['stars'].str.replace(',', '').astype(int)
    if fork_contains_str:
        df['forks'] = df['forks'].str.replace(',', '').astype(int)

    if rule == "f100":
        # filter the projects with 100+ stars and 10+ forks
        df_filter_100 = df[(df['stars'] > 100) & (df['forks'] > 10)]  # and
        rows_filter_0 = df_filter_100.shape[0]
        print("%d repositoies after filter with 100+ stars and 10+ forks" % rows_filter_0)
        save_json(filename, df_filter_100)

    elif rule == "f50":
        # filter the projects with 50+ stars and 5+ forks
        df_filter_50 = df[(df['stars'] > 50) & (df['forks'] > 5)]  # and
        rows_filter_1 = df_filter_50.shape[0]
        print("%d repositoies after filter with 50+ stars and 5+ forks" % rows_filter_1)
        save_json(filename, df_filter_50)

    else:
        print("rule not defined")


def collect( filename = 'dataset.json', limit: int = 200):
    # for mypy dependent repos
    url = 'https://github.com/python/mypy/network/dependents'
    # for pyright dependent repos
    # url = 'https://github.com/microsoft/pyright/network/dependents'
    i = 1  # page check
    repo_num = 0

    while repo_num < limit:
        url, repo_list, star_list, fork_list = get_dependency_list(url)
        # dependent_list = dependent_list + repo_list
        dataframe = pd.DataFrame({'repo_name': repo_list, 'star_num': star_list, 'fork_num': fork_list})
        dataframe.to_csv('dataset_rough.csv', mode='a', index=False, header=False)
        repo_num += dataframe.shape[0]
        print("Page %d has been crawled and saved to the csv" % i)
        i = i + 1
        time.sleep(5)

    deduplicate()

    csv_to_json()

    repo_filter(filename)