#!/usr/bin/env conda run -n sleap python

from SLEAP_model import SLEAPModel

import argparse

from SLEAP_parser import SleapParser

parser = argparse.ArgumentParser(
    prog='SLEAPyTracks',
    description='A tracker for tracking exploration behavior. Currently trained for use on red knot exploration tests.',
    epilog='Still a work in progress!')
parser.add_argument('video_dir', help="path to the directory containing the videos to be tracked")
parser.add_argument("--output_dir", "-o", help="path to the directory to store the csv output files",
 metavar="")
parser.add_argument("-n", "--number_of_animals", help="the number of animals that are in the video", default=1)
parser.add_argument("-t", "--tracking", action="store_true", help="use tracking functionality (not trained properly "
                                                                  "yet!)", metavar="")

args = parser.parse_args()

model = SLEAPModel(args.video_dir)
model.predict(args.number_of_animals, args.tracking)

SleapParser().get_results(r"predictions\tracks", args.output_dir)

print("all done!")

