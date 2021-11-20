#!/bin/bash

set -euxo pipefail

# change 2

# required env variables
echo "REPOSITORY_DIR: $REPOSITORY_DIR"
echo "RPM_BASEARCH: $RPM_BASEARCH"
echo "REPOSITORY_NAME: $REPOSITORY_NAME"
echo "PACKAGES_DIR: $PACKAGES_DIR"
echo "SCRIPTS_DIR: $SCRIPTS_DIR"
echo "S3_BUCKET_NAME: $S3_BUCKET_NAME"

mkdir -p $REPOSITORY_DIR/rpm/$RPM_BASEARCH

# NOTE: the ACLs for public reading are removed until we use a test private bucket. Will need to be enabled for production

aws s3 sync s3://$S3_BUCKET_NAME/$REPOSITORY_NAME/rpm/$RPM_BASEARCH/ $REPOSITORY_DIR/rpm/$RPM_BASEARCH/ --exact-timestamps # --acl public-read 
# ls -1tdr $REPOSITORY_DIR/rpm/$RPM_BASEARCH/*sysdig*.rpm | head -n -5 | xargs -d '\n' rm -f || true

cp $PACKAGES_DIR/*rpm $REPOSITORY_DIR/rpm/$RPM_BASEARCH
createrepo $REPOSITORY_DIR/rpm/$RPM_BASEARCH

cp $SCRIPTS_DIR/draios.repo $REPOSITORY_DIR/rpm
sed -i s/_REPOSITORY_/$REPOSITORY_NAME/g $REPOSITORY_DIR/rpm/draios.repo

aws s3 cp $REPOSITORY_DIR/rpm/draios.repo s3://$S3_BUCKET_NAME/$REPOSITORY_NAME/rpm/ # --acl public-read
aws s3 sync $REPOSITORY_DIR/rpm/$RPM_BASEARCH/ s3://$S3_BUCKET_NAME/$REPOSITORY_NAME/rpm/$RPM_BASEARCH/ --exact-timestamps # --acl public-read 
