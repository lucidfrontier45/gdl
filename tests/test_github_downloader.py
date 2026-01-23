"""Tests for GitHub Binary Downloader."""

import pytest
from typing import cast, Sequence
from unittest.mock import patch, MagicMock

from gdl.github_downloader import get_host_os, get_host_arch, match_assets, Asset
from pathlib import Path
import httpx


class TestPlatformDetection:
    """Test platform detection functions."""

    @patch("platform.system")
    def test_get_host_os_linux(self, mock_system):
        mock_system.return_value = "Linux"
        assert get_host_os() == "linux"

    @patch("platform.system")
    def test_get_host_os_windows(self, mock_system):
        mock_system.return_value = "Windows"
        assert get_host_os() == "windows"

    @patch("platform.system")
    def test_get_host_os_macos(self, mock_system):
        mock_system.return_value = "Darwin"
        assert get_host_os() == "macos"

    @patch("platform.machine")
    def test_get_host_arch_x86_64(self, mock_machine):
        mock_machine.return_value = "x86_64"
        assert get_host_arch() == "x86_64"

    @patch("platform.machine")
    def test_get_host_arch_amd64(self, mock_machine):
        mock_machine.return_value = "AMD64"
        assert get_host_arch() == "x86_64"

    @patch("platform.machine")
    def test_get_host_arch_aarch64(self, mock_machine):
        mock_machine.return_value = "aarch64"
        assert get_host_arch() == "aarch64"


class TestAssetMatching:
    """Test asset matching logic."""

    def test_match_assets_basic(self):
        assets: list[Asset] = [
            {
                "name": "binary-linux-x86_64.zip",
                "browser_download_url": "http://example.com/linux.zip",
            },
            {
                "name": "binary-windows-x86_64.exe",
                "browser_download_url": "http://example.com/win.exe",
            },
            {
                "name": "binary-linux-aarch64.tar.gz",
                "browser_download_url": "http://example.com/linux.tar.gz",
            },
        ]
        matches = match_assets(assets, "linux", "x86_64", [])
        assert len(matches) == 1
        assert matches[0]["name"] == "binary-linux-x86_64.zip"

    def test_match_assets_blacklist(self):
        assets: list[Asset] = [
            {
                "name": "binary-linux-x86_64.zip",
                "browser_download_url": "http://example.com/linux.zip",
            },
            {
                "name": "binary-debug-linux-x86_64.zip",
                "browser_download_url": "http://example.com/debug.zip",
            },
        ]
        matches = match_assets(assets, "linux", "x86_64", ["debug"])
        assert len(matches) == 1
        assert matches[0]["name"] == "binary-linux-x86_64.zip"

    def test_match_assets_synonyms(self):
        assets: list[Asset] = [
            {
                "name": "binary-win32-x86_64.zip",
                "browser_download_url": "http://example.com/win32.zip",
            },  # win32 instead of windows
            {
                "name": "binary-linux-amd64.tar.gz",
                "browser_download_url": "http://example.com/linux.tar.gz",
            },  # amd64 instead of x86_64
            {
                "name": "binary-mac-arm64.dmg",
                "browser_download_url": "http://example.com/mac.dmg",
            },  # mac and arm64
        ]
        matches = match_assets(assets, "windows", "x86_64", [])
        assert len(matches) == 1
        assert matches[0]["name"] == "binary-win32-x86_64.zip"

        matches = match_assets(assets, "linux", "x86_64", [])
        assert len(matches) == 1
        assert matches[0]["name"] == "binary-linux-amd64.tar.gz"

        matches = match_assets(assets, "macos", "aarch64", [])
        assert len(matches) == 1
        assert matches[0]["name"] == "binary-mac-arm64.dmg"


def test_list_releases_prints_tags(monkeypatch, capsys):
    # Mock HTTP response for releases
    releases = [
        {"tag_name": "v1.0"},
        {"tag_name": "v1.1"},
        {"tag_name": "v2.0"},
    ]

    mock_get = MagicMock()
    mock_resp = MagicMock()
    mock_resp.json.return_value = releases
    mock_resp.raise_for_status.return_value = None
    mock_get.return_value = mock_resp

    monkeypatch.setattr(httpx, "get", mock_get)

    # Run main with --list
    from gdl import github_downloader as gd

    class A:
        repo = "owner/repo"
        tag = None
        os = None
        arch = None
        blacklist = []
        no_decompress = False
        bin_name = None
        dest = Path(".")
        list_version = True

    monkeypatch.setattr(gd.tyro, "cli", lambda cls: A())
    gd.main()
    captured = capsys.readouterr()
    assert "v1.0" in captured.out
    assert "v1.1" in captured.out
    assert "v2.0" in captured.out
