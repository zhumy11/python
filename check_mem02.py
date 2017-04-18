#!/usr/bin/env python

from optparse import OptionParser
import sys

unit = {'b':1, 'k':2**10, 'm':2**20, 'g':2**30}
def opt():
    parser = OptionParser("Usage: %prog [-w WARNING] [-c CRITICAL]")
    parser.add_option('-w',
                      dest='warning',
                      action='store',
                      default='500M',
                      help='WARNING')
    parser.add_option('-c',
                      dest='critical',
                      action='store',
                      default='200M',
                      help='CRITICAL')
    options, args = parser.parse_args()
    return options, args

def getMem(f):
    with open(f) as fd:
        for line in fd:
            if line.startswith('MemFree'):
                mem = line.split()[1].strip()
                break
    return int(mem) * 1024

def scaleUnit(s):
    lastchar = s[-1].lower()
    num = s[:-1]
    if lastchar in unit:
        return float(num) * unit[lastchar]
    else:
        return float(s)

def change(byte):
    for k, v in unit.items():
        num = float(byte)/v
        if 1 < num <= 1024:
            num = "%.2f" %num
            result = str(num)+k.upper()
            return result

def main():
    options, args = opt()
    w = scaleUnit(options.warning)
    c = scaleUnit(options.critical)
    mem = getMem('/proc/meminfo')
    h_mem = change(mem) 
    if mem > w:
        print "OK \-",'MemFree: ' + h_mem
        sys.exit(0)
    elif c < mem <= w:
        print "WARNING \-",'MemFree: ' + h_mem
        sys.exit(1)
    elif mem <= c:
        print "CRITICAL \-",'MemFree: ' + h_mem
        sys.exit(2)
    else:
        print "UNKNOWN"
        sys.exit(3)

if __name__ == '__main__':
    main()
