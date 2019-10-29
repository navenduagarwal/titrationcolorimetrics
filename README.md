# Titration Analysis using colorimetrics and alarm to indicate process completion

Colorimetrics involve analyzing the color of portion in an image. In current example titrant is being added to an analyte

[![Watch the video](https://img.youtube.com/vi/NLSY5S8CABk/maxresdefault.jpg)](https://youtu.be/NLSY5S8CABk)
Source: DataCarpentry Colorimetrics Challenge

We use image processing to look at the color of the solution, and determine when the titration is complete. Program uses Python3 and OpenCV to analyze video on a frame-by-frame basis. Sample a image kernel from the same location on each frame and determine the average red, green and blue channel value.  

The graph shows how the three component colors (red, green, and blue) of the solution change over time; the change in the solution’s color can be used to activate an alarm.

![Colorimetrics Graph](output/titration.png?raw=true "Output Graph")
