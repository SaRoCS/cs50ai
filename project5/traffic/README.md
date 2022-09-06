To find the best model for this problem, I first chose starting
layers and values according to those given in the handwriting example.
My idea was to run tests altering each factor by either increasing or decreasing
it and seeing how that affected the accuracy and speed. The first parameter I tested was kernel size.
The starting size was three by three, so I tested a five by five kernel. This greatly improved the accuracy,
so I tried a seven by seven kernel. A seven by seven kernel decreased accuracy while also making the training
process slower. Next I tested pool size. A four by four pool size only slightly decreased accuracy, but greatly
improved speed. A six by six pool decreased accuracy again but did not affect speed. In testing pool size,
I noticed that the larger the pool size the wider the range of accuracy. For the number of convolution filters
I tested 16 and 64. Sixteen filters decreased accuracy and increased speed, and 64 filters only decreased speed.
The final basic test in the convolution and pooling step was the number of layers. Two set of convolution and
pooling greatly increased accuracy while only minimally decreasing speed. Three sets had little added benefits.
Using two sets on convolution and pooling, I started incorporating different kernel and pool size. A five, two
to a three, two merely decreased speed, and a five, four to a three, two decreased accuracy. A single five, four layer
also had decreaed accuracy, and a five, four to a five, two tremendously decreased accuracy.  I finally decided on
a kernel size of five, pool size of four, then a kernel size of three as the best balance between speed and accuracy.

The next step was to test amount and size of hidden layers and dropout. Two hidden layers increased accuracy without
affecting speed and three hidden layers further increased accuracy with only minimal decrease in speed. 64 and 96 units
in a layer decreased speed and accuracy, while 256 improved accuracy.  With hidden layers I observed that more units is
better if speed is not required. Testing various combinations of layer sizes (256:96:128, 1024:512:256, 512:512:256, etc.)
I chose 512:512:256 for its speed and accuracy. Finally, I tested dropout. 0.75 dropout decreased accuracy and 0.25 dropout
decreased speed so I kept the dropout at 0.5. All of these parameters left me with a model that on average had an accuracy
of around 95 percent while taking around twelve seconds each epoch.