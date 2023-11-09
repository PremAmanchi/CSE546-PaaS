import boto3
import csv
import glob
# Replace with the directory where you want to save the files
local_directory = '/Users/premkumaramanchi/CODE/PROJECTS/ACADEMIC/CSE546-PaaS/load-generator/results/'
bucket_name = 'cse546-paas-output-bucket-results'
# Create an S3 client
s3 = boto3.client('s3')

# List objects in the bucket
paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=bucket_name)

# Counter to keep track of the number of files downloaded
download_count = 0

# Iterate over objects in the bucket
for page in pages:
    if 'Contents' in page:
        for obj in page['Contents']:
            if download_count < 100:
                key = obj['Key']
                local_file_name = f"{local_directory}/{key}"
                try:
                    s3.download_file(bucket_name, key, local_file_name)
                    print(
                        f"File {key} downloaded to {local_file_name} successfully.")
                    download_count += 1
                except Exception as e:
                    print(f"An error occurred while downloading {key}: {e}")
            else:
                break  # Exit the loop once 100 files have been downloaded

count = 0
file_path = 'mapping'  # Replace with the actual file path
try:
    with open(file_path, 'r') as file:
        for line in file:
            print(line, end='')
            print(type(line))
            for l in line.split('\n'):
                if ':' in l:
                    key, value = l.split(':')
                    print(f"Key: {key}, Value: {value}")
                    dir_path = 'videos'
                    key = key+"_.csv"
                    path = dir_path+"/"+key
                    print(path)
                    with open(path, mode='r') as file:
                        reader = csv.reader(file)
                        next(reader)
                        for row in reader:
                            print(row)
                            print(row[1])
                            val1, val2 = value.split(',')
                            print(val1, val2)
                            if val1 == row[1] and val2 == row[2]:
                                count += 1
except FileNotFoundError:
    print(f"The file {file_path} does not exist.")
except IOError:
    print(f"An error occurred while reading the file {file_path}.")
except:
    print("An unknown error occurred.")


print(count)


# Replace 'file_paths' with a list of file paths
# dir_paths = 'videos/*.csv'
# file_paths  = glob.glob(dir_paths)

# for path in file_paths:
#     with open(path, mode='r') as file:
#         print(file)
#         reader = csv.reader(file)
#         for row in reader:
#             print(row)
