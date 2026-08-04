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

T1 - Frames 20, 40, 60, 80, 100, 120, 140 Valid; Rest invalid (Accaptance tolerance at >= 95%)

Status: Failed (Exception)

Notice: We learned that the structural part of SSIM can give small variations in the score, because it takes small snippets of the large frame. 
So even if a shape is missing we can still get a high score, but varies smally. In this case it was about 0.7%, so we adjusted the acceptance tolerance for test 2. Since T2 passed succesfully this test is given an exception. 

T2 - Frames 20, 40, 60, 80, 100, 120, 140 Valid; Rest invalid (Now with acceptance tolerance at >= 98.3%)

Status: Passed

Status: Passed Milestone Complete


Milestone 4 -- Detecting Rotational Motion on simple BFD Display

For this milestone the goal is to succesfully detect rotational motion types, such as Clockwise, and counterclockwise. Additionally, we will need to make sure that when no motion occurs the system doesn't report motion. 

For testing this will be broken down into 3 tests. 

T1 - Correctly Detects CCW Motion 

Status: Passed 

T2 - Rejects CW video for CCW movement 

Status: Passed 

T3 - Rejects no motion video for CCW movement

Status: Passed 

Notice: It took some digging but, it is important to have a distinct object. In this case it was a green arrow, and we also had to choose the farthest green contour from the center, as the center axis is also green. 

Status: Passed Milestone Complete 


Milestone 5 - BFD Detecting Rotational motion an video frame comparison (Dynamic and static validation all in one)

For this milestone we are wanting to bring milestone 4, and 3 all in one. So that we can validate movement on the displayed image, and we can also ensure the image matches as intended. 