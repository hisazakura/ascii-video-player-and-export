import subprocess
import time
import cv2
import os
import math
import ffmpeg
import pygame
import yaml
from tqdm import tqdm
from pygame import mixer

# Import YAML config
with open('config.yaml', 'r') as stream:
    config = yaml.safe_load(stream)
print("Running with the following config")
for key in config:
    print(key, " : ", config[key])

# ASCII Variables
density = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^`' "  # Sorted bright to dark
factor = 3.8  # math.ceil(255/len(density))

# FFMPEG

# Delete existing files
files = os.listdir('data/frames')
if len(files) != 0:
    for f in files:
        os.remove(os.path.join('data/frames', f))

# Load video
print("Loading video...")
start = time.time_ns()
if os.path.exists('input/video.mp4'):
    video = (
        ffmpeg
            .input('input/video.mp4')
            .filter('fps', fps='30')
            .filter('scale', -1, 48)
            .output('data/frames/out%d.png', start_number=0)
            .overwrite_output()
            .run(quiet=True)
    )
    audio = (
        ffmpeg
            .input('input/video.mp4')
            .output('data/audio/audio.mp3')
            .overwrite_output()
            .run(quiet=True)
    )
    max_frame = len(os.listdir('data/frames'))
    end = time.time_ns()
    print("Video loaded in " + str(round((end - start) / 1000000, 2)) + " ms")
else:
    raise Exception("Video does not exist! Did you forget to rename?")


# Pre-load images (slower loading but reduces frame lag)
def preload():
    start = time.time_ns()
    ASCII_list = []
    progress = 0
    for index in tqdm(range(len(os.listdir('data/frames')) - 1), desc= "Pre-loading..."):
        path = r'data/frames/out' + str(index) + '.png'
        img = cv2.imread(path, 0)
        ASCII = []
        for i in range(len(img)):
            row = ""
            for j in range(len(img[0])):
                row += density[67 - math.floor(img[i][j] / factor)] + ' '
            ASCII.append(row)
        ASCII_list.append(ASCII)
        progress += 1
    end = time.time_ns()
    print("Pre-load completed in " + str(round((end - start) / 1000000, 2)) + " ms")
    return ASCII_list


# Pre-load loop function (enable if using pre-load)
def preload_display(ASCII_list):
    if ASCII_list is None:
        return
    ASCII = ASCII_list[frame - 1]
    for i in range(len(ASCII)):
        string = ASCII[i]
        text = font.render(string, False, WHITE, False)
        screen.blit(text, (0, font_size * i))


# Pre-load mode
ascii_list = None
if config['preload']:
    ascii_list = preload()


# Normal display loop
def display():
    path = r'data/frames/out' + str(frame - 1) + '.png'
    img = cv2.imread(path, 0)
    for i in range(len(img)):
        string = ""
        for j in range(len(img[0])):
            string += density[67 - math.floor(img[i][j] / factor)] + ' '
        text = font.render(string, False, WHITE, False)
        screen.blit(text, (0, font_size * i))


# Pygame settings

# Screen size optimized for 64x48px image
WIDTH = 1152
HEIGHT = 720

# Default colors for grayscale image
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initiation
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Font
font_size = 15
font = pygame.font.SysFont('Mono', font_size)  # I found out that Mono font is consistent with the width

# Clock and frame
clock = pygame.time.Clock()
frame = 0

# Music
mixer.init()
mixer.music.load('data/audio/audio.mp3')
mixer.music.set_volume(0.5)
mixer.music.play()

# Main Loop
print("Playing video...")
running = True
while running:
    dt = clock.tick(30)  # FPS control

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    frame += 1
    if frame > max_frame - 1:
        frame = max_frame - 1

    screen.fill(BLACK)

    # Pre-load mode
    if config['preload']:
        preload_display(ascii_list)

    # Normal load
    else:
        display()

    if config['export']:
        pygame.image.save(screen, 'data/sc/sc' + str(frame) + '.png')
    pygame.display.flip()
pygame.quit()
print("Playback complete!")
# Export
if config['export']:
    print("Exporting...")
    start = time.time_ns()
    subprocess.call([
        'ffmpeg',
        '-r', '30',
        '-i', 'data/sc/sc%d.png',
        'export/export_video.mp4'],
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL
    )
    export_video = ffmpeg.input('export/export_video.mp4')
    export_audio = ffmpeg.input('data/audio/audio.mp3')
    export_final = (
        ffmpeg
            .concat(export_video, export_audio, v=1, a=1)
            .output('export/export.mp4', pix_fmt='yuv420p', profile='main')
            .overwrite_output()
            .run(quiet=True)
    )
    os.remove('export/export_video.mp4')
    end = time.time_ns()
    print("Export completed " + str(round((end - start) / 1000000, 2)) + " ms")

# Delete used files
print("Deleting caches...")
files = os.listdir('data/frames')
for f in files:
    os.remove(os.path.join('data/frames', f))
files = os.listdir('data/sc')
for f in files:
    os.remove(os.path.join('data/sc', f))
files = os.listdir('data/audio')
for f in files:
    os.remove(os.path.join('data/audio', f))
print("Process complete, exiting...")
