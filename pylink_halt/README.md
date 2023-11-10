# Details
- Ozone V3.30c (2023-10-19) [Ozone Download](https://www.segger.com/downloads/jlink/#Ozone)
- J-Link Software and Documentation Pack V7.92k (2023-10-18) [J-Link Software and Documentation Pack Download](https://www.segger.com/downloads/jlink/#J-LinkSoftwareAndDocumentationPack)
- Zephyr V3.4.0 (2023-06-01) [Zephyr GitHub](https://github.com/zephyrproject-rtos)
- square/pylink V1.2.0 (2023-07-28) [Pylink GitHub](https://github.com/square/pylink/tree/master)

# Reproduction Script
To enhance the reproducibility of this issue, I've created a script that intermittently halts the CPU, reads registers, and restarts it.
Running this script while connecting to an STM32H743 (and likely other Cortex M7/M4 devices) generates output like the following:

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

The frequency of this error largely depends on the firmware being used.
In my case, it's most pronounced when utilizing a Zephyr sample ([Zephyr Philosophers](https://github.com/zephyrproject-rtos/zephyr/tree/main/samples/philosophers)),
which involves frequent context switches, potentially exacerbating the issue.
For easier debugging i added the firmware of the sample to the repo, but make sure to use the correct hardware when using this prebuilt *.elf file.
Ideally, sending a "Halt CPU" command should pause the CPU at the next available instruction.
