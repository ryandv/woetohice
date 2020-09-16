#!/usr/bin/env python3

import json
import re
import sys

from pdfminer.layout import LAParams, LTContainer, LTText, LTChar, LTAnno, LTTextLineHorizontal
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice

from woetohice import PointGrouper, Point

class TreePrinter(object):
    def visit(self, obj, depth):
        if issubclass(obj.__class__, LTContainer):
            print('{} {}'.format(' ' * depth * 4, obj))
            search(self, obj, depth + 1)
        elif obj.__class__ not in [LTChar, LTAnno]:
            print('{} {}'.format(' ' * depth * 4, obj))

class TextlinePrinter(object):
    def visit(self, obj, depth):
        if obj.__class__ == LTTextLineHorizontal:
            print(obj)
        elif issubclass(obj.__class__, LTContainer):
            search(self, obj, depth + 1)

class TransactionPrinter(object):
    def __init__(self):
        self.state = 0
        self.acc = []

    def visit(self, obj, depth):
        if obj.__class__ == LTTextLineHorizontal:
            if obj.x0 <= 350.00:
                self.acc.append(Point(x0=obj.x0, y0=obj.y0, data=obj.get_text().rstrip()))
        elif issubclass(obj.__class__, LTContainer):
            search(self, obj, depth + 1)

def search(visitor, cont, depth=0):
    for obj in cont:
        visitor.visit(obj, depth)

def main():
    with open(sys.argv[1], 'rb') as pdffile:
        parser = PDFParser(pdffile)
        doc = PDFDocument(parser)
        if not doc.is_extractable:
            raise PDFTextExtractionNotAllowed
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        groups = []
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
            layout = device.get_result()
            strategy = TransactionPrinter()
            search(strategy, layout.groups)

            grouper = PointGrouper(tolerance=0.5)
            groups = groups + grouper.group(strategy.acc)

        print(json.dumps(list(
            map(lambda g:
                list(map(lambda p:
                    str(p.data),
                    sorted(g, key=lambda p: p.x0)
                    )),
                filter(lambda g: len(list(g)) == 4 and map(lambda pt: re.compile(r"(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC) \d{1,2}").match(pt.get_text()), g), groups)))))

if __name__ == '__main__':
    main()
