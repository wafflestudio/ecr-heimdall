# ecr-heimdall
## detects ecr push and reflects it to waffle-world

### how it works
1. GitHub Actions (in each repo) build and push docker image to ECR
2. ECR push event triggers AWS Lambda function
3. This Lambda function updates the image tag of the corresponding manifest file in [waffle-world](https://github.com/wafflestudio/waffle-world)
4. ArgoCD detects the change in the manifest file and deploys the new image

### how to deploy
```
docker build -t ecr-heimdall . --platform linux/amd64
```
```
docker run --platform linux/amd64 -v ~/.aws/credentials:/root/.aws/credentials -it ecr-heimdall
```
