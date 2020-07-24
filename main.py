import coordinates
import crop_video

def main():
    frames = coordinates.generate_frames()
    crop_video.generate_cropped_video(frames)

if __name__ == '__main__':
    main()