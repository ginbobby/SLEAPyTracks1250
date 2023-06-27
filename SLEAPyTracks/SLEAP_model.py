#!/usr/bin/env python
"""
Takes a model that was made with SLEAP and uses it to estimate keypoint positions of animals on a video

autor: Antsje van der Leij


"""

import sys
import os
import sleap
import glob
import subprocess
import argparse

parser = argparse.ArgumentParser(
    prog='SLEAPyTracks',
    description='A tracker for tracking exploration behavior.',
    epilog='Still a work in progress!')
parser.add_argument('video_dir', help="path to the directory containing the videos to be tracked")
parser.add_argument("-n", "--number_of_animals", help="the number of animals that are in the video")
args = parser.parse_args()


class SLEAPModel:
    """
    A Class that predicts animal poses using a video as input.
    Returns a csv file with the pixel coordinates of key points found bij the model.
    Uses a model that is trained using the SLEAP GUI.
    """

    def __init__(self, video_dir, predictions_out_dir="predictions/"):

        self.video_dir = video_dir
        self.model = self.load_model()
        self.predictions_out_dir = predictions_out_dir

    def get_files_from_dir(self, path, file_extension):
        print("get files")

        # check if file exists
        if not os.path.isdir(path):
            print(path)
            sys.exit("File path to videos does not exist or is incorrect!")

        # get only one type of file
        files = [f for f in os.listdir(path) if f.endswith(file_extension) or f.endswith(file_extension.upper())]

        # check if any files match file type
        if not files:
            sys.exit("no " + file_extension + " found in " + path)

        return files

    def load_video(self, path_to_video):
        print("load video")

        loaded_video = sleap.load_video(path_to_video)
        return loaded_video

    def load_model(self):
        """
        loads a trained SLEAP model
        """
        print("load model")

        # use glob to make a variable model path so name of model doesn't matter
        model_path = glob.glob('model/*')

        model = sleap.load_model(model_path)

        return model

    def run_tracker(self, labels, instance_count):

        print(labels)
        print("initializing tracker")

        # Here I'm removing the tracks so we just have instances without any tracking applied.
        for instance in labels.instances():
            instance.track = None
        labels.tracks = []

        # Create tracker
        tracker = sleap.nn.tracking.Tracker.make_tracker_by_name(
            # General tracking options
            tracker="flow",
            track_window=5,

            # Matching options
            similarity="instance",
            match="greedy",
            min_new_track_points=1,
            min_match_points=1,

            # Optical flow options (only applies to "flow" tracker)
            img_scale=0.5,
            of_window_size=21,
            of_max_levels=3,

            # Pre-tracking filtering options
            target_instance_count=instance_count,
            pre_cull_to_target=True,
            pre_cull_iou_threshold=0.8,

            # Post-tracking filtering options
            post_connect_single_breaks=True,
            clean_instance_count=instance_count,
            clean_iou_threshold=None,
        )

        tracked_lfs = []
        for lf in labels:
            lf.instances = tracker.track(lf.instances, img=lf.image)
            tracked_lfs.append(lf)
            print(lf)

        tracked_labels = sleap.Labels(tracked_lfs)



        return tracked_labels

    def run_model(self, video):
        """
        Loads a pre-trained model from SLEAP.
        Runs the model on video to generate predictions.
        Predictions are then saved.
        """

        print('running model...')

        # run model

        labels = self.model.predict(video)
        labels = sleap.Labels(labels.labeled_frames)
        # save predictions to file

        return labels

    def predict(self, instance_count, tracking):
        print("running predecit")

        videos = self.get_files_from_dir(self.video_dir, ".mp4")
        print(videos)
        for video in videos:

            print("run prediction for:")
            print(video)
            # use video name as name for predictions save file
            save_file = video.replace(".mp4", "")
            save_file = save_file.replace(".MP4", "")
            sleap_video = self.load_video(self.video_dir + "/" + video)
            try:
                labels = self.run_model(sleap_video)
                labels.save("predictions/" + save_file)
            except KeyError:
                print("ran into error while indexing video: " + video)
                print("Attempting to fix it. please wait...")
                subprocess.run(
                    ["ffmpeg", "-y", "-i", self.video_dir + "/" + video, "-c:v", "libx264", "-pix_fmt", "yuv420p",
                     "-preset", "superfast", "-crf", "23", self.video_dir + "/fixed" + video])
                try:
                    sleap_video = self.load_video(self.video_dir + "/fixed" + video)
                    labels = self.run_model(sleap_video)
                    labels.save("predictions/" + save_file)
                except KeyError:
                    print("unable to fix video")
                    print("continue with next video (if there are any)")

            if tracking:

                print("tracking...")
                print("this can take a few minutes")
                tracked_labels = self.run_tracker(labels, instance_count)
                print(tracked_labels)

                tracked_labels.save("predictions/tracks/" + save_file)


def main():
    print("in main")
    print(args)

    model = SLEAPModel(args.video_dir)
    model.predict()


if __name__ == "__main__":
    sys.exit(main())
