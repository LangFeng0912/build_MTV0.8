from argparse import ArgumentParser
from buildMT.build_dataset import build

def build_main(args):
    print(1)
    if args.l:
        collect_limit = args.l
        build(args.p, collect_limit)
    else:
        build(args.p, 200)

def main():

    arg_parser = ArgumentParser(description="Build a Dataset for a new version of ManyTypes4Py")
    sub_parsers = arg_parser.add_subparsers(dest='cmd')

    build_parser = sub_parsers.add_parser('build')
    build_parser.add_argument("--p", required=True, type=str, help="Path to Python projects")
    build_parser.add_argument("--l", required=False, type=int, help="Number of projects to collect")
    build_parser.set_defaults(func=build_main)

    args = arg_parser.parse_args()
    args.func(args)