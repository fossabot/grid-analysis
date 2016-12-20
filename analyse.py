#!/usr/bin/env python
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

import zipfile

# To get arguments from user
import argparse

import os

import csv

import io

import dscreader

import time


def decompress(user_zip):
    """
    Decompress a ZIP file into a folder called 'decompressed_frames'
    :param user_zip: The zip file to be decompressed
    """
    archive = zipfile.ZipFile(user_zip, 'r')
    zipfile.ZipFile.extractall(archive, 'decompressed_frames')


def analyse_folder(folder):
    """
    Analyse a folder of XYC formatted files from a Timepix radiation detector, saving the output into a memory stream.

    :param folder: The folder containg the files to be analysed
    :return: A BytesIO representation of the CSV file
    """
    output = io.BytesIO()

    writer = csv.writer(output)

    writer.writerow(["Frame Name", "Capture Time", "Detector ID", "Bias Voltage", "Acquisition Time", "Alpha", "Beta", "Gamma", "Proton", "Muon", "Other"])

    files = []

    for f in os.listdir(folder):
        # We don't want to add DSC files to the list, they can't be read by the xyc reader!
        if not f.endswith(".dsc"):
            files.append(f)

    for file in files:
        frame = xycreader.read(folder + "/" + file)

        try:
            dsc = dscreader.DscFile(folder + "/" + file + ".dsc")
        except IOError:
            dsc = None
        # Analyse every frame...
        clusters = blobbing.find(frame)

        counts = {'alpha': 0, 'beta': 0, 'gamma': 0, 'proton': 0, 'muon': 0, 'other': 0}

        for cluster in clusters:
            particle_type = classify(cluster)
            counts[particle_type] += 1

        # Write the output of our analysis to the CSV file (well... the CSV file which is actually a bytes object)
        if dsc is not None:
            writer.writerow([file, dsc.getStartTime(), dsc.getChipId(), dsc.getBiasVoltage(), dsc.getAcqTime(),
                            counts['alpha'], counts['beta'], counts['gamma'], counts['proton'], counts['muon'],
                            counts['other']])
        else:
            writer.writerow([file, "", "", "", "", counts['alpha'], counts['beta'], counts['gamma'],
                            counts['proton'], counts['muon'], counts['other']])

    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='GridPP Analysis Script for Timepix data in the XYC format')

    parser.add_argument('user_zip', metavar='user_zip', type=str,
                   help='a path to the folder containing files to be analysed.')

    args = parser.parse_args()

    decompress(args.user_zip)

    output = analyse_folder('decompressed_frames')

    with open("grid-analysis-frames.csv", "wb") as f:
        output.seek(0)
        # Write the binary stream to the file. We do it here instead of line by line to save writing thousands of lines
        # to a file. Quicker to keep things in memory up until we really need to write it.
        f.write(output.getvalue())
