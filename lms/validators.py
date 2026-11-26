from urllib.parse import urlparse

from django.core.exceptions import ValidationError

ALLOWED_HOSTS = {'youtube.com', 'www.youtube.com', 'm.youtube.com', 'youtu.be'}


def validate_video_url(value):
    """Для URLField: разрешены только ссылки на youtube."""
    if not value:
        return
    host = (urlparse(value).netloc or '').lower()
    if host.startswith('www.'):
        host = host[4:]
    if host not in ALLOWED_HOSTS:
        raise ValidationError(
            'Разрешены только ссылки на youtube.com, а не на сторонние ресурсы.'
        )


def validate_text_links(value):
    """Для текстовых полей (описаний): внутри текста ссылки — только на youtube."""
    if not value:
        return
    import re
    for url in re.findall(r'https?://[^\s<>"\']+', value):
        validate_video_url(url)
