# Program To Read video
# and Extract Frames
from . import image_stitching_core
import cv2
import math
import os


class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

# Function to extract frames


IMAGE_STORE_DIR = "Frames\\"


def clearFolder():
    folder = IMAGE_STORE_DIR
    print('--Current working directory')
    print(os.path.join(os.getcwd(), IMAGE_STORE_DIR))
    for the_file in os.listdir(os.path.join(os.getcwd(), IMAGE_STORE_DIR)):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)


def FrameCapture(path):
    # Clear frames folder
    clearFolder()

    # Path to video file
    vidObj = cv2.VideoCapture(path)

    # Used as counter variable
    count = 0

    # checks whether frames were extracted
    success = 1

    images_paths = []
    frameRate = vidObj.get(5)  # frame rate

    while(vidObj.isOpened()):
        frameId = vidObj.get(1)  # current frame number
        success, frame = vidObj.read()
        if (success != True):
            break
        if (frameId % math.floor(frameRate) == 0):
            # Create new file name
            file_path = ".\\Frames\\frame%d.jpg" % count

            # Saves the frames with frame-count
            cv2.imwrite(file_path, frame,)

            images_paths.append(file_path)

        count += 1

    args = {
        'image_paths': images_paths,
        'knn': 2,
        'min_correspondence': 10,
        'lowe': 0.7,
        'save_path': 'stitched.png',
        'display': True,
        'save': True,
        'quiet': False,
        'debug': False
    }

    image_stitching_core.Stitch(dotdict(args))

    results = {
        'images_paths': images_paths,
        'save_path': args['save_path']
    }
    return results
