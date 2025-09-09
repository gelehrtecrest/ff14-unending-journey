import os
import re
import argparse
from pathlib import Path

def generate_html(project_root, target_dir, language, custom_title):
    project_root = Path(project_root).resolve()
    target_dir_path = project_root / target_dir
    md_file = target_dir_path / f'index_{language}.md'
    output_html_file = target_dir_path / f'index_{language}.html'

    if not md_file.exists():
        print(f"エラー: 必須ファイルが見つかりません: {md_file}")
        return

    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    if custom_title:
        title = custom_title
    else:
        title_parts = [part.replace("_", " ").title() for part in target_dir.split(os.sep) if part.lower() not in ['docs', 'special']]
        title = " ".join(title_parts)

    try:
        docs_dir_path = project_root / 'docs'
        path_inside_docs = target_dir_path.relative_to(docs_dir_path)
        depth = len(path_inside_docs.parts)
        docs_path_prefix = '../' * depth
    except ValueError:
        print(f"エラー: target_dir '{target_dir}' は 'docs' ディレクトリの中にありません。")
        return

    css_rel_path = f'{docs_path_prefix}css/main_index.css'
    bootstrap_js_rel_path = f'{docs_path_prefix}js/bootstrap.min.js'
    gallery_js_rel_path = f'{docs_path_prefix}js/gallery_modal.js'
    root_index_path = f'{docs_path_prefix}index.html'

    gallery_html_parts = ['<div class="image-gallery" id="image-gallery">']
    for line in md_content.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        match = re.match(r'\[!\[(.*?)\]\((.*?)\)\]\((.*?)\)', line)
        if match:
            alt_text, thumb_path, original_path = match.groups()
            thumb_path = thumb_path if thumb_path.startswith('./') else './' + thumb_path
            original_path = original_path if original_path.startswith('./') else './' + original_path
            gallery_html_parts.append(f"    <a href='{original_path}' data-bs-toggle='modal' data-bs-target='#imageModal' data-bs-original='{original_path}'><img src='{thumb_path}' class='img-thumbnail' alt='{alt_text.strip()}'></a>")
    gallery_html_parts.append('</div>')
    gallery_html = "\n".join(gallery_html_parts)

    try:
        with open(project_root / 'header_special.txt', 'r', encoding='utf-8') as f:
            header_content = f.read()
    except FileNotFoundError:
        header_content = ""

    try:
        with open(project_root / 'footer.txt', 'r', encoding='utf-8') as f:
            footer_content = f.read()
    except FileNotFoundError:
        footer_content = ""

    header_content = header_content.replace('{title}', title)
    header_content = header_content.replace('{lang}', language)
    header_content = header_content.replace('{relative_path_prefix}css/index.css', css_rel_path)
    header_content = header_content.replace('{root_index_path}', root_index_path)

    final_html_template = '''
{header_content}
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
<script src="{bootstrap_js_rel_path}"></script>
<script src="{gallery_js_rel_path}"></script>
</body>
</html>'''

    final_html = final_html_template.format(
        header_content=header_content,
        gallery_html=gallery_html,
        footer_content=footer_content,
        bootstrap_js_rel_path=bootstrap_js_rel_path,
        gallery_js_rel_path=gallery_js_rel_path
    )

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