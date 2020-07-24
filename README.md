# opencv-extract-signer

### Explanation of .gitignore
In the .gitignore, I am ignoring all files within ```\opencv```, ```\openpose_output\videos```, and ```\openpose_output\json``` with an exception. The exception is that any .gitkeep file will not be ignored. This is done so that I can upload the empty folders to GitHub, which the script requires. **Before running the script**, be sure to delete the .gitkeep files from the 3 directories, otherwise the script won't work.