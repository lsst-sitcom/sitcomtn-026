#!/usr/bin/env ccs-script
#
# A simple script for initializing the ATS using Stuart's approved procedure 
# Modified 06Jan25 by Craig Lage following instructions from Yousuke.
from org.lsst.ccs.scripting import *
from org.lsst.ccs.bus.states import AlertState
from optparse import OptionParser
from org.lsst.ccs.subsystem.rafts.fpga.compiler import FPGA2ModelBuilder
from java.io import File
import time
from org.lsst.ccs.utilities.image.samp import SampUtils
from java.io import File
from java.time import Duration

CCS.setThrowExceptions(True)

# Connect to subsystems
raftsub = CCS.attachSubsystem("ats-fp")
powersub = CCS.attachSubsystem("ats-power")

# Check initial state
dphiOn = powersub.sendSynchCommand("isDphiOn")
if dphiOn:
   raise RuntimeError("DPHI must be off to run this script")
hvOn = powersub.sendSynchCommand("isHvBiasOn")
if hvOn:
   raise RuntimeError("HVBias must be off to run this script")

ccdTypes = raftsub.sendSynchCommand("getCCDType")
ccdType = ccdTypes['R00/RebW']
if ccdType != "itl":
   raise RuntimeError("Invalid CCDType %s" % ccdType)

register_prev = raftsub.sendSynchCommand("R00/RebW getRegister 0x100000 1")
print register_prev

if register_prev.getValues()[0] == 0:
   raise RuntimeError("The sequencer state is zero. did the sequencer get loaded?")

raftsub.sendSynchCommand("R00/RebW setCCDClocksLow")

register = raftsub.sendSynchCommand("R00/RebW getRegister 0x100000 1")
print register

raftsub.sendSynchCommand(Duration.ofSeconds(300), "R00/RebW testCCDShorts")
dphiOn = powersub.sendSynchCommand("dphiOn")
time.sleep(1.0)
raftsub.sendSynchCommand(Duration.ofSeconds(300), "R00/RebW powerCCDsOn")

# restore register
raftsub.sendSynchCommand("R00/RebW setRegister 0x100000 [0x%x]" % register_prev.getValues()[0])
register = raftsub.sendSynchCommand("R00/RebW getRegister 0x100000 1")
print register

