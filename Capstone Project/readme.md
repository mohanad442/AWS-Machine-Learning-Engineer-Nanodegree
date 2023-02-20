# Amazon Inventory Reconciliation Using AI

Inventory management is critical to Amazon's success. Thus, the need arises to apply artificial intelligence to assure the correctness of deliveries.
Amazon Fulfillment Centers are bustling hubs of innovation that allow Amazon to deliver millions of products to over 100 countries worldwide. These products are randomly placed in bins, which are carried by robots.
Occasionally, items are misplaced while being handled, resulting in a mismatch: the recorded bin inventory, versus its actual content.
The project predicts the number of items in a bin, thus detecting any inventory variance. By correcting variance upon detection, Amazon will better serve its customers.will better serve its customers.


## Project Set Up and Installation
For this project, it is highly recommended to use Sagemaker Studio from the course provided AWS workspace. This will simplify much of the installation needed to get started.

For local development, you will need to setup a jupyter lab instance.

Follow the jupyter install link for best practices to install and start a jupyter lab instance.
If you have a python virtual environment already installed you can just pip install it.


## Dataset

![classes.png](https://github.com/mohanad442/AWS-Machine-Learning-Engineer-Nanodegree/blob/main/Capstone%20Project/classes.png)

### Overview
Amazon has made public the Bin Image Dataset. It contains images and metadata from bins of a pod in an operating Amazon Fulfillment
Center. The bin images in this dataset are captured as robot units carrying pods as part of normal operations. The Bin Image dataset provides the metadata for each image from where the number of items in the bin can be derived.

### Access

To download data using the AWS Command Line Interface, you can use the "cp" command. For instance, the following command will copy the image named 523.jpg to your local directory:

aws s3 cp s3://aft-vbi-pds/bin-images/523.jpg 523.jpg

## Model Training
I used Resnet 50 pre-trained model for feature extractions from our images data by freezing all the weights of the neural network and only changing the classification layer so the model only needs to train these weights at the last classification layer, I used a learning rate of 0.001, batch size 32, with 50 epochs and the loss function was categorical cross entropy for 5 classes.

### Model Evaluation:
The accuracy of the benchmark model chosen is 53.8 %, the experiment model didn’t achieve the results of the Benchmark because of it trained on a small part of the data so we can download the whole data to get more accuracy.

![loss.png](https://github.com/mohanad442/AWS-Machine-Learning-Engineer-Nanodegree/blob/main/Capstone%20Project/Loss.png)

### Hyperparameters

The following hyper-parameters are identified for tunning.
1. Learning Rate
2. Batch Size
3. Epoch
The Learning rate for the Adam optimizer is identified as one of the hyper-parameters which could help improve the training process rather than the predefined default.
Batch Size could help us optimize the computation speed and convergence.
The Number of Epochs could help the model to better train the model over a long time and different possibilities can be checked for tunning.
For the experiment, 5 Jobs are created for the tunning and one among them is chosen based on the results i.e., objective metric.

![hyperparameter.png](https://github.com/mohanad442/AWS-Machine-Learning-Engineer-Nanodegree/blob/main/Capstone%20Project/hyperparameter.PNG)

## Machine Learning Pipeline
![pipeline.png](https://github.com/mohanad442/AWS-Machine-Learning-Engineer-Nanodegree/blob/main/Capstone%20Project/manual-pipeline.png)