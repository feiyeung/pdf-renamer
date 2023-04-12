#!/usr/bin/env python3

import argparse as AP
import os, os.path, datetime, shutil
from PyPDF2 import PdfReader

def main():
    ARGS = get_args()
    for f in get_files(ARGS.path):
        print("processing file " + f)
        try:
            statement_date = get_statement_date(f)
            path_new = os.path.join(
                    os.path.dirname(f), statement_date.strftime("Statement_%Y-%m-%d.pdf"))
            print(f"rename {f} to {path_new}")
            shutil.move(f, path_new)
        except:
            print("\n**********************************************")
            print("* failed to process file %s" % f)
            print("**********************************************\n")

def get_args():
    ap = AP.ArgumentParser()
    ap.add_argument("path", help="dir path for the scan to start")
    return ap.parse_args()

def get_files(path):
    ret = []
    for root, dirs, files in os.walk(path):
        for f in files:
            if f.startswith("GetDocument") and f.endswith(".pdf"):
                ret.append(os.path.join(root, f))
    return ret

def get_statement_date(path):
    parts = []
    def pdf_visitor_text_for_statement_date(text, cm, tm, fontDict, fontSize):
        y = tm[5]
        x = tm[4]
        if y > 756 and x > 432:
            parts.append(text)

    reader = PdfReader(path)
    page = reader.pages[0]
    page.extract_text(visitor_text=pdf_visitor_text_for_statement_date)
    text_body = "".join(parts).strip()
    print("parsing date out of: %s" % text_body)
    return parse_date(text_body)

def parse_date(date_str):
    return datetime.datetime.strptime(date_str, "%B %d, %Y")

main()