import argparse
import copy
import difflib
import json
from collections import OrderedDict


def main():
    args = parse_args()
    for path in args.files:
        remove_output(path, preview=args.dry_run)


def parse_args():
    psr = argparse.ArgumentParser()
    psr.add_argument("files", nargs="*", help="ipynb files")
    psr.add_argument("--dry-run", action="store_true", default=False)
    return psr.parse_args()


def check_if_unremovable(source):
    """comment annotation must be the first line and started with #"""
    for s in source:
        ss = s.strip()
        if ss.startswith("#") and "[pin]" in ss:
            return True
    return False


def remove_output(path, preview):
    """If preview=True, Do not overwrite a path, only display an diffs"""
    with open(path, "rt") as f:
        data = json.load(f, object_pairs_hook=OrderedDict)
    new_data = copy.deepcopy(data)
    for cell in new_data["cells"]:
        if "outputs" in cell and "source" in cell:
            source = cell["source"]
            if not isinstance(source, list):
                continue
            if check_if_unremovable(source):
                continue
            cell["outputs"] = []
    dump_args = {"ensure_ascii": False, "separators": (",", ": "), "indent": 1}
    if preview:
        before_j = json.dumps(data, **dump_args).splitlines()
        after_j = json.dumps(new_data, **dump_args).splitlines()
        print("\n".join(difflib.unified_diff(before_j, after_j, fromfile="before", tofile="after")))
    else:
        with open(path, "wt", encoding="utf-8") as fo:
            json.dump(new_data, fo, **dump_args)


if __name__ == "__main__":
    main()
