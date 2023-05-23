#!/usr/bin/env python

"""Tests for `facial_keypoints_detection` package."""


import unittest
from click.testing import CliRunner

from facial_keypoints_detection import facial_keypoints_detection
from facial_keypoints_detection import cli


class TestFacial_keypoints_detection(unittest.TestCase):
    """Tests for `facial_keypoints_detection` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'facial_keypoints_detection.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
