"""

grid-analysis analyse.py

This is designed to work on Scientific Linux 6, and therefore GridPP for analysing Timepix datasets in
x,y,C format.

Requires lucid-utils for actually analysing files.

"""
# Makes it easy to convert between Python 2 and Python 3
from __future__ import print_function

# Required for analysis of files
from lucid_utils import blobbing, xycreader

from lucid_utils.classification.old_algorithm import classify

# To get arguments from user
import argparse

# For output use
import json

import time

import os


def get_hostname():
    try:
        with open("/etc/hostname", 'r') as f:
            return f.read()
    except IOError:
        return "Unknown"



def analyse_frame(frame):
    clusters = blobbing.find(frame)

    counts = {'alpha': 0, 'beta': 0, 'gamma': 0, 'proton': 0, 'muon': 0, 'other': 0}

    for cluster in clusters:
        particle_type = classify(cluster)
        counts[particle_type] += 1

    return counts


def analyse_folder(folder, final_output):

    files = []
    final_output["frames"] = {}

    for file in os.listdir(folder):
        # We don't want to add DSC files to the list, they can't be read by the xyc reader!
        if not file.endswith(".dsc"):
            files.append(file)

    for file in files:

        if file.endswith(".txt"):
            filename = file[:-4]
        else:
            filename = file

        frame = xycreader.read(folder + "/" + file)

        counts = analyse_frame(frame)

        final_output["frames"][filename] = {}
        final_output["frames"][filename]["counts"] = counts

    return final_output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='GridPP Analysis Script for Timepix data in the XYC format')

    parser.add_argument('folder', metavar='folder', type=str,
                   help='a path to the folder containing files to be analysed.')

    args = parser.parse_args()

    # Set up our final output, which will eventually be a JSON file. This is just some metadata that the user might
    # not always need - but can be pretty useful in some situations.

    final_output = {}

    final_output["metadata"] = {}
    final_output["metadata"]["generator"] = 'grid-analysis'
    final_output["metadata"]["algorithm"] = 'lucid-utils-old'
    final_output["metadata"]["node"] = get_hostname()
    final_output["metadata"]["gentime"] = time.time()

    final_output = analyse_folder(args.folder, final_output)

    final_file = json.dumps(final_output, sort_keys=True, indent=4)

    json_file = open("frames.json", "w")

    json_file.write(final_file)

    json_file.close()

