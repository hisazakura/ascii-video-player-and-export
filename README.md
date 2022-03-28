# ASCII Video Player and Export
ASCII Video is a program to play and export a video into a video that is made of ASCII texts. ASCII Video 
use FFMPEG for it's main converter.

This program still has minor bugs and is still subject to updates.

## Quick Guide
1. Put your video file in /input/ folder and rename it "video.mp4" (without the quotes).
2. Before you run the application, make sure you checked config.yaml for necessary program configuration.
3. Run "main.exe".
4. After the playback is finished, exit the playback window to exit.
5. If export mode is on, the exported video can be found in "/export/".


## Installation
### Requirements
- Python 3.0

Download Python on https://www.python.org/download/releases/3.0/

- FFMPEG

FFMPEG download link and install guide can be found on https://www.wikihow.com/Install-FFmpeg-on-Windows

## Installation
- Make sure you installed all the requirements properly.
- Download the latest version on releases.
- Extract it in a folder of choice.
 
# Running the program
For the program to run properly, please do not change or delete the necessary directories. With default configurations, simply put the video in /input/ folder and rename it to video.mp4, then run the program. After running the program, a console will appear and after loading for a while another screen will playback the video in ASCII. For some computers, the playback might experience [frame lag](#frame-lag). The playback will stop at the last frame of the video, so it's not frozen but it just finished playback. For now, the program can only playback once so when it's done doing playback, you can exit the playback window.

## Configurations
This program has additional configurations. Available configurations in config.yaml are:
- preload: True/False (toggles pre-load)
- export: True/False (toggles export)
### Pre-load
Pre-load mode can be toggled on to load everything necessary before playback. This will significantly increase loading time but will reduce [frame lag](#frame-lag), making the playback smoother. 

### Export
Export mode can be toggled on to record the playback and export it to /export/ directory. This will significantly increase [frame lag](#frame-lag) caused by the rendering.

## Additional Terms

### Frame Lag
Frame lag is when the frames lag behind due to a process taking too long and reducing the frame rate, making them lag behind the audio. Frame lag intensity depends on processor speed.

# WARNINGS
Please do not exit the playback window when it's still playing as it will mess up exporting process!
