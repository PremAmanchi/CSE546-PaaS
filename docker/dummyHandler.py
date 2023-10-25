from fileinput import filename
from boto3 import client as boto3_client
import face_recognition
import pickle
import urllib.parse
import boto3
import botocore
import os
import ffmpeg
import csv
from decimal import Decimal
from boto3.dynamodb.conditions import Attr

# Specify the directory paths
current_directory = os.getcwd()

print(current_directory)

# video_directory =  os.path.join(current_directory, "video")
video_directory =  current_directory + "/video/"

images_directory = current_directory + "/images/"

# Create the directories if they don't exist
os.makedirs(video_directory, exist_ok=True)
os.makedirs(images_directory, exist_ok=True)

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

table_name = 'Student-academic-records'
table = dynamodb.Table(table_name)


# Constants for your S3 bucket and object
input_bucket_name = 'paas-input-bucket-videos'
output_bucket_name = 'paas-output-bucket-results'
object_key = 'video.mp4'
input_path = '/Users/premkumaramanchi/CODE/DEV/CSE546-PaaS/AWS/'
images_path = '/Users/premkumaramanchi/CODE/DEV/CSE546-PaaS/AWS/output/'
encoding_file_path = '/Users/premkumaramanchi/CODE/DEV/CSE546-PaaS/docker/encoding.dat'

# Function to download the video from S3
def download_video_from_s3(bucket_name, object_key, destination_path):
    try:
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        data = response['Body'].read()
        with open(destination_path + object_key, 'wb') as f:
            f.write(data)
        s3.delete_object(Bucket=bucket_name, Key=object_key)
    except Exception as e:
        print(f'Error while downloading video from S3: {e}')

# Function to extract images from the video
def extract_images_from_video(video_path, image_output_path):
    try:
        os.system(f"ffmpeg -i {video_path} -r 1 {image_output_path}image-%3d.jpeg")
    except Exception as e:
        print(f'Error while extracting images: {e}')


# Process image and return result
def process_image(img_path):

    image_files = face_recognition.load_image_file(img_path)
    image_file_encoding = face_recognition.face_encodings(image_files)[0]

    # get known face encodings from file
    with open(encoding_file_path, 'rb') as f: 
        face_names_and_encoding = pickle.load(f)
        known_names = face_names_and_encoding['name']
        known_face_encodings = face_names_and_encoding['encoding']
    # compare known face with unknown face encodings
    result = face_recognition.compare_faces(known_face_encodings, image_file_encoding)
    for ans in result:
        if ans:
            index = result.index(ans)
            return (known_names[index])

def get_target_from_dynamodb(name):
        try:
            response = table.scan(FilterExpression=Attr('name').eq(name))
            items = response.get('Items', [])
            if items:
                return items[0]  # Assuming name is unique, so we return the first match
        except Exception as e:
            print(f"An error occurred while querying the table: {e}")
        return None

def create_csv_file(object_key, record):
    
    print("creating csv file")
    
    filename = object_key + record["name"] + ".csv"
    filepath = '/tmp/' + object_key + filename
    with open(filepath, 'w') as csvfile: 
        filewriter = csv.writer(csvfile, delimiter=',',
                            quoting=csv.QUOTE_MINIMAL)               
        filewriter.writerow(['Name','Major','Year'])
        filewriter.writerow([record['name'], record['major'], record['year']])

    print("upload file started")
    s3.upload_file(
                    Bucket = output_bucket_name,
                    Filename = filepath,
                    Key = filename
                )  
    print("upload file completed")      
    os.remove(filepath)  
    # return filename  



def face_recognition_handler(event, context):    
# def face_recognition_handler():    
    bucket = event['Records'][0]['s3']['bucket']['name']
    object_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    # bucket = input_bucket_name
    # object_key = "test_7.mp4"
    try : 
        download_video_from_s3(bucket, object_key, video_directory)

        extract_images_from_video(video_directory + object_key, images_directory)
    
        target_name = process_image(images_directory+ "image-002.jpeg")

        result = get_target_from_dynamodb(target_name)

        create_csv_file(object_key, result)

    except Exception as e :
        print(e)
        raise e


def main():

    # download_video_from_s3(input_bucket_name, object_key, input_path)

    # extract_images_from_video(input_path + 'test_1.mp4', images_path)
    
    # target_name = process_image(images_path+"image-002.jpeg")

    # result = get_target_from_dynamodb(target_name)

    # create_csv_file(result)

    face_recognition_handler()

if __name__ == "__main__":
    main()
