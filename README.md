# Recallify

Slack と GitHub の日次活動を自動的に収集・分析し、LLM を使ってサマリーを生成するシステムです。

## 概要

Recallify は以下の機能を提供します：

### 実装済み機能

- ✅ プロジェクト構造とスケルトンコード
- ✅ データベーススキーマ（SQLite）
- ✅ APScheduler による定時実行
- ✅ タスクのモジュール化
- ✅ CLI レポート生成コマンド（プレースホルダー）

### これから実装する機能

- 🔲 GitHub API 連携（PR、レビュー、コメントの取得）
- 🔲 Slack API 連携（POST、スレッド会話の取得）
- 🔲 AWS Bedrock (Claude) によるサマリー生成
- 🔲 期間指定レポート生成
- 🔲 エラーハンドリングとリトライ機能
- 🔲 Web UI（将来的に）

## アーキテクチャ

### スケジューラーデーモン

深夜2時に以下の4つのタスクを順次実行：

1. **GitHub データ取得** - GitHub API から前日の活動データを取得
2. **Slack データ取得** - Slack API から前日の活動データを取得
3. **GitHub サマライズ** - 取得したデータを LLM でサマリー生成
4. **Slack サマライズ** - 取得したデータを LLM でサマリー生成

### データベース

SQLite で以下の2テーブルを管理：

- `raw_activities` - 生データ保存（source, date, data）
- `daily_summaries` - サマリー保存（source, date, summary, model_id）

## セットアップ

### 前提条件

- Docker & Docker Compose
- GitHub Personal Access Token
- Slack API Token
- AWS アカウント（Bedrock アクセス）

### 環境変数の設定

`.env.example` をコピーして `.env` を作成し、必要な値を設定：

```bash
cp .env.example .env
```

`.env` ファイルを編集：

```env
# Database
DATABASE_PATH=./data/recallify.db

# GitHub
GITHUB_TOKEN=your_github_token_here
GITHUB_REPOS=owner/repo1,owner/repo2

# Slack
SLACK_TOKEN=your_slack_token_here
SLACK_CHANNELS=channel1,channel2

# AWS Bedrock
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20241022-v2:0
```

### ビルドと起動

```bash
# ビルドして起動
docker compose up --build

# バックグラウンドで起動
docker compose up -d --build

# ログを確認
docker compose logs -f app

# 停止
docker compose down
```

## 使い方

### スケジューラーデーモン

コンテナを起動すると、スケジューラーが自動的に起動し、深夜2時に4つのタスクを実行します。

```bash
docker compose up -d
```

### 手動でタスクを実行

各タスクを個別に実行できます：

```bash
# GitHub データ取得
docker compose exec app uv run python -m src.tasks.fetch_github

# Slack データ取得
docker compose exec app uv run python -m src.tasks.fetch_slack

# GitHub サマライズ
docker compose exec app uv run python -m src.tasks.summarize_github

# Slack サマライズ
docker compose exec app uv run python -m src.tasks.summarize_slack
```

### CLI レポート生成

指定期間のアクティビティレポートを生成（実装予定）：

```bash
# 標準出力にレポート表示
docker compose exec app uv run python -m src.cli --from 2025-01-01 --to 2025-01-07

# ファイルに出力
docker compose exec app uv run python -m src.cli --from 2025-01-01 --to 2025-01-07 -o report.md
```

## プロジェクト構造

```
recallify/
├── src/
│   ├── __init__.py
│   ├── main.py                     # スケジューラーデーモン
│   ├── cli.py                      # CLI レポート生成
│   ├── config.py                   # 設定管理
│   ├── scheduler.py                # APScheduler 設定
│   ├── database/
│   │   ├── models.py               # SQLAlchemy モデル
│   │   └── connection.py           # DB 接続管理
│   ├── collectors/
│   │   ├── github.py               # GitHub API 連携
│   │   └── slack.py                # Slack API 連携
│   ├── llm/
│   │   ├── bedrock.py              # AWS Bedrock 連携
│   │   └── summarizer.py           # サマリー生成
│   └── tasks/
│       ├── fetch_github.py         # GitHub データ取得タスク
│       ├── fetch_slack.py          # Slack データ取得タスク
│       ├── summarize_github.py     # GitHub サマライズタスク
│       └── summarize_slack.py      # Slack サマライズタスク
├── data/                           # データベース保存先
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── .env.example
└── README.md
```

## 開発

### 依存関係

主要な依存パッケージ：

- `apscheduler` - タスクスケジューリング
- `sqlalchemy` - データベース ORM
- `boto3` - AWS Bedrock 連携
- `pygithub` - GitHub API
- `slack-sdk` - Slack API
- `xid` - ユニークID生成
- `click` - CLI フレームワーク
- `python-dotenv` - 環境変数管理

### データベース確認

SQLite データベースに直接アクセス：

```bash
docker compose exec app sqlite3 /app/data/recallify.db

# テーブル確認
.tables

# データ確認
SELECT * FROM raw_activities ORDER BY created_at DESC LIMIT 5;
SELECT * FROM daily_summaries ORDER BY created_at DESC LIMIT 5;

# 終了
.quit
```

## ライセンス

MIT License

## 貢献

Issue や Pull Request を歓迎します。
