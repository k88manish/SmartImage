# Program To Read video
# and Extract Frames
import cv2
import math

from . import image_stitching_core


class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

# Function to extract frames


def FrameCapture(path):

    # Path to video file
    vidObj = cv2.VideoCapture(path)

    # Used as counter variable
    count = 0

    # checks whether frames were extracted
    success = 1

    images_paths = []
    frameRate = vidObj.get(5) #frame rate

    while(vidObj.isOpened()):
        frameId = vidObj.get(1) #current frame number
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
    }
    return results
