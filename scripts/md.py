#!/usr/bin/env python

"""
Convert PDF files to markdown with docling, in a best effort way.
"""

from docling.datamodel.base_models import ConversionStatus
from docling.document_converter import DocumentConverter
import docling
import glob
import os
import sys

DIR = "/tmp/tmp.BtyOeuTyF1"


if __name__ == "__main__":
    doc_converter = DocumentConverter()
    for path in glob.glob(DIR + "/*.pdf"):
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

