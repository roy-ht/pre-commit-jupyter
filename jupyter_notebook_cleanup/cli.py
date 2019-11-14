import argparse
import copy
import difflib
import json
from collections import OrderedDict


def main():
    args = parse_args()
    patterns = args.pin_patterns.split(";")
    for path in args.files:
        remove_output(path, patterns=patterns, preview=args.dry_run, remove_kernel_metadata=args.remove_kernel_metadata)


def parse_args():
    psr = argparse.ArgumentParser()
    psr.add_argument("files", nargs="*", help="ipynb files")
    psr.add_argument("--dry-run", action="store_true", default=False)
    psr.add_argument("--remove-kernel-metadata", action="store_true", default=False)
    psr.add_argument(
        "-p", "--pin-patterns", default="[pin]", help="semicolon-separated patterns (wildcards are not supported)"
    )
    return psr.parse_args()


def check_if_unremovable(source, patterns):
    """comment annotation must be the first line and started with #"""
    for s in source:
        ss = s.strip()
        if ss.startswith("#") and any(x in ss for x in patterns):
            return True
    return False


def remove_output(path, patterns, preview, remove_kernel_metadata):
    """If preview=True, Do not overwrite a path, only display an diffs"""
    with open(path, "rt") as f:
        data = json.load(f, object_pairs_hook=OrderedDict)
    new_data = copy.deepcopy(data)
    if remove_kernel_metadata:
        kernelspec = new_data.get("metadata", {}).get("kernelspec", {})
        if "display_name" in kernelspec:
            kernelspec["display_name"] = ""
        if "name" in kernelspec:
            kernelspec["name"] = ""
    for cell in new_data["cells"]:
        if "execution_count" in cell:
            cell["execution_count"] = None
        if "outputs" in cell and "source" in cell:
            source = cell["source"]
            if not isinstance(source, list):
                continue
            if check_if_unremovable(source, patterns):
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
