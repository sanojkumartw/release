import re

def slugify(text: str) -> str:
    slug = text.lower()
    slug = re.sub(r'[^a-z0-9]+', '_', slug)
    return slug.strip('_')
