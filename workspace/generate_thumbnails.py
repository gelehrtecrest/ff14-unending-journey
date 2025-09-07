import argparse
import os
import shutil
import subprocess

def generate_thumbnails(project_root, target_dir_rel, language):
    """
    Generates thumbnails and a markdown file for a gallery.

    Args:
        project_root (str): The absolute path to the project's root directory.
        target_dir_rel (str): The relative path from the project root to the target gallery directory.
        language (str): The language code ('j' or 'e').
    """
    target_dir_abs = os.path.join(project_root, target_dir_rel)
    img_dir = os.path.join(target_dir_abs, f"image_{language}")
    thumb_dir = os.path.join(target_dir_abs, f"image_{language}_thumb")
    md_file = os.path.join(target_dir_abs, f"index_{language}.md")

    if not os.path.isdir(img_dir):
        print(f"Error: Image directory not found at '{img_dir}'")
        return

    print("Cleaning up old files and directories...")
    if os.path.exists(md_file):
        os.remove(md_file)
    if os.path.exists(thumb_dir):
        shutil.rmtree(thumb_dir)
    os.makedirs(thumb_dir)
    print(f"Thumbnail directory created at: {thumb_dir}")

    print("Generating thumbnails and markdown...")
    try:
        image_files = sorted([f for f in os.listdir(img_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))])
        with open(md_file, 'w', encoding='utf-8') as f:
            for filename in image_files:
                print(f"Processing {filename}...")
                src_path = os.path.join(img_dir, filename)
                thumb_filename = filename + ".thumb.jpg"
                dest_path = os.path.join(thumb_dir, thumb_filename)

                # Run ImageMagick command
                result = subprocess.run(
                    ["magick", "convert", "-resize", "480x270", src_path, dest_path],
                    check=True,
                    capture_output=True,
                    text=True,
                    encoding='utf-8'
                )

                # Write markdown line
                f.write(f"[![{{filename}}](./image_{{language}}_thumb/{{thumb_filename}})](./image_{{language}}/{filename})\n\n")
        print(f"Successfully generated markdown file: {md_file}")

    except subprocess.CalledProcessError as e:
        print(f"Error during ImageMagick execution: {e}")
        print(f"Stderr: {e.stderr}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate thumbnails and markdown for an image gallery.")
    parser.add_argument("--project_root", type=str, default=".", help="The root directory of the project.")
    parser.add_argument("--target_dir", type=str, required=True, help="Relative path to the target directory under the project root (e.g., 'docs/special/2025/MyNewQuest').")
    parser.add_argument("--language", type=str, required=True, choices=['j', 'e'], help="Language for the gallery ('j' for Japanese, 'e' for English).")

    args = parser.parse_args()

    project_root_abs = os.path.abspath(args.project_root)
    generate_thumbnails(project_root_abs, args.target_dir, args.language)