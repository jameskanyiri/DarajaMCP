import pytest
from unittest.mock import patch, MagicMock
from database.database import get_analyzed_documents


class TestDatabase:
    """Test cases for database functionality"""
    
    @patch('database.database.workflow_collection')
    def test_get_analyzed_documents_success(self, mock_collection):
        """Test successful retrieval of analyzed documents"""
        # Mock documents from MongoDB
        mock_docs = [
            {"_id": "1", "text": "Document 1 content", "metadata": {}},
            {"_id": "2", "text": "Document 2 content", "metadata": {}},
            {"_id": "3", "text": "Document 3 content", "metadata": {}}
        ]
        
        mock_collection.find.return_value = mock_docs
        
        result = get_analyzed_documents()
        
        # Verify the function returns only the text content
        expected = ["Document 1 content", "Document 2 content", "Document 3 content"]
        assert result == expected
        
        # Verify MongoDB find was called
        mock_collection.find.assert_called_once()
    
    @patch('database.database.workflow_collection')
    def test_get_analyzed_documents_empty_result(self, mock_collection):
        """Test retrieval when no documents exist"""
        mock_collection.find.return_value = []
        
        result = get_analyzed_documents()
        
        assert result == []
        mock_collection.find.assert_called_once()
    
    @patch('database.database.workflow_collection')
    def test_get_analyzed_documents_missing_text_field(self, mock_collection):
        """Test handling of documents without text field"""
        mock_docs = [
            {"_id": "1", "text": "Document 1 content"},
            {"_id": "2", "metadata": {}},  # Missing text field
            {"_id": "3", "text": "Document 3 content"}
        ]
        
        mock_collection.find.return_value = mock_docs
        
        result = get_analyzed_documents()
        
        # Should handle missing text fields gracefully (returns None for missing)
        expected = ["Document 1 content", None, "Document 3 content"]
        assert result == expected
    
    @patch('database.database.workflow_collection')
    def test_get_analyzed_documents_database_error(self, mock_collection):
        """Test handling of database errors"""
        mock_collection.find.side_effect = Exception("Database connection error")
        
        with pytest.raises(Exception) as exc_info:
            get_analyzed_documents()
        
        assert "Database connection error" in str(exc_info.value)
    
    @patch.dict('os.environ', {'MONGODB_URI': 'mongodb://test:test@localhost:27017/test'})
    @patch('database.database.MongoClient')
    def test_database_connection_initialization(self, mock_mongo_client):
        """Test database connection initialization"""
        # Reimport to trigger the initialization with mocked environment
        import importlib
        import database.database
        importlib.reload(database.database)
        
        # Verify MongoClient was called with correct URI
        mock_mongo_client.assert_called_with(
            'mongodb://test:test@localhost:27017/test',
            server_api=database.database.ServerApi("1")
        )
