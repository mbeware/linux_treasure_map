#!/usr/bin/env python3
import sys
from pathlib import Path

def standardize(title: str) -> str:
    """
    Convert a heading title into a safe filename:
    - lowercase
    - spaces replaced by underscores
    - keep only letters, numbers, underscores, and dashes
    """
    result = []
    for char in title.lower().strip():
        if char.isalnum() or char in ("_", "-"):
            result.append(char)
        elif char.isspace():
            result.append("_")
        # everything else is ignored
    return "".join(result)

def main(markdown_file: Path):
    if not markdown_file.exists():
        print(f"Error: file not found -> {markdown_file}")
        sys.exit(1)

    output_dir = markdown_file.parent / "topics"
    output_dir.mkdir(exist_ok=True)

    created = 0

    with markdown_file.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip()

            # Detect level-3 markdown headings
            if line.startswith("### "):
                title = line[4:].strip()
                filename = standardize(title) + ".md"
                file_path = output_dir / filename

                if file_path.exists():
                    print(f"Skipped (already exists): {filename}")
                    continue

                file_path.write_text(
                    f"# {title}\n\n",
                    encoding="utf-8"
                )

                print(f"Created: {filename}")
                created += 1

    if created == 0:
        print("No level-3 headings found.")
    else:
        print(f"Done. {created} files created.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: extract_topics.py <markdown_file>")
        sys.exit(1)

    main(Path(sys.argv[1]))
