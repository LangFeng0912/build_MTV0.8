from argparse import ArgumentParser
from buildMT.build_dataset import build


def main():

    arg_parser = ArgumentParser(description="Build a Dataset for a new version of ManyTypes4Py")
    sub_parsers = arg_parser.add_subparsers(dest='cmd')

    build_parser = sub_parsers.add_parser('build')
    build_parser.set_defaults(func=build)

    args = arg_parser.parse_args()
    args.func(args)