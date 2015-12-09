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

parser = argparse.ArgumentParser(description='Analyse some files.')
parser.add_argument('folder', metavar='F', type=str, nargs='+',
                   help='a path to the folder containing files to be analysed.')


def analyse_frame(frame):
    clusters = blobbing.find(frame)

    counts = {'alpha': 0, 'beta': 0, 'gamma': 0, 'proton': 0, 'muon': 0, 'other': 0}

    for cluster in clusters:
        particle_type = classify(cluster)
        counts[particle_type] += 1

    return counts


def analyse_folder(folder, final_output):

    output = []

    # This will NOT work currently - just for reference
    for file in folder:

        filename = "x" # to be implemented

        frame = xycreader.read(file)

        counts = analyse_frame(frame)

        final_output["frames"] = {}
        final_output["frames"][filename] = {}
        final_output["frames"]["filename"]["counts"] = counts

        #f = open("counts.json", 'w')

        #f.write(json.dumps()"\n")

        #f.close()


if __name__ == "__main__":
    print("Main program logic")

    filename = "cas000"

    counts = {'alpha': 0, 'beta': 0, 'gamma': 0, 'proton': 0, 'muon': 0, 'other': 0}

    final_output = {}

    final_output["metadata"] = {}
    final_output["metadata"]["generator"] = 'grid-analysis'
    final_output["metadata"]["gentime"] = time.time()


    print(final_output)

