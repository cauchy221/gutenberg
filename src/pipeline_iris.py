# -*- coding: utf-8 -*-
from .cleanup import strip_headers
import os
import io

def process_book(
    path_to_raw_file=None,
    text_dir=None,
    language="english",
    log_file="",
    cleanup_f=strip_headers,
    overwrite_all=False,
    ):
    if text_dir is None:
        raise ValueError("You must specify a path to save the text files.")
    
    if path_to_raw_file is None:
        raise ValueError("You must specify a path to the raw file to process.")
    
    # get PG number
    PG_number = path_to_raw_file.split("/")[-1].split("_")[0][2:]

    if overwrite_all or\
        (not os.path.isfile(os.path.join(text_dir,"PG%s_text.txt"%PG_number))):
        # read raw file
        with io.open(path_to_raw_file, encoding="UTF-8") as f:
            text = f.read()

        # clean it up
        clean = cleanup_f(text)

        # write text file
        target_file = os.path.join(text_dir,"PG%s_text.txt"%PG_number)
        with io.open(target_file,"w", encoding="UTF-8") as f:
            f.write(clean)

        # write log info if log_file is not None
        if log_file != "":
            raw_nl = text.count("\n")
            clean_nl = clean.count("\n")
            with io.open(log_file, "a") as f:
               f.write("PG"+str(PG_number)+"\t"+language+"\t"+str(raw_nl)+"\t"+str(clean_nl)+"\n")