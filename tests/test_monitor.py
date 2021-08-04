"""Tests for monitor class."""
import unittest
from monitor import Monitor


class TestMonitor(unittest.TestCase):
    """Monitor class tests."""

    def setUp(self) -> None:
        self.monitor = Monitor()

    def test_class(self):
        """Tests class."""
        self.assertTrue(isinstance(self.monitor, Monitor))
