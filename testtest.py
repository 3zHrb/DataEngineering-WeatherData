import ast
import array
import boto3
import ast
import datetime
import pandas as pd
import os


# currentPath = os.listdir(os.getcwd())


# for file in currentPath:

#     if file.startswith("weather") and file.endswith(".csv"):
#         os.remove(f"{os.getcwd()}/{file}")

s3 = boto3.resource(
    service_name="s3",
    region_name="us-west-2",
    aws_access_key_id="AKIASZVBO2X2UOQT32DQ",
    aws_secret_access_key="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",
)

arrayOfFiles = []

for file in s3.Bucket("weatherdata-project").objects.all():
    arrayOfFiles.append(file)


print(len(arrayOfFiles))

# print(
#     s3.Bucket("weatherdata-project")
#     .Object("weatherData_s3_at_2023-05-19 07:45:34.427167.csv")
#     .get()
# )

# s3Client = boto3.client(
#     "s3",
#     aws_access_key_id="AKIASZVBO2X2UOQT32DQ",
#     aws_secret_access_key="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",
# )


# creatingBucket = s3.create_bucket(
#     Bucket="whatif-resource",
#     CreateBucketConfiguration={"LocationConstraint": "us-west-2"},
# )

# print(creatingBucket)

# s3Client.delete_bucket(Bucket="whatif-client")

bucket = s3.Bucket("weatherdata-project")
object = bucket.Object("myfile.csv")
object.delete()


arrayOfFiles = []

for file in s3.Bucket("weatherdata-project").objects.all():
    arrayOfFiles.append(file)


print(len(arrayOfFiles))


# Replace with the name of the bucket

bucket = s3.Bucket("weatherdata")
objects = list(bucket.objects.all())

objects.sort(key=lambda obj: obj.last_modified, reverse=True)

if objects:
    last_object = objects[0].key
    print("Last added object:", last_object)
else:
    print("No objects found in the bucket.")
