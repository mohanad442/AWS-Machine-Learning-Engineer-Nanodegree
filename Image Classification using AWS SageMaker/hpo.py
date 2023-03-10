
#TODO: Import your dependencies.
#For instance, below are some dependencies you might need if you are using Pytorch
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.models as models
import torchvision.transforms as transforms
from torchvision import datasets, transforms, models
from collections import OrderedDict
import argparse
import os
import logging
import sys
from tqdm import tqdm
from PIL import ImageFile


ImageFile.LOAD_TRUNCATED_IMAGES = True
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

def test(model, test_loader, criterion, device):
    model.eval()        # for testing using evalualion function
    running_loss=0      # assign running loss
    running_corrects=0  # assign running corrects
    
    for inputs, labels in test_loader:
        inputs = inputs.to(device)
        labels = labels.to(device)
        outputs=model(inputs)
        loss=criterion(outputs, labels)
        _, preds = torch.max(outputs, 1)
        running_loss += loss.item() * inputs.size(0)            # calculate running loss
        running_corrects += torch.sum(preds == labels.data)     # calculate running corrects

    total_loss = running_loss // len(test_loader)       
    total_acc = running_corrects.double() // len(test_loader)
    
    logger.info(f"Testing Loss: {total_loss}")
    logger.info(f"Testing Accuracy: {total_acc}") # print the loss and accuracy values
    

def train(model, train_loader, validation_loader, loss_criterion, optimizer, device):
    loss_counter=0
    best_loss=1e6
    epochs = 50
    image_dataset={'train':train_loader, 'valid':validation_loader}
    
    for epoch in range(epochs):
        logger.info(f"Epoch:{epoch}")
        for phase in ['train', 'valid']:
            if phase == 'train':
                model.train()
            else:
                model.eval()
            running_loss = 0.0
            running_corrects = 0
            
            for inputs, labels in image_dataset[phase]:
                inputs = inputs.to(device)
                labels = labels.to(device)
                outputs = model(inputs)
                loss = loss_criterion(outputs, labels)
                
                if phase == 'train':
                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()
                
                _, preds = torch.max(outputs, 1)
                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)
                
            epoch_loss = running_loss // len(image_dataset[phase])
            epoch_acc = running_corrects // len(image_dataset[phase])
            
            if phase=='valid':
                if epoch_loss<best_loss:
                    best_loss=epoch_loss
                else:
                    loss_counter+=1
            
            logger.info('{} loss: {:.4f}, acc: {:.4f}, best loss: {:.4f}'.format(phase,
                                                                                 epoch_loss,
                                                                                 epoch_acc,
                                                                                 best_loss))
        if loss_counter==1:
            break
        if epoch==0:
            break
    return model
    
def net():

    model = models.resnet34(pretrained=True) # using the pretrained resnet34 model with 34 layers

    for param in model.parameters():
        param.requires_grad = False # freeze the model
        nfeatures = model.fc.in_features
    model.fc = nn.Sequential(
                   nn.Linear(nfeatures, 512),
                   nn.ReLU(inplace = True),
                   nn.Linear(512, 256), # adding own NN layers to the output of the pretrained model
                   nn.ReLU(inplace=True),
                   nn.Linear(256, 133)) # output should be 133 as we have 133 classes of dog breeds

     
    return model

def create_data_loaders(data, batch_size):
    
    train_data_path = os.path.join(data, 'train') # Calling OS Environment variable and split it into 3 sets
    test_data_path = os.path.join(data, 'test')
    validation_data_path=os.path.join(data, 'valid')
    
    train_transform = transforms.Compose([
        transforms.RandomResizedCrop((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        ]) # transforming the training image data
                                                            
    test_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        ]) # transforming the testing image data

    # loading train,test & validation data from S3 location using torchvision datasets' Imagefolder function
    train_data = torchvision.datasets.ImageFolder(root=train_data_path, transform=train_transform)
    train_data_loader = torch.utils.data.DataLoader(train_data, batch_size=batch_size, shuffle=True)

    test_data = torchvision.datasets.ImageFolder(root=test_data_path, transform=test_transform)
    test_data_loader  = torch.utils.data.DataLoader(test_data, batch_size=batch_size)

    validation_data = torchvision.datasets.ImageFolder(root=validation_data_path, transform=test_transform)
    validation_data_loader  = torch.utils.data.DataLoader(validation_data, batch_size=batch_size) 
    
    return train_data_loader, test_data_loader, validation_data_loader

def main(args): # args to use with jypyter notebook's Estimater function
    
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"Running on Device {device}")
    logger.info(f'Hyperparameters are LR: {args.lr}, Batch Size: {args.batch_size}')
    logger.info(f'Data Paths: {args.data}')
    train_loader, test_loader, validation_loader=create_data_loaders(args.data, args.batch_size)
   
    model=net() # Initialize a model by calling the net function
    model=model.to(device)
    loss_criterion = nn.CrossEntropyLoss(ignore_index=133) # using cross Entropy loss function
    optimizer = optim.Adam(model.fc.parameters(), lr=args.lr) #using adam optimizer
    
    logger.info("Start Model Training")
    model=train(model, train_loader, validation_loader, loss_criterion, optimizer, device) # calling the train function to start the training
    
    logger.info("Testing Model")
    test(model, test_loader, loss_criterion, device) # testing model
    

    logger.info("Saving Model")
    torch.save(model.state_dict(), os.path.join(args.model_dir, "model.pth"))
    logger.info('Model Saved!')# save the trained model to S3

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser() # adding the args parsers to use with the notebook estimator call

    
    parser.add_argument(
        "--batch-size",
        type = int,
        default = 64,
        metavar = "N",
        help = "input batch size for training (default: 64)",
    )
    
    parser.add_argument(
        "--lr", 
        type = float, 
        default = 0.1, 
        metavar = "LR", 
        help = "learning rate (default: 1.0)"
    )
    # Using sagemaker OS Environ's channels to locate the training data, model dir and output dir to save in S3 bucket.
    parser.add_argument('--data-dir', type=str, default=os.environ['SM_CHANNEL_TRAIN'])
    parser.add_argument('--model_dir', type=str, default=os.environ['SM_MODEL_DIR'])
    parser.add_argument('--output_dir', type=str, default=os.environ['SM_OUTPUT_DATA_DIR'])
    
    args = parser.parse_args()
    print(args)
    main(args)