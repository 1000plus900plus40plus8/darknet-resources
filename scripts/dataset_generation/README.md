# dataset_generation 

This script is used for generating a data set, including the images and text files in the darknet format. 

The generated images contain one of the following shapes:
* square
* rectangle
* circle
* ellipses
* line
* arrow
* triangle

For each image generation iteration, We select two random colors. The first color is used for our background and the second color is used for the shape which is randomly placed on the image. 

Our shapes are given a random size to diversify the data set. 

We generate 15 images of each shape and save them in a folder whose name is the background color. 

At the moment only images with one shape are generated. 

# Improvements to be made:

* Generate multiple shapes per image. 

* Generate images of more than one size. 

* Add rotation to shapes. 

* Add more shapes. 

* Add unit tests.
