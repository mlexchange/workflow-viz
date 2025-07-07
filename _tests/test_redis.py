import json
import os
from unittest.mock import MagicMock, Mock, call, patch

import pytest

from utils.redis import RedisConn


@pytest.fixture
def mock_redis():
    """Create a mock redis connection for testing."""
    return MagicMock()


@pytest.fixture
def redis_conn(mock_redis):
    """Create a RedisConn instance with mocked redis connection."""
    return RedisConn(mock_redis)


def test_redis_conn_init(mock_redis):
    """Test RedisConn initialization."""
    redis_conn = RedisConn(mock_redis)
    assert redis_conn.redis_conn == mock_redis


def test_get(redis_conn, mock_redis):
    """Test get method."""
    # Arrange
    test_key = "test_key"
    expected_value = "test_value"
    mock_redis.get.return_value = expected_value

    # Act
    result = redis_conn.get(test_key)

    # Assert
    mock_redis.get.assert_called_once_with(test_key)
    assert result == expected_value


def test_set(redis_conn, mock_redis):
    """Test set method."""
    # Arrange
    test_key = "test_key"
    test_value = "test_value"

    # Act
    redis_conn.set(test_key, test_value)

    # Assert
    mock_redis.set.assert_called_once_with(test_key, test_value)


def test_get_json_with_valid_data(redis_conn, mock_redis):
    """Test get_json method with valid JSON data."""
    # Arrange
    test_key = "test_key"
    test_data = {"name": "test", "value": 123}
    json_string = json.dumps(test_data)
    mock_redis.get.return_value = json_string

    # Act
    result = redis_conn.get_json(test_key)

    # Assert
    mock_redis.get.assert_called_once_with(test_key)
    assert result == test_data


def test_get_json_with_no_data(redis_conn, mock_redis):
    """Test get_json method when no data exists."""
    # Arrange
    test_key = "test_key"
    mock_redis.get.return_value = None

    # Act
    result = redis_conn.get_json(test_key)

    # Assert
    mock_redis.get.assert_called_once_with(test_key)
    assert result == {}


def test_get_json_with_empty_string(redis_conn, mock_redis):
    """Test get_json method with empty string."""
    # Arrange
    test_key = "test_key"
    mock_redis.get.return_value = ""

    # Act
    result = redis_conn.get_json(test_key)

    # Assert
    mock_redis.get.assert_called_once_with(test_key)
    assert result == {}


def test_set_json(redis_conn, mock_redis):
    """Test set_json method."""
    # Arrange
    test_key = "test_key"
    test_data = {"name": "test", "value": 123}
    expected_json_string = json.dumps(test_data)

    # Act
    redis_conn.set_json(test_key, test_data)

    # Assert
    mock_redis.set.assert_called_once_with(test_key, expected_json_string)


def test_redis_subscribe(redis_conn, mock_redis):
    """Test redis_subscribe method."""
    # Arrange
    channel_name = "test_channel"
    callback = MagicMock()

    # Mock pubsub
    mock_pubsub = MagicMock()
    mock_redis.pubsub.return_value = mock_pubsub

    # Mock messages
    mock_messages = [
        {"type": "subscribe", "channel": "scattering"},  # Should be ignored
        {"type": "message", "channel": "scattering", "data": "test_data_1"},
        {"type": "message", "channel": "scattering", "data": "test_data_2"},
    ]
    mock_pubsub.listen.return_value = mock_messages

    # Act
    redis_conn.redis_subscribe(channel_name, callback)

    # Assert
    mock_redis.pubsub.assert_called_once()
    mock_pubsub.subscribe.assert_called_once_with("scattering")

    # Check that callback was called for message types only
    expected_calls = [
        call("test_data_1"),
        call("test_data_2"),
    ]
    callback.assert_has_calls(expected_calls)


def test_schedule_job_not_implemented():
    """Test that schedule_job raises NotImplementedError."""
    with pytest.raises(NotImplementedError, match="Job scheduling not implemented."):
        RedisConn.schedule_job("test_function", {"param": "value"})


def test_check_status_not_implemented():
    """Test that check_status raises NotImplementedError."""
    with pytest.raises(
        NotImplementedError, match="Job status checking not implemented."
    ):
        RedisConn.check_status("test_job_id")


@patch("utils.redis.redis.Redis")
@patch("utils.redis.redis.ConnectionPool")
def test_from_settings(mock_connection_pool, mock_redis):
    """Test from_settings class method."""
    # Arrange
    mock_pool = MagicMock()
    mock_connection_pool.return_value = mock_pool
    mock_redis_instance = MagicMock()
    mock_redis.return_value = mock_redis_instance

    settings = Mock()
    settings.host = "test_host"
    settings.port = 6380

    # Act
    redis_conn = RedisConn.from_settings(settings)

    # Assert
    mock_connection_pool.assert_called_once_with(
        host="test_host", port=6380, decode_responses=True
    )
    mock_redis.assert_called_once_with(connection_pool=mock_pool)
    assert redis_conn.redis_conn == mock_redis_instance


