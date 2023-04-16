#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import sys

if len(sys.argv) != 3 or \
   sys.argv[1] not in ["--add", "--del"]:
    print(f"Usage: {sys.argv[0]} (--add | --del) SFOS_VERSION")
    sys.exit(1)

add = (sys.argv[1] == "--add")
target = sys.argv[2]
arch_list = ["i486", "aarch64", "armv7hl"]

txt = sys.stdin.read().strip()
root = ET.fromstring(txt)
build = None
for child in root.findall("build"):
    build = child

if build is None:
    build = ET.SubElement(root, "build")
    ET.SubElement(build, "disable") # disable all by default

if add:
    for arch in arch_list:
        r = ET.SubElement(build, "enable",
                          attrib=dict(repository = f"{target}_{arch}"))
else:
    for enabled in build.findall("enable"):
        repository = enabled.attrib.get("repository", "")
        if repository.split("_")[0] == target:
            build.remove(enabled)

ET.indent(root)
print(ET.tostring(root, encoding="unicode"))

