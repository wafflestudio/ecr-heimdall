import base64
import json
import logging
import os

import boto3
from github import Github

LOG = logging.getLogger(__name__)
LOG.setLevel(os.environ.get('LOG_LEVEL', 'INFO'))

SECRETS_MANAGER = boto3.client("secretsmanager", region_name="ap-northeast-2")

ECR_HOST = "405906814034.dkr.ecr.ap-northeast-2.amazonaws.com"


def get_credential(key):
    credential = SECRETS_MANAGER.get_secret_value(SecretId="ecr-image-tag-updater")
    return json.loads(credential["SecretString"])[key]


GITHUB_ACCESS_TOKEN = get_credential("github-access-token")
GITHUB_CLIENT = Github(GITHUB_ACCESS_TOKEN)


def update_waffle_world_image_tag(event, context):
    try:
        ecr_repo = event["detail"]["repository-name"]  # ex> snutt-dev/snutt-ev
        namespace, app = ecr_repo.split("/")
        image_tag = event["detail"]["image-tag"]

        gh_repo = GITHUB_CLIENT.get_repo("wafflestudio/waffle-world")
        target_file = gh_repo.get_contents(f"apps/{namespace}/{app}/{app}.yaml")
        decoded_lines = base64.b64decode(target_file.content).decode("utf-8").split("\n")

        lines = []
        for line in decoded_lines:
            if f"image: {ECR_HOST}/{ecr_repo}" in line:
                old_image_tag = line.split(":")[-1].split(" ")[0].strip()
                line = line.replace(f":{old_image_tag}", f":{image_tag}")

            lines.append(line)

        gh_repo.update_file(
            target_file.path,
            f"Automated commit by ECR push ({ecr_repo}:{image_tag})",
            "\n".join(lines),
            target_file.sha,
        )
        return 'SUCCESS'
    except:
        LOG.exception("Lambda function failed:")
        return 'ERROR'
