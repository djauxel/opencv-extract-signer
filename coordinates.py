import json
import os
import cv2 as cv2

from bounding_box import BoundingBox
from frame import Frame

def get_json_dir():
    return 'C:\\Projects\\openpose-extract-signer\\openpose_output\\json'

def get_video_dir():
    return 'C:\\Projects\\openpose-extract-signer\\openpose_output\\videos'

# Return a list of only x-coordinates from an array that contains
# x-coordinates, y-coordinates, and confidence scores
def get_x_coordinates(keypoints):
    return keypoints[::3]

# Return a list of only y-coordinates from an array that contains
# x-coordinates, y-coordinates, and confidence scores
def get_y_coordinates(keypoints):
    return keypoints[1::3]

def valid_body_part(index):
    invalid_body_parts = [8, 9, 10, 11, 12, 13, 14, 19, 20, 21, 22, 23, 24]

    if index not in invalid_body_parts:
        return True
    
    return False

# TODO: FIX THE VIDEO PATH
def get_video_width(video_file):
    video_dir = get_video_dir()
    video_path = video_dir + '\\' + video_file

    vid = cv2.VideoCapture(video_path)
    width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)

    return width

# TODO: FIX THE VIDEO PATH
def get_video_height(video_file):
    video_dir = get_video_dir()
    video_path = video_dir + '\\' + video_file

    vid = cv2.VideoCapture(video_path)
    height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    return height

def get_bounding_box(keypoints, bounding_box, is_pose, count, width, height):
    x_coordinates = get_x_coordinates(keypoints)
    y_coordinates = get_y_coordinates(keypoints)

    if count == 0:
        bounding_box.min_x = x_coordinates[0]
        bounding_box.max_x = x_coordinates[0]
        bounding_box.min_y = y_coordinates[0]
        bounding_box.max_y = y_coordinates[0]

    # Assume that the first number in the x-coordinate list is the 
    # largest and smallest
    min_x = x_coordinates[0]
    max_x = x_coordinates[0]

    # Assume that the first number in the y-coordinate list is the
    # largest and smallest
    min_y = y_coordinates[0]
    max_y = y_coordinates[0]

    # Find the minimum and maximum x-coordinate values
    for index, value in enumerate(x_coordinates):
        if ((not is_pose) or (is_pose and valid_body_part(index))) and (value != 0):
            if value < min_x:
                min_x = value

            if value > max_x:
                max_x = value

    # Find the minimum and maximum y-coordinate values
    for index, value in enumerate(y_coordinates):
        if ((not is_pose) or (is_pose and valid_body_part(index))) and (value != 0):
            if value < min_y:
                min_y = value

            if value > max_y:
                max_y = value

    # Compare the minimum and maximum x and y coordinate values with
    # BoundingBox's values
    if (min_x < bounding_box.min_x) and (min_x != 0):
        bounding_box.min_x = min_x

    if max_x > bounding_box.max_x:
        if max_x > width:
            bounding_box.max_x = width
        else:
            bounding_box.max_x = max_x

    if (min_y < bounding_box.min_y) and (min_y != 0):
        bounding_box.min_y = min_y

    if max_y > bounding_box.max_y:
        if max_y > height:
            bounding_box.max_y = height
        else:
            bounding_box.max_y = max_y

def get_average_coordinates(bounding_boxes, width, height):
    avg_min_x = 0
    avg_min_y = 0
    avg_max_x = 0
    avg_max_y = 0

    margin = 30

    for item in bounding_boxes:
        avg_min_x += item.min_x
        avg_min_y += item.min_y
        avg_max_x += item.max_x
        avg_max_y += item.max_y

    avg_min_x = round(avg_min_x / len(bounding_boxes))
    avg_min_y = round(avg_min_y / len(bounding_boxes))
    avg_max_x = round(avg_max_x / len(bounding_boxes))
    avg_max_y = round(avg_max_y / len(bounding_boxes))

    # Add left margin
    if avg_min_x >= margin:
        avg_min_x -= margin

    # Add top margin
    if avg_min_y >= margin:
        avg_min_y -= margin
    
    # Add right margin
    if (width - avg_max_x) >= margin:
        avg_max_x += margin

    return avg_min_x, avg_min_y, avg_max_x, avg_max_y

def generate_frames():
    json_dir = get_json_dir()
    positions = ['pose', 'face', 'hand_left', 'hand_right']
    frames = []

    # Iterate through all the .json folders in the json directory
    for folder in os.listdir(json_dir):
        folder_path = json_dir + '\\' + folder
        
        folder_name = os.path.splitext(folder)
        folder_name = folder_name[0]
        folder_name += '.avi'
        
        width = get_video_width(folder_name)
        height = get_video_height(folder_name)

        bounding_boxes = []

        f = Frame()

        # Iterate through all the .json files in a .json folder
        for file in os.listdir(folder_path):
            file_path = folder_path + '\\' + file

            bb = BoundingBox()

            # Read the json file and close properly once finished
            with open(file_path) as json_file:
                # Create a BoundingBox instance
                count = 0

                # Get the json object
                data = json.load(json_file)

                # Get the json data of the person
                person = data['people'][0]

                # Iterate through the openpose positions:
                # pose -> face -> left hand -> right hand
                for position in positions:
                    is_pose = True if position == 'pose' else False
                    position += '_keypoints_2d'
                    keypoints = person[position]
                    get_bounding_box(keypoints, bb, is_pose, count, width, height)
                    count += 1

            # After the file has been processed 
            bounding_boxes.append(bb)
            del bb

        avg_min_x, avg_min_y, avg_max_x, avg_max_y = get_average_coordinates(bounding_boxes, width, height)

        f.topLeft = (avg_min_x, avg_min_y)
        f.topRight = (avg_max_x, avg_min_y)
        f.bottomRight = (avg_max_x, avg_max_y)
        f.bottomLeft = (avg_min_x, avg_max_y)

        frames.append(f)
        del f

    return frames