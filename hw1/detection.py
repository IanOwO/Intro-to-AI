import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
# from PIL import Image

def detect(dataPath, clf):
    """
    Please read detectData.txt to understand the format. Load the image and get
    the face images. Transfer the face images to 19 x 19 and grayscale images.
    Use clf.classify() function to detect faces. Show face detection results.
    If the result is True, draw the green box on the image. Otherwise, draw
    the red box on the image.
      Parameters:
        dataPath: the path of detectData.txt
      Returns:
        No returns.
    """
    # Begin your code (Part 4)
    #raise NotImplementedError("To be implemented")
    i=os.getcwd() # get the absolute path of the current execution place
    dp=os.path.normpath(dataPath) # normalize the path
    imagePath = os.path.join(i,os.path.normpath('data\detect')) # get detect's path
    txtpath = os.path.join(i,dataPath) # get .txt path
    with open(txtpath,'r') as txt: # open .txt
      line = txt.readlines() # read all line and store in line
    txt.close() # close .txt

    colorimg = [] # image with RGB color 
    face = [] # the face area
    result = [] # is face or not
    img_num = [] # the image has how many faces
    image = None # the variable to store image that is read
    count = 0 # which image is now
    curlinenum = 0 # counting the current line
    tmp_face = [] # to store the face in one image
    tmp_result = [] # to store the result in one image
    for i in line: # go through all line
      num = i.split(' ') # split the space between the line
      if num[0][-4:] == ".jpg": # if the first word in the line is image path
        image = cv2.imread(os.path.join(imagePath,num[0])) # read the image by the path
        rgbcolor = cv2.cvtColor(image,cv2.COLOR_BGR2RGB) # convert to RGB
        colorimg.append(rgbcolor) # store RGB image
        image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # convert to gray
        curlinenum = int(num[1]) # get the number of the faces in the image
        img_num.append(int(num[1])) # store the number of the faces in the image
        tmp_face = [] # clear the array
        tmp_result = [] # clear the array
        continue
      else:
        tmp = np.zeros((int(num[2]),int(num[3]))) # create an empty array, size = face size
        for pixel_y in range(int(num[2])): # go through pixels in y-axis
          for pixel_x in range(int(num[3])): # go through pixels in x-axis
            tmp[pixel_y][pixel_x] = image[int(num[1])+pixel_y][int(num[0])+pixel_x] # copy face to tmp
        tmp = cv2.resize(tmp,(19,19),interpolation=cv2.INTER_AREA) # resize to train size
        tmp_face.append(num) # add face's coordinates to num
        tmp_result.append(clf.classify(tmp)) # classify the face and store result
        
      count+=1 # count how many faces has loaded
      if count == curlinenum: # if the number of the faces is same as the given num
        count = 0 # reset count
        face.append(tmp_face) # add the face's coordinates list of the image to array
        result.append(tmp_result) # add the result list of the image to array
    
    count = 0 # reset count
    for i in colorimg: # go through all color images
      for f in range(img_num[count]): # go through all faces in one image 
        if(result[count][f] == 1): # draw green if result of the face is 1
          for pixel_y in range(int(face[count][f][3])): # go through pixels in y-axis
            for pixel_x in range(int(face[count][f][2])):  # go through pixels in x-axis

              # draw a 3 pixels line for green 
              if pixel_y == 0 or pixel_y == int(face[count][f][3]) - 1:
                i[int(face[count][f][1]) + pixel_y - 1][int(face[count][f][0]) + pixel_x] = (0,255,0)
                i[int(face[count][f][1]) + pixel_y][int(face[count][f][0]) + pixel_x] = (0,255,0)
                i[int(face[count][f][1]) + pixel_y + 1][int(face[count][f][0]) + pixel_x] = (0,255,0)
              elif pixel_x == 0 or pixel_x == int(face[count][f][2]) - 1:
                i[int(face[count][f][1]) + pixel_y][int(face[count][f][0]) + pixel_x - 1] = (0,255,0)
                i[int(face[count][f][1]) + pixel_y][int(face[count][f][0]) + pixel_x] = (0,255,0)
                i[int(face[count][f][1]) + pixel_y][int(face[count][f][0]) + pixel_x + 1] = (0,255,0)
        
        else : # draw red if result of the face is 0
          for pixel_y in range(int(face[count][f][3])):
            for pixel_x in range(int(face[count][f][2])):

              # draw a 3 pixels line for red
              if pixel_y == 0 or pixel_y == int(face[count][f][3]) - 1:
                i[int(face[count][f][1]) + pixel_y - 1][int(face[count][f][0]) + pixel_x] = (255,0,0)
                i[int(face[count][f][1]) + pixel_y][int(face[count][f][0]) + pixel_x] = (255,0,0)
                i[int(face[count][f][1]) + pixel_y + 1][int(face[count][f][0]) + pixel_x] = (255,0,0)
              elif pixel_x == 0 or pixel_x == int(face[count][f][2]) - 1:
                i[int(face[count][f][1]) + pixel_y][int(face[count][f][0]) + pixel_x - 1] = (255,0,0)
                i[int(face[count][f][1]) + pixel_y][int(face[count][f][0]) + pixel_x] = (255,0,0)
                i[int(face[count][f][1]) + pixel_y][int(face[count][f][0]) + pixel_x + 1] = (255,0,0)
      
      plt.imshow(i) # plot the color image
      plt.show() # show image
      count+=1 # add one to count, meaning that to load next image
      
    # End your code (Part 4)
