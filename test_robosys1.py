#!/usr/bin/env python3
# Copyright (c) 2026 Ryoto Sunaga
# SPDX-License-Identifier: BSD-3-Clause

import os
import subprocess
import sys
import tempfile
import unittest

from datetime import date, datetime, time, timedelta
from pathlib import Path

from robosys1 import (
    count_today_characters,
    calculate_productivity
)


SCRIPT = Path(__file__).with_name("robosys1.py")


class TestRobosys1(unittest.TestCase):

    def setUp(self):

        today_time = datetime.combine(date.today(), time(12, 0))
        yesterday_time = datetime.combine(
            date.today() - timedelta(days=1),
            time(12, 0)
        )

        self.today_timestamp = int(today_time.timestamp())
        self.yesterday_timestamp = int(yesterday_time.timestamp())

    # ① 今日のコマンドを数える
    def test_today_commands(self):

        history = (
            f"#{self.today_timestamp}\n"
            "ls\n"
            f"#{self.yesterday_timestamp}\n"
            "pwd\n"
        )

        result = count_today_characters(history, date.today())

        self.assertEqual(result, 2)

    # ② 昨日のコマンドを除外する
    def test_yesterday_commands(self):

        history = (
            f"#{self.yesterday_timestamp}\n"
            "python3 --version\n"
        )

        result = count_today_characters(history, date.today())

        self.assertEqual(result, 0)

    # ③ 複数行のコマンドを数える
    def test_multiple_lines(self):

        command = "echo one\necho two"

        history = (
            f"#{self.today_timestamp}\n"
            f"{command}\n"
        )

        result = count_today_characters(history, date.today())

        self.assertEqual(result, len(command))

    # ④ 作業量を正しく計算する
    def test_productivity(self):

        result = calculate_productivity(2, 100)

        self.assertEqual(result, 50.0)

    # ⑤ 0時間をエラーにする
    def test_zero_hours(self):

        with self.assertRaises(ValueError):
            calculate_productivity(0, 100)

    # ⑥ nanをエラーにする
    def test_nan_hours(self):

        with self.assertRaises(ValueError):
            calculate_productivity(float("nan"), 100)

    # ⑦ マイナス時間をエラーにする
    def test_negative_hours(self):

        with self.assertRaises(ValueError):
            calculate_productivity(-1, 100)

    # ⑧ 標準入力と標準出力を確認する
    def test_standard_input_output(self):

        with tempfile.TemporaryDirectory() as temp_dir:

            history_file = Path(temp_dir) / "history"

            history_file.write_text(
                f"#{self.today_timestamp}\nls\n",
                encoding="utf-8"
            )

            env = os.environ.copy()
            env["TEXT_WORK_COUNTER_HISTORY_FILE"] = str(
                history_file
            )

            result = subprocess.run(
                [sys.executable, str(SCRIPT)],
                input="2\n",
                text=True,
                capture_output=True,
                env=env
            )

            self.assertEqual(result.returncode, 0)
            self.assertIn("作業時間：2時間", result.stdout)
            self.assertIn("入力文字数：2文字", result.stdout)

            self.assertIn(
                "1時間当たりの入力文字数：1.0文字/時間",
                result.stdout
            )


if __name__ == "__main__":
    unittest.main()
