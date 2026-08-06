Automated Visual Regression Testing System Architecture 


There are two 


Validation is broken down into two different categories ​‌


Static Validation ​‌
1. Displays populate correctly ​‌
2. No missing elements/shapes​‌
3. No corruption/artifacts ​‌

Dynamic Validation ​‌
1. Dispays behave correctly over time ​‌
- Rotates CCW ​‌
- Animates correctly ​‌



Static Validation Architecture 

Golden Image Comparison 

Golden Frame
      ↓
Current Frame
      ↓
SSIM / Difference Analysis

Dynamic Validation Architecture 
1. Find Center of the object 
2. Identify a distinct rotating feature (Visual element)
3. Measure Angular Position and compare over each frame 


What is SSIM (Structural Similarity Index Measure) / Difference Analysis? 

For each small window of the image (Typically 11 x 11 pixels) SSIM computes: 

1. Luminance Comparison 

Image A mean = 120
Image B mean = 121

Very Similar -> High Score 

2. Contrast Comparison 
(Are the variations in brightness similar?)

A: Dark and bright areas vary a lot
B: Darl and bright areas vary a lot 

High Score

3. Structure Comparison 
(Do the edges and patterns line up?)

A: Circle 
B: Circle 

High Score 

But 

A: Circle 
B: Square 

Lower Score 

SSIM Formula 

SSIM = Luminance * Contrast * Structure (No given weights)

Notice: SSIM may give small differences in score even if a shape is missing, because it may effect only a small part of the frame when you are dealing with 
large windows. 


SSIM Data analysis 

After SSIM is collected for each sampled n frame. We will then take the average, min, and max of the data. 

For the figure being analyzed an accetpable threshold must be made. This threshold will will represent the minimum acceptable average SSIM percentage over all of the n samples frames. An important note, is that each figure may be different, and there cannot be one standardized acceptable value. 