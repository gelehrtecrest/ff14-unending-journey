# 高機能な画像ギャラリー生成プロンプト

## 目的

現在のディレクトリにある画像ディレクトリ（`image_j` または `image_e`）とサムネイルディレクトリ（`image_j_thumb` または `image_e_thumb`）を元に、ユーザー体験の高いインタラクティブな画像ギャラリーページを生成します。

既存のHTMLファイルは、多数の画像を単純に縦に並べているだけで一覧性が低く、使いづらいという問題を解決することを目的とします。

## 満たすべき要件

1.  **ファイル構成**
    -   HTML: `index_[言語].html` （例: `index_j.html` または `index_e.html`）
    -   CSS: `css/index.css` （`css` ディレクトリがなければ作成する）
    -   JavaScript: `js/index.js` （`js` ディレクトリがなければ作成する）

2.  **レイアウト**
    -   サムネイル画像は、レスポンシブ対応のグリッドレイアウトで表示すること。
    -   画面の幅に応じて、表示される列数が自動的に調整されるようにCSSを設計すること。

3.  **インタラクション**
    -   サムネイル画像をクリックすると、ページ遷移することなく、その場でモーダルウィンドウ（ライトボックス）が開き、対応する元画像が拡大表示されること。
    -   ライトボックス表示中は、背景が暗くなり、画像が際立つように演出すること。
    -   ライトボックスは、閉じるボタン、または背景の暗い部分をクリックすることで閉じられるようにすること。

4.  **動的な画像リスト**
    -   指定された言語に対応するサムネイルディレクトリ内の画像ファイルを読み取り、そのリストを元にHTMLのギャラリー部分を動的に生成すること。
    -   各サムネイル画像（例: `image_[言語]_thumb/ffxiv_xxxx.png.thumb.jpg`）は、クリックされた際に表示すべき元画像（例: `image_[言語]/ffxiv_xxxx.png`）のパス情報を保持していること。

5.  **タイトル設定の汎用化**
    -   HTMLの `<title>` タグおよび `<h1>` タグのテキストは、プロンプト実行時にユーザーが指定できるようにすること。
    -   ユーザーが「タイトル [任意の文字列]」のように指示した場合、その文字列をタイトルとして使用すること。
    -   タイトルが指定されなかった場合は、AIがユーザーにタイトルを問い合わせること。

6.  **言語設定の汎用化**
    -   プロンプト実行時にユーザーが言語（日本語: `j` または 英語: `e`）を指定できるようにすること。
    -   ユーザーが「言語 日本語」または「言語 英語」のように指示した場合、それに応じて以下のパスを決定すること。
        -   サムネイル画像ディレクトリ: `image_[言語]_thumb`
        -   元画像ディレクトリ: `image_[言語]`
        -   出力HTMLファイル名: `index_[言語].html`
        -   CSSファイル名: `css/index.css`
        -   JavaScriptファイル名: `js/index.js`
    -   言語が指定されなかった場合は、AIがユーザーに言語を問い合わせること。

7.  **共通のhead要素の追加**
    -   生成されるHTMLファイルの `<head>` セクションに、以下の共通要素を含めること。
        ```html
        <meta http-equiv="Content-type" content="text/html;charset=UTF-8">
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="twitter:card" content="summary_large_image">
        <meta name="twitter:site" content="gelehrte_crest">
        <meta property="og:title" content="英語で楽しむFF14のための紀行録">
        <meta property="og:description" content="本サイトは、ゲレの工房が企画「英語で楽しむFF14」のために作成されたサイトです。現在、私のPCフォルダには大量の画像が入っています。このファイルを外部の人にも公開し、誰でも画像を見れるように紀行録として使っていただければと思います。">
        <meta property="og:image" content="https://www.gelehrte.com/ff14-unending-journey/image/gelehrte_crest.png">
        <meta property="og:url" content="https://www.gelehrte.com/ff14-unending-journey/">
        <link rel="icon" href="https://www.gelehrte.com/image/favicon.ico">
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-98GV0TKBJV"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());

          gtag('config', 'G-98GV0TKBJV');
        </script>
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9341622472626262"
        crossorigin="anonymous"></script>
        ```

8.  **共通のフッター要素の追加**
    -   生成されるHTMLファイルの `</body>` タグの直前に、以下のフッター要素を含めること。
        ```html
        <footer class="footer mt-auto py-3 bg-light">
        <div class="container">
        <p><a href="/"><span class="text-muted">ゲレの工房へ</span></a></p>
        <p><span class="text-muted">© 2025 ゲレの工房</span></p>
        <p><span class="text-muted">Copyright © 英語で楽しむFF14のための紀行録 Project . All rights reserved</span></p>
        <p><span class="text-muted">Copyright © SQUARE ENIX CO., LTD. All Rights Reserved.</span></p>
        <p><span class="text-muted">記載されている会社名・製品名・システム名などは、各社の商標、または登録商標です。当サイトは、FF14プレイヤー発起によるイベント公式サイトです。株式会社スクウェア・エニックスとは関わりはありません。</span></p>
        </div>
        </footer>
        ```

9.  **トップページへのリンク**
    -   `<h1>`タグのすぐ下に、トップページ（`../../../index.html`）へのリンクを「トップページに戻る」というテキストで設置すること。

## 実行手順の提案

1.  **ユーザーからの言語指定を確認する。指定がない場合は、ユーザーに言語を問い合わせる。**
2.  **ユーザーからのタイトル指定を確認する。指定がない場合は、ユーザーにタイトルを問い合わせる。**
3.  手順1で決定した言語に基づき、サムネイル画像ディレクトリに存在するファイルの一覧を取得する。
4.  `css` と `js` ディレクトリが存在しない場合は、それぞれ作成する。
5.  `css/index.css` ファイルを作成し、グリッドレイアウトとライトボックスのスタイルを記述する。
6.  `js/index.js` ファイルを作成し、サムネイルのクリックイベントを検知してライトボックスの表示・非表示を制御するロジックを記述する。
7.  `index_[言語].html` を作成する。このHTMLには、CSSとJSファイルへのリンクを含め、手順3で取得したファイルリストに基づいて、各画像のサムネイルを表示するための `<img>` タグを並べる。この際、`<title>` タグと `<h1>` タグには、手順2で決定したタイトルを適用し、上記「共通のhead要素」に記載された全てのタグとスクリプトを含めること。**また、`<h1>`タグと「トップページに戻る」リンクを `<div class="container">` で囲んで追加すること。**
8.  **生成される `index_[言語].html` の `</body>` タグの直前に、上記「共通のフッター要素」に記載されたフッター要素を追加する。**