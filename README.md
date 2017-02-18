# grid-analysis

grid-analysis allows you to upload and analyse large datasets of Timepix XYC files to the UK Computing Grid (GridPP)
It's intended to make your life a bit easier as you don't need to worry about writing lots of different submission scripts, JDLs etc.

Simply do
```
python run.py
```
and you'll get an interactive prompt for submitting your job.

Or if you'd like to use a simple one liner, you can pass arguments like so (this means use the job name 'analysis_test', get my data from '/mnt/shared/gridpp/mydata/frames.zip' and run this on the grid rather than locally):

```
python run.py --jobname analsis_test --zip /mnt/shared/gridpp/mydata/frames.zip --grid
```

That's it! Check the status of your job at https://dirac.gridpp.ac.uk or use Ganga's 'jobs' command.

You may get asked to enter your certificate passphrase when using this software. Ganga is responsible for this as it will generate a proxy for you if you don't have one already.

This software has only been tested on the GridPP CernVM. It is written in Python 2 and requires access to CVMFS and Ganga.

For more general instructions on setting up a CernVM or using Ganga, check out the GridPP user guide! https://www.gridpp.ac.uk/userguide/