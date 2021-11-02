"""
Easy to use wrapper around the MYX's platform APIs.

Make a client that will authenticate you with the API with the supplied
credentials.
```
from myx import Client

client = Client("your.user@example.com", "your.password")
```

You can use this client to operate on your twins:

List all twins
--------------

```
for twin in client.get_twins():
   print(twin)
```


Make a new twin from drone images
---------------------------------
```
new_twin = client.make_new_twin("Made with the MYX Python library")
client.upload_images(new_twin.id, "drone-flight-today/")
client.finish_upload(new_twin.id)
```


Download a file from twin
-------------------------
```
report = client.get_file(new_twin.id, 'report.pdf')
if report is None:
    print("report.pdf not created yet. Try again later")
```
"""

from myx.client import Client
