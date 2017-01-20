#!/usr/bin/env python3

example_usage = """example:

    python main.py --target-number 19729729729 --caller-id 12142142142 --sound-file tt-monkeys --trunk kazoo --context kazoo-outgoing --stdout

    INFO: The --sound-file flag isn't currently used but must be provided (so just give it _any_ value for now)
"""

import argparse
argp = argparse.ArgumentParser(description = "Asterisk Call file generator",
        epilog=example_usage,
        formatter_class=argparse.RawDescriptionHelpFormatter)

argp.add_argument("--target-number", type=str, help="The number to call", required=True)
argp.add_argument("--caller-id", type=str, help="The number to call from", required=True)
argp.add_argument("--sound-file", type=str, help="Name of the audio file to play not including the extension", required=True)
argp.add_argument("--filename", type=str, help="Name of the callfile -- `<this>.call` will be written to disk")
argp.add_argument("--trunk", type=str, help="Name of your trunk (e.g. kazoo)", required=True)
argp.add_argument("--context", type=str, help="Dialplan context to execute upon answer", required=True)

argp.add_argument("--stdout", dest="stdout", help="If given write to stdout instead of disk", action="store_true")

argp.add_argument("--tmp-dir" \
        ,type=str \
        ,default="/tmp" \
        ,help="Absolute path to the tmp directory (to hold the call file til it should be moved)")

argp.add_argument("--spool-dir" \
        ,type=str \
        ,default="/var/spool/asterisk/outgoing" \
        ,help="Absolute path to the outgoing directory (where asterisk looks for `.call` files)")


template = """Channel: SIP/{trunk}/{target_number}
Callerid: {caller_id}
WaitTime: 5
Archive: yes
Context: {context}
Extension: s
Priority: 1
# Setvar: PLAYBACK_FILENAME={sound_file}

# DEBUG
# tmp_dir={tmp_dir}
# spool_dir={spool_dir}
# tmp_filename_full={tmp_filename_full}
# DEBUG"""

import random
import string
from os import path

def _gen_random_string(length=8, chars=string.ascii_letters + string.digits):
    return 'tmp' + ''.join(random.choice(chars) for _ in range(length))

def main_cli():
    args = argp.parse_args()

    tmp_filename = (args.filename or _gen_random_string()) + '.call'
    tmp_filename_full = path.join(args.tmp_dir, tmp_filename)

    file_text = template.format(\
             target_number     = args.target_number \
            ,caller_id         = args.caller_id \
            ,sound_file        = args.sound_file \
            ,tmp_filename_full = tmp_filename_full \
            ,tmp_dir           = args.tmp_dir \
            ,spool_dir         = args.spool_dir \
            ,trunk             = args.trunk \
            ,context           = args.context)

    if args.stdout:
        print(file_text)
    else:
        try:
            with open(tmp_filename_full, 'w') as fh:
                fh.write(file_text)
        except: 
            print("Err!")
        else:
            print("Wrote to {file_name}".format(file_name = tmp_filename_full))

if __name__ == '__main__':
    main_cli()
