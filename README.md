# githubactions-cicd

GitHub Actions + Cloud Run Functions (Python) サンプル

## 概要

このリポジトリは、Google Cloud Run Functions（Gen2）にデプロイ可能な、超シンプルな Python 関数（functions-framework 利用）と、その自動デプロイ用 GitHub Actions ワークフローのサンプルです。

---

## ディレクトリ構成

- `main.py` : Cloud Run Functions 用のエントリポイント関数
- `requirements.txt` : 必要なパッケージ（functions-framework のみ）
- `.github/workflows/ci.yml` : CI（Continuous Integration）用ワークフロー
- `.github/workflows/deploy-cloud-run.yml` : Cloud Run Functions への自動デプロイ用ワークフロー

---

## CI（Continuous Integration）

`.github/workflows/ci.yml` で以下の CI 処理が自動実行されます：

### トリガー

- PR 作成時（main/develop ブランチ向け）

### 実行内容

1. **テストジョブ**

   - Python 3.11 環境セットアップ
   - 依存関係インストール（pip cache 利用）
   - リンティング（flake8）
   - コードフォーマットチェック（black）
   - コードカバレッジ生成・Codecov アップロード

2. **セキュリティジョブ**

   - 依存関係セキュリティチェック（safety）
   - コードセキュリティスキャン（bandit）
   - セキュリティレポート生成・アーティファクト保存

3. **関数テストジョブ**
   - 関数のインポートテスト
   - functions-framework 動作確認
   - 関数ファイルのアーティファクト保存

---

## ローカル実行方法

```bash
# 依存パッケージのインストール
pip install -r requirements.txt

# ローカルで関数を起動（http://localhost:8080）
functions-framework --target=github_actions_cicd --port=8080
```

---

## デプロイ用 GitHub Actions ワークフロー

`.github/workflows/deploy-cloud-run.yml` で、main ブランチ push 時や手動実行で Cloud Run Functions に自動デプロイされます。

### 必要な GitHub Secrets

- `GCP_PROJECT_ID` : GCP プロジェクト ID
- `GCP_SA_KEY` : サービスアカウントの JSON キー

### デプロイ先の関数名・リージョン等はワークフロー内で指定しています。

---

## デプロイ先での挙動

- HTTP リクエストを受けると、"Hello world"を標準出力し、`finish` という文字列を返します。
- 例: curl で確認

```bash
curl http://YOUR_CLOUD_FUNCTION_URL/
# => finish
```

---

## Cloud Run Functions 用デプロイコマンド例（手動）

```bash
gcloud functions deploy github-actions-cicd \
  --gen2 \
  --runtime=python311 \
  --region=asia-northeast1 \
  --source=. \
  --entry-point=github_actions_cicd \
  --trigger=http \
  --allow-unauthenticated
```

---

## 注意点

- このサンプルは functions-framework の最小構成です。
- Flask 等の Web フレームワークは使っていません。
- レスポンスは文字列/JSON どちらも返せます。
- GCP のサービスアカウント権限や API 有効化は事前に行ってください。

---

## ライセンス

MIT License
