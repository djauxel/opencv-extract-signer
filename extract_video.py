from cv2 import cv2
import numpy as np
import os

from coordinates import get_video_dir

def get_opencv_dir():
    return 'C:\\Projects\\openpose-extract-signer\\opencv'

def generate_cropped_video(frames):
    MAX_EXTRACT_COUNT = 500
    extract_count = 1
    
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

        print(f'\nEXTRACTING {extract_count} of {MAX_EXTRACT_COUNT}')
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
        extract_count += 1

    print('EXTRACTING FINISHED')

def convert_command(video_avi, video_mp4):
    
    base_command = 'ffmpeg' + ' '
    input_commands = '-i ' + '\"' + video_avi + '\"' + ' ' 
    options = '-vcodec libx264 -f mp4 -vb 1200k -preset slow' + ' '
    output_commands = '\"' + video_mp4 + '\"'
    
    return base_command + input_commands + options + output_commands

def convert_to_mp4():
    MAX_CONVERT_COUNT = 500
    convert_count = 1

    opencv_dir = get_opencv_dir()

    os.chdir(opencv_dir)

    for file in os.listdir(opencv_dir):
        video_avi_path = opencv_dir + '\\' + file

        video_mp4 = os.path.splitext(file)[0] + '.mp4'
        video_mp4_path = opencv_dir + '\\' + video_mp4

        print(f'\nCONVERTING {convert_count} of {MAX_CONVERT_COUNT}')
        print(f'Writing {video_mp4} . . .')

        os.system('cmd /c' + convert_command(video_avi_path, video_mp4_path))
        os.remove(video_avi_path)

        convert_count += 1

    print('CONVERTING FINISHED')