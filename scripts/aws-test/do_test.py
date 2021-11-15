#!/usr/bin/env python3

import sys
import boto3

# change 3

def main():
    print(f"aws test script. boto3 version: {boto3.__version__}")

if __name__ == '__main__':
    sys.exit(main())