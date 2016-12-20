#!/bin/bash

# Wrapper for setting environment variables


# Add the Python packages from the CERN@school CVMFS
# repository to the PYTHONPATH environment variable.
export PYTHONPATH=/cvmfs/lucid.egi.eu/libraries/python2.6/site-packages/:/cvmfs/cernatschool.egi.eu/lib/python2.6/site-packages/:/cvmfs/cernatschool.egi.eu/lib64/python2.6/site-packages/:$PYTHONPATH
#
# Add CERN@school libraries to the LD_LIBRARY_PATH.
export LD_LIBRARY_PATH=/cvmfs/lucid.egi.eu/libraries/python2.6/site-packages/:/cvmfs/cernatschool.egi.eu/lib/:/cvmfs/cernatschool.egi.eu/lib64/:/cvmfs/cernatschool.egi.eu/lib64/atlas:$LD_LIBRARY_PATH
#
# Add CERN@school libraries to the PATH.
export PATH=/cvmfs/lucid.egi.eu/libraries/python2.6/site-packages/:/cvmfs/cernatschool.egi.eu/lib64/:/cvmfs/cernatschool.egi.eu/lib/:/cvmfs/cernatschool.egi.eu/lib64/atlas:$PATH

# Run the analysis
python analyse.py $1


