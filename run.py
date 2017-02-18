from __future__ import print_function

import sys
sys.path.append("/cvmfs/ganga.cern.ch/Ganga/install/LATEST/python/")

from ganga import Job, File, LocalFile, Executable, DiracFile, Dirac
import zipfile

import time

# To get arguments from user
import argparse

VERSION = str(20170218)


def menu():
    """
    This function presents a 'graphical' menu for a user to enter their options for analysis.
    :return:
    """
    print("################################################")
    print("#             grid-analysis                    #")
    print("#          Version  " + VERSION + "                 #")
    print("#                   ~~~                        #")
    print("# https://github.com/willfurnell/grid-analysis #")
    print("#             Also on IRIS CVMFS               #")
    print("################################################")

    print("\n")
    print("This software will automatically upload data to a storage element and analyse it. Please provide a ZIP file"
          " of DSC and XYC files to be analysed, and a CSV file will be produced containing particle counts.")
    print("MAKE A NOTE OF YOUR JOB ID! You'll need it for checking status or retrieving data.")
    print("\n")
    print("What would you like to do?")
    print("1. Submit a job")
    print("2. Check a job status")
    print("3. Retrieve data locally")
    user_input = raw_input("> ")
    return user_input


def submit_job_interactive():
    """
    Allow a user to interactively submit a job, either locally or on GridPP.
    This will check that their input is valid and submit the job.
    """
    job_name = raw_input("Job name? > ")

    foundzip = False

    while foundzip is False:
        zip_name = raw_input("Path to ZIP file? Full path on your system please! > ")
        if not zipfile.is_zipfile(zip_name):
            # Not a zip file - so need to get them to enter again!
            print("The file you have supplied is not a zip file!")
            foundzip = False
        else:
            foundzip = True

    backend_chosen = False
    while backend_chosen is False:
        print("Note: Choosing the grid backend will automatically upload input to DIRAC storage in your home area for your VO.")
        backend_choice = raw_input("Grid backend? [Y/N] > ")
        if backend_choice.lower() == "y":
            backend = "grid"
            backend_chosen = True
        elif backend_choice.lower() == "n":
            backend = "local"
            backend_chosen = True
        else:
            backend_chosen = False

    j = Job()
    j.name = "grid-analysis_" + job_name
    # Tell Ganga it's running an executable
    j.application = Executable()
    j.application.exe = File('run_analyse.sh')
    if backend == "grid":
        grid_backend(j, zip_name, job_name)
    else:
        local_backend(j, zip_name)

    j.submit()


def submit_job(job_name, zip_name, backend):
    """
    Allows a user non-interactively submit a job (eg from a script)
    :param job_name: The name of the job (to be shown in DIRAC)
    :param zip_name: The path to the zip file
    :param backend: The backend to run, local or grid
    """

    if not zipfile.is_zipfile(zip_name):
        # Not a zip file - so need to get them to enter again!
        print("The file you have supplied is not a zip file!")
        raise Exception("ZIPFileError", "The ZIP file you supplied is not a ZIP file! Cannot continue.")

    j = Job()
    j.name = "grid-analysis_" + job_name
    # Tell Ganga it's running an executable
    j.application = Executable()
    j.application.exe = File('run_analyse.sh')

    if backend == "grid":
        grid_backend(j, zip_name)
    else:
        local_backend(j, zip_name)
    j.submit()


def grid_backend(j, zip_name):
    """
    Submit a job to the GridPP DIRAC instance. This is a lot more involved than the local one as we need to first
    upload the data to a storage element. Then we need to actually get working on submitting the job!
    :param j: The job
    :param zip_name: The path to the zip file (locally)
    :return:
    """

    # Set up a DiracFile object with the ZIP file the user specified
    # With thanks to https://lhcb.github.io/second-analysis-steps/01-managing-files-with-ganga.html
    df = DiracFile(zip_name)

    df.put() # Put to the users default SE

    j.inputfiles = [df, LocalFile('dscreader.py'), LocalFile('analyse.py')]
    j.outputfiles = [LocalFile('grid-analysis-frames.csv')]  # For now we'll download the output
    j.application.args = [df.namePattern]
    j.backend = Dirac()
    # We can force somewhere to run here, QMUL isn't working atm.
    # https://twiki.cern.ch/twiki/bin/view/LHCb/FAQ/GangaLHCbFAQ#How_can_I_set_which_Grid_site_my
    j.backend.settings['Destination'] = 'LCG.UKI-NORTHGRID-LIV-HEP.uk'
    # Don't have InputSandbox AND InputData!
    j.backend.settings['InputData'] = ''

def local_backend(j, zip_name):
    """
    Submit a job to the local Ganga instance, and run it locally. No fancy stuff here, just all LocalFiles
    :param j: The job
    :param zip_name: The path to the zip file (locally)
    :return:
    """
    j.inputfiles = [LocalFile(zip_name), LocalFile('dscreader.py'), LocalFile('analyse.py')]
    j.outputfiles = [LocalFile('grid-analysis-frames.csv')]
    j.application.args = [zip_name]


def check_job_status():
    raise NotImplementedError


def retrieve_data():
    raise NotImplementedError

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ganga based submission tool for Timepix data on GridPP/local running')

    parser.add_argument('--jobname', '-j', metavar='job_name', type=str,
                    help='the name of the job to conduct the analysis under.')

    parser.add_argument('--zip', '-z', metavar='user_zip', type=str,
                    help='a path to the zip file containing files to be analysed.')

    parser.add_argument('--grid', '-g', action='store_true',
                    help='if set grid-analysis will use the DIRAC backend (GridPP).')

    parser.add_argument('--interactive', '-i', action='store_true',
                    help='force the program to run in interactive mode.')

    args = parser.parse_args()

    if args.interactive is True or args.jobname is None or args.zip is None:
        user_input = ""

        while user_input not in ['1', '2', '3']:
            user_input = menu()

        if user_input is "1":
            submit_job_interactive()
        elif user_input is "2":
            check_job_status()
        elif user_input is "3":
            retrieve_data()

    else:
        if args.grid is None:
            backend = "local"
        else:
            backend = "grid"
        submit_job(args.jobname, args.zip, backend)
