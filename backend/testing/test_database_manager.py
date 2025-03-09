import pytest
from unittest.mock import Mock, patch
from sqlalchemy.exc import DBAPIError, OperationalError
from backend.db_service.database_manager import DatabaseManager, PostgresConnection

@pytest.fixture
def db_manager():
    conn =  DatabaseManager.connection
    db_mang = DatabaseManager(conn, "test_db")
    return db_mang

@pytest.fixture
def mock_connection():
    with patch('backend.db_service.database_manager.PostgresConnection') as mock_conn:
        yield mock_conn

def test_execute_query_success(db_manager, mock_connection):
    # Arrange
    test_query = "SELECT * FROM <schema_name>.table"
    expected_query = "SELECT * FROM test_schema.table"
    mock_result = Mock()
    mock_conn = Mock()
    mock_connection.get_engine.return_value.connect.return_value.__enter__.return_value = mock_conn
    mock_conn.execute.return_value = mock_result

    # Act
    result = db_manager.execute_query(test_query)

    # Assert
    assert result == mock_result
    mock_conn.execute.assert_called_once()

def test_read_data_success(db_manager, mock_connection):
    # Arrange
    test_query = "SELECT * FROM <schema_name>.table"
    expected_query = "SELECT * FROM test_schema.table"
    mock_result = Mock()
    mock_result.fetchall.return_value = [(1, "test"), (2, "test2")]
    mock_conn = Mock()
    mock_connection.get_engine.return_value.connect.return_value.__enter__.return_value = mock_conn
    mock_conn.execute.return_value = mock_result

    # Act
    data = db_manager.read_data(test_query)

    # Assert
    assert data == [(1, "test"), (2, "test2")]
    mock_conn.execute.assert_called_once()
    mock_result.fetchall.assert_called_once()

def test_commit_transaction_success():
    # Arrange
    mock_trans1 = Mock()
    mock_trans2 = Mock()
    transactions = [mock_trans1, mock_trans2]

    # Act
    DatabaseManager.commit_transaction(transactions)

    # Assert
    mock_trans1.commit.assert_called_once()
    mock_trans2.commit.assert_called_once()

def test_commit_transaction_db_error():
    # Arrange
    mock_trans = Mock()
    mock_trans.commit.side_effect = DBAPIError(statement="", params={}, orig=Exception())
    transactions = [mock_trans]

    # Act & Assert
    with pytest.raises(DBAPIError):
        DatabaseManager.commit_transaction(transactions)

def test_rollback_transaction_success():
    # Arrange
    mock_trans1 = Mock()
    mock_trans2 = Mock()
    transactions = [mock_trans1, mock_trans2]

    # Act
    DatabaseManager.rollback_transaction(transactions)

    # Assert
    mock_trans1.rollback.assert_called_once()
    mock_trans2.rollback.assert_called_once()

def test_rollback_transaction_error():
    # Arrange
    mock_trans = Mock()
    mock_trans.rollback.side_effect = Exception("Rollback failed")
    transactions = [mock_trans]

    # Act & Assert
    with pytest.raises(Exception):
        DatabaseManager.rollback_transaction(transactions)

def test_execute_query_connection_error(db_manager, mock_connection):
    # Arrange
    test_query = "SELECT * FROM <schema_name>.table"
    mock_connection.get_engine.side_effect = OperationalError(statement="", params={}, orig=Exception())

    # Act & Assert
    with pytest.raises(OperationalError):
        db_manager.execute_query(test_query)
