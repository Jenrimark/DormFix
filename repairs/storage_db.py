"""
将上传文件存储到数据库，不占用本地磁盘。部署到平台时所有数据均在 DB。
"""
from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.conf import settings
from .models import StoredFile


class DatabaseStorage(Storage):
    """文件存数据库，路径格式为 db/<id>。"""

    def _save(self, name, content):
        content_type = getattr(content, 'content_type', None) or 'application/octet-stream'
        if hasattr(content, 'read'):
            data = content.read()
        else:
            data = content
        obj = StoredFile.objects.create(name=name, content=data, content_type=content_type or '')
        return f'db/{obj.id}'

    def _open(self, name, mode='rb'):
        if not name.startswith('db/'):
            raise ValueError(f'DatabaseStorage only handles db/<id>, got {name}')
        pk = name.split('/')[1]
        obj = StoredFile.objects.get(pk=pk)
        return ContentFile(obj.content, name=obj.name)

    def exists(self, name):
        if not name.startswith('db/'):
            return False
        try:
            pk = name.split('/')[1]
            return StoredFile.objects.filter(pk=pk).exists()
        except (IndexError, ValueError):
            return False

    def delete(self, name):
        if not name.startswith('db/'):
            return
        try:
            pk = name.split('/')[1]
            StoredFile.objects.filter(pk=pk).delete()
        except (IndexError, ValueError):
            pass

    def size(self, name):
        if not name.startswith('db/'):
            return 0
        try:
            pk = name.split('/')[1]
            obj = StoredFile.objects.get(pk=pk)
            return len(obj.content)
        except (StoredFile.DoesNotExist, IndexError, ValueError):
            return 0

    def url(self, name):
        if not name.startswith('db/'):
            return ''
        base = settings.MEDIA_URL.rstrip('/')
        return f'{base}/{name}'

    def path(self, name):
        raise NotImplementedError('DatabaseStorage does not use local path.')
