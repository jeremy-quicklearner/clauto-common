# setup.py for clauto-common package
# Relies on clauto-common-version.txt being populated, which should be done by the release.sh script

import setuptools
import re

# Pull description from README
with open("README.md", "r") as fh:
    long_description = fh.read()

# Pull version from version file, populated before
with open("clauto-common-version.txt", "r") as fh:
    lines = fh.readlines()

# Filter out comments and whitespace
lines = [line.strip() for line in lines]
lines = [line for line in lines if not line == ""]
lines = [line for line in lines if not line.startswith('#')]

# Sanity checks
if not len(lines) == 1:
    print("[setup.py] clauto-common-version contents invalid")
    exit(1)
if not re.match(r"^[0-9]+\.[0-9]+\.[0-9]+$", lines[0]):
    print("[setup.py] Invalid version <" + lines[0] + ">")
    exit(1)
clauto_common_version = lines[0]

setuptools.setup(
    name="clauto_common",
    version=clauto_common_version,
    author="Jeremy Lerner",
    author_email="jeremy.cpsc.questions@gmail.com",
    description="Consumables-Listing AUTOmation Common Code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jeremy-quicklearner/clauto-common",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
