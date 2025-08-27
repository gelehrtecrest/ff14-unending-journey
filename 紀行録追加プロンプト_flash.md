# 新規紀行録ページ作成手順（簡易版）

この手順書は、画像フォルダから新しい紀行録ページ（HTML）を作成するためのコマンドを記載しています。

## 前提条件

- ImageMagickがインストール済みであること。
- Pythonがインストール済みであること。

## 手順

**例として `docs/special/2025/MyNewQuest` ディレクトリで、言語 `j` (日本語) のページを作成します。**

### ステップ1: サムネイルと画像リストの作成

1.  **作業ディレクトリへ移動**
    コマンドプロンプトを開き、対象の紀行録ディレクトリに移動します。
    ```bash
    cd D:\workspace\github\ff14-unending-journey\docs\special\2025\MyNewQuest
    ```

2.  **古いファイルを削除**
    既存のサムネイルフォルダとMarkdownファイルを削除します。
    ```bash
    if exist index_j.md del index_j.md
    if exist image_j_thumb rmdir /s /q image_j_thumb
    ```

3.  **サムネイルとMarkdownファイルを生成**
    以下のコマンドを実行して、`image_j` フォルダ内の全画像からサムネイル (`image_j_thumb`へ) と `index_j.md` を一括で作成します。
    ```bash
    mkdir image_j_thumb && (for %f in (image_j\*.*) do @echo [![](.\image_j_thumb\%~nxf.thumb.jpg)](.\image_j\%~nxf)>> index_j.md && magick convert -resize 480x270 "image_j\%f" "image_j_thumb\%~nxf.thumb.jpg")
    ```
    *注意: このコマンドはコマンドプロンプトで直接実行する形式です。バッチファイルにする場合は `%f` を `%%f` に変更してください。*

### ステップ2: HTMLページの生成

1.  **プロジェクトのルートディレクトリへ移動**
    ```bash
    cd D:\workspace\github\ff14-unending-journey
    ```

2.  **HTML生成スクリプトを実行**
    以下のコマンドを実行して、`index_j.md` から `index_j.html` を生成します。
    ```bash
    python workspace/generate_gallery.py --target_dir "docs/special/2025/MyNewQuest" --language "j" --title "新しいクエスト"
    ```
    *`--title` の "新しいクエスト" の部分は、ページのタイトルに合わせて変更してください。*

以上で新しい紀行録ページが作成されます。
