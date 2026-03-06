# Markdoor 面接前タスク: Todo管理アプリ

FastAPI + SQLite を使って、バックエンド実装を中心にした Todo 管理アプリを作成しました。  
課題の要件をベースに、CRUD・状態管理・データ永続化・最小限のUIまでを実装しています。

## 技術スタック

- **Backend**: Python, FastAPI, SQLAlchemy
- **Database**: SQLite
- **Frontend**: HTML/CSS/JavaScript (Vanilla)
- **Test**: pytest, FastAPI TestClient

## 機能一覧

### 実装済み

- タスク作成（タイトル必須・詳細任意）
- タスク一覧取得
- タスク更新（タイトル/詳細/完了状態）
- タスク削除
- 完了/未完了の切り替え
- 完了状態でのフィルタリング（全件/完了済み/未完了）
- 作成/更新日時の自動付与
- SQLiteによるデータ永続化
- フロントエンドでの即時フィードバック（トースト表示）
- 入力バリデーション（空タイトル時のエラー表示）

### スコープ外（未実装）

- ユーザー認証
- マルチユーザー対応
- リアルタイム共同編集
- 高度な通知機能
- カレンダー連携
- インポート/エクスポート

## セットアップ手順

### 1. 依存関係をインストール

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. アプリを起動

```bash
uvicorn app.main:app --reload
```

### 3. アクセス

- アプリ: http://127.0.0.1:8000
- APIドキュメント: http://127.0.0.1:8000/docs

## API概要

- `GET /api/tasks?completed=true|false` タスク一覧取得
- `POST /api/tasks` タスク作成
- `PUT /api/tasks/{task_id}` タスク更新
- `DELETE /api/tasks/{task_id}` タスク削除

## テスト実行

```bash
pytest -q
```

## 設計メモ

- `app/main.py` に **アプリ生成関数 (`create_app`)** を置き、テスト時にDBを差し替えられる構成。
- `crud.py` でDB操作責務を分離し、保守性・拡張性を確保。
- `schemas.py` で入出力バリデーションを定義。
- 将来的に認証やユーザー別タスクへ拡張しやすいように、層構造を意識。
