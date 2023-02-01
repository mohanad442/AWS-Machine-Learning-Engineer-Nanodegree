# Image Classification using AWS SageMaker

Use AWS Sagemaker to train a pretrained model that can perform image classification by using the Sagemaker profiling, debugger, hyperparameter tuning and other good ML engineering practices. This can be done on either the provided dog breed classication data set or one of your choice.

## Project Set Up and Installation
Enter AWS through the gateway in the course and open SageMaker Studio. 
Download the starter files.
Download/Make the dataset available. 

## Dataset
The provided dataset is the dogbreed classification dataset which can be found in the classroom.
The project is designed to be dataset independent so if there is a dataset that is more interesting or relevant to your work, you are welcome to use it to complete the project.

### Access
Upload the data to an S3 bucket through the AWS Gateway so that SageMaker has access to the data. 

## Hyperparameter Tuning
What kind of model did you choose for this experiment and why? Give an overview of the types of parameters and their ranges used for the hyperparameter search

I used Resnet50 as it is a pretrained model so i can use transfer learning, I specified the learning rate range (0.001 - 0.1) and the batch sizes [32, 64, 128].

Remember that your README should:
- Include a screenshot of completed training jobs
![training job.png](https://github.com/mohanad442/AWS-Machine-Learning-Engineer-Nanodegree/blob/main/Image%20Classification%20using%20AWS%20SageMaker/training%20job.PNG)

- Logs metrics during the training process
Done in the main script

- Tune at least two hyperparameters
learning rate range (0.001 - 0.1) and the batch sizes [32, 64, 128].

- Retrieve the best best hyperparameters from all your training jobs
best hyperparameters : batch size = 32, learning rate = 0.006272548584758591

## Debugging and Profiling
**TODO**: Give an overview of how you performed model debugging and profiling in Sagemaker

install smdebug package in sagemaker and many other dependances.
Using the best hyperparameters, create and finetune a new model
Set up debugging and profiling rules and hooks and configurations.
Create and fit an estimator on the data.


### Results
**TODO**: What are the results/insights did you get by profiling/debugging your model?

The model was overfitting, maybe it needs more hyperparameter tuning
The step duration for forward and backward pass should be roughly the same throughout the training.
the data I/O wait time is high and the GPU utilization is low. It might indicate IO bottlenecks where GPU is waiting for data to arrive from storage.
The batch size is too small


**TODO** Remember to provide the profiler html/pdf file in your submission.
Done


## Model Deployment
**TODO**: Give an overview of the deployed model and instructions on how to query the endpoint with a sample input.

from PIL import Image
import io
with open("./test.jpg", "rb") as f:
    payload = f.read()
    
type(payload)

response=predictor.predict(payload, initial_args={"ContentType": "image/jpeg"})
response

**TODO** Remember to provide a screenshot of the deployed active endpoint in Sagemaker.

![endpoint](https://github.com/mohanad442/AWS-Machine-Learning-Engineer-Nanodegree/blob/main/Image%20Classification%20using%20AWS%20SageMaker/endpoint.PNG)

## Standout Suggestions
**TODO (Optional):** This is where you can provide information about any standout suggestions that you have attempted.
