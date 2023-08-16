import os
import hashlib


def file_hash(file_path: str, hash_method) -> str:
    if not os.path.isfile(file_path):
        print('This file does not exist')
        return ''
    h = hash_method()
    with open(file_path, 'rb') as f:
        while b := f.read(8192):
            h.update(b)
    return h.hexdigest()


def file_md5(file_path: str) -> str:
    return file_hash(file_path, hashlib.md5)


def file_sha256(file_path: str) -> str:
    return file_hash(file_path, hashlib.sha256)


def traverse(path):
    count = 0
    file_dict = dict()
    for root, dirs, files in os.walk(path):

        for f in files:
            curfile = os.path.join(root, f)
            suffix = os.path.splitext(curfile)[-1]
            if suffix == '.py':
                hash_code = file_sha256(curfile)
                if not hash_code in file_dict:
                    file_dict[hash_code] = curfile
                else:
                    if not os.path.isdir(curfile):
                        os.remove(curfile)
                        count = count + 1

        for d in dirs:
            curfile = os.path.join(root, d)
            suffix = os.path.splitext(curfile)[-1]
            if suffix == '.py':
                hash_code = file_sha256(curfile)
                if not hash_code in file_dict:
                    file_dict[hash_code] = curfile
                else:
                    if not os.path.isdir(curfile):
                        os.remove(curfile)
                        count = count + 1
    print("%d duplicated files have been removed" % count)


def deduplicate_files(path):
    traverse(path)