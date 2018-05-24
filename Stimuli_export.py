#! python
# -*-coding:Latin-1 -*

import sys;
import os;
import argparse;
import struct;
import io;

def get_stringFromValue(val, args):
    if args.b:
        if args.e:
            return ("{:#010b}".format(val))[2:];
        else:
            return ["{:#010b}".format(val)];
    else:
        if not args.x:
            return ["{:>#3}".format(val)];
        else:
            return ["{:=#04x}".format(val)];

#sys.argv = ['sd_copy.py', 'H:', '-o test.raw'];

parser = argparse.ArgumentParser(description='Reformat a stimul file.');
parser.add_argument('input', help='the input stimuli file');
parser.add_argument('-f', action="append", metavar='field', help='the field name to export');
parser.add_argument('-m', action="append", metavar='mask', help='the bit to export', default=[]);
parser.add_argument('-i', action="append", metavar='init', type=int, help='init value of the byte', default=[]);
parser.add_argument('-e', action='store_true', help='explode the value is bits');
parser.add_argument('-x', action='store_true', help='hexadecimal output');
parser.add_argument('-b', action='store_true', help='binary output');
parser.add_argument('-s', type=int, help='start time', default=0);
args = parser.parse_args();

if len(args.f) != len(args.m):
    if len(args.m) == 0:
        args.m = [0xFF];
    if len(args.m) > 1:
        raise ValueError("Invalid number of mask occurence {}".format(args.m));
    else:
        args.m = args.m * len(args.f);

if len(args.f) != len(args.i):
    if len(args.m) == 0:
        args.i = [None];
    if len(args.i) > 1:
        raise ValueError("Invalid number of initial value occurence");
    else:
        args.i = args.i * len(args.f);

print("{}".format(args.f));
print("{}".format(args.m));
print("{}".format(args.i));

try:
    for i in range(len(args.f)):
        lField = args.f[i];
        lInit = args.i[i];
        lMask = args.m[i];

        print("{} {} {}".format(lField, lInit, lMask));
        inputFile = args.input.strip();

        lIndex = inputFile.rfind('.');
        if lIndex != -1 and lIndex > 0:
            outputFile = inputFile[0:lIndex] + '_' + lField + inputFile[lIndex:];
        else:
            outputFile = inputFile + '_' + lField;

        lTimeArray = list();
        lValueArray = list();

        lCurrentTime = None;
        lCurrentValue = None;
        lLastValue = None;

        lIndex = lMask.find('x');
        if lIndex != -1:
            lMask = int(lMask[lIndex+1:], 16);
        else:
            lMask = int(lMask);
            if lMask < 8:
                lMask = pow(2, lMask);
            else:
                raise ValueError("Invalid bit number");

        print (outputFile);
      
        with open(inputFile, 'r') as f, open(outputFile, 'w') as fout:

            for lLine in f:
                lLine = lLine.strip();
                if lLine.startswith('#'):
                    if lCurrentTime is not None:
                        lCurrentTime = lCurrentTime + int(lLine[1:]);
                    else:
                        lCurrentTime = 0;

                if lCurrentTime is not None and (len(lField) > 0) and lLine.startswith(lField):
                    lIndex = lLine.find('x');

                    if (lIndex != -1):
                        lNewValue = (int(lLine[lIndex+1:], 16) & lMask);
                        lBoolValue = int(lNewValue > 0);

                        if lLastValue is None:
                            if lInit is not None and lCurrentValue is None:
                                lCurrentValue = lInit;
                                
                            if args.s is None:
                                if lCurrentTime > 0:
                                    print("{:>#06}".format(0) + "".join(["{: >12}".format(v) for v in get_stringFromValue(lCurrentValue, args)]), file=fout);
                                    print("{:>#06}".format(lCurrentTime-1) + "".join(["{: >12}".format(v) for v in get_stringFromValue(lCurrentValue, args)]), file=fout);

                                print("{:>#06}".format(lCurrentTime) + "".join(["{: >12}".format(v) for v in get_stringFromValue(lNewValue, args)]), file=fout);
                                lLastValue = lNewValue;
                            elif lCurrentTime == args.s:
                                print("{:>#06}".format(lCurrentTime) + "".join(["{: >12}".format(v) for v in get_stringFromValue(lNewValue, args)]), file=fout);
                                lLastValue = lNewValue;
                            elif lCurrentTime > args.s:
                                print("{:>#06}".format(args.s) + "".join(["{: >12}".format(v) for v in get_stringFromValue(lCurrentValue, args)]), file=fout);
                                print("{:>#06}".format(lCurrentTime-1) + "".join(["{: >12}".format(v) for v in get_stringFromValue(lCurrentValue, args)]), file=fout);
                                print("{:>#06}".format(lCurrentTime) + "".join(["{: >12}".format(v) for v in get_stringFromValue(lNewValue, args)]), file=fout);
                                lLastValue = lNewValue;

                        elif lNewValue != lLastValue:
                            print("{:>#06}".format(lCurrentTime-1) + "".join(["{: >12}".format(v) for v in get_stringFromValue(lLastValue, args)]), file=fout);
                            print("{:>#06}".format(lCurrentTime) + "".join(["{: >12}".format(v) for v in get_stringFromValue(lNewValue, args)]), file=fout);
                            lLastValue = lNewValue;

                        lCurrentValue = lNewValue;

            if lLastValue is not None:
                print("{:>#06}".format(lCurrentTime) + "".join(["{: >12}".format(v) for v in get_stringFromValue(lLastValue, args)]), file=fout);

    print("# Export terminé.");
except (FileNotFoundError, IOError) as e:
    print(str(e));
except StopIteration:
    print("# Fin du fichier");





