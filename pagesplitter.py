#!/usr/bin/env python
#
# Splits pages in a PDF. Useful when one has scanned A5 pages in an A4 scanner
# and every PDF page contains two sheets.
#
# Adapted from  https://unix.stackexchange.com/questions/12482/split-pages-in-pdf
from __future__ import print_function
import copy, sys
from pyPdf import PdfFileWriter, PdfFileReader

input = PdfFileReader(sys.stdin)
output = PdfFileWriter()
for i in range(0, input.getNumPages()):
    rotation = 90 if i % 2 == 0 else 270
    p = input.getPage(i).rotateClockwise(rotation)
    q = copy.copy(p)
    (w, h) = p.mediaBox.upperRight
    p.mediaBox.upperRight = (w/2, h)
    q.mediaBox.upperLeft = (w/2, h)
    output.addPage(p)
    output.addPage(q)
output.write(sys.stdout)
