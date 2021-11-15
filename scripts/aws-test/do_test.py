#!/usr/bin/env python3

import sys
import io

import boto3

# change 6

def main():
    print(f"[*] aws test script. boto3 version: {boto3.__version__}")

    s3 = boto3.client('s3')

    bio = io.BytesIO()
    bio.write(b'Hello s3')
    bio.seek(0)

    s3.upload_fileobj(bio, "lucag-test-personal", "hello_s3/hello.bin")
    print("[*] test upload completed.")

if __name__ == '__main__':
    sys.exit(main())