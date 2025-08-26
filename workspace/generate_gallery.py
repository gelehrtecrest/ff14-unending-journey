import os
import re
import argparse
from pathlib import Path

def generate_html(project_root, target_dir, language, custom_title):
    # パスの正規化
    project_root = Path(project_root).resolve()
    target_dir_path = project_root / target_dir
    
    md_file = target_dir_path / f'index_{language}.md'
    output_html_file = target_dir_path / f'index_{language}.html'

    if not md_file.exists():
        print(f"エラー: 必須ファイルが見つかりません: {md_file}")
        return

    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # タイトルの決定
    if custom_title:
        title = custom_title
    else:
        # target_dirから自動生成
        title_parts = [part.replace("_", " ").title() for part in target_dir.split(os.sep) if part.lower() not in ['docs', 'special']]
        title = " ".join(title_parts)

    # --- 相対パスの計算 ---
    try:
        # プロジェクトルートからの相対パスを取得
        relative_to_root = target_dir_path.relative_to(project_root)
        # docsディレクトリからの相対的な深さを計算
        depth = len(relative_to_root.parts)
        relative_path_prefix = '../' * depth
    except ValueError:
        # プロジェクトルート外のパスが指定された場合など
        print(f"エラー: target_dir '{target_dir}' は project_root '{project_root}' の中にありません。")
        return

    # ルートの各リソースへのパス
    css_rel_path = f'{relative_path_prefix}css/index.css'
    js_rel_path = f'{relative_path_prefix}js/index.js'
    root_index_path = f'{relative_path_prefix}index.html'

    gallery_html = '<div class="image-gallery" id="image-gallery">\n'
    for line in md_content.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        # Markdownリンク形式 `[![alt-text](thumb_path)](original_path)` を正規表現で探す
        match = re.match(r'\[!\[(.*?)\]\((.*?)\)\]\((.*?)\)', line)
        if match:
            alt_text, thumb_path, original_path = match.groups()
            # パスが `./` で始まっていることを確認
            thumb_path = thumb_path if thumb_path.startswith('./') else './' + thumb_path
            original_path = original_path if original_path.startswith('./') else './' + original_path
            gallery_html += f"    <a href='{original_path}' data-bs-toggle='modal' data-bs-target='#imageModal' data-bs-original='{original_path}'><img src='{thumb_path}' class='img-thumbnail' alt='{alt_text.strip()}'></a>\n"
    gallery_html += '</div>'

    # header.txt と footer.txt の内容を読み込む
    try:
        with open(project_root / 'header_special.txt', 'r', encoding='utf-8') as f:
            header_content = f.read()
    except FileNotFoundError:
        print("警告: header_special.txt が見つかりません。")
        header_content = ""

    try:
        with open(project_root / 'footer.txt', 'r', encoding='utf-8') as f:
            footer_content = f.read()
    except FileNotFoundError:
        print("警告: footer.txt が見つかりません。")
        footer_content = ""

    # プレースホルダーを置換
    header_content = header_content.replace('{title}', title)
    header_content = header_content.replace('{lang}', language)
    header_content = header_content.replace('{relative_path_prefix}', relative_path_prefix)
    header_content = header_content.replace('{root_index_path}', root_index_path)


    final_html = f"""{header_content}
{gallery_html}
<!-- Modal -->
<div class="modal fade" id="imageModal" tabindex="-1" aria-labelledby="imageModalLabel" aria-hidden="true">
  <div class="modal-dialog modal-xl modal-dialog-centered">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <img src="" class="img-fluid" id="modalImage">
      </div>
    </div>
  </div>
</div>
{footer_content}
<script src="{js_rel_path}"></script>
</body>
</html>"""

    with open(output_html_file, 'w', encoding='utf-8') as f:
        f.write(final_html)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='指定されたディレクトリから画像ギャラリーHTMLを生成します。')
    parser.add_argument('--project_root', type=str, required=True, help='プロジェクトのルートディレクトリ')
    parser.add_argument('--target_dir', type=str, required=True, help='HTMLを生成する対象のディレクトリ (docsから始まる相対パス)')
    parser.add_argument('--language', type=str, required=True, choices=['j', 'e'], help='言語 (j または e)')
    parser.add_argument('--title', type=str, help='HTMLのタイトル (任意)')

    args = parser.parse_args()

    generate_html(args.project_root, args.target_dir, args.language, args.title)

    output_html_file = Path(args.project_root) / args.target_dir / f'index_{args.language}.html'
    print(f"HTMLが正常に生成されました: {output_html_file}")
