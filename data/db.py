import boto3

# Define your data
data = [
    {
        "id": 1,
        "name": "mr_bean",
        "major": "lawyer",
        "year": "freshman"
    },
    {
        "id": 2,
        "name": "president_biden",
        "major": "history",
        "year": "sophomore"
    },
    {
        "id": 3,
        "name": "vin_diesel",
        "major": "computer_science",
        "year": "sophomore"
    },
    {
        "id": 4,
        "name": "floki",
        "major": "history",
        "year": "junior"
    },
    {
        "id": 5,
        "name": "president_trump",
        "major": "physics",
        "year": "junior"
    },
    {
        "id": 6,
        "name": "morgan_freeman",
        "major": "math",
        "year": "senior"
    },
    {
        "id": 7,
        "name": "president_obama",
        "major": "electrical_engineering",
        "year": "senior"
    },
    {
        "id": 8,
        "name": "johnny_dep",
        "major": "computer_science",
        "year": "senior"
    }
]

# Initialize the DynamoDB client
dynamodb = boto3.client('dynamodb')

# Specify the name of your DynamoDB table
table_name = 'student-academic-records'

# Iterate through the data and put items into the DynamoDB table
for item in data:
    response = dynamodb.put_item(
        TableName=table_name,
        Item={
            'id': {'N': str(item['id'])},
            'name': {'S': item['name']},
            'major': {'S': item['major']},
            'year': {'S': item['year']}
        }
    )

    # Print the response to verify the operation was successful
    print(f"Uploaded item {item['id']} - {item['name']}")

print("Data upload completed.")
