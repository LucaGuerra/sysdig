#!/usr/bin/env python3

import sys
import io

import boto3
from botocore.errorfactory import ClientError

# change 7

def s3_exists(s3, bucket: str, key: str) -> bool:
    try:
        s3.head_object(Bucket=bucket, Key=bucket)
    except ClientError:
        # Not found
        return False

    return True

def main():
    print(f"[*] aws test script. boto3 version: {boto3.__version__}")

    s3 = boto3.client('s3')

    if s3_exists("lucag-test-personal", "hello_s3/hello.bin"):
        print("[*] key already exists on S3")
    else:
        print("[*] key does not exist on s3")

    bio = io.BytesIO()
    bio.write(b'Hello s3')
    bio.seek(0)

    s3.upload_fileobj(bio, "lucag-test-personal", "hello_s3/hello.bin")
    print("[*] test upload completed.")

if __name__ == '__main__':
    sys.exit(main())