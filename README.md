# robosys2026

ロボットシステム学の演習で作成したコマンドを管理するリポジトリです。

## 1. オリジナルコマンド：robosys1.py

### 概要

UbuntuのBash履歴から、その日にターミナルで実行したコマンドの文字数を自動集計するプログラムです。

作業時間だけを手入力すると、入力文字数と1時間当たりの入力文字数を計算します。

ターミナルでの作業量を振り返るために利用できます。

### 主な機能

- 作業時間の手入力
- Bash履歴から当日のコマンドを取得
- 入力文字数の自動集計
- 複数行コマンドに対応
- 1時間当たりの入力文字数を計算
- 不正な作業時間を検出

### 動作環境

- Ubuntu 24.04 LTS
- Bash
- Python 3.12以上

外部ライブラリは不要です。

### 使用前の設定

ホームディレクトリの `.bashrc` に、日時付き履歴を保存する設定が必要です。

```bash
export HISTFILE="$HOME/.bash_history"
export HISTTIMEFORMAT='%F %T '
export HISTSIZE=100000
export HISTFILESIZE=200000
export HISTCONTROL=
export HISTIGNORE=

shopt -s histappend cmdhist lithist

case ";${PROMPT_COMMAND-};" in
    *";history -a;"*) ;;
    *) PROMPT_COMMAND="history -a${PROMPT_COMMAND:+; $PROMPT_COMMAND}" ;;
esac
```

設定を追加した後、新しいターミナルを開いてください。

### 実行方法

```bash
chmod +x robosys1.py
./robosys1.py
```

作業時間だけを時間単位で入力します。

例：
- 30分：0.5
- 1時間：1
- 2時間：2

文章を入力する必要はありません。

### 実行例

入力：

```text
今日の作業時間を入力してください（時間）：2
```

出力例：

```text
--- 今日のターミナル作業結果 ---
作業日：2026-11-24
作業時間：2時間
入力文字数：1000文字
1時間当たりの入力文字数：500.0文字/時間
```

### 計算方法

1時間当たりの入力文字数は、次の式で計算します。

入力文字数 ÷ 作業時間

空白や記号、複数行コマンドの内部改行も文字数に含みます。

### 注意事項

- Bashの履歴に記録されたコマンドが集計対象です。
- nanoなどのエディタ内で入力した文章は対象外です。
- 履歴の日時情報を設定する前の入力は、正確に日別集計できません。
- パスワードや秘密情報をコマンドに直接入力しないでください。
- Bash履歴ファイルはGitHubに公開しません。

### テスト方法

```bash
python3 -m unittest discover -s . -p 'test_*.py' -v
```

## 2. 著作権・ライセンス

Copyright (c) 2026 Ryoto Sunaga

このプログラムはBSD 3-Clause Licenseの条件で公開しています。

詳細はLICENSEファイルを確認してください。
