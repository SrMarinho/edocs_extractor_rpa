import pytest
from unittest.mock import patch, mock_open, MagicMock
from src.core.use_cases.send_to_ts import SendToTs

@pytest.fixture
def send_to_ts_instance():
    return SendToTs(
        host="10.20.19.15",
        username="test_user@domain.local",
        password="test_password",
        files=["test_file.xml"],
        destination="test_destination"
    )

def test_send_to_ts_initialization(send_to_ts_instance):
    """Test if SendToTs class is initialized with correct attributes"""
    assert send_to_ts_instance.host == "10.20.19.15"
    assert send_to_ts_instance.username == "test_user@domain.local"
    assert send_to_ts_instance.password == "test_password"
    assert send_to_ts_instance.files == ["test_file.xml"]
    assert send_to_ts_instance.destination == "test_destination"

@patch('src.core.use_cases.send_to_ts.Connection')
@patch('src.core.use_cases.send_to_ts.Open')
@patch('builtins.open', new_callable=mock_open, read_data=b"test data")
def test_execute_successful_transfer(mock_file_open, mock_open_class, mock_connection, send_to_ts_instance):
    """Test successful file transfer execution"""
    # Setup mock connection
    mock_conn_instance = MagicMock()
    mock_connection.return_value = mock_conn_instance

    # Setup mock file context
    mock_remote_file = MagicMock()
    mock_open_instance = MagicMock()
    mock_open_instance.__enter__.return_value = mock_remote_file
    mock_open_class.return_value = mock_open_instance

    # Execute the transfer
    send_to_ts_instance.execute()

    # Verify connection was established
    mock_connection.assert_called_once_with("10.20.19.15", "rafael.silva@drogariaglobo.local", "RS@2025%Gl0b0#")
    mock_conn_instance.connect.assert_called_once()

    # Verify file operations
    mock_open_class.assert_called_once()
    mock_file_open.assert_called_once()
    mock_remote_file.write.assert_called_once_with(b"test data")

@patch('src.core.use_cases.send_to_ts.Connection')
def test_execute_connection_error(mock_connection, send_to_ts_instance):
    """Test handling of connection error"""
    # Setup mock to raise an exception
    mock_connection.side_effect = Exception("Connection failed")

    # Verify that the exception is raised
    with pytest.raises(Exception) as exc_info:
        send_to_ts_instance.execute()
    
    assert str(exc_info.value) == "Connection failed"
