import coordinates
import extract_video

def main():
    frames = coordinates.generate_frames()
    extract_video.generate_cropped_video(frames)
    extract_video.convert_to_mp4()

if __name__ == '__main__':
    main()