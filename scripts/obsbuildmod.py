#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import argparse
import sys

parser = argparse.ArgumentParser(
    description='Modifies a package build targets in XML that is used by OBS for its "meta" information'
)
parser.add_argument("version", nargs="?", default=None)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--add", action="store_true")
group.add_argument("--delete", action="store_true")
group.add_argument("--reset", action="store_true")
args = parser.parse_args()

if (args.add or args.delete) and args.version is None:
    print("Error: SFOS Version unspecified\n")
    parser.print_help()
    sys.exit(-1)

arch_list = ["i486", "aarch64", "armv7hl"]
target = args.version

txt = sys.stdin.read().strip()
root = ET.fromstring(txt)
build = None
for child in root.findall("build"):
    if args.reset:
        root.remove(child)
    else:
        build = child

if build is None:
    build = ET.SubElement(root, "build")
    ET.SubElement(build, "disable")  # disable all by default

if args.add:
    for arch in arch_list:
        r = ET.SubElement(build, "enable", attrib=dict(repository=f"{target}_{arch}"))
elif args.delete:
    for enabled in build.findall("enable"):
        repository = enabled.attrib.get("repository", "")
        if repository.split("_")[0] == target:
            build.remove(enabled)

ET.indent(root)
print(ET.tostring(root, encoding="unicode"))
