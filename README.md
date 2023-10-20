# Details
- Ozone V3.30c (2023-10-19) [Ozone Download](https://www.segger.com/downloads/jlink/#Ozone)
- J-Link Software and Documentation Pack V7.92k (2023-10-18) [J-Link Software and Documentation Pack Download](https://www.segger.com/downloads/jlink/#J-LinkSoftwareAndDocumentationPack)
- Zephyr V3.4.0 (2023-06-01) [Zephyr GitHub](https://github.com/zephyrproject-rtos)
- square/pylink V1.2.0 (2023-07-28) [Pylink GitHub](https://github.com/square/pylink/tree/master)

# Introduction
I'm currently grappling with an issue in the Segger JLink software. When using a Segger JLink for debugging applications on an STM32, the "Halt CPU" command sometimes fails, resulting in a "Could not hold CPU" error message. Attempting to read register values in this state returns a "Cannot read register xx (Rxx) while CPU is running" error. I primarily develop applications based on the open-source Zephyr RTOS, and it seems that the problem may be related to the CPU entering deep sleep phases during idle states. Another potential cause could be how Zephyr handles context changes and multiple threads. When this issue occurs in conjunction with Ozone, it causes Ozone and the target to fall out of sync, necessitating a reconnection to bring them back to a common state. Nevertheless, I would expect that sending the "Halt CPU" command should awaken and halt the CPU.

# Reproduction Script
To enhance the reproducibility of this issue, I've created a script that intermittently halts the CPU, reads registers, and restarts it. Running this script while connecting to an STM32H743 (and likely other Cortex M7/M4 devices) generates output like the following:

```yaml
--------------
R11: 0x00000000,R12: 0x00000000,R13: 0x24004780,R14: 0xFFFFFFFF,R15: 0x08001990, cycle_cnt: 0
--------------
R11: 0x00000000,R12: 0x00000000,R13: 0x24002810,R14: 0x0800204B,R15: 0x080051DE, cycle_cnt: 1
--------------
R11: 0xA05F0001,R12: 0xA05F0001,R13: 0xA05F0001,R14: 0xA05F0001,R15: 0xA05F0001, cycle_cnt: 2
--------------
Cannot read register 11 (R11) while CPU is running
Cannot read register 12 (R12) while CPU is running
Cannot read register 13 (R13) while CPU is running
Cannot read register 14 (R14) while CPU is running
Cannot read register 15 (R15) while CPU is running
R11: 0x00000000,R12: 0x00000000,R13: 0x00000000,R14: 0x00000000,R15: 0x00000000, cycle_cnt: 3
--------------
Exception raised: Target could not be halted
```

The frequency of this error largely depends on the firmware being used. In my case, it's most pronounced when utilizing a Zephyr sample ([Zephyr Philosophers](https://github.com/zephyrproject-rtos/zephyr/tree/main/samples/philosophers)), which involves frequent context switches, potentially exacerbating the issue. for easyer debugging i added the firmware of the sample to the repo, but make sure to use the correct hardware when using this prebuilt *.elf file. Ideally, sending a "Halt CPU" command should pause the CPU at the next available instruction.

# Reproduction Repository
For the best reproducibility, I've created this repository that contains the necessary steps and resources. To execute the provided script, you'll need the latest versions of JLink and Ozone. Additionally, the Pylink package is required for the script to interact with the target. The repository also includes the built firmware for the Philosophers example on an STM32H743ZI. If you're using a different board, you'll need to modify the script invocation and build an alternative firmware.

I recommend using Ozone for flashing firmware. However, if, for any reason, that's not possible, you can also flash the firmware using the script. To do this, you can invoke the script as follows:

```yaml
$ python3 poll_halt.py -d STM32H743ZI -f zephyr-philosophers-STM32H743ZI.elf
```
The easiest way to reproduce the error is to first flash the firmware and then start the script while the target is running. The script initiates a reset, so it starts from the beginning.
Currently, I am working on a bare-metal example because I believe that the issue has nothing to do with Zephyr itself but is caused by some idle states or deep sleeps.

# Goal
The primary objective of this request is to pinpoint the root cause of this issue. Ultimately, our goal is to develop and deliver a suitable patch for the next version of the JLink software to resolve this problem effectively. Additional details and context will be invaluable in diagnosing and addressing this issue.
