# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['s3upload']

package_data = \
{'': ['*'],
 's3upload': ['src/*',
              'src/app/*',
              'src/app/actions/*',
              'src/app/components/*',
              'src/app/constants/*',
              'src/app/reducers/*',
              'src/app/store/*',
              'src/app/utils/*',
              'static/s3upload/css/*',
              'static/s3upload/js/*',
              'templates/s3upload/*']}

install_requires = \
['boto3>=1.14,<2.0', 'django>=2.2,<5.0']

setup_kwargs = {
    'name': 'django-s3-upload',
    'version': '0.4',
    'description': 'Integrates direct client-side uploading to s3 with Django.',
    'long_description': 'django-s3-upload\n================\n\nCompatibility\n-------------\n\nThis library now supports Python3 and Django v1.11 and above only.\n\n\n[![Build Status](https://travis-ci.org/yunojuno/django-s3upload.svg?branch=master)](https://travis-ci.org/yunojuno/django-s3upload)\n\n**Allows direct uploading of a file from the browser to AWS S3 via a file input field rendered by Django.**\n\nThe uploaded file\'s URL is then saveable as the value of that field in the database.\n\nThis avoids the problem of uploads timing out when they go via a web server before being handed off to S3.\n\nFeatures include:\n\n* displaying a progress bar\n* support for ACLs (eg, private uploads)\n* support for encrypted-at-rest S3 buckets\n* mimetype and file extension whitelisting\n* specifying different bucket destinations on a per-field basis\n\n## Installation\n\nInstall with Pip:\n\n```pip install django-s3-upload```\n\n## AWS Setup\n\n### Access Credentials\n\nYou have two options of providing access to AWS resources:\n\n1. Add credentials of an IAM user to your Django settings (see below)\n2. Use the EC2 instance profile and its attached IAM role\n\nWhether you are using an IAM user or a role, there needs to be an IAM policy\nin effect that grants permission to upload to S3:\n\n```json\n"Statement": [\n  {\n    "Effect": "Allow",\n    "Action": ["s3:PutObject", "s3:PutObjectAcl"],\n    "Resource": "arn:aws:s3:::your-bucket-name/*"\n  }\n]\n```\n\nIf the instance profile is to be used, the IAM role needs to have a\nTrust Relationship configuration applied:\n\n```json\n"Statement": [\n\t{\n\t\t"Effect": "Allow",\n\t\t"Principal": {\n\t\t\t"Service": "ec2.amazonaws.com"\n\t\t},\n\t\t"Action": "sts:AssumeRole"\n\t}\n]\n```\n\nNote that in order to use the EC2 instance profile, django-s3-upload needs\nto query the EC2 instance metadata using utility functions from the\n[botocore] [] package. You already have `botocore` installed if `boto3`\nis a dependency of your project.\n\n### S3 CORS\n\nSetup a CORS policy on your S3 bucket.\n\n```xml\n<CORSConfiguration>\n    <CORSRule>\n        <AllowedOrigin>http://yourdomain.com:8080</AllowedOrigin>\n        <AllowedMethod>POST</AllowedMethod>\n        <AllowedMethod>PUT</AllowedMethod>\n        <MaxAgeSeconds>3000</MaxAgeSeconds>\n        <AllowedHeader>*</AllowedHeader>\n    </CORSRule>\n</CORSConfiguration>\n```\n\n## Django Setup\n\n### settings.py\n\n```python\nINSTALLED_APPS = [\n    ...\n    \'s3upload\',\n    ...\n]\n\nTEMPLATES = [{\n    ...\n    \'APP_DIRS\': True,\n    ...\n}]\n\n# AWS\n\n# If these are not defined, the EC2 instance profile and IAM role are used.\n# This requires you to add boto3 (or botocore, which is a dependency of boto3)\n# to your project dependencies.\nAWS_ACCESS_KEY_ID = \'\'\nAWS_SECRET_ACCESS_KEY = \'\'\n\nAWS_STORAGE_BUCKET_NAME = \'\'\n\n# The region of your bucket, more info:\n# http://docs.aws.amazon.com/general/latest/gr/rande.html#s3_region\nS3UPLOAD_REGION = \'us-east-1\'\n\n# [Optional] Custom bucket endpoint url, with following keys (also optional):\n# region - region of your bucket\n# bucket - your bucket name\n# S3UPLOAD_BUCKET_ENDPOINT = \'https://{region}.non-amazon-s3-url.com/{bucket}\'\n\n# Destinations, with the following keys:\n#\n# key [required] Where to upload the file to, can be either:\n#     1. \'/\' = Upload to root with the original filename.\n#     2. \'some/path\' = Upload to some/path with the original filename.\n#     3. functionName = Pass a function and create your own path/filename.\n# auth [optional] An ACL function to whether the current Django user can perform this action.\n# allowed [optional] List of allowed MIME types.\n# acl [optional] Give the object another ACL rather than \'public-read\'.\n# cache_control [optional] Cache control headers, eg \'max-age=2592000\'.\n# content_disposition [optional] Useful for sending files as attachments.\n# bucket [optional] Specify a different bucket for this particular object.\n# server_side_encryption [optional] Encryption headers for buckets that require it.\n\nS3UPLOAD_DESTINATIONS = {\n    \'example_destination\': {\n        # REQUIRED\n        \'key\': \'uploads/images\',\n\n        # OPTIONAL\n        \'auth\': lambda u: u.is_staff, # Default allow anybody to upload\n        \'allowed_types\': [\'image/jpeg\', \'image/png\', \'video/mp4\'],  # Default allow all mime types\n        \'allowed_extensions\': (\'.jpg\', \'.jpeg\', \'.png\'), # Defaults to all extensions\n        \'bucket\': \'pdf-bucket\', # Default is \'AWS_STORAGE_BUCKET_NAME\'\n        \'acl\': \'private\', # Defaults to \'public-read\'\n        \'cache_control\': \'max-age=2592000\', # Default no cache-control\n        \'content_disposition\': \'attachment\',  # Default no content disposition\n        \'content_length_range\': (5000, 20000000), # Default allow any size\n        \'server_side_encryption\': \'AES256\', # Default no encryption\n    }\n}\n```\n\n### urls.py\n\n```python\nurlpatterns = [\n    path(r\'^s3upload/\', include(\'s3upload.urls\')),\n]\n```\n\nRun ```python manage.py collectstatic``` if required.\n\n## Use in Django admin\n\n### models.py\n\n```python\nfrom django.db import models\nfrom s3upload.fields import S3UploadField\n\nclass Example(models.Model):\n    video = S3UploadField(dest=\'example_destination\')\n```\n\n## Use the widget in a custom form\n\n### forms.py\n\n```python\nfrom django import forms\nfrom s3upload.widgets import S3UploadWidget\n\nclass S3UploadForm(forms.Form):\n    images = forms.URLField(widget=S3UploadWidget(dest=\'example_destination\'))\n```\n\n__*Optional.__ You can modify the HTML of the widget by overiding template __s3upload/templates/s3upload-widget.tpl__\n\n### views.py\n\n```python\nfrom django.views.generic import FormView\nfrom .forms import S3UploadForm\n\nclass MyView(FormView):\n    template_name = \'form.html\'\n    form_class = S3UploadForm\n```\n\n### templates/form.html\n\n```html\n<html>\n<head>\n    <meta charset="utf-8">\n    <title>s3upload</title>\n    {{ form.media }}\n</head>\n<body>\n    <form action="" method="post">{% csrf_token %}\n        {{ form.as_p }}\n    </form>\n</body>\n</html>\n```\n\n\n## Examples\n\nExamples of both approaches can be found in the examples folder. To run them:\n```shell\n$ git clone git@github.com:yunojuno/django-s3-upload.git\n$ cd django-s3-upload\n\n# Add your AWS keys to your environment\nexport AWS_ACCESS_KEY_ID=\'...\'\nexport AWS_SECRET_ACCESS_KEY=\'...\'\nexport AWS_STORAGE_BUCKET_NAME=\'...\'\nexport S3UPLOAD_REGION=\'...\'    # e.g. \'eu-west-1\'\n\n$ docker-compose up\n```\n\nVisit ```http://localhost:8000/admin``` to view the admin widget and ```http://localhost:8000/form``` to view the custom form widget.\n\n[botocore]: https://github.com/boto/botocore\n',
    'author': 'YunoJuno',
    'author_email': 'code@yunojuno.com',
    'maintainer': 'YunoJuno',
    'maintainer_email': 'code@yunojuno.com',
    'url': 'https://github.com/yunojuno/django-s3-upload',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
