# Program To Read video
# and Extract Frames
import cv2

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

    while success:
        vidObj.set(cv2.CAP_PROP_POS_MSEC, (count*1000))
        # vidObj object calls read
        # function extract frames
        success, image = vidObj.read()

        # Create new file name
        file_path = ".\\Frames\\frame%d.jpg" % count

        # Saves the frames with frame-count
        cv2.imwrite(file_path, image,)

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