@patch("utils.redis.redis.Redis")
@patch("utils.redis.redis.ConnectionPool")
@patch.dict(os.environ, {"REDIS_HOST": "test_env_host", "REDIS_PORT": "6381"})
def test_from_env_with_env_vars(mock_connection_pool, mock_redis):
    """Test from_env class method with environment variables set."""
    # Arrange
    mock_pool = MagicMock()
    mock_connection_pool.return_value = mock_pool
    mock_redis_instance = MagicMock()
    mock_redis.return_value = mock_redis_instance

    # Act
    redis_conn = RedisConn.from_env()

    # Assert
    mock_connection_pool.assert_called_once_with(
        host="test_env_host", port="6381", decode_responses=True
    )
    mock_redis.assert_called_once_with(connection_pool=mock_pool)
    assert redis_conn.redis_conn == mock_redis_instance


@patch("utils.redis.redis.Redis")
@patch("utils.redis.redis.ConnectionPool")
@patch.dict(os.environ, {}, clear=True)
def test_from_env_with_defaults(mock_connection_pool, mock_redis):
    """Test from_env class method with default values."""
    # Arrange
    mock_pool = MagicMock()
    mock_connection_pool.return_value = mock_pool
    mock_redis_instance = MagicMock()
    mock_redis.return_value = mock_redis_instance

    # Act
    redis_conn = RedisConn.from_env()

    # Assert
    mock_connection_pool.assert_called_once_with(
        host="localhost", port=6379, decode_responses=True
    )
    mock_redis.assert_called_once_with(connection_pool=mock_pool)
    assert redis_conn.redis_conn == mock_redis_instance


def test_json_roundtrip():
    """Test setting and getting JSON data works correctly."""
    # Arrange
    mock_redis = MagicMock()
    redis_conn = RedisConn(mock_redis)

    test_key = "test_key"
    test_data = {"name": "test", "value": 123, "nested": {"key": "value"}}
    json_string = json.dumps(test_data)

    # Set up mock to return the JSON string when get is called
    mock_redis.get.return_value = json_string

    # Act
    redis_conn.set_json(test_key, test_data)
    result = redis_conn.get_json(test_key)

    # Assert
    mock_redis.set.assert_called_once_with(test_key, json_string)
    mock_redis.get.assert_called_once_with(test_key)
    assert result == test_data


def test_subscription_with_multiple_channels():
    """Test subscription behavior with multiple message types."""
    # Arrange
    mock_redis = MagicMock()
    redis_conn = RedisConn(mock_redis)

    callback = MagicMock()
    mock_pubsub = MagicMock()
    mock_redis.pubsub.return_value = mock_pubsub

    # Mock various message types
    mock_messages = [
        {"type": "subscribe", "channel": "scattering"},
        {"type": "message", "channel": "scattering", "data": b"binary_data"},
        {"type": "message", "channel": "other_channel", "data": "other_data"},
        {"type": "message", "channel": "scattering", "data": "string_data"},
        {"type": "unsubscribe", "channel": "scattering"},
    ]
    mock_pubsub.listen.return_value = mock_messages

    # Act
    redis_conn.redis_subscribe("test_channel", callback)

    # Assert
    # Should only call callback for message types on the scattering channel
    expected_calls = [
        call(b"binary_data"),
        call("string_data"),
    ]
    callback.assert_has_calls(expected_calls)
    assert callback.call_count == 2


# Additional pytest-style tests for edge cases and error handling


def test_get_json_with_invalid_json(redis_conn, mock_redis):
    """Test get_json method with invalid JSON data."""
    # Arrange
    test_key = "test_key"
    invalid_json = "invalid_json_string"
    mock_redis.get.return_value = invalid_json

    # Act & Assert
    with pytest.raises(json.JSONDecodeError):
        redis_conn.get_json(test_key)


def test_set_json_with_complex_data(redis_conn, mock_redis):
    """Test set_json method with complex nested data."""
    # Arrange
    test_key = "complex_key"
    test_data = {
        "list": [1, 2, 3],
        "nested": {"deeply": {"nested": {"value": "test"}}},
        "boolean": True,
        "null_value": None,
        "number": 42.5,
    }
    expected_json_string = json.dumps(test_data)

    # Act
    redis_conn.set_json(test_key, test_data)

    # Assert
    mock_redis.set.assert_called_once_with(test_key, expected_json_string)


def test_redis_subscribe_with_exception(redis_conn, mock_redis):
    """Test redis_subscribe method handles exceptions gracefully."""
    # Arrange
    channel_name = "test_channel"
    callback = MagicMock()

    # Mock pubsub to raise an exception
    mock_redis.pubsub.side_effect = Exception("Redis connection error")

    # Act & Assert
    with pytest.raises(Exception, match="Redis connection error"):
        redis_conn.redis_subscribe(channel_name, callback)
