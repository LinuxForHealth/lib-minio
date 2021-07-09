# whpa-cdp-minio-python-client

Minio python sdk wrapper library for use in CDP python based services.

## Build

### Gradle Setup

Make sure you have setup `taasArtifactoryUsername` and `taasartifactoryPassword` in `gradle.properties`

A gradle python plugin is being used for the build, a local build file can be used to override certain behaviour for working locally. 

The project contains [local.build.gradle](local.build.gradle) which can be leveraged to get the project building locally, it overrides the python executable and also adds wh-imaging-pypi-virtual as an added extra index url so internal dependencies can be installed.

in summary following python block wioth local build gradle is updated like

```groovy
python {

    //Python dependencies start
    pythonBinary = 'python3'
    extraIndexUrls = [whImagingPypiVirtual]
    trustedHosts "https://na.artifactory.swg-devops.com"
    pip 'minio:7.0.3'
    pip 'whi-caf-lib-python-logger:3.1.0'
    pip 'whi-caf-lib-configreader:3.2.0'
    pip 'pytest-mock:3.6.1'
    pip 'asyncio:3.4.3'
    //Python dependencies end

    envPath = '/opt/ibm/whi/app'
}
```
>**NOTE**: `whImagingPypiVirtual` should be set to pypi repository in `gradle.properties` like "https://\<IBM email>:\<Artifactory-key>@na.artifactory.swg-devops.com/artifactory/api/pypi/wh-imaging-pypi-virtual/simple"

**Alternatively** for internal dependencies, you can update the `pip.conf` file at appropiate location to have --index-url set to correct pypi repository. just add following to `pip.conf`

```properties
[global]
timeout = 60
index-url = https://<IBM email>:<Artifactory-key>@na.artifactory.swg-devops.com/artifactory/api/pypi/wh-imaging-pypi-virtual/simple
```

>Note: location of pip file maybe determined by `pip config list -v`

Run gradle build with specific file

```bash
gradle clean build -b local.build.gradle #build the project creates artifacts and runs unit tests
```

>Note: The craeted artifact will be in `build/dist` directory

## Basic Usage/ Testing

The package is hosted at our internal pypi repository, install using pip by

```python
pip install whpa-cdp-minio-python-client --index-url "https://<IBM email>:<Artifactory-key>@na.artifactory.swg-devops.com/artifactory/api/pypi/wh-imaging-pypi-virtual/simple"
```

>NOTE: you can alternatively `pip install build/dist/whpa_cdp_minio_python_client-0.0.1-py3-none-any.whl` this .whl artifact is created as part of build so you can install it after running gradle build.

```python
from cdp_minio.wrapper import MinioClientApi
import asyncio
import io

"""
Sample code to show usage of this library
"""


client = MinioClientApi("localhost:9001", "minio", "minio123")


async def execute():
    await client.make_bucket("client-c")
    exists = await client.bucket_exists("client-c")

    print(f"Bucket Exists: {exists}")

    # upload object to bucket, can use fput_object to upload a file as object instead
    result = await client.put_object(
        bucket_name="client-c",
        object_name="hello",
        data=io.BytesIO(b"hello"),
        length=-1,
        part_size=10 * 1024 * 1024,
    )

    print(
        "created {0} object; etag: {1}, version-id: {2}".format(
            result.object_name,
            result.etag,
            result.version_id,
        ),
    )

    # download object from bucket, can use fget_object to download toa  file instead.
    myobject = await client.get_object(bucket_name="client-c", object_name="hello")
    print(f"retrieved object {myobject}")


asyncio.run(execute())

```

### Functional Testing Notes

- can run a minio instance and execute library methods for checking bucket uploading object and retrieving it etc.
- refer [wrapper.py](src/cdp_minio/wrapper.py) for avaiable methods
