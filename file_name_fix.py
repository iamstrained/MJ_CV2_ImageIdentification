# after manual adjustments to files, if you migrate all error files (quad or review) to a staging folder this script will remove the _quad or _review name label from each file name to clean up the processing after work completes.

import os
from os import path
import glob
import numpy as np
# identify target folder - then if passing test of exists, move to iterator pull directory details
ref_images_folder = input('Enter a directory target path (end with \): ') # e.g. C:\Users\Bob\Desktop\
# Create an empty art filename array
my_images = []

if os.path.exists(ref_images_folder):
    
    # All files and directories ending with .txt and that don't begin with a dot, capture for iteration:
    my_images = glob.glob(ref_images_folder + "*.png")
    #print(my_images)
    for imgs_path in my_images:

        oldfilename = os.path.basename(imgs_path)[:-4]
        targetval = oldfilename.rfind('_')
        widthstring = len(oldfilename) - targetval
        reduced_fn= oldfilename[:-widthstring]
        extract = oldfilename[targetval:targetval+7]
        extract2 = oldfilename[targetval:targetval+5]
        if extract == "_review" or extract2 == "_quad":
            newfilename = os.path.join(ref_images_folder, (reduced_fn + '.png'))
            os.rename(path.realpath(imgs_path), newfilename)
