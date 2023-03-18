import boto3
from fastapi import Depends

boto_session = boto3.session.Session()


def get_boto_session():
    return boto_session


def get_sqs_client(session: boto3.Session = Depends(get_boto_session)):
    return session.client("sqs")


def get_dynamodb_client(session: boto3.Session = Depends(get_boto_session)):
    return session.client("dynamodb")
