import re
import os
from pathlib import Path

def parse_markdown(md_content):
    sections = []
    current_section = None
    current_card = None

    for line in md_content.splitlines():
        line = line.strip()
        # Section Title (##)
        if line.startswith('## '):
            section_title = line[3:].strip()
            current_section = {'title': section_title, 'cards': []}
            sections.append(current_section)
            current_card = None
        # Card Title (###)
        elif line.startswith('### ') and current_section is not None:
            card_title = line[4:].strip()
            current_card = {'title': card_title, 'links': []}
            current_section['cards'].append(current_card)
        # Link Item (- [text](url))
        elif line.startswith('- ') and current_card is not None:
            match = re.match(r'-\s*\[(.*?)\]\((.*?)\)', line)
            if match:
                link_text = match.group(1)
                link_url = match.group(2)
                current_card['links'].append({'text': link_text, 'url': link_url})
    return sections

def generate_html_from_sections(sections):
    cards_html = ''
    for section in sections:
        if not section['cards']:
            continue
        
        section_id = section['title'].lower().replace(' ', '-')
        cards_html += f'<section id="{section_id}" class="mb-5">\n'
        cards_html += f'    <h2 class="section-title">{section['title']}</h2>\n'
        cards_html += f'    <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">\n'
        for card in section['cards']:
            cards_html += '        <div class="col">\n'
            cards_html += f'            <div class="card h-100 card-item">\n'
            cards_html += f'                <div class="card-body">\n'
            cards_html += f'                    <h5 class="card-title">{card["title"]}</h5>\n'
            cards_html += f'                    <ul class="list-unstyled mb-0">\n'
            for link in card['links']:
                cards_html += f'                        <li><a href="{link["url"]}">{link["text"]}</a></li>\n'
            cards_html += f'                    </ul>\n'
            cards_html += f'                </div>\n'
            cards_html += f'            </div>\n'
            cards_html += '        </div>\n'
        cards_html += '    </div>\n'
        cards_html += '</section>\n'

    return cards_html

def main():
    project_root = Path(__file__).parent.parent.resolve()
    md_file_path = project_root / 'docs' / 'index.md'
    output_html_path = project_root / 'docs' / 'index.html'
    
    # header_index.txt と footer_index.txt の内容を読み込む
    try:
        with open(project_root / 'header_index.txt', 'r', encoding='utf-8') as f:
            header_template = f.read()
    except FileNotFoundError:
        print("エラー: header_index.txt が見つかりません。テンプレートファイルを作成してください。")
        return

    try:
        with open(project_root / 'footer_index.txt', 'r', encoding='utf-8') as f:
            footer_template = f.read()
    except FileNotFoundError:
        print("エラー: footer_index.txt が見つかりません。テンプレートファイルを作成してください。")
        return

    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Markdownの解析とHTMLの生成
    sections = parse_markdown(md_content)
    main_content_html = generate_html_from_sections(sections)

    # 最終的なHTMLの組み立て
    final_html = header_template + main_content_html + footer_template

    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(final_html)

    print(f"Successfully generated {output_html_path}")

if __name__ == '__main__':
    main()
