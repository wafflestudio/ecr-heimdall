FROM python:3.9-slim

WORKDIR /tmp

RUN set -ex \
	&& pip install --no-cache-dir -U pip awscli \
	&& apt-get update \
	&& apt-get install -y \
		build-essential \
		zip \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY requirements.txt ./

RUN set -ex \
	&& pip install --no-cache-dir -r requirements.txt -t /vendor \
	&& cd /vendor && zip -r9 /function.zip  . -x '*/__pycache__/*' \
	&& cd / && rm -rf /vendor

COPY *.py ./
RUN zip -9g /function.zip *.py

CMD aws --region ap-northeast-2 lambda update-function-code --function-name ecr-image-tag-updater --zip-file fileb:///function.zip
