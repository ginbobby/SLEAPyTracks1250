#!/usr/bin/env python
"""
Uses a model that was trained with SLEAP and uses it to estimate keypoint positions of the red knot in video's.

autor: Antsje van der Leij

"""

import sys
import os
import sleap
import glob
import subprocess


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
        """
        gets files names ending with the file exetntion from target directory and returns those files as a list
        :param path: absolute path to target directory
        :param file_extension: the extension of retrieved files
        :return: list with files ending with the file_extension
        """

        # check if file exists
        if not os.path.isdir(path):
            sys.exit("File path to videos does not exist or is incorrect!")
            print(path)

        # get only one type of file
        files = [f for f in os.listdir(path) if f.endswith(file_extension) or f.endswith(file_extension.upper())]

        # check if any files match file type
        if not files:
            sys.exit("no " + file_extension + " found in " + path)

        return files

    def load_video(self, path_to_video):
        """
        Loads a mp4 video as SLEAP video object
        :param path_to_video:
        :return: SLEAP video object
        """
        print("load video")

        loaded_video = sleap.load_video(path_to_video)
        return loaded_video

    def load_model(self):
        """
        loads a trained SLEAP model directory model
        """
        print("load model")

        # use glob to make a variable model path so name of model doesn't matter
        model_path = glob.glob('model/*')

        model = sleap.load_model(model_path)

        return model

    def run_tracker(self, labels, instance_count):

        """
        initialises SLEAP tracker
        :param labels: SLEAP Labels object
        :param instance_count: int
        :return: SLEAP Labels object
        """

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
        :param video: video file name
        :return: SLEAP Labels object
        """

        print(f'running model on {video}')


        # run model

        labels = self.model.predict(video)
        labels = sleap.Labels(labels.labeled_frames)

        return labels

    def predict(self, instance_count, tracking):
        """
        run model over every video in target directory and actives tracking if tracking is True
        :param instance_count: (int) amount of expected animals in videos
        :param tracking: (boolean)

        """

        videos = self.get_files_from_dir(self.video_dir, ".mp4")
        print(videos)
        for video in videos:

            print("run prediction for:")
            print(video)
            # use video name as name for predictions save file
            save_file = video.replace(".mp4", "")
            save_file = save_file.replace(".MP4", "")
            sleap_video = self.load_video(self.video_dir + "/" + video)
            # remove slp from previous run
            # for testing and corrections this is done now and not after program is completed
            if os.path.exists("predictions/"):
                files = [f for f in os.listdir("predictions/")]
                for f in files:
                    if os.path.exists("predictions/" + f):
                        os.remove("predictions/" + f)

            # most common error is KeyError while indexing videos
            try:
                labels = self.run_model(sleap_video)
                labels.save("predictions/" + save_file)
            # ffmpeg command is a quick fix for KeyError while indexing
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
                    continue

            # if tracking flag is set to True start tracking function
            if tracking:
                print("tracking...")
                print("this can take a few minutes")
                tracked_labels = self.run_tracker(labels, instance_count)
                print(tracked_labels)

                tracked_labels.save("predictions/tracks/" + save_file)


def main():
    print("in main")

    model = SLEAPModel(args.video_dir)
    model.predict()


if __name__ == "__main__":
    sys.exit(main())
