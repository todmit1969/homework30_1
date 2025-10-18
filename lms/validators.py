from rest_framework.exceptions import ValidationError
import re

class VideoLinkValidator:
    def __init__(self, field):
        self.field = field
    def __call__(self, value):
        video_pattern = re.compile(r'^https?://(?:www\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w-]+')
        if not video_pattern.match(value['video_link']):
            raise ValidationError("Можно ссылку только с YouTube.com!")