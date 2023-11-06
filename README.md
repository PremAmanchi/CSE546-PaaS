# CSE546 PaaS Project Report 📚

## Team
- Prem Kumar Amanchi (Email: pamanchi@asu.edu, ASUID: 1224421289) 🧑‍💼
- Manohar Veeravalli (Email: mveerava@asu.edu, ASUID: 1225551522) 🧑‍💼
- Sudhanva Moudgalya (Email: srmoudga@asu.edu, ASUID: 1219654267) 🧑‍💼

## Table of Contents 📜
1. [Problem Statement](#problem-statement) 🎯
2. [Design and Implementation](#design-and-implementation) 🛠️
    - [Architecture](#architecture) 🏛️
    - [AutoScaling](#autoscaling) ⚖️
    - [Member Tasks](#member-tasks) 👥
3. [Testing and Evaluation](#testing-and-evaluation) 🧪
4. [Code](#code) 📝
5. [Setup](#setup) 🚀

## Problem Statement 🎯
The project's goal is to leverage AWS Lambda for image recognition within video files. Users initiate the process by uploading video files to the designated S3 input bucket. The Lambda function is triggered, extracting frames from the video and performing image recognition. The recognized images are cross-referenced with student data stored in DynamoDB, and the results are stored in a CSV file in an output S3 bucket. The final output provides educators with insights into their classrooms.

## Design and Implementation 🛠️
### Architecture 🏛️
![Architecture](architecture.png)
- Users upload videos to an S3 input bucket.
- AWS Lambda, containerized within a Docker image, processes the video and extracts frames.
- Image recognition is performed on the first frame.
- Student data is fetched from DynamoDB for matched images.
- The results are stored as CSV files in an output S3 bucket.

### AutoScaling ⚖️
The application utilizes Platform as a Service (PaaS) in conjunction with AWS Lambda for dynamic scaling. AWS manages the auto-scaling, allowing efficient responses to real-time demands.

### Member Tasks 👥
- **Prem Kumar Amanchi**
    - Deployed the container image in Lambda.
    - Created the face recognition module in handler.py.
    - Assigned a role to the Lambda function.
- **Manohar Veeravalli**
    - Built and uploaded the Docker image to AWS ECR.
    - Uploaded the dataset into DynamoDB.
    - Implemented data extraction from DynamoDB.
- **Sudhanva Moudgalya**
    - Created S3 buckets in AWS for data storage.
    - Assisted in video retrieval and CSV file upload.
    - Created a DynamoDB table to store relevant data.

## Testing and Evaluation 🧪
The application was tested by uploading a single video file to the S3 input bucket. Custom logs were used to monitor the workflow. Additional testing involved using a workload generator to upload test video files.

## Code 📝
The project's code, located in the `handler.py` file, contains the following functions:
- `download_video_from_s3`: Downloads a video from an S3 bucket.
- `extract_images_from_video`: Extracts images from a video using FFmpeg.
- `process_image`: Processes an image for face recognition.
- `get_target_from_dynamodb`: Retrieves data from DynamoDB.
- `create_csv_file`: Creates a CSV file with academic records.
- `face_recognition_handler`: The main Lambda function for processing facial recognition.

## Setup 🚀
### Cloning the Repository
To get started, clone the GitHub repository for the project to your local machine using the following terminal command:
```bash
git clone https://github.com/PremAmanchi/CSE546-PaaS


## Building and Pushing Docker Image
1. Navigate to the "docker" directory within the cloned repository.
2. Build and push the Docker image to Amazon Elastic Container Registry (ECR) using the provided commands.

## Setting Up AWS Resources
1. Create an S3 input bucket named "cse546-paas-input-bucket-videos."
2. Create an S3 output bucket named "cse546-paas-output-bucket-results."
3. Create a DynamoDB table named "student-academic-records" and load the "student_data.json" file into this table.

## Creating an AWS Lambda Function
1. Create an AWS Lambda function using the Docker image from ECR.
2. Set the trigger point to the S3 input bucket.
3. Adjust memory and timeout settings.

## Executing the Workload Generator
1. Use the workload generator tool to upload video files to the S3 input bucket.

## AWS Lambda Function Processing
1. The AWS Lambda function will process images, run the face-recognition module, and store student details in a CSV file in the S3 output bucket.

By following these setup instructions, you can configure the system, build and deploy the Docker image, and run the code to process videos and recognize students' faces.

I hope you find this README informative and engaging! 🚀📚
