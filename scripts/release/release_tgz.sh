#!/bin/bash

set -euxo pipefail

echo "REPOSITORY_DIR: $REPOSITORY_DIR"
echo "BASEARCH: $BASEARCH"
echo "REPOSITORY_NAME: $REPOSITORY_NAME"
echo "S3_BUCKET_NAME: $S3_BUCKET_NAME"
echo "PACKAGES_DIR: $PACKAGES_DIR"

mkdir -p $REPOSITORY_DIR/tgz/$BASEARCH

aws s3 sync s3://$S3_BUCKET_NAME/$REPOSITORY_NAME/tgz/$BASEARCH/ $REPOSITORY_DIR/tgz/$BASEARCH/ --exact-timestamps --acl public-read # --delete
# ls -1tdr $REPOSITORY_DIR/tgz/$BASEARCH/*sysdig* | head -n -5 | xargs -d '\n' rm -f || true

cp $PACKAGES_DIR/*tar.gz $REPOSITORY_DIR/tgz/$BASEARCH
aws s3 sync $REPOSITORY_DIR/tgz/$BASEARCH/ s3://$S3_BUCKET_NAME/$REPOSITORY_NAME/tgz/$BASEARCH --exact-timestamps --acl public-read # --delete
