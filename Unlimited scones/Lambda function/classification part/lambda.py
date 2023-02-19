import json
import sagemaker
import base64
from sagemaker.serializers import IdentitySerializer


# Fill this in with the name of your deployed model
ENDPOINT = 'image-classification-2022-10-31-11-50-58-625'
runtime= boto3.client('runtime.sagemaker')


def lambda_handler(event, context):

    # Decode the image data
    image = base64.b64decode(event["image_data"]

    # Instantiate a Predictor
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME, ContentType='image/png', Body=image)
    
    
    # Make a prediction:
    inferences = json.loads(response['Body'].read())
    
    # We return the data back to the Step Function    
    event["inferences"] = inferences.decode('utf-8')
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }
    
    