import os
import cv2


def loadImages(dataPath):
    """
    load all Images in the folder and transfer a list of tuples. The first 
    element is the numpy array of shape (m, n) representing the image. 
    The second element is its classification (1 or 0)
      Parameters:
        dataPath: The folder path.
      Returns:
        dataset: The list of tuples.
    """
    # Begin your code (Part 1)
    # raise NotImplementedError("To be implemented")
    i=os.getcwd() # get the absolute path of the current execution place
    dp=os.path.normpath(dataPath) #  normalize the datapath, make “ / ” become “ \ “
    path = os.path.join(i,dp) # join current path and the given path
    dataset = [] # to store the input image
    for filename in os.listdir(path): # go through all folder in train or test (face or non-face)
       for second_file in os.listdir(os.path.join(path,filename)): # go through all data in face or non-face
          img = cv2.imread(os.path.join(os.path.join(path,filename),second_file)) # read image
          if img is not None: # check if img is none or not
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert the color to grayscale
            if filename == 'face': # if the folder is face, give a label 1
               dataset.append([img,1])
            else : # else, give a label 0
               dataset.append([img,0])

    # End your code (Part 1)

    #encounter problem
    #1.path problem, use normpath
    #2.executing place, cd at cmd to the right folder
    #3.path problem, use getcwd
    return dataset
