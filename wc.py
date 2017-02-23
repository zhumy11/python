#!/usr/bin/env python

import os
import sys
from optparse import OptionParser

def opt():
    parser = OptionParser()
    parser.add_option("-c", "--char",
                      dest="chars",
                      action="store_true",
                      default=False,
                      help="only count chars")
    
    parser.add_option("-w", "--word",
                      dest="words",
                      action="store_true",
                      default=False,
                      help="only count words")
    
    parser.add_option("-l", "--line",
                      dest="lines",
                      action="store_true",
                      default=False,
                      help="only count lines")
    
    options, args = parser.parse_args()
    return options, args

def count(s):
    chars = len(s)
    words = len(s.split())
    lines = s.count('\n')
    return chars, words, lines

def print_wc(options, chars, words, lines, fn):
    if options.lines:
        print lines,
    if options.words:
        print words,
    if options.chars:
        print chars,
    print fn
    
def main():
    options, args = opt()
    if not (options.chars or options.words or options.lines):
        options.chars, options.words, options.lines = True, True, True
    
    if not args:
        s = sys.stdin.read()
        fn = ''
        chars, words, lines = count(s)
        print_wc(options, chars, words, lines, fn)
    else:
        total_chars, total_words, total_lines = 0, 0, 0
        for fn in args:
            if os.path.isfile(fn):
                with open(fn) as fd:
                    s = fd.read()
                chars, words, lines = count(s)
                print_wc(options, chars, words, lines, fn)
                total_chars += chars
                total_words += words
                total_lines += lines
            elif os.path.isdir(fn):
                print >> sys.stderr, "%s: is a directory" %fn
            else:
                sys.stderr.write("%s: No such file or directory\n" %fn) 
        if len(args) > 1:
            print_wc(options, total_chars, total_words, total_lines, 'Total')
            
if __name__ == '__main__':
    main()





