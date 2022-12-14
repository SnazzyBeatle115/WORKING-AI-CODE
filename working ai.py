"""
first recieve an image
then encode
then compare it to every student
"""

import cv2
import face_recognition
import time
import numpy as np
import PIL
from PIL import Image
import math


saveNum = 0

# * server calls this with list of recieved images
def recognize_face(images):
    # print("iamges",images)
    # startingtime=time.time()
    imgs = get_image(images)
    # print("Time to reduce res: ", time.time()-startingtime)
    # cv2.imshow("Image", imgs[0])
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # print("IMGS", len(imgs))
    # print("img",imgs)
    encoded = encode_image(imgs)
    print("Encoded", len(encoded))
    print("encoded",encoded)
    result = compare_faces(encoded)
    # print("result",result)
    return result

# * Given a list of imgs, returns list of cv2 imgs
# ! for now this takes in a list of paths, change to directly somehow
def get_image(imgs):
    result = []
    for img in imgs:
        im = cv2.cvtColor(cv2.imread(img, 0), cv2.COLOR_BGR2RGB)
        result.append(low_res(im))
        # result.append(im)

    return result


def crop(cv2_img):
    global saveNum
    im_pil = Image.fromarray(cv2_img)
    width, height = im_pil.size
    if width>height:
        croppedIm = im_pil.crop(((width/2)-(height/2), 0, (width/2)+(height/2), height))
    else:
        croppedIm = im_pil.crop((0, (height/2)-(width/2), width, (height/2)+(width/2)))
        
    croppedIm.save(f"images/save{saveNum}.jpg")
    saveNum += 1

    croppedIm = np.array(croppedIm)

    return croppedIm

def low_res(cv2_img):
    #preimg = cv2.imread(np.asarray(cv2_img))
    height, width, channel, = cv2_img.shape
    # cf = commonfactors(width, height)
    factor = 1
    #for i in range(len(cf) - 1, -1, -1):
    # for i in cf:    
    #     if not(int(width/i)<100 or int(height/i) < 100):
    #         factor = i
    #         break
    new_height = 128
    new_width = new_height*width//height
    # print("orig h,w",height,width)
    # print("mew",new_height,new_width)
    reduced_res = cv2.resize(cv2_img, (new_width, new_height), interpolation = cv2.INTER_AREA)
    return reduced_res


def factors(x):
    f = {1, x}
    for i in range(2, math.ceil(math.sqrt(x))):
        if x % i == 0:
            f.add(i)
            f.add(x//i)
    return f


def commonfactors(x, y):
    fx = factors(x)
    fy = factors(y)

    cf = list(fx & fy)
    cf.sort() 
    return list(reversed(cf))



# * Given a list of cv2 imgs, returns the encoded list of imgs
def encode_image (imgs):
    all_faces = []
    for _ in imgs:

        faces = face_recognition.face_encodings(_)
        if len(faces) > 0:
        #     cv2.imshow("Image", _)
        #     cv2.waitKey(0)
        #     cv2.destroyAllWindows()
            all_faces.append(faces[0])
        else:
        #     cv2.imshow("Image", _)
        #     cv2.waitKey(0)
        #     cv2.destroyAllWindows()
            print("No face detected.")
        # all_faces.append(faces)
    print(np.asarray(all_faces).shape)
    return all_faces

# * Given a list of encoded imgs, compares the imgs to every img in the database
# ! for now just compare to preset img
def compare_faces(imgs):
    # known = cv2.imread("images/mrmusk2.jpg", 0)
    # known = cv2.cvtColor(known, cv2.COLOR_BGR2RGB)
    # known = low_res(known)
    
    # known_encoding = encode_image([known])
    
    # cv2.imshow("Image",known)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # print("now",len(known_encoding),known_encoding)
    # print(known_encoding)
    # print(len(imgs))
    # for i in range(100):
    #     [face_recognition.compare_faces(known_encoding, _) for _ in imgs]
    return [face_recognition.compare_faces(known_encoding, _) for _ in imgs]

def getTestImage(img):
    return encode_image(get_image(img))
known_encoding = getTestImage(["images/mrmusk2.jpg"])

startingtime = ( time.time() )
print(recognize_face(["images/mrmusk.jpg"]))
endingtime = ( time.time() )
print("Time taken for 1 image:",endingtime-startingtime)
# startingtime = int( time.time() )
# print(recognize_face(["images/Unknown1.jpg", "images/mrmusk.jpg"]))
# endingtime = int( time.time() )
# print("Time taken for 2 images:",endingtime-startingtime)
# startingtime = int( time.time() )
# print(recognize_face(["images/Unknown1.jpg", "images/mrmusk.jpg", "images/mrmusk2.jpg"]))
# endingtime = int( time.time() )
# print("Time taken for 3 images:",endingtime-startingtime)
# startingtime = int( time.time() )
# print(recognize_face(["images/Unknown1.jpg", "images/mrmusk.jpg", "images/mrmusk2.jpg", "images/mrmusk2.jpg", "images/mrmusk2.jpg", "images/mrmusk2.jpg", "images/mrmusk2.jpg", "images/mrmusk2.jpg", "images/mrmusk2.jpg", "images/mrmusk2.jpg"]))
# endingtime = int( time.time() )
# print("Time taken for 10 images:",endingtime-startingtime)