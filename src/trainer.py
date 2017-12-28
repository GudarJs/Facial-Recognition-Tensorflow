import os
import time
import math
import pickle
import cv2
import facenet
import numpy as np

from .face import Detection, Encoder, Face
from sklearn.svm import SVC

scale = 1
dataset_path = 'datasets'
name = raw_input('Please enter a name: ')
path = dataset_path + '/' + name
classifier_filename = 'classifier/face_classifier.pkl'
face_encoder = Encoder()

def save_image(face_image, face_id):
    if not os.path.isdir(path):
        os.mkdir(path)
    cv2.imwrite('{}/{}_{}.png'.format(path, name, str(face_id).zfill(3)), face_image)

def verify_detection(face_bb, face_landmarks, margin=5):
    counter = 0
    eyes_center = (int(face_landmarks[5] + (face_landmarks[6] - face_landmarks[5]) / 2)) * scale
    nose_center = (int(face_bb[0] + (face_bb[2] / 2))) * scale

    # Check eyes position
    left_eye_validation = face_landmarks[5] >= eyes_center - margin and face_landmarks[5] <= eyes_center + margin
    right_eye_validation = face_landmarks[6] >= eyes_center - margin and face_landmarks[6] <= eyes_center + margin
    if (left_eye_validation and right_eye_validation):
        counter += 1
    # Check nose position
    if (face_landmarks[2] >= nose_center - margin and face_landmarks[2] <= nose_center + margin):
        counter += 1
    
    if (counter == 2):
        return True
    else:
        return False

def add_overlays(frame, face, face_bb, face_landmarks, frame_rate):
    if face is not None:
        if face.image is not None:
            cv2.imshow('face', face.image)

    if face_landmarks is not None:
        # Draw eyes line
        eyes_center = (int(face_landmarks[5] + (face_landmarks[6] - face_landmarks[5]) / 2)) * scale
        cv2.line(frame, (int(face_bb[0]) * scale, eyes_center), (int(face_bb[0] + face_bb[2]) * scale, eyes_center), (0,0,255), 2)

        # Draw landmarks
        for i in range(0, 3):
            cv2.circle(frame, (int(face_landmarks[i]) * scale, int(face_landmarks[i+5]) * scale), 5, (255,0,0), -1)
    
    if face_bb is not None:
        # Draw nose line
        nose_center = (int(face_bb[0] + (face_bb[2] / 2))) * scale
        cv2.line(frame, (nose_center, int(face_bb[1]) * scale), (nose_center, int(face_bb[1] + face_bb[3]) * scale), (0,0,255), 2)

        # Draw bounding box
        cv2.rectangle(frame,
            (int(face_bb[0]) * scale, int(face_bb[1]) * scale), (int(face_bb[0] + face_bb[2]) * scale, int(face_bb[1] + face_bb[3]) * scale),
            (0, 255, 0), 2)

    # Draw number of fotograms per second
    cv2.putText(frame, str(frame_rate) + " fps", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                thickness=2, lineType=2)

def main():
    frame_interval = 5  # Number of frames after which to run face detection
    fps_display_interval = 0  # seconds
    frame_rate = 0
    frame_count = 0
    images_saved = 0

    video_capture = cv2.VideoCapture(1)
    face_detection = Detection()
    start_time = time.time()

    # Setting camera parameters
    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640);
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480);

    while True:
        # Read frame from camera
        ok, frame = video_capture.read()
        if not ok:
            break

        if (frame_count % frame_interval) == 0:
            faces = face_detection.find_faces(cv2.resize(frame, (frame.shape[1] / scale, frame.shape[0] / scale)))

            # Check our current fps
            end_time = time.time()
            if (end_time - start_time) > fps_display_interval:
                frame_rate = int(frame_count / (end_time - start_time))
                start_time = time.time()
                frame_count = 0

        # Check if a face was detected to add the overlays at frame
        # if not refresh fotograms per second at screen
        if len(faces) > 0:
            face_landmarks = faces[0].landmarks
            face_bb = faces[0].bounding_box
            face_bb = (face_bb[0], face_bb[1], face_bb[2] - face_bb[0], face_bb[3] - face_bb[1])
            add_overlays(frame, faces[0], face_bb, face_landmarks, frame_rate)

            if (verify_detection(face_bb, face_landmarks)):
                images_saved += 1
                save_image(faces[0].image, images_saved)
        else:
            add_overlays(frame, None, None, None, frame_rate)

        frame_count += 1
        cv2.imshow('Video', frame)

        if (images_saved == 50):
            train_classifier();
            break

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
