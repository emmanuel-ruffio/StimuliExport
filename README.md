# StimuliExport
A basic python script to export Atmel Studio stimul files (*.stim) to column data files (to plot)
(Not fully tested)

I am a very beginner in python but this script does its job...
It may be used to generate plots from stimuli files. For exemple, here is an example of stimuli datas:
```
#163492
DDRB = 0x02
#9199
DDRD = 0x10
#588
DDRD = 0x00
(...)
```

Running the script with the following options:

python Stimuli_export.py mystimulifile.stim -f DDRD -f DDRB -f PORTD -f PORTB -m 0xFF -i 0 -b -e -s 0

with:
- "-f": specify the registers to export
- "-m": a bit mask to select which bit to export. (may be different for each register)
- "-i": the initial value of register (may be different for each register)
- "-b": value are exported in a binary format "0b00011010". Specify "-x" instead to use a hexadecimal format.
- "-e": with "-b" options, it "explodes" the byte in 8 columns, so that a column is generated for each bit
- "-s": start export at time (clock) 0

A file is generated for each register. In this example, 4 files are created:
1) "mystimulifile_DDRD.stim"
2) "mystimulifile_DDRB.stim"
3) "mystimulifile_PORTD.stim"
4) "mystimulifile_PORTB.stim"

The output file <mystimulifile_DDRD.stim> would be for example:
```
# cpu time       b7         b6          b5          b4          b3          b2          b1          b0
000000           0           0           0           0           0           0           0           0
009198           0           0           0           0           0           0           0           0
009199           0           0           0           1           0           0           0           0
009786           0           0           0           1           0           0           0           0
009787           0           0           0           0           0           0           0           0
010237           0           0           0           0           0           0           0           0
010238           0           0           0           1           0           0           0           0
010241           0           0           0           1           0           0           0           0
(...)
```

With Octave, matlab, gnuplot, etc it is straightfoward to get something like this:
![Atmel studio Simuli file export](/ExportExample.png)

