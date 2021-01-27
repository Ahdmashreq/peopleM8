import tempfile
import os


class BaseStorage:
    def __init__(self, name=None):
        self.name = name

    def save(self, data, mode='w'):
        raise NotImplementedError

    def read(self, read_mode='r'):
        raise NotImplementedError

    def remove(self):
        raise NotImplementedError


class TempFolderStorage(BaseStorage):
    def open(self, mode='r'):
        if self.name:
            return open(self.get_full_path(), mode)
        else:
            tmp_file = tempfile.NamedTemporaryFile(delete=False)
            self.name = tmp_file.name
            return tmp_file

    def save(self, data, mode='w'):
        with self.open(mode=mode) as file:
            file.write(data)

    def read(self, mode='r'):
        with self.open(mode=mode) as file:
            return file.read()

    def remove(self):
        os.remove(self.get_full_path())

    def get_full_path(self):
        return os.path.join(
            tempfile.gettempdir(),
            self.name
        )
