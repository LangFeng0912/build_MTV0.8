from argparse import ArgumentParser
from buildMT.build_dataset import build
from buildMT.project_split import split_projects

def build_main(args):
    if args.l:
        collect_limit = args.l
        build(args.p, args.collect_repo, collect_limit)
    else:
        build(args.p, args.collect_repo)

def split_main(args):
    split_projects(args.p, args.csv)

def main():

    arg_parser = ArgumentParser(description="Build a Dataset for a new version of ManyTypes4Py")
    sub_parsers = arg_parser.add_subparsers(dest='cmd')

    build_parser = sub_parsers.add_parser('build')
    build_parser.add_argument("--p", required=True, type=str, help="Path to Python projects")
    build_parser.add_argument("--l", required=False, type=int, help="Number of projects to collect")
    build_parser.add_argument("--collect", dest='collect_repo', action='store_true', help="Whether to collect repos from Github")

    build_parser.set_defaults(collect_repo=False)
    build_parser.set_defaults(func=build_main)

    split_parser = sub_parsers.add_parser('split')
    split_parser.add_argument("--p", required=True, type=str, help="Path to Python projects")
    split_parser.add_argument("--csv", type=str, help="Path to store the csv file", default='dataset_split.csv')
    split_parser.set_defaults(func=split_main)

    args = arg_parser.parse_args()
    args.func(args)