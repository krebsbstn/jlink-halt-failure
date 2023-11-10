# Introduction
Encountering a persistent issue with the Segger JLink software,
I've initiated an investigation to address the "Could not hold CPU" error that intermittently occurs during debugging sessions.
This issue, particularly evident when working with the Zephyr RTOS on an STM32 platform, seems to be related to the CPU entering deep sleep phases during idle states.
The problem manifests when the "Halt CPU" command fails, resulting in a desynchronization between Ozone and the target.

# Reproduction Repository
To facilitate collaboration and issue reproduction, I've created a dedicated repository containing the necessary resources and steps.
The repository includes a script, `poll_halt.py`, utilizing Pylink to interact with the target, attempting to halt and start the CPU until the error occurs.
Additionally, the repository provides the built firmware for the Zephyr Philosophers example on an STM32H743ZI.
Users can build der own firmware of the example and adapt the script for different boards or directly use Ozone for flashing firmware.

For flashing firmware using the script:
```bash
$ python3 pylink_halt/poll_halt.py -d STM32H743ZI -f zephyr-philosophers-STM32H743ZI.elf
```
Currently, I am working on a bare-metal example because I believe that the issue has nothing to do with Zephyr itself but is caused by some idle states or deep sleeps.

# Ozone Automation Tool
The Ozone Automation Tool is an alternative approach to replicate the issue.
This method involves automating Ozone's GUI to simulate the "Halt CPU" command and monitor for the error.
The provided script interacts with Ozone, clicking on the Play/Pause-Button to reproduce the issue in a controlled manner.

# Usage

1. Clone this repository:
   ```bash
   git clone https://github.com/krebsbstn/jlink-halt-failure.git
   cd jlink-halt-failure
   ```

2. Use the script or the Ozone Automation to stop and release the MCU till "CPU-Could not be halted"-Occures.

# Goal
The primary goal is to identify the root cause of the "Could not hold CPU" error.
Two reproducibility methods are presented: one through direct interaction with the JLink using Pylink and the other through the Ozone Automation Tool.
Collaborators are encouraged to explore both avenues, providing additional context and details to aid in diagnosing and resolving this issue.
