__author__ = 'Manish Kumar'

# Built-in Modules
import os
import sys
import time
import logging
import cv2
from stat import S_ISREG, ST_MODE, ST_MTIME


from . import image_stitching


def Stitch(args):
    print(args.debug)
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("main")

    logging.info("beginning sequential matching")

    if image_stitching.helpers.is_cv2():
        sift = cv2.SIFT()
    elif image_stitching.helpers.is_cv3():
        sift = cv2.xfeatures2d.SIFT_create()
    else:
        raise RuntimeError("error! unknown version of python!")

    result = None
    result_gry = None

    flann = cv2.FlannBasedMatcher({'algorithm': 0, 'trees': 5}, {'checks': 50})

    image_paths = args.image_paths
    image_index = -1
    for image_path in image_paths:
        if not os.path.exists(image_path):
            logging.error('{0} is not a valid path'.format(image_path))
            continue
        if os.path.isdir(image_path):
            extensions = [".jpeg", ".jpg", ".png"]

            entries = (os.path.join(image_path, file_name)
                       for file_name in os.listdir(image_path))

            entries = ((os.stat(path), path) for path in entries)
            # leave only regular files, insert creation date
            entries = ((stat[ST_MTIME], path)
                       for stat, path in entries if S_ISREG(stat[ST_MODE]))
            # NOTE: on Windows `ST_CTIME` is a creation date
            #  but on Unix it could be something else
            # NOTE: use `ST_MTIME` to sort by a modification date

            # for cdate, path in sorted(entries):
            #    print(time.ctime(cdate), os.path.basename(path))

            # for file_path in os.listdir(image_path):
            for cdate, path in sorted(entries):
                file_path = os.path.basename(path)
                if os.path.splitext(file_path)[1].lower() in extensions:
                    image_paths.append(os.path.join(image_path, file_path))
                    print(image_paths)
            continue

        logging.info("reading image from {0}".format(image_path))
        image_colour = cv2.imread(image_path)

        if image_colour is None:
            continue

        image_gray = cv2.cvtColor(image_colour, cv2.COLOR_RGB2GRAY)

        image_index += 1

        if image_index == 0:
            result = image_colour
            result_gry = image_gray
            continue

        logger.debug('computing sift features')
        features0 = sift.detectAndCompute(result_gry, None)
        features1 = sift.detectAndCompute(image_gray, None)

        matches_src, matches_dst, n_matches = image_stitching.compute_matches(
            features0, features1, flann, knn=args.knn)

        if n_matches < args.min_correspondence:
            logger.error("error! too few correspondences")
            continue

        logger.debug("computing homography between accumulated and new images")
        H, mask = cv2.findHomography(matches_src, matches_dst, cv2.RANSAC, 5.0)
        result = image_stitching.combine_images(image_colour, result, H)

        if args.display and not args.quiet:
            image_stitching.helpers.display('result', result)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        result_gry = cv2.cvtColor(result, cv2.COLOR_RGB2GRAY)

    logger.info("processing complete!")

    if args.display and not args.quiet:
        cv2.destroyAllWindows()
    if args.save:
        logger.info("saving stitched image to {0}".format(args.save_path))
        image_stitching.helpers.save_image(args.save_path, result)
