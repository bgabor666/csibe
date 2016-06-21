#!/usr/bin/env python

import os
import subprocess
import sys

llvm_svn_url = "http://llvm.org/svn/llvm-project/llvm/trunk"
clang_svn_url = "http://llvm.org/svn/llvm-project/cfe/trunk"

llvm_path = "llvm"

def checkout_llvm(path):
    return checkout_svn(llvm_svn_url, path)

def checkout_clang(path):
    return checkout_svn(clang_svn_url, path)

def checkout_svn(url, path):
    return subprocess.call(
               ["svn",
                "co",
                clang_svn_url,
                path])

def run_llvm_cmake(llvm_path, build_path):
    if not os.path.isdir(build_path):
        os.makedirs(build_path)
    return subprocess.call(
               ["cmake",
                llvm_path,
                "-DCMAKE_BUILD_TYPE=Release",
                "-B{}".format(build_path)])

def run_llvm_build(build_path):
    return subprocess.call(
               ["make",
                "-C{}".format(build_path)])

if __name__ == "__main__":
    checkout_llvm("llvm")
    #checkout_clang("llvm/tools/clang")
    run_llvm_cmake("llvm", "build")
    run_llvm_build("build")
    
