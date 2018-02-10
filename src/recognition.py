import io
import base64

import cv2
import numpy as np

def add_overlays(image, faces):
    for i, face in enumerate(faces):
        face_bb = face.bounding_box.astype(int)
        cv2.rectangle(image,
                        (face_bb[0], face_bb[1]), (face_bb[2], face_bb[3]),
                        (0, 255, 0), 2)
                        
        if face.name != 'Unknown':
            cv2.putText(image, face.name, (face_bb[0], face_bb[3]),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0),
                        thickness=2, lineType=2)
        else:
            cv2.putText(image, 'Unknown', (face_bb[0], face_bb[3]),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),
                        thickness=2, lineType=2)
        faces[i] = {
            'name': face.name,
            'confidence': face.confidence
        }

def decode_image(encoded_image):
    in_memory_file = io.BytesIO()
    encoded_image.save(in_memory_file)
    data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
    return cv2.imdecode(data, 1) # 1 for decode as a color image

def recognize_faces(encoded_image, face_recognition):
    image = decode_image(encoded_image)
    faces = face_recognition.identify(image)

    add_overlays(image, faces)
    _, image_buffer = cv2.imencode('.jpg', image)
    image = base64.b64encode(image_buffer)

    return image, faces
