from src.cdp_minio.wrapper import MinioClientApi
import pytest


@pytest.fixture
def mock_minio_client(mocker):
    mocker.patch("src.cdp_minio.wrapper.Minio")
    mc = MinioClientApi("test", "test", "test")
    return mc


@pytest.mark.asyncio
async def test_make_bucket(mock_minio_client):

    client = "cloud1"
    await mock_minio_client.make_bucket(client)
    mock_minio_client._client.make_bucket.assert_called_once_with(client)


@pytest.mark.asyncio
async def test_bucket_exists(mock_minio_client):

    client = "cloud1"
    await mock_minio_client.bucket_exists(client)
    mock_minio_client._client.bucket_exists.assert_called_once_with(client)


@pytest.mark.asyncio
async def test_put_object(mock_minio_client):

    client = "cloud1"
    object = "myobject"
    data = b"hello"
    ps = 10 * 1024 * 1024
    length = -1
    await mock_minio_client.put_object(client, object, data, length, part_size=ps)
    mock_minio_client._client.put_object.assert_called_once()


@pytest.mark.asyncio
async def test_get_object(mock_minio_client):

    client = "cloud1"
    object = "myobject"
    await mock_minio_client.get_object(client, object)
    mock_minio_client._client.get_object.assert_called_once()


@pytest.mark.asyncio
async def test_fput_object(mock_minio_client):

    client = "cloud1"
    object = "myobject"
    filepath = "test"
    await mock_minio_client.fput_object(client, object, filepath)
    mock_minio_client._client.fput_object.assert_called_once()


@pytest.mark.asyncio
async def test_fget_object(mock_minio_client):

    client = "cloud1"
    object = "myobject"
    filepath = "test"
    await mock_minio_client.fget_object(client, object, filepath)
    mock_minio_client._client.fget_object.assert_called_once()


@pytest.mark.asyncio
async def test_delete_object(mock_minio_client):

    client = "cloud1"
    object = "myobject"
    await mock_minio_client.delete_object(client, object)
    mock_minio_client._client.remove_object.assert_called_once()
