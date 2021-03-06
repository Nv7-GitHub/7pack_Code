# -*- coding: utf-8 -*-
import argparse
from sys import argv
from requests import get
from json import loads, load, dump
from git import Git
from shutil import rmtree
from os import chdir, getcwd, remove
from subprocess import call
from os.path import isfile
from os import mkdir
from sys import executable
from git.exc import GitCommandError
chdir("/".join(executable.split("/")[:-1]))

parser = argparse.ArgumentParser(description='A python package manager.')
parser.add_argument("pkgs", type=str, help="Packages to perform action.", nargs="+", default=True)
parser.add_argument("--user", help="User install", default=False, action='store_true')
parser.add_argument("--list", help="List all packages", default=False, action='store_true')
parser.add_argument("--install", help="Install pkgs", default=False, action='store_true')
parser.add_argument("--uninstall", help="Uninstall pkgs", default=False, action='store_true')
parser.add_argument("--upgrade", help="Upgrade packages", default=False, action='store_true')
args = parser.parse_args(argv[1:])
pkgs = args.pkgs

if args.pkgs == ["all"]:
    print("Locating all packages...")
    with open("indexed.json") as f:
        files_indexed = load(f)

    pkgs = list(files_indexed.keys())


if args.install:
    print("Fetching index...")
    index_url = "https://raw.githubusercontent.com/Nv7-GitHub/7Pack/master/repo.json"
    index = loads(get(index_url).text)
    try:
        mkdir("tmp")
    except FileExistsError:
        rmtree("tmp")
        mkdir("tmp")

    for pkg in pkgs:
        if pkg in index:
            try:
                print("Downloading package from " + index[pkg] + "...")
                Git("tmp").clone(index[pkg])
                pkgfile = index[pkg].split("/")[-1]
            except GitCommandError:
                print("Skipping " + pkg + " as it has not been indexed in the 7pack index.")
                continue

            print("Running setup.py...")
            origdir = getcwd()
            chdir("tmp/" + pkgfile)
            options = ["python3", "setup.py", "install", "--record", "record.txt"]
            if args.user:
                options.append("--user")
            try:
                call(options)

                print("Indexing installed files...")
                with open("record.txt") as f:
                    files = f.read()
            except Exception as e:
                print(e)

            chdir(origdir)
            with open("indexed.json") as f:
                before = load(f)
                before[pkg] = files.split("\n")
            with open("indexed.json", "w") as f:
                dump(before, f)

            print("Cleaning up...")
            rmtree("tmp/" + pkgfile)

            print("Installed " + pkg)

        else:
            print("Skipping " + pkg + " as it has not been indexed in the 7pack index.")

    rmtree("tmp")

if args.uninstall:
    print("Loading installed index.")
    with open("indexed.json") as f:
        files_indexed = load(f)

    for pkg in pkgs:
        if pkg in files_indexed:
            files = files_indexed[pkg]
            for file in files:
                if isfile(file):
                    print("Deleting " + file)
                    remove(file)
            print("Uninstalled " + pkg)
            del files_indexed[pkg]
        else:
            print("Skipping " + pkg + " as it has not been installed with 7pack.")

    print("Cleaning up...")
    with open("indexed.json", "w") as f:
        dump(files_indexed, f)

if args.upgrade:
    print("Uninstalling Packages... ")
    print("Loading installed index.")
    with open("indexed.json") as f:
        files_indexed = load(f)

    for pkg in pkgs:
        if pkg in files_indexed:
            files = files_indexed[pkg]
            for file in files:
                if isfile(file):
                    print("Deleting " + file)
                    remove(file)
            print("Uninstalled " + pkg)
            del files_indexed[pkg]
        else:
            print("Skipping " + pkg + " as it has not been installed with 7pack.")

    with open("indexed.json", "w") as f:
        dump(files_indexed, f)

    print("Installing latest versions...")
    print("Fetching index...")
    index_url = "https://raw.githubusercontent.com/Nv7-GitHub/7Pack/master/repo.json"
    index = loads(get(index_url).text)
    try:
        mkdir("tmp")
    except FileExistsError:
        rmtree("tmp")
        mkdir("tmp")

    for pkg in pkgs:
        if pkg in index:
            print("Downloading package from " + index[pkg] + "...")
            Git("tmp").clone(index[pkg])
            pkgfile = index[pkg].split("/")[-1]

            print("Running setup.py...")
            origdir = getcwd()
            chdir("tmp/" + pkgfile)
            options = ["python3", "setup.py", "install", "--record", "record.txt"]
            if args.user:
                options.append("--user")
            call(options)

            print("Indexing installed files...")
            with open("record.txt") as f:
                files = f.read()
            chdir(origdir)
            with open("indexed.json") as f:
                before = load(f)
                before[pkg] = files.split("\n")
            with open("indexed.json", "w") as f:
                dump(before, f)

            print("Cleaning up...")
            rmtree("tmp/" + pkg)

            print("Installed " + pkg)

        else:
            print("Skipping " + pkg + " as it has not been indexed in the 7pack index.")

    rmtree("tmp")

if args.list:
    print("Locating all packages...")
    with open("indexed.json") as f:
        files_indexed = load(f)

    pkgs = list(files_indexed.keys())

    for pkg in pkgs:
        print(pkg)
