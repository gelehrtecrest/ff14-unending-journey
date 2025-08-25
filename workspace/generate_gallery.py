
import os
import re
import argparse

def generate_html(project_root, target_dir, language):
    """
    指定された情報に基づいて画像ギャラリーのHTMLページを生成します。
    """
    # --- パスの設定 ---
    # ルートからの絶対パス
    full_target_dir = os.path.join(project_root, target_dir)
    
    # 各種ファイルのパス
    header_file = os.path.join(project_root, 'header.txt')
    footer_file = os.path.join(project_root, 'footer.txt')
    md_file = os.path.join(full_target_dir, f'index_{language}.md')
    output_html_file = os.path.join(full_target_dir, f'index_{language}.html')
    css_file = os.path.join(project_root, 'css', 'index.css')
    js_file = os.path.join(project_root, 'js', 'index.js')

    # --- 必要なファイルの存在チェック ---
    required_files = [header_file, footer_file, md_file, css_file, js_file]
    for f in required_files:
        if not os.path.exists(f):
            print(f"エラー: 必須ファイルが見つかりません: {f}")
            return

    # --- 相対パスの計算 ---
    # target_dirの深さを計算して、CSS/JSへのパスを生成
    depth = len(target_dir.split(os.sep))
    relative_path_prefix = '../' * depth
    css_rel_path = os.path.join(relative_path_prefix, 'css', 'index.css').replace('\\', '/')
    js_rel_path = os.path.join(relative_path_prefix, 'js', 'index.js').replace('\\', '/')

    # --- ファイル内容の読み込み ---
    with open(header_file, 'r', encoding='utf-8') as f:
        header_content = f.read()
    with open(footer_file, 'r', encoding='utf-8') as f:
        footer_content = f.read()
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # --- HTMLコンテンツの生成 ---
    # Markdownから画像ギャラリー部分を生成
    gallery_html = '<div class="image-gallery" id="image-gallery">\n'
    for line in md_content.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        match = re.match(r'\[\[(.*?)\]\((.*?)\)\]\((.*?)\)', line)
        if match:
            alt_text, thumb_path, original_path = match.groups()
            gallery_html += f'    <img src="{thumb_path}" data-original="{original_path}" alt="{alt_text.strip()}">\n'
    gallery_html += '</div>'

    # モーダル用HTML
    modal_html = """
<!-- The Modal -->
<div id="myModal" class="modal">
  <span class="close">&times;</span>
  <img class="modal-content" id="img01">
</div>
"""

    # --- すべての要素を結合 ---
    final_html = f"""<!DOCTYPE html>
<html lang="{language}">
<head>
    <meta charset="UTF-8">
    <title>Unending Journey</title>
    {header_content}
    <link rel="stylesheet" href="{css_rel_path}">
</head>
<body>
    {gallery_html}
    {modal_html}
    {footer_content}
    <script src="{js_rel_path}"></script>
</body>
</html>"""

    # --- HTMLファイルへの書き込み ---
    with open(output_html_file, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"HTMLファイルを生成しました: {output_html_file}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='FF14 紀行録の画像ギャラリーHTMLを生成します。')
    parser.add_argument('--project_root', type=str, required=True, help='プロジェクトのルートディレクトリの絶対パス')
    parser.add_argument('--target_dir', type=str, required=True, help='対象ディレクトリの相対パス (例: docs/special/2025/Moonfire_Faire)')
    parser.add_argument('--language', type=str, required=True, choices=['j', 'e'], help='言語 (j または e)')
    
    args = parser.parse_args()
    
    generate_html(args.project_root, args.target_dir, args.language)
