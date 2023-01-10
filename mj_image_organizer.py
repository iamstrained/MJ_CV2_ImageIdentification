# iterate - for each image in folder
    # pull image, capture name reference in array,
    # iterate over array (because using the name in the folder will cause a loop bug if we aren't careful)
    # for each name in array - open file in processing tool:
        # perform image analysis on pulled image
        # if passes 4-square test (sic., it's an Upscale), rename image,
        # if it fails, re-test removing the blur to see if it can tenatively flag it for Review; manual intervention may be needed.
        ## NOTE: This step causes more false negatives and pops a few extra into REVIEW that would otherwise be left as proper upscales. May be able to tweak.
        # more to next in array,

        # close out

# leverages the Win10 OS module to support file system manipulation
import os
from os import path
# leverages the openCV module to analyze the pictures and determine if they are 4-square images, leveages glob, leverages numpy
import cv2
import glob
import numpy as np
from matplotlib import pyplot as plt
# Create an empty art filename array
my_images = []

# identify target folder - then if passing test of exists, move to iterator pull directory details
ref_images_folder = input('Enter a directory target path (end with \): ') # e.g. C:\Users\Bob\Desktop\

#defind and read the template into memory for CV2
# ref_template = input('Enter your template image target path (end with a .png or similar extension)') # grid.png
# template = cv2.imread(ref_template,0)
# w, h = template.shape[::-1]

#Reset template to proper read for scanner after finishing w-h extractions
# template = cv2.imread(ref_template,)

if os.path.exists(ref_images_folder):
    
    # All files and directories ending with .txt and that don't begin with a dot, capture for iteration:
    my_images = glob.glob(ref_images_folder + "*.png")
    #print(my_images)
    for imgs_path in my_images:

        # Read the original image
        img = cv2.imread(imgs_path)
        ihei, iwid = img.shape[0:2]
        #using height slice small portion of image out for attempt to compare
        #snag middle and assign middle to updated variables
        iwid = int(iwid/2)
        ihei = int(ihei/2)
        
        ##DEBUG Option
        # Display original image
        #cv2.imshow('Original', img2)
        ##END DEBUG Option

        img2 = img[ihei-40:ihei+40, iwid-40:iwid+40].copy()
        horiz_slice = img[ihei-10:ihei+10, iwid-40:iwid+40].copy()
        vert_slice = img[ihei-40:ihei+40, iwid-10:iwid+10].copy()
        kernel = np.ones((2,2),np.uint8)
        # gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
        
        #### Section for HORIZ Axis
        blurry = cv2.GaussianBlur(horiz_slice, (3, 3), 0)
        hedges = cv2.Canny(blurry,100,200)
        
        ihedges, ihwedges = hedges.shape[0:2]
        ihedges = int(ihedges/2)
        ihwedges = int(ihwedges/2)

        #sum the x axis
        hedges_reduced = hedges[ihedges-3:ihedges+3, ihwedges-40:ihwedges+40].copy()
        img_dilation = cv2.dilate(hedges_reduced, kernel, iterations=1)
        linesum_horiz = np.sum(img_dilation, axis=1, keepdims=True)
        linesum_horiz = np.squeeze(linesum_horiz)

        ##### Section for VERT Axis
        blurry = cv2.GaussianBlur(vert_slice, (3, 3), 0)
        vedges = cv2.Canny(blurry,100,200)
        
        #capture size for manipulation into smaller slice
        ihedges, ihwedges = vedges.shape[0:2]
        #convert to middle of image reference
        ihedges = int(ihedges/2)
        ihwedges = int(ihwedges/2)


        vedges_reduced = vedges[ihedges-40:ihedges+40, ihwedges-3:ihwedges+3].copy()
        img_dilation = cv2.dilate(vedges_reduced, kernel, iterations=1)
        linesum_vert = np.sum(img_dilation, axis=0, keepdims=True)
        linesum_vert = np.squeeze(linesum_vert)

# rename the file based upon the logic gate
        if (linesum_vert[2] >= 10200 or linesum_vert[3] >= 10200) or (linesum_horiz[2] >= 10200 or linesum_horiz[3] >= 10200):
          oldfilename = os.path.basename(imgs_path)[:-4]
          newfilename = os.path.join(ref_images_folder, (oldfilename + '_quad.png'))
          os.rename(path.realpath(imgs_path), newfilename)
          
#if the if fails; double check by re-performing assessment without blurry, if it passes 40% or more then, mark for "review"
        else:
              hedges = cv2.Canny(horiz_slice,100,200)
              
              ihedges, ihwedges = hedges.shape[0:2]
              ihedges = int(ihedges/2)
              ihwedges = int(ihwedges/2)

              #sum the x axis
              hedges_reduced = hedges[ihedges-3:ihedges+3, ihwedges-40:ihwedges+40].copy()
              img_dilation = cv2.dilate(hedges_reduced, kernel, iterations=1)
              linesum_horiz = np.sum(img_dilation, axis=1, keepdims=True)
              linesum_horiz = np.squeeze(linesum_horiz)

              ##### Section for VERT Axis
              vedges = cv2.Canny(vert_slice,100,200)
              
              #capture size for manipulation into smaller slice
              ihedges, ihwedges = vedges.shape[0:2]
              #convert to middle of image reference
              ihedges = int(ihedges/2)
              ihwedges = int(ihwedges/2)


              vedges_reduced = vedges[ihedges-40:ihedges+40, ihwedges-3:ihwedges+3].copy()
              img_dilation = cv2.dilate(vedges_reduced, kernel, iterations=1)
              linesum_vert = np.sum(img_dilation, axis=0, keepdims=True)
              linesum_vert = np.squeeze(linesum_vert)

              # rename the file based upon the logic gate / second pass attempt
              if (linesum_vert[2] >= 9588 or linesum_vert[3] >= 9588) or (linesum_horiz[2] >= 9588 or linesum_horiz[3] >= 9588):
                oldfilename = os.path.basename(imgs_path)[:-4]
                newfilename = os.path.join(ref_images_folder, (oldfilename + '_review.png'))
                os.rename(path.realpath(imgs_path), newfilename)
