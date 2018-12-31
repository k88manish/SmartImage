#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Will Brennan'


import argparse

import image_stitching_core

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('image_paths', type=str, nargs='+',
                        help="paths to one or more images or image directories")
    parser.add_argument('-b', '--debug', dest='debug',
                        action='store_true', help='enable debug logging')
    parser.add_argument('-q', '--quiet', dest='quiet',
                        action='store_true', help='disable all logging')
    parser.add_argument('-d', '--display', dest='display',
                        action='store_true', help="display result")
    parser.add_argument('-s', '--save', dest='save',
                        action='store_true', help="save result to file")
    parser.add_argument("--save_path", dest='save_path',
                        default="stitched.png", type=str, help="path to save result")
    parser.add_argument('-k', '--knn', dest='knn', default=2,
                        type=int, help="Knn cluster value")
    parser.add_argument('-l', '--lowe', dest='lowe', default=0.7,
                        type=float, help='acceptable distance between points')
    parser.add_argument('-m', '--min', dest='min_correspondence',
                        default=10, type=int, help='min correspondences')
    args = parser.parse_args()

    image_stitching_core.Stitch(args)
