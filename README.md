# Forza Self Driving
This is an experiment to see how well I can make a self-driving car with hard-coded algorithms (no machine learning).
Forza Horizon 4 is the game this is being tested on. Currently still in development.

## Image Processing
Screen is captured in real time and the goal is to extract the two main lane lines. The process used is described
as follows:
* Convert to greyscale to save processing time and space. There is no need for color here.
* Apply Canny edge detection to image to extract the edges. The main goal here is to remove as much
noise as possible, while ensuring the main lane lines do not get lost.
* Apply a mask to region where sky and car is expected, because we don't want the horizon line or car lines
 interfering with the detection of the lane lines.
 * Apply a blur to smooth remaining lines out so jagged lane lines will be easier to detect.
 
 The image at this stage has gone through all the pre-processing and now algorithms will be applied onto it.
 
 ## Line detection
 The main assumption is that lane lines are for the most part locally straight. So we can use a hough transform to try and 
 detect them. The full process is:
 * Apply Hough Transform on the image. In the perfect world,this would only detect the two lane lines, however
 there will usually be noise that interferes and the lane lines for a bend on the road are not exactly straight.
    * Instead the Hough Transform is used to detect **LOCALLY** straight lines. This results in a lot of shorter lines as shown below.
* Group these shorter lines if their **positions** and **slopes** are close enough to neighbouring ones.
* Then take the 2 groups that have the most sub-lines in them and have different signed slopes. We know the two lane 
lines cannot have the same signed slope due to perspective.
    * This step relies on the fact that the pre-processing of the image removes any lines that could be more prominent than
    the two lane lines.
    
## Driving algorithms
There are two methodologies used here.

1. Try to keep the middle of the screen (x-coordinate) aligned with the intersection of the two lane lines (x-coordinate).
    * This method works best when the pre-processing of the image is perfect and there is no noise being detected
    as a lane line. If noise is detected, it may cause the intersection of the two lines to be wildly inaccurate 
    resulting in a huge unwanted over-correction.
2. Try to keep the middle of the screen equidistant from the two lane lines.
    * This method works better overall, but is less responsive to sharper turns. Since the difference in distance
    between a straight road and a turn isn't huge, this usually will not result in large responses from the driving algorithm.

## Video Demonstration of Current Progress
Below is a video showcasing the real time processing of the screen. All driving is done automatically except when manual adjustment needs
to be made to get car back on road.

[![Demo](https://i.ytimg.com/vi/Nhu4X4QFcHM/hqdefault.jpg?sqp=-oaymwEbCKgBEF5IVfKriqkDDggBFQAAiEIYAXABwAEG\u0026rs=AOn4CLDP87qNENayviyuhwZgZBBjBJkBNg")](http://www.youtube.com/watch?v=Nhu4X4QFcHM)

## Future improvements
1. Pre-processing of image is not always perfect. Will need better methods to remove noise while preserving lane lines.
2. Driving algorithms fail when only one lane line is detected. Should add smarter logic to fix this.
    * Maybe have a default lane line that gets used if one can't be detected.
