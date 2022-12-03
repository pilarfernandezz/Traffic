https://cs50.harvard.edu/ai/2020/projects/5/traffic/



#Experiementation Process
By reducing the pool size from (3,3) to the (2,2) on the max poll layer, I've noticed that there was a slight increse in the duration of execution and decrease in the final accuracy.

By reducing the pool size from (3,3) to the (2,2) on the convolution layer, I've noticed that there was a considerable decrease in the final accuracy.

By adding new layers of max polling and convolution layer, I've noticed that was also decrease in the final accuracy.

I've noticed that adding hidden layers was increasing the final accuracy until reached 3 layers, after that number, the accuracy did not changed as much.

I've noticed that adding dropouts biggr 0.2 was decreasing the accuracy, and also adding a dropout of 0.1 in all the 3 hidden layers. The better results were with a 0,1 dropout in the just the 2 first layers.
