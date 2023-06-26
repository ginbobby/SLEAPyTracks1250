
# README SLEAPyTracks #
.

## What is this repository for? ##



This is a tracker for tracking exploration behavior of birds. Currently trained for use on red knot exploration tests.
Runs a trained SLEAP model over multiple videos and returns tracking data as a csv file.

More functionality to be added soon!

* Version 0.1.0

## Installation ##

SLEAPyTracks uses the SLEAP library. So first we install SLEAP using miniconda.

The following instructions are for Windows

### Install Miniconda ###

Anaconda is a Python environment manager that makes it easy to install SLEAP and its necessary dependencies without affecting other Python software on your computer.

Miniconda is a lightweight version of Anaconda. To install it:

Go to: https://docs.conda.io/en/latest/miniconda.html#latest-miniconda-installer-links

Download the latest version for your OS.

Follow the installer instructions.



### Install SLEAP ###

open "Anaconda Powershell Prompt" from the start menu

Execute the following lines in the Anaconda powershell:

```bash
conda create -y -n sleap -c sleap -c nvidia -c conda-forge sleap=1.3.0
```

```bash
conda install -n sleap ffmpeg
```

### Install SLEAPyTrack ###

Clone the SLEAPyTrack repo from GitHub

in the Anaconda powershell:

```bash
git clone https://github.com/aavanderleij/SLEAPyTracks.git
```
## Usage ##

with the Anaconda powershell got into the map for SLEAPyTracks

```bash
cd SLEAPyTracks
```
run SLEAPyTracks on the directory you want to track

```bash
python SLEAPyTracks <your_video_dir_location>
```

## References ##
SLEAP is the successor to the single-animal pose estimation software LEAP (Pereira et al., Nature Methods, 2019).

If you use SLEAP in your research, please cite:

T.D. Pereira, N. Tabris, A. Matsliah, D. M. Turner, J. Li, S. Ravindranath, E. S. Papadoyannis, E. Normand, D. S. Deutsch, Z. Y. Wang, G. C. McKenzie-Smith, C. C. Mitelut, M. D. Castro, J. D’Uva, M. Kislin, D. H. Sanes, S. D. Kocher, S. S-H, A. L. Falkner, J. W. Shaevitz, and M. Murthy. Sleap: A deep learning system for multi-animal pose tracking. Nature Methods, 19(4), 2022

## Contact ##

for questions or suggestions please email me at:
antsje.van.der.leij@nioz.nl

https://github.com/aavanderleij
