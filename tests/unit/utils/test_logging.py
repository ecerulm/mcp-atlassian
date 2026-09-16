import io
import logging
from pathlib import Path

from mcp_atlassian.utils.logging import setup_logging


def test_setup_logging_default_level(tmp_path: Path):
    """Test setup_logging with default WARNING level"""
    logger = setup_logging(log_path=tmp_path / "mcp.log")

    # Check logger level is set to WARNING
    assert logger.level == logging.WARNING

    # Check root logger is configured
    root_logger = logging.getLogger()
    assert root_logger.level == logging.WARNING

    # Verify handler and formatter
    assert len(root_logger.handlers) == 2
    stream_handler, file_handler = root_logger.handlers
    assert isinstance(stream_handler, logging.Handler)
    assert stream_handler.formatter._fmt == "%(levelname)s - %(name)s - %(message)s"
    assert isinstance(file_handler, logging.Handler)
    assert (
        file_handler.formatter._fmt
        == "%(asctime)s %(levelname)s %(name)s: %(message)s"
    )


def test_setup_logging_custom_level(tmp_path: Path):
    """Test setup_logging with custom DEBUG level"""
    logger = setup_logging(logging.DEBUG, log_path=tmp_path / "mcp.log")

    # Check logger level is set to DEBUG
    assert logger.level == logging.DEBUG

    # Check root logger is configured
    root_logger = logging.getLogger()
    assert root_logger.level == logging.DEBUG


def test_setup_logging_removes_existing_handlers(tmp_path: Path):
    """Test that setup_logging removes existing handlers"""
    # Add a test handler
    root_logger = logging.getLogger()
    test_handler = logging.StreamHandler()
    root_logger.addHandler(test_handler)
    # Setup logging should remove existing handler
    setup_logging(log_path=tmp_path / "mcp.log")

    # Verify only one handler remains
    assert len(root_logger.handlers) == 2
    assert test_handler not in root_logger.handlers


def test_setup_logging_logger_name(tmp_path: Path):
    """Test that setup_logging creates logger with correct name"""
    logger = setup_logging(log_path=tmp_path / "mcp.log")
    assert logger.name == "mcp-atlassian"


def test_setup_logging_logging_stream(tmp_path: Path):
    """Test that setup_logging uses the correct stream"""
    stream = io.StringIO()
    logger = setup_logging(logging.DEBUG, stream, tmp_path / "mcp.log")
    logger.debug("test")
    assert stream.getvalue() == f"DEBUG - {logger.name} - test\n"
