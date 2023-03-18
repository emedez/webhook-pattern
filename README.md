# webhook-pattern

## Deployment 

Requirements:
* AWS SAM CLI should be installed already
* AWS credentials configured already


To deploy, build the artifacts first:

```
sam build
```

After successfully generating the artifacts, deploy using the command:
```
sam deploy
```

## Testing

Testing the endpoint uses the deployed resources. You will need to configure
the following environment variables:
* QUEUE_URL
* DYNAMO_TABLE

You can create .env file for this which will be loaded by python-dotenv package as
environment variables.

To run unit tests:

```
pytest
```
