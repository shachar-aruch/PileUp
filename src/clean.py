import re
import ftfy


def clean_text(raw: str) -> str:
    text = ftfy.fix_text(raw)
    lines = text.splitlines()
    lines = [line for line in lines if line.strip() == "" or re.search(r'[a-zA-Z0-9]', line)]
    text = "\n".join(lines)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()
