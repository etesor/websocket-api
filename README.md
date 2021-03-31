# websocket-api
This application allows you to put data on a DynamoDB table using the following structure:
```buildoutcfg
{"action": "putwords","data": ["amet","deserunt","veniam","ad","minim","dolore","laboris"]}
```

Another route allows you to retreive a random word from the database.
```buildoutcfg
{"action":"getrandom"}
```
## Deploy the sample application

```bash
sam build --use-container
sam deploy --guided
```

## Test the API
It is recommended to use the [wscat client](https://github.com/websockets/wscat).

Refereces:
- [AWS Docs about using wscat](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-how-to-call-websocket-api-wscat.html)