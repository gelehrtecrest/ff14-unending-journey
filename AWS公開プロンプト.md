# AWS S3 公開プロンプト

## 目的

このプロジェクトのウェブサイトコンテンツ (`docs` ディレクトリ全体) を、AWS S3バケットにアップロードし、公開するための手順を定義します。

`aws s3 sync` コマンドを使用することで、ローカルの `docs` ディレクトリとS3バケットの状態を効率的に同期させます。

---

## 前提条件

1.  **AWS CLIのインストール**: ご利用の環境に [AWS Command Line Interface (CLI)](https://aws.amazon.com/jp/cli/) がインストールされている必要があります。

2.  **AWS認証情報の設定**: S3バケットへのアクセス権限を持つIAMユーザーの認証情報（アクセスキーIDとシークレットアクセスキー）が設定済みである必要があります。設定がまだの場合は、以下のコマンドを実行して設定してください。
    ```bash
    aws configure
    ```

---

## デプロイ手順

### ステップ1: ドライラン（推奨）

まず、実際にファイルをアップロードせずに、どのファイルがアップロード対象になるかを確認します。意図しないファイルが含まれていないか、パスが正しいかを確認するための重要なステップです。

1.  **コマンドプロンプトまたはターミナルを開きます。**

2.  **プロジェクトのルートディレクトリに移動します。**
    ```bash
    cd D:\workspace\github\ff14-unending-journey
    ```

3.  **以下のドライランコマンドを実行します。**
    -   `--dryrun` フラグが付いているため、実際のアップロードは行われません。

    ```bash
    aws s3 sync ./docs s3://gelehrte.com/ff14-unending-journey/ --dryrun
    ```

4.  **実行結果を確認します。**
    -   `(dryrun)` と表示された、アップロード予定のファイルリストが表示されます。リストの内容に問題がないことを確認してください。

### ステップ2: 本番同期

ドライランで問題がないことを確認したら、実際にファイルをS3にアップロードします。

    ```bash
    aws s3 sync ./docs s3://gelehrte.com/ff14-unending-journey/ --delete
    ```

### ステップ3: CloudFrontキャッシュのクリア（必要な場合）

S3にファイルをアップロードしても、CloudFront（CDN）に古いキャッシュが残っていると、ブラウザで変更が反映されないことがあります。その場合は、キャッシュを手動でクリア（Invalidation）する必要があります。

1.  **ディストリビューションIDの確認**
    サイト (`www.gelehrte.com`) に関連付けられたCloudFrontのディストリビューションIDを以下のコマンドで確認します。

    ```bash
    aws cloudfront list-distributions --query "DistributionList.Items[?Aliases.Items[?@=='www.gelehrte.com']].Id | [0]" --output text
    ```

2.  **キャッシュのクリアを実行**
    取得したディストリビューションIDを使って、特定のファイルのキャッシュをクリアします。`<YOUR_DISTRIBUTION_ID>` の部分を、上記で取得したIDに置き換えてください。

    -   **特定のファイルのみクリアする場合 (例: index.html)**
        ```bash
        aws cloudfront create-invalidation --distribution-id <YOUR_DISTRIBUTION_ID> --paths "/ff14-unending-journey/index.html"
        ```

    -   **サイト全体のキャッシュをクリアする場合**
        サイト全体に大きな変更を加えた場合は、以下のコマンドで全てのファイルのキャッシュをクリアできます。
        ```bash
        aws cloudfront create-invalidation --distribution-id <YOUR_DISTRIBUTION_ID> --paths "/*"
        ```

3.  **完了**:
    -   コマンドが成功すると、キャッシュの無効化リクエストが作成されます。反映には数分かかることがあります。
    -   ブラウザで `https://www.gelehrte.com/ff14-unending-journey/index.html` にアクセスし、サイトが正しく更新されているか確認してください。（必要であればスーパーリロード `Ctrl+F5` を試してください）

---

## コマンド解説

-   `aws s3 sync`: AWS S3の機能の一つで、ディレクトリ間の同期を行います。
-   `./docs`: 同期元となるローカルのディレクトリです。
-   `s3://gelehrte.com/ff14-unending-journey/`: 同期先となるS3バケット名 (`gelehrte.com`) と、その中のフォルダ（プレフィックス `ff14-unending-journey/`）を指定します。
-   `--dryrun`: 実行される内容を事前に確認します。
-   `--delete`: 同期元に存在しないファイルを、同期先から削除します。
-   `aws cloudfront create-invalidation`: CloudFrontのキャッシュを無効化します。

**注意:** S3同期コマンドでファイルが公開されるためには、S3バケットに適切な「バケットポリシー」が設定されている必要があります。もしアップロード後にファイルが表示されない場合は、S3バケットのアクセス許可設定をご確認ください。