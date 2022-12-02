"""
first recieve an image
then encode
then compare it to every student
"""

import cv2
import face_recognition


# * server calls this with list of recieved images
def recognize_face(images):
    # print("iamges",images)
    imgs = get_image(images)
    # print("img",imgs)
    encoded = encode_image(imgs)
    # print("encoded",encoded)
    result = compare_faces(encoded)
    print("result",result)
    return result

# * Given a list of imgs, returns list of cv2 imgs
# ! for now this takes in a list of paths, change to directly somehow
def get_image(imgs):
    return [cv2.cvtColor(cv2.imread(_, 0), cv2.COLOR_BGR2RGB) for _ in imgs]

# * Given a list of cv2 imgs, returns the encoded list of imgs
def encode_image (imgs):
    # print("akushdakshdakihsdlia", imgs)
    return [face_recognition.face_encodings(_)[0] for _ in imgs]

# * Given a list of encoded imgs, compares the imgs to every img in the database
# ! for now just compare to preset img
def compare_faces(imgs):
    known = cv2.imread("images/mrmusk.jpg", 0)
    known = cv2.cvtColor(known, cv2.COLOR_BGR2RGB)
    
    known_encoding = encode_image([known])

    print(len(imgs))
    return [face_recognition.compare_faces([known_encoding], _) for _ in imgs]

print(recognize_face(["images/mrmusk2.jpg"]))