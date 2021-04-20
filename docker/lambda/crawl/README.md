
- build

```bash
FinAppBackend$ sudo docker build -t finapp_lambda_crawl -f docker/lambda/crawl/Dockerfile . 
```

- Docker CLI Authentication

```bash
$ export ECR_ACCOUNT=***********
```

```bash
FinAppBackend$ sudo aws ecr get-login-password --region ap-northeast-1 | sudo docker login --username AWS --password-stdin ${ECR_ACCOUNT}.dkr.ecr.ap-northeast-1.amazonaws.com
```

- Create ECR

```bash
$ aws ecr create-repository --repository-name finapp-lambda-crawl --image-scanning-configuration scanOnPush=true
```

- Tagging

```bash
$ sudo docker tag finapp_lambda_crawl:latest ${ECR_ACCOUNT}.dkr.ecr.ap-northeast-1.amazonaws.com/finapp-lambda-crawl:latest
```

- Push to ECR

```bash
$ sudo docker push ${ECR_ACCOUNT}.dkr.ecr.ap-northeast-1.amazonaws.com/finapp-lambda-crawl:latest
```