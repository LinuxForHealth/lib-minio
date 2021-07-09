from minio import Minio
import asyncio


class MinioClientApi:
    """
    A minio python SDK wrapper Library for bucket and object operations in Clinical Data Pipeline Project
    """

    def __init__(self, endpoint, access_key, secret_key):

        self._client: Minio = Minio(
            endpoint, secure=False, access_key=access_key, secret_key=secret_key
        )

    async def make_bucket(self, bucket_name):
        """
        creates a bucket with the specified name"""

        loop = asyncio.get_event_loop()

        response = await loop.run_in_executor(
            None, self._client.make_bucket, bucket_name
        )
        # response = self._client.make_bucket(bucket_name)
        return response

    async def bucket_exists(self, bucket_name):
        """
        checks if bucket exists

        Args:
            bucket_name (String): The name of the bucket to check
        """
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, self._client.bucket_exists, bucket_name
        )

        return response

    async def put_object(
        self,
        bucket_name,
        object_name,
        data,
        length,
        content_type="application/octet-stream",
        metadata=None,
        sse=None,
        progress=None,
        part_size=0,
        num_parallel_uploads=3,
        tags=None,
        retention=None,
        legal_hold=False,
    ):
        """
        Uploads data from a stream to an object in a bucket.
        """
        loop = asyncio.get_event_loop()

        response = await loop.run_in_executor(
            None,
            self._client.put_object,
            bucket_name,
            object_name,
            data,
            length,
            content_type,
            metadata,
            sse,
            progress,
            part_size,
            num_parallel_uploads,
            tags,
            retention,
            legal_hold,
        )

        return response

    async def get_object(
        self,
        bucket_name,
        object_name,
        offset=0,
        length=0,
        request_headers=None,
        ssec=None,
        version_id=None,
        extra_query_params=None,
    ):
        """
        retrieves an object from a given bucket and object key

        Args:
            bucket_name (String): name of the bucket from where to retrieve the object
            object_name (String): the object key within the bucket
        """

        loop = asyncio.get_event_loop()
        data = None
        try:
            response = await loop.run_in_executor(
                None,
                self._client.get_object,
                bucket_name,
                object_name,
                offset,
                length,
                request_headers,
                ssec,
                version_id,
                extra_query_params,
            )
            data = response.read()
        finally:
            response.close()

        return data

    async def fput_object(
        self,
        bucket_name,
        object_name,
        file_path,
        content_type="application/octet-stream",
        metadata=None,
        sse=None,
        progress=None,
        part_size=0,
        num_parallel_uploads=3,
        tags=None,
        retention=None,
        legal_hold=False,
    ):
        """
        Uploads data from a file to an object in a bucket.

        Refer Minio sdk for documentation of parameters
        """
        loop = asyncio.get_event_loop()

        response = await loop.run_in_executor(
            None,
            self._client.fput_object,
            bucket_name,
            object_name,
            file_path,
            content_type,
            metadata,
            sse,
            progress,
            part_size,
            num_parallel_uploads,
            tags,
            retention,
            legal_hold,
        )
        return response

    async def fget_object(
        self,
        bucket_name,
        object_name,
        file_path,
        request_headers=None,
        ssec=None,
        version_id=None,
        extra_query_params=None,
        tmp_file_path=None,
    ):

        """
        downloads data of an object to a file
        """
        loop = asyncio.get_event_loop()

        response = await loop.run_in_executor(
            None,
            self._client.fget_object,
            bucket_name,
            object_name,
            file_path,
            request_headers,
            ssec,
            version_id,
            extra_query_params,
            tmp_file_path,
        )
        return response

    async def delete_object(self, bucket_name, object_name, version_id=None):
        """
        deletes an object from a bucket
        """
        loop = asyncio.get_event_loop()

        response = await loop.run_in_executor(
            None, self._client.remove_object, bucket_name, object_name, version_id
        )

        return response
