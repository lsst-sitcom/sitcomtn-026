.. raw:: latex

   \vspace{-15mm}

.. raw:: latex

   \maketitle

.. raw:: latex

   \vspace{-5mm}

Introduction
============

The AuxTel CCD has been successfully operated at Cerro Pachon and is
taking astronomical spectra and images. During start-up, the WREB board
which drives the CCD had an issue where it sometimes powered up in a
state where the parallel clocks were disabled. In this case the CCD does
not function. A workaround was developed which is documented here. We
believe this workaround is no longer needed, since a change to the
power-up sequence appears to have fixed this problem. However, until we
are sure that the problem is fixed, it is a good idea to check that the
board is operating properly as documented here. This document details
the power-up and power-down sequences to make sure the CCD operates.
Note that once the WREB Seq. Power has been powered up in the “good”
state, it remains in the good state as long as power is applied.
Therefore, ideally we should try to keep the WREB board SEQ Power
powered up at all times. However, if the Seq Power is powered down for
any reason, this document describes how to get it operating again. This
assumes that you are operating within the LSST-WAP network at Cerro
Pachon or in La Serena, although this can be run from outside using VPN.

Getting Started
===============

There are several options for controlling the CCD, but the procedure I
have been following is to open three screens, as follows:

-  Login to atsccs1, using ssh -X -Y yourname@atsccs1.cp.lsst.org

-  On this machine, cd to /lsst/ccs/prod/bin

-  Then launch the ccs-console, using ./ccs-console&

-  The ccs-console should then appear in an X-window. You will need to
   launch three tabs in the CCS_Subsystems pull down menu:

   -  ats-power

   -  ats-wreb Monitor

   -  ats-wreb Control

-  Then launch the ccs-shell, using ./ccs-shell

-  Login to atshcu1, using ssh yourname@atshcu1.cp.lsst.org

-  On this machine, cd to /home/ccs/scripts

-  In order to run the power up and power down scripts, you will need to
   include /lsst/ccs/prod/bin in your path; (e.g. export ). You might
   want to add this to your .bashrc file. These scripts should run from
   your account. If they don’t, you will need to either logout and log
   back in as ccs@atshcu1, or if you have sudo privileges, transfer to
   the ccs login using the command: sudo su ccs.

Your screen should now look something like this, and you are ready to
begin powering up the WREB and the CCD.

|image|

Powering up from a completely cold state
========================================

Assuming you are powering up the CCD from a completely cold state where
all power is off, run the following commands:

-  In the ccs-console ats-power tab:

   -  Turn Fan on

   -  Turn OTM on

   -  Turn Seq. Power on

   -  In the atshcu1 screen, run ./atsInit.py

This command should run, and the CCD should power up successfully. Check
that PClk0 is equal to PClkU. If it is not, you will need to move to the
section below titled “Powering up if the WREB board PClk0 test has
failed” Then:

-  In atsccs1 ccs-shell run: ats-wreb/WREB setBackBias true

-  In the ccs-console ats-power tab, Turn HV Bias On.

Note that both of these steps must be performed to turn on the HV bias.
The CCD should now be powered up and ready to run.

Powering up the CCD when Seq Power is already on
================================================

If the Seq Power is already on, then we know the WREB is still in the
state where the parallel clocks are enabled. In this case, all that is
required to power up the CCD is the following:

-  In the atshcu1 screen, run ./atsInit.py

This command should run, and the CCD should power up successfully. Check
that PClk0 is equal to PClkU. Then:

-  In atsccs1 ccs-shell run: ats-wreb/WREB setBackBias true

-  In the ccs-console ats-power tab, Turn HV Bias On.

Note that both of these steps must be performed to turn on the HV bias.
The CCD should now be powered up and ready to run.

Powering down the CCD, leaving Seq Power on
===========================================

To power down the CCD, leaving the WREB Seq Power on, do the following
steps. This should be the normal sequence for powering down the CCD:

-  In atsccs1 ccs-shell run: ats-wreb/WREB setBackBias false

-  In the ccs-console ats-power tab, Turn HV Bias Off.

-  In atsccs1 ccs-shell run: ats-wreb/WREB powerCCDsOff

-  In the ccs-console ats-power tab, Turn DPHI Off.

The CCD is now powered down, but the WREB is still powered up.

Powering down completely
========================

If, for some reason, you want to completely power down the entire
camera, do the following steps. Note that if you then want to power up
after this, you need to follow the “Powering up from a completely cold
state” section above.

-  In the atshcu1 screen, run ./atsOff.py

The system should now be completely off.

.. raw:: latex

   \clearpage

Note: The sections below should not be needed.

Powering up if the WREB board PClk0 test has failed
===================================================

Assuming you are powering up the CCD from a completely cold state where
all power is off, run the following commands:

-  In the ccs-console ats-power tab:

   -  Turn Fan on

   -  Turn OTM on

   -  Turn Seq. Power on

   -  Turn DPHI on.

-  In atsccs1 ccs-shell run: ats-wreb/WREB powerCCDsOn

The CCD is now powered up, but you need to determine whether or not it
has powered up in the state where the parallel clocks are enabled. To
check this, look at the PClk0 entry in the ats-wreb Monitor screen. It
should be equal to either PClkU or PClkL, depending whether the parallel
clock is high or low. You can check this by doing the following:

-  In atsccs1 ccs-shell run: ats-wreb/WREB setRegister 0x100000 [0x2d4]

-  When this is done, PClk0 should be equal to PClkL.

-  In atsccs1 ccs-shell run: ats-wreb/WREB setRegister 0x100000 [0x3d4]

-  When this is done, PClk0 should be equal to PClkU.

If this test passes, the WREB has powered up successfully and you can
continue with the power up. If PClk0 has any other value, (typically
0.01V), the the WREB power up has failed and you need to power cycle it
again.

If the WREB has powered up successfully
---------------------------------------

In this case, run the following steps.

-  In atsccs1 ccs-shell run: ats-wreb/WREB powerCCDsOff

-  In the ccs-console ats-power tab, Turn DPHI off.

-  In the atshcu1 screen, run ./atsInit.py

This command should run, and the CCD should power up successfully. Check
that PClk0 is equal to PClkU. Then:

-  In atsccs1 ccs-shell run: ats-wreb/WREB setBackBias true

-  In the ccs-console ats-power tab, Turn HV Bias On.

The CCD should now be powered up and ready to run.

If the WREB has not powered up successfully
-------------------------------------------

If the WREB failed to power up successfully, you need to power cycle the
Seq Power and try again, checking if the WREB has powered up
successfully. You need to repeat the power cycles until the WREB powers
up successfully. The sequence in this case, starting from the point
where the WREB failed to power up successfully is:

-  In atsccs1 ccs-shell run: ats-wreb/WREB powerCCDsOff

-  In the ccs-console ats-power tab:

   -  Turn DPHI off.

   -  Turn Seq. Power off

   -  Turn Seq. Power on

   -  Turn DPHI on.

-  In atsccs1 ccs-shell run: ats-wreb/WREB powerCCDsOn

-  Check again whether the WREB has powered up successfully.

Continue this sequence until the WREB test passes, at which point you
continue with the “If the WREB has powered up successfully” section
above.

.. |image| image:: Screens.png
   :width: 99.0%
