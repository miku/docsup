#!/usr/bin/env python

"""
Convert PDF files to markdown with docling, in a best effort way.
"""

import argparse
from docling.datamodel.base_models import ConversionStatus
from docling.document_converter import DocumentConverter
import docling
import glob
import os
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", "-d", required=True, metavar="DIR", type=str, help="directory with PDF files to convert")
    args = parser.parse_args()

    doc_converter = DocumentConverter()
    dir = args.dir.rstrip("/")
    pdfs = glob.glob(dir + "/*.pdf")

    print(f"[..] found {len(pdfs)} files", file=sys.stderr)

    for path in pdfs:
        dst = path.replace(".pdf", ".md")
        tmp = dst + ".tmp"
        if os.path.exists(dst):
            print("done: {}".format(dst), file=sys.stderr)
            continue
        try:
            result = doc_converter.convert(path)
        except docling.exceptions.ConversionError as exc:
            print("conversion failed for {} with {}".format(path, exc), file=sys.stderr)
            continue
        if result.status != ConversionStatus.SUCCESS:
            print("conversion failed for {} with {}".format(path, result.status), file=sys.stderr)
            continue
        with open(tmp, "w") as f:
            f.write(result.document.export_to_markdown())
        os.rename(tmp, dst)
        print("done: {}".format(dst), file=sys.stderr)

