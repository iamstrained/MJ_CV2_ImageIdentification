# MJ_CV2_ImageIdentification
Python3 Midjourney Scriplet for Win10 using CV2 to identify Quad Images versus Upscales.

**Intent:** Midjourney website as of early (Jan-2023) does not provide a means to only export your upscales. This leads to a lot of chaff for quad images that are not often desireable for subsequent use. This script is a machine assistance to accelerate the identification of QUAD versus UPSCALE images to assist Midjourney users on their local machine when using the output .zip image files.

## Procedure Summary


### Python Requires
You should ensure you PIP install all elements listed that may be required for functionality. CV2 does install many of these, but please perform your pip --user installs as required.

```python

import os
from os import path
# leverages the openCV module to analyze the pictures and determine if they are 4-square images, leveages glob, leverages numpy
import cv2
import glob
import numpy as np
from matplotlib import pyplot

```
