# Titration Analysis using colorimetrics and alarm to indicate process completion

Colorimetric involves analyzing the color of a portion in an image. In current example titrant is being added to an analyte

[![Watch the video](https://img.youtube.com/vi/NLSY5S8CABk/maxresdefault.jpg)](https://youtu.be/NLSY5S8CABk)
Source: DataCarpentry Colorimetrics Challenge

We use image processing to look at the color of the solution and determine when the titration is complete. The program uses Python3 and OpenCV to analyze video on a frame-by-frame basis. Sample an image kernel from the same location on each frame and determine the average red, green, and blue channel values.  

The graph shows how the three component colors (red, green, and blue) of the solution change over time; the difference in the solution’s color can be used to activate an alarm.

![Colorimetrics Graph](output/titration.png?raw=true "Output Graph")

A similar video analytics code can be written to analyze other industrial processes or do quality control on an assembly line.