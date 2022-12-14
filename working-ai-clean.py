"""
first recieve an image
then encode
then compare it to every student
"""

import cv2
import face_recognition
import time

known_encodings = {}

# * server calls this with list of recieved images
def recognize_face(images):
    imgs = get_image(images)
    encoded = encode_image(imgs, images)
    result = compare_faces(encoded)
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
# * reduces the resolution of the image
def low_res(cv2_img):
    height, width, channel, = cv2_img.shape
    new_height = 128
    new_width = new_height*width//height
    reduced_res = cv2.resize(cv2_img, (new_width, new_height), interpolation = cv2.INTER_AREA)
    return reduced_res

# * Given a list of cv2 imgs, returns the encoded list of imgs
def encode_image (imgs, path=None):
    all_faces = []
    for i in range(len(imgs)):
        img = imgs[i]
        faces = face_recognition.face_encodings(img)
        if len(faces) > 0:
            all_faces.append(faces[0])
        else:
            if path is not None:
                print(f"No face detected in {path[i]}.")
            else:
                print("No face detected.")
    return all_faces

# * Given a list of encoded imgs, compares the imgs to every img in the database
# ! for now just compare to preset img
def compare_faces(imgs):
    global known_encodings
    best = ["Nobody", 0]
    for person in known_encodings:
        encoding = known_encodings[person]
        total_trues = 0
        for img in imgs:
            # print(face_recognition.compare_faces(encoding, img))
            if face_recognition.compare_faces(encoding, img)[0]:
                total_trues+=1
        if total_trues > best[1]:
            best = [person, total_trues]

    
    return best

def getTestImage(img):
    return encode_image(get_image([img]), [img])

# TEST BY ADDING MORE KNOWN ENCODINGS AND MORE IMAGES
known_encodings["Musk"] = getTestImage("images/mrmusk3.jpg")
known_encodings["David"] = getTestImage("images/Unknown1.jpg")

unknown_faces = ["images/mrmusk.jpg","images/mrmusk2.jpg","images/David.jpg"]

startingtime = ( time.time() )
print(recognize_face(unknown_faces))
endingtime = ( time.time() )
print(f"Time taken for {len(unknown_faces)} image(s):",endingtime-startingtime)
