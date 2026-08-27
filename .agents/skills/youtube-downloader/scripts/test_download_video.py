"""Regression tests for local, opt-in video downloads."""

import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch


SCRIPT_PATH = Path(__file__).with_name("download_video.py")
SPEC = importlib.util.spec_from_file_location("download_video", SCRIPT_PATH)
download_video = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(download_video)


class DownloaderDefaultsTest(unittest.TestCase):
    def test_default_output_path_is_a_downloads_directory_below_the_current_directory(self):
        default_output_path = download_video.download_video.__defaults__[0]
        self.assertEqual(default_output_path, str(Path.cwd() / "downloads"))

    def test_missing_yt_dlp_reports_install_instructions_without_installing(self):
        with patch.object(download_video.subprocess, "run", side_effect=[FileNotFoundError(), None]):
            with self.assertRaisesRegex(RuntimeError, "yt-dlp"):
                download_video.check_yt_dlp()


if __name__ == "__main__":
    unittest.main()
