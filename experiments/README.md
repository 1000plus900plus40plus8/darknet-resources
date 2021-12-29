# Darknet training experiments. 

**Can darknet training, be improved using transfer learning?**

For instance if I train a network with six classes, and I want to add a seventh class, Is it beneficial to start with the weights from my network that has six classes? 

**For a network that has many classes how many images are required for each one?** 

For instance, for a network that has 20 classes, Is there any benefit to have 5,000 images of each class versus 500? 

From a training perspective, the more images you have in your data set, the longer it will take for darknet to run the map calculations. However, if we have a smaller data set map calculations are run more frequently. 

In certain circumstances when you have many images, you may reach a few thousand iterations without running any map calculations. 

And given the darknet's tendency to randomly crash. This can result in wasted computing time. 

**What is more beneficial for training? What is more effective for training?** 
