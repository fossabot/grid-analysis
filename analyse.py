"""

grid-analysis analyse.py

This is designed to work on Scientific Linux 6, and therefore GridPP for analysing Timepix datasets in
x,y,C format.

Requires lucid-utils for actually analysing files.

"""


from lucid_utils import blobbing, xycreader

from lucid_utils.classification.old_algorithm import classify

import argparse

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


def analyse_folder(folder):

    # This will NOT work currently - just for reference
    for file in folder:

        filename = "x" # to be implemented

        frame = xycreader.read(file)

        counts = analyse_frame(frame)

        f = open("counts", 'w')

        f.write(filename + "|" + str(counts) + "\n")

        f.close()
