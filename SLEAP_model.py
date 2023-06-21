#!/usr/bin/env python
"""
Takes a model that was made with SLEAP and uses it to estimate keypoint positions of animals on a video

autor: Antsje van der Leij


"""
import argparse
from contextlib import contextmanager
import sys
import os
import sleap
import glob

parser = argparse.ArgumentParser(
    prog='SLEAPyTracks',
    description='A tracker for tracking exploration behavior.',
    epilog='Still a work in progress!')
parser.add_argument('video_dir', help="path to the directory containing the videos to be tracked")


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
        files = [f for f in os.listdir(path) if f.endswith(file_extension)]

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

    def run_model(self, video, save_name):
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

        labels.save("predictions/" + save_name)

    def predict(self):
        print("running predecit")

        videos = self.get_files_from_dir(self.video_dir, ".mp4")
        print(videos)
        for video in videos:
            print("run prediction for:")
            print(video)
            # use video name as name for predictions save file
            save_file = video.replace(".mp4", "")
            sleap_video = self.load_video(self.video_dir + "/" + video)

            self.run_model(sleap_video, save_file)


def main():
    print("in main")
    # model = SLEAPModel("/export/lv9/user/avdleij/dunlin_project/test_set/video")
    # model.predict()


if __name__ == "__main__":
    sys.exit(main())
