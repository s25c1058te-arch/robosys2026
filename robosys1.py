#!/usr/bin/env python3
# Copyright (c) 2026 Ryoto Sunaga
# SPDX-License-Identifier: BSD-3-Clause

import math
import os
import re
import sys
from datetime import date, datetime
from pathlib import Path


def parse_history_entries(history_text):
    """Bash履歴から日時とコマンドを取り出す。"""

    entries = []
    current_timestamp = None
    current_command = []

    for line in history_text.splitlines():

        match = re.fullmatch(r"#(\d+)", line)

        if match:
            if current_timestamp is not None:
                entries.append(
                    (current_timestamp, "\n".join(current_command))
                )

            current_timestamp = int(match.group(1))
            current_command = []

        elif current_timestamp is not None:
            current_command.append(line)

    if current_timestamp is not None:
        entries.append(
            (current_timestamp, "\n".join(current_command))
        )

    return entries


def count_today_characters(history_text, target_date):
    """今日のコマンドの文字数を合計する。"""

    total_characters = 0

    for timestamp, command in parse_history_entries(history_text):

        try:
            command_date = datetime.fromtimestamp(timestamp).date()
        except (ValueError, OSError, OverflowError):
            continue

        if command_date == target_date:
            total_characters += len(command)

    return total_characters


def calculate_productivity(work_hours, characters):
    """1時間当たりの入力文字数を計算する。"""

    if not math.isfinite(work_hours) or work_hours <= 0:
        raise ValueError(
            "作業時間は0より大きい数値にしてください。"
        )

    return characters / work_hours


def main():

    # 作業時間をコマンドライン引数から受け取る
    if len(sys.argv) != 2:
        print(
            "使い方: ./robosys1.py 作業時間（時間）",
            file=sys.stderr
        )
        return 1

    try:
        work_hours = float(sys.argv[1])

        if not math.isfinite(work_hours) or work_hours <= 0:
            raise ValueError

    except ValueError:
        print(
            "エラー：作業時間は0より大きい数値にしてください。",
            file=sys.stderr
        )
        return 1

    # 履歴ファイルの場所を取得する
    history_path = Path(
        os.environ.get(
            "TEXT_WORK_COUNTER_HISTORY_FILE",
            os.environ.get(
                "HISTFILE",
                str(Path.home() / ".bash_history")
            )
        )
    ).expanduser()

    # 履歴を読み込む
    try:
        history_text = history_path.read_text(
            encoding="utf-8",
            errors="replace"
        )

    except OSError:
        print(
            "履歴ファイルを読み込めませんでした。",
            file=sys.stderr
        )
        return 1

    # 日時付き履歴があるか確認する
    entries = parse_history_entries(history_text)

    if not entries:
        print(
            "日時付きのコマンド履歴がありません。",
            file=sys.stderr
        )
        return 1

    # 今日の日付を取得する
    today = date.today()

    # 今日の入力文字数を集計する
    characters = count_today_characters(
        history_text,
        today
    )

    # 1時間当たりの作業量を計算する
    productivity = calculate_productivity(
        work_hours,
        characters
    )

    # 標準出力には計算結果だけを出す
    print(
        f"{today},{work_hours:g},{characters},{productivity:.1f}"
    )

    if characters == 0:
        print(
            "注意：今日のコマンド履歴が0文字です。",
            file=sys.stderr
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
    