from openai import OpenAI
import sys
from pathlib import Path

client = OpenAI()

SYSTEM_MSG = (
    "You are a strict but supportive web development mentor helping a college "
    "student finalize an honors-level ePortfolio site. You MUST explain issues "
    "clearly so they can learn, not just silently fix them."
)

TEMPLATE = """
You will review a single HTML file from a student's ePortfolio website.

Tasks:
1. Identify any HTML syntax errors or invalid structure
   (unclosed tags, wrong nesting, missing <head> pieces, etc.).
2. Point out accessibility issues
   (missing alt text on important images, heading order, etc.).
3. Suggest improvements for readability and maintainability
   (simpler structure, less repetition), but do NOT completely change their visual style.
4. Keep the tone constructive and educational.

Output format:

ISSUES:
- bullet list of concrete problems and specific suggestions

CORRECTED FILE:
(full corrected version of the file)

Now review this file.

[FILE NAME]: {name}

[CONTENT START]
{content}
[CONTENT END]
"""


def review_file(path_str: str) -> None:
    path = Path(path_str)
    if not path.exists():
        print(f"Error: File '{path_str}' does not exist.")
        sys.exit(1)

    content = path.read_text(encoding="utf-8")
    user_prompt = TEMPLATE.format(name=path.name, content=content)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_MSG},
            {"role": "user", "content": user_prompt},
        ],
    )

    print(response.choices[0].message.content)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ai_review.py path/to/file.html")
        sys.exit(1)

    review_file(sys.argv[1])
