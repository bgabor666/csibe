#!/usr/bin/env python

import argparse
import os
import shutil
import subprocess
import sys
import time

def copy_result_files(result_origin_dir, csibe_results_path, llvm_revision):
    date_as_path = time.strftime("%Y/%m")
    date_with_dashes = time.strftime("%Y-%m-%d")

    json_dir = os.path.join(csibe_results_path, 'daily-results', date_as_path)
    json_result_file_path = os.path.join(json_dir, '{}-results.json'.format(date_with_dashes))

    csv_to_json_path = os.path.join(csibe_results_path, 'bin', 'csibe_csv_to_json.py')

    if not os.path.isdir(json_dir):
        os.makedirs(json_dir)

    for subdir in os.listdir(result_origin_dir):
        target_dir = os.path.join(csibe_results_path, subdir, date_as_path)

        if not os.path.isdir(target_dir):
            os.makedirs(target_dir)

        target_file = os.path.join(target_dir, "{}-{}-r{}-results.csv".format(date_with_dashes, subdir, llvm_revision))
        shutil.copyfile(os.path.join(result_origin_dir, subdir, "all_results.csv"),
                        target_file)

        f = open(target_file, "r")
        contents = f.readlines()
        f.close()

        contents.insert(4, "Revision,{}\n".format(llvm_revision))

        f = open(target_file, "w")
        contents = "".join(contents)
        f.write(contents)
        f.close()

        subprocess.call(['python', csv_to_json_path, '--csv-path', target_file, '--json-path', json_result_file_path])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--result-origin-dir")
    parser.add_argument("--csibe-results-path")
    parser.add_argument("--llvm-svn-path")

    args = parser.parse_args()

    llvm_revision = subprocess.check_output(["svnversion", args.llvm_svn_path])

    copy_result_files(args.result_origin_dir, args.csibe_results_path, llvm_revision.rstrip())

    git_add_return_value = subprocess.call(
                              ["git",
                               "-C",
                               args.csibe_results_path,
                               "add",
                               "--all"])

    if git_add_return_value:
        sys.exit(git_add_return_value)

    git_commit_return_value = subprocess.call(
                                 ["git",
                                  "-C",
                                  args.csibe_results_path,
                                  "commit",
                                  "-m",
                                  "Add results for r{}".format(llvm_revision.rstrip())])

    if git_commit_return_value:
        sys.exit(git_commit_return_value)

    git_push_return_value = subprocess.call(
                               ["git",
                                "-C",
                                args.csibe_results_path,
                                "push"])

    if git_push_return_value:
        sys.exit(git_push_return_value)
