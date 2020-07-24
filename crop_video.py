from cv2 import cv2
import numpy as np
import os

from coordinates import get_video_dir

def get_opencv_dir():
    return 'C:\\Projects\\openpose-extract-signer\\opencv'

def generate_cropped_video(frames):
    MAX_PROCESS_COUNT = 500
    process_count = 1
    
    video_dir = get_video_dir()

    frame_index = 0

    for file in os.listdir(video_dir):
        video_path = video_dir + '\\' + file

        cap = cv2.VideoCapture(video_path)

        obj = frames[frame_index]
        x1 = obj.topLeft[0]
        y1 = obj.topLeft[1]
        x2 = obj.bottomRight[0]
        y2 = obj.bottomRight[1]

        video_output = get_opencv_dir() + '\\' + file
        fps = cap.get(cv2.CAP_PROP_FPS)
        fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
        frame_width = x2 - x1
        frame_height = y2 - y1

        out = cv2.VideoWriter(video_output, fourcc, fps, (frame_width,frame_height))

        print(f'\nPROCESS {process_count} of {MAX_PROCESS_COUNT}')
        print(f'Writing {file} . . .')

        while True:
            ret, frame = cap.read()

            if ret:
                # Region of interest
                roi = frame[y1:y2, x1:x2]
                
                out.write(roi)

                # cv2.imshow('frame', roi)

                # if cv2.waitKey(1) & 0xFF == ord('q'):
                #     break
            
            else:
                break

        # When everything is done, release the video capture and video write objects
        cap.release()
        out.release()

        # Close all the frames
        cv2.destroyAllWindows()

        frame_index += 1
        process_count += 1

    print('PROCESS FINISHED')