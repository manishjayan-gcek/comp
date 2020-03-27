import os
import get_coeff as comp
import utils as util
import numpy as np
import PIL
import time
from PIL import Image, ImageEnhance
from sys import argv
import boto3

#from resizeimage import resizeimage
import math


def running(file, comp_file,fname):
    
    bucketname = file # replace with your bucket name
    filename =fname # replace with your object key
    ext = str(filename[len(filename)-4:len(filename)])
    client = boto3.client('s3',aws_access_key_id='AKIAJA5O2DUFZAPU6BAQ',aws_secret_access_key='8xnMVqXeIK/WWq8Lh+DEYuLa1AqfRPzhNf/HkhqA')
    s3 = boto3.resource('s3')
    temp='temp'+ext
    s3.Bucket(bucketname).download_file(filename, temp)
    img = util.load_img('temp.jpg')                       # Loads the image selected
    coef = comp.extract_rgb_coeff(img)              # Extracts the RBG Coefficients from the image 
    t1=time.time()
    image = comp.img_from_dwt_coeff(coef)           # Forms the new image using the dwt coeeficients
    t2=time.time()
    print(t2-t1)
    comp_file = "compress_"+filename[0:len(filename)-4]+ext
    print(comp_file)
    print(image.save(comp_file))   
                            # Saves the image
    s3.Object(bucketname,comp_file).upload_file(Filename=comp_file)
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(2)
   
    file_enh = "enhanced_"+filename[0:len(filename)-4]+ext
    image.save(file_enh)
    im = Image.open(file_enh)
    size = get_image_dimensions(temp)
    im_resized = im.resize(size, Image.
                           ANTIALIAS)
    im_resized.save(comp_file)
    '''
    os.remove(comp_file)
    os.remove(file_enh)
    '''
    return os.path.getsize(temp)/os.path.getsize(comp_file)


def get_image_dimensions(imagefile):             # Function to get the dimensions of the image
    with Image.open(imagefile) as img:
        width, height = img.size
    return int(width), int(height)              # returns the width and height of the image in terms of pixels


def create_folder():
    path = "Compressed_Images"                  # Creates the folder and in order to save the image in this folder
    os.rmdir(path)
    os.mkdir(path)


def run():  
    '''
    Main Function to run the compression
    '''
    
    print(argv[2])
    fname=argv[2]
    file =[]
    file.append(argv[1])
    # create_folder()
    ans = 0
    mini = math.inf
    maxi = -math.inf
    for i in range(len(file)):
        x = list(file[i])
        ind = 0
        for j in range(len(x)):
            if x[j] == '/':
                ind = j
        file2 = "Compressed_Images/"+file[i][ind+1:len(x)-4]+"_compressed"    # create the path inorder to save the  compressed image in the created folder
        ans1 = running(file[i], file2,fname)                                       # The function to compress the image which returns the compression ratio
    
        '''
        Finds the maximum compression and minimum compression ratio when multiple images are selected
        '''
        mini = min(mini, ans1)
        maxi = max(maxi, ans1)                                                        
        ans += ans1
    
    print("\nCompression Ratio : %.2f" % (ans/len(file)))
    print("\nMax : "+str(maxi) + "\nMin : " + str(mini))
    
    

if __name__ == "__main__":
    run()
