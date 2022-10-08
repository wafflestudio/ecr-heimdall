from handler import update_waffle_world_image_tag

if __name__ == '__main__':
    update_waffle_world_image_tag({  # dummy event data
        'account': '123456789012',
        'detail': {
            'action-type': 'PUSH',
            'image-digest': 'sha256:52055aa558d234465e1149228f468b7277eb0a14f2ddbd4aaa118142138ce4c3',
            'image-tag': 'new-image-tag',
            'repository-name': 'snutt-dev/snutt-ev',
            'result': 'SUCCESS'
        },
        'detail-type': 'ECR Image Action',
        'id': 'fa204081-50f2-5a5f-0c48-68aeb623801c',
        'region': 'ap-northeast-2',
        'resources': [],
        'source': 'aws.ecr',
        'time': '2022-10-05T15:03:15Z',
        'version': '0',
    }, None)
