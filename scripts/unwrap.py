# Take a list of WARC files, containing video/mp4 content, extract one image from each.
import argparse
import tempfile
import os
import time
import json

from warcio.archiveiterator import ArchiveIterator

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("f", nargs="*", metavar="FILE", help="files")
    parser.add_argument(
        "-d",
        "--directory",
        type=str,
        default=".",
        metavar="DIR",
        help="directory to extract files to",
    )
    parser.add_argument(
        "-l",
        "--limit",
        default=0,
        type=int,
        metavar="N",
        help="maximum number of files to extract",
    )
    args = parser.parse_args()

    # Note the seen payload digests.
    seen = set()
    done = False

    # keep path and WARC-Target-URI associated
    manifest = []

    for fn in args.f:
        if done:
            break
        with open(fn, "rb") as stream:
            for record in ArchiveIterator(stream):
                if record.rec_type != "response":
                    continue
                rh = record.rec_headers
                hh = record.http_headers
                if hh.get("Content-Type") not in ("application/pdf",):
                    continue

                content_length = hh.get("Content-Length")

                payload_digest = rh.get("WARC-Payload-Digest")
                if not payload_digest:
                    continue

                hv = payload_digest.split(":")[1]
                if hv in seen:
                    continue

                seen.add(hv)

                if args.limit and args.limit > 0 and len(seen) > args.limit:
                    done = True
                    break

                dst = os.path.join(args.directory, "{}.pdf".format(hv))
                if os.path.exists(dst):
                    continue

                uri = rh.get("WARC-Target-URI")
                if not uri:
                    raise RuntimeError("file w/o URI: {}".format(payload_digest))

                manifest.append(
                    {
                        "file": dst,
                        "uri": uri,
                        "size": content_length,
                    }
                )

                with tempfile.NamedTemporaryFile(delete=False) as tf:
                    data = record.raw_stream.read()
                    tf.write(data)

                os.rename(tf.name, dst)

    mfile = os.path.join(args.directory, "manifest-{:0.0f}.json".format(time.time()))
    with open(mfile, "w") as f:
        for m in manifest:
            f.write("{}\n".format(json.dumps(m)))
