from buildMT.build_dataset import build


def main(cli_command):
    if cli_command == "build":
        build()