"""
Wrapper class and helper methods for the Timepix DSC files. This file is primarily written by Dr. Tom Whyntie, and has
been modified by Will Furnell for just getting values from the DSC files (removing non relevant parts and includes).
"""

import time
import re

"""
Convenience values pertaining to the DSC files.
"""

DSC_ACQ_MODE_STRING = "\"Acq mode\" (\"Acquisition mode\"):"

DSC_ACQ_TIME_STRING = "\"Acq time\" (\"Acquisition time [s]\"):"

DSC_CHIPID_STRING = "\"ChipboardID\" (\"Medipix or chipboard ID\"):"

DSC_DACS_STRING = "\"DACs\" (\"DACs values of all chips\"):"

DSC_FIRMWARE_STRING = "\"Firmware\" (\"Firmware version\"):"

DSC_BIAS_VOLTAGE_STRING = "\"HV\" (\"Bias voltage [V]\"):"

DSC_HW_TIMER_STRING = "\"Hw timer\" (\"Hw timer mode\"):"

DSC_INTERFACE_STRING = "\"Interface\" (\"Medipix interface\"):"

DSC_MPX_CLOCK_STRING = "\"Mpx clock\" (\"Medipix clock [MHz]\"):"

DSC_MPX_TYPE_STRING = "\"Mpx type\" (\"Medipix type (1-2.1, 2-MXR, 3-TPX)\"):"

DSC_PIXELMAN_VERSION_STRING = "\"Pixelman version\" (\"Pixelman version\"):"

DSC_POLARITY_STRING = "\"Polarity\" (\"Detector polarity (0 negative, 1 positive)\"):"

DSC_START_TIME_STRING = "\"Start time\" (\"Acquisition start time\"):"

DSC_START_TIME_S_STRING = "\"Start time (string)\" (\"Acquisition start time (string)\"):"

#DSC_TPX_CLOCK_STRING = "\"Timepix clock\" (\"Timepix clock (0-3: 10MHz, 20MHz, 40MHz, 80MHz)\"):"
DSC_TPX_CLOCK_STRING = "Timepix clock"

DSC_NAME_SN_STRING = "\"Name+SN\" (\"Name and serial number\"):"

"""
Convenience values for dataset processing.
Obtained from: https://raw.githubusercontent.com/CERNatschool/daqmap-zip-processor/master/cernatschool/datavals.py
"""

TPX_CLOCK_VALS = {
    0 : 10.0,
    1 : 20.0,
    2 : 40.0,
    3 : 80.0
}

"""
Handler methods for various parts of the Timepix datafiles.
"""


def isChipIdValid(chipid):
    """ Does the chip ID conform to the UVV-XYYYY format? """

    # regex match for the chipboard ID.
    r = re.compile(r'[A-Z]\d{2,2}-[A-Z]\d{4,4}')

    if r.match(chipid) is not None:
        return True
    else:
        return False


def getPixelmanTimeString(st):
    """ Get the timestring in the Pixelman (custom) format. """

    ## The seconds from the start time provided.
    sec = int(str(st).split(".")[0])

    ## The seb-second value.
    #sub = int(("%.7f" % st).strip().split(".")[1])
    sub = ("%.6f" % st).strip().split(".")[1]

    ## The time represented as a Python time object.
    mytime = time.gmtime(sec)

    ## The time in the Pixelman format.
    #sts = time.strftime("%a %b %d %H:%M:%S.", mytime) + ("%06d" % (sub)) + time.strftime(" %Y", mytime)
    sts = time.strftime("%a %b %d %H:%M:%S.", mytime) + ("%s" % (sub)) + time.strftime(" %Y", mytime)

    return sec, sub, sts

"""
The actual parsing code is HERE!
"""


