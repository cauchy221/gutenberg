"""
Modified based on process_data.py

"""
import os
from os.path import join
import argparse
import glob

from src.utils import get_langs_dict
from src.pipeline_iris import process_book


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        "Processing raw texts from Project Gutenberg:"
        "just removing headers.")
    # raw folder
    parser.add_argument(
        "-r", "--raw",
        help="Path to the raw-folder",
        default='data/raw/',
        type=str)
    # text folder
    parser.add_argument(
        "-ote", "--output_text",
        help="Path to text-output (text_dir)",
        default='data/text/',
        type=str)
    # pattern to specify subset of books
    parser.add_argument(
        "-p", "--pattern",
        help="Patttern to specify a subset of books",
        default='*',
        type=str)

    # quiet argument, to supress info
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Quiet mode, do not print info, warnings, etc"
    )

    # log file
    parser.add_argument(
        "-l", "--log_file",
        help="Path to log file",
        default=".log",
        type=str)

    # add arguments to parser
    args = parser.parse_args()

    # load languages dict
    langs_dict = get_langs_dict()

    # loop over all books in the raw-folder
    pbooks = 0
    for filename in glob.glob(join(args.raw, 'PG%s_raw.txt' % (args.pattern))):
        # The process_books function will fail very rarely, whne
        # a file tagged as UTf-8 is not really UTF-8. We kust
        # skip those books.
        try:
            # get PG_id
            PG_id = filename.split("/")[-1].split("_")[0]

            # get language from metadata
            # default is english
            language = "english"

            # process the book: strip headers, tokenize, count
            process_book(
                path_to_raw_file=filename,
                text_dir=args.output_text,
                language=language,
                log_file=args.log_file
            )
            pbooks += 1
            if not args.quiet:
                print("Processed %d books..." % pbooks, end="\r")
        except UnicodeDecodeError:
            if not args.quiet:
                print("# WARNING: cannot process '%s' (encoding not UTF-8)" % filename)
        except Exception as e:
            if not args.quiet:
                print("# WARNING: cannot process '%s' (unkown error)" % filename)