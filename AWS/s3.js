// Import necessary AWS SDK components
const AWS = require("aws-sdk");
const fs = require("fs");

// Initialize AWS configuration with your credentials
AWS.config.update({
  accessKeyId: "AKIAZYSJTIT5ZDN5PQX4",
  secretAccessKey: "qQ38D5mGLURJ6JzwglDbn2Ru6ShexoFklj8EKbpR",
  region: "us-east-1",
});

// Create an S3 instance
const s3 = new AWS.S3();

// Define your S3 bucket name and the file path on your local machine
const bucketName = "paas-input-bucket-videos";
const filePath =
    "/Users/premkumaramanchi/CODE/DEV/CSE546-PaaS/data/test_cases/test_case_1/test_0.mp4"; // Update with your local video file path
const key = "video.mp4"; // The name under which the file will be stored on S3

// Read the video file from your local file system
const fileContent = fs.readFileSync(filePath);

// Set S3 parameters
const params = {
  Bucket: bucketName,
  Key: key,
  Body: fileContent,
};

// Upload the video to S3
s3.upload(params, (err, data) => {
  if (err) {
    console.error("Error uploading:", err);
  } else {
    console.log("Video uploaded successfully. S3 URL:", data.Location);
  }
});