class DscFile:
    """
    A wrapper class for the Pixelman DSC files.
    """

    def __init__(self, dscfilename):
        """ The constructor. """

        ## The frame width.
        self.__fWidth = None

        ## The frame height.
        self.__fHeight = None

        ## The acquisition mode.
        self.__acqMode = None

        ## The acquisition time.
        self.__acqTime = None

        ## The chip ID.
        self.__chipid = None

        ## The DAC values.
        self.__dacs = None

        ## The firmware version.
        self.__firmwarev = None

        ## The bias voltage.
        self.__hv = None

        ## The HW timer mode.
        self.__hwTimerMode = None

        ## The interface.
        self.__interface = None

        ## The Medipix clock value.
        self.__mpxClock = None

        ## The Medipix type.
        self.__mpxType = None

        ## The Pixelman version.
        self.__pixelmanv = None

        ## The polarity.
        self.__polarity = None

        ## The start time.
        self.__startTime = None

        ## The start time (string).
        self.__startTimeS = None

        ## The Timepix clock value.
        self.__tpxClock = None

        ## The name and serial number.
        self.__nameAndSN = None

        # BiasLVDS defined here as it breaks if not defined in the file
        self.__BiasLVDS = None

        ## The DSC file name.
        self.__dscfilename = dscfilename

        self.__datafilename = dscfilename[:-4]

        # Process the DSC file.
        self.processDscFile()

    def __lt__(self, other):
        return self.getStartTime() < other.getStartTime()

    def getDscFilename(self):
        return self.__dscfilename

    def getDataFilename(self):
        return self.__datafilename

    def getFrameWidth(self):
        return self.__fWidth

    def getFrameHeight(self):
        return self.__fHeight

    def getAcqMode(self):
        return self.__acqMode

    def getAcqTime(self):
        return self.__acqTime

    def getChipId(self):
        return self.__chipid

    def getDACs(self):
        return self.__dacs

    def getFirmwareVersion(self):
        return self.__firmwarev

    def getBiasVoltage(self):
        return self.__hv

    def getIKrum(self):
        return self.__IKrum

    def getDisc(self):
        return self.__Disc

    def getPreamp(self):
        return self.__Preamp

    def getBuffAnalogA(self):
        return self.__BuffAnalogA

    def getBuffAnalogB(self):
        return self.__BuffAnalogB

    def getHist(self):
        return self.__Hist

    def getTHL(self):
        return self.__THL

    def getTHLCoarse(self):
        return self.__THLCoarse

    def getVcas(self):
        return self.__Vcas

    def getFBK(self):
        return self.__FBK

    def getGND(self):
        return self.__GND

    def getTHS(self):
        return self.__THS

    def getBiasLVDS(self):
        return self.__BiasLVDS

    def getRefLVDS(self):
        return self.__RefLVDS

    def getHwTimerMode(self):
        return self.__hwTimerMode

    def getInterface(self):
        return self.__interface

    def getMpxClock(self):
        return self.__mpxClock

    def getMpxType(self):
        return self.__mpxType

    def getPixelmanVersion(self):
        return self.__pixelmanv

    def getPolarity(self):
        return self.__polarity

    def getStartTime(self):
        return self.__startTime

    def getStartTimeS(self):
        return self.__startTimeS

    def getTpxClock(self):
        return self.__tpxClock

    def getNameAndSerialNumber(self):
        return self.__nameAndSN


    def processDscFile(self):
        """ Process the detector settings file (.dsc). """

        # The DSC file.
        f = open(self.__dscfilename, "r")

        ## The lines of the DSC file.
        ls = f.readlines()

        # Close the DSC file.
        f.close()

        # The frame width and height.
        whvals = ls[2].strip().split(" ")

        try:
            self.__fWidth = int(whvals[2].split("=")[1])
        except TypeError:
            raise IOError("BAD_WIDTH")

        if self.__fWidth < 256 or self.__fWidth > 1024:
            raise IOError("BAD_WIDTH")

        try:
            self.__fHeight = int(whvals[3].split("=")[1])
        except TypeError:
            raise IOError("BAD_HEIGHT")

        if self.__fHeight < 256 or self.__fHeight > 1024:
            raise IOError("BAD_HEIGHT")


        # Loop over the lines of the DSC file.
        for i, l in enumerate(ls):
            #print("%5d: %s" % (i, l.strip()))

            # Acquisition mode.
            if DSC_ACQ_MODE_STRING in l:
                try:
                    self.__acqMode = int(ls[i+2].strip())
                except ValueError:
                    raise IOError("BAD_ACQ_MODE")

            elif DSC_ACQ_TIME_STRING in l:
                try:
                    self.__acqTime = float(ls[i+2].strip())
                except ValueError:
                    raise IOError("BAD_ACQ_TIME")

            elif DSC_CHIPID_STRING in l:

                chipid = ls[i+2].strip()
                if not isChipIdValid(chipid):
                    raise IOError("Invalid chip ID in the DSC file.")
                self.__chipid = chipid

            elif DSC_DACS_STRING in l:

                # Break down the DAC string.
                self.__dacs = [int(x) for x in ls[i+2].strip().split(" ")]

                self.__IKrum       = self.__dacs[0]
                self.__Disc        = self.__dacs[1]
                self.__Preamp      = self.__dacs[2]
                self.__BuffAnalogA = self.__dacs[3]
                self.__BuffAnalogB = self.__dacs[4]
                self.__Hist        = self.__dacs[5]
                self.__THL         = self.__dacs[6]
                self.__THLCoarse   = self.__dacs[7]
                self.__Vcas        = self.__dacs[8]
                self.__FBK         = self.__dacs[9]
                self.__GND         = self.__dacs[10]
                self.__THS         = self.__dacs[11]
                self.__BiasLVDS    = self.__dacs[12]
                self.__RefLVDS     = self.__dacs[13]


            elif DSC_FIRMWARE_STRING in l:
                self.__firmwarev = ls[i+2].strip()

            # Note - needs 'lower()' because of a 2.1.1/2.2.2 mismatch...
            elif DSC_BIAS_VOLTAGE_STRING.lower() in l.lower():
                try:
                    hv = float(ls[i+2].strip())
                except ValueError:
                    raise IOError("BAD_HV_VALUE")

                if hv < 0.0 or hv > 100.0:
                    raise IOError("BAD_HV_VALUE")

                self.__hv = hv

            elif DSC_HW_TIMER_STRING in l:
                try:
                    self.__hwTimerMode = int(ls[i+2].strip())
                except ValueError:
                    raise IOError("BAD_HW_TIMER_MODE")

            elif DSC_INTERFACE_STRING in l:
                self.__interface = ls[i+2].strip()

            elif DSC_MPX_CLOCK_STRING in l:
                try:
                    mpxClock = float(ls[i+2].strip())
                except ValueError:
                    raise IOError("BAD_MPX_CLOCK")
                self.__mpxClock = mpxClock

            elif DSC_MPX_TYPE_STRING in l:
                try:
                    mpxType = int(ls[i+2].strip())
                except ValueError:
                    raise IOError("BAD_MPX_TYPE")
                if mpxType not in [1,2,3]:
                    raise IOError("BAD_MPX_TYPE")
                self.__mpxType = mpxType

            elif DSC_PIXELMAN_VERSION_STRING in l:
                self.__pixelmanv = ls[i+2].strip()

            elif DSC_POLARITY_STRING in l:
                try:
                    pol = int(ls[i+2].strip())
                except ValueError:
                    raise IOError("BAD_POLARITY")
                if pol not in [0,1]:
                    raise IOError("BAD_POLARITY")
                self.__polarity = pol

            elif DSC_START_TIME_STRING in l:

                try:
                    ## The full start time.
                    st = float(ls[i+2].strip())

                    self.__startTime = st

                except:
                    raise IOError("BAD_START_TIME")

                sec, sub, sts = getPixelmanTimeString(st)

                self.__startTimeS = sts

            elif DSC_TPX_CLOCK_STRING.lower() in l.lower():

                if "byte[1]" in ls[i+1].strip():

                    val = int(ls[i+2].strip())

                    if val not in [0,1,2,3]:
                        raise("BAD_TPX_CLOCK_MODE")

                    self.__tpxClock = TPX_CLOCK_VALS[val]

                elif "double[1]" in ls[i+1].strip():
                    self.__tpxClock = float(ls[i+2].strip())
                else:
                    raise IOError("BAD_TPX_CLOCK")

            elif DSC_NAME_SN_STRING in l:
                self.__nameAndSN = ls[i+2].strip()
