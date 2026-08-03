AUTO HUD Display Validation 

This project is aimed to validate aircraft displays witho ut the need of manual approval on Avionics Test Stations. Utilizing Python libraries such as OpenCV for image processing and computer vision. 


Milestone 1 -- Basic Image Matching 

In this milestone, we will be using a sample image that will contain a few elements. We will also make false versions of the image that wont contain certain elements. 

Acceptance Criteria: The software rejects the false images, and accepts the only good one. 


Status: Passed Milestone Complete 

Testing Note: Tested with basic shapes, each 'bad' image is missing a shape. When testing each one failed when matching it with the 'good' image. 


Milestone 2 -- OpenCV Frame Capture 

In this milestone we will test OpenCV capabilities for frame capturing. Using a mp4 video we want to ensure that OpenCV can reliably read the video.

Acceptance Criteria: Can reliably load the video, inspect properties, and step through frames. 

Will be seperated into 5 tests for complete acceptance

Test 1 - Video Properties
Status: Passed

Test 2 - Plays the video frame by frame 
Status: Passed 

Test 3 - Print Frame Numbers 
Status: Passed 

Test 4 - Save Specific Frames 
Status: Passed

Test 5 - Sample every n frames 
Status: Passed

Status: Passed Milestone Complete 



Milestone 3 -- Simple Video Frame Comparison

For this milestone we will have an image in which we know is correct aka "The golden Image". During testing it will capture one out of every 20 frames to compare. Now we will compare the Golden image vs. the captured frame, utilizing the basic image matching from milestone 1. 

Test Description: To test this we will construct a basic structure for the golden image with just a few shapes. Then a video will be taken of the image within paint, and in a certain time period of the video some objects may be missing. 

Test 1 -- First 5 seconds good, rest of video invalid

Status: (INCOMPLETE) Left off with issues with files needing the same dimensions. 
