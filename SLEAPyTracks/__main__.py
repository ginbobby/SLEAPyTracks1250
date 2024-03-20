#!/usr/bin/env python


import argparse

parser = argparse.ArgumentParser(
    prog='SLEAPyTracks',
    description='A tracker for tracking exploration behavior. Currently trained for use on red knot exploration tests.',
    epilog='Still a work in progress!')
parser.add_argument('video_dir', help='path to the directory containing the videos to be tracked', type=str)
parser.add_argument('-o', '--output_dir', help='path to the directory to store the csv output files',
                    default='', type=str)
parser.add_argument('-n', '--number_of_animals', help='the maximum number of animals that are visible in one video',
                    type=int,
                    default=1)
parser.add_argument('-t', '--tracking', action='store_true', help='use tracking functionality (not trained properly '
                                                                  'yet!)')

if __name__ == "__main__":
    args = parser.parse_args()
    print("Starting SLEAPyTracks...")

    from SLEAP_parser import SleapParser
    from SLEAP_model import SLEAPModel

    model = SLEAPModel(args.video_dir)
    model.predict(args.number_of_animals, args.tracking)

    if args.output_dir == '':
        SleapParser().get_results( args.video_dir + 'SLEAPyTracks_output')
    else:
        SleapParser().get_results(args.output_dir)

    print('all done!')
