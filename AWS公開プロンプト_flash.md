# AWS S3へのデプロイ手順（簡易版）

この手順書は、ウェブサイトのコンテンツをAWS S3にアップロードするためのコマンドを記載しています。

## 前提条件

- AWS CLIがインストール済みであること。
- `aws configure` コマンドで認証情報が設定済みであること。

## デプロイ手順

**重要:** コマンドはプロジェクトのルートディレクトリ (`D:\workspace\github\ff14-unending-journey`) で実行してください。

### ステップ1: 変更内容の確認（ドライラン）

まず、どのファイルがアップロードされるかを確認します。実際のアップロードは行われません。

```bash
aws s3 sync ./docs s3://gelehrte.com/ff14-unending-journey/ --dryrun
```

### ステップ2: ファイルの同期（本番アップロード）

確認後、実際にファイルをアップロードします。ローカルの`docs`ディレクトリにないファイルはS3上から削除されます。

```bash
aws s3 sync ./docs s3://gelehrte.com/ff14-unending-journey/ --delete
```

### ステップ3: 公開サイトの確認

ブラウザで `http://gelehrte.com/ff14-unending-journey/index.html` を開き、サイトが正しく更新されていることを確認してください。
