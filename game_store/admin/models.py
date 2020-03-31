from abc import ABCMeta, abstractmethod


class SelectItem:

    def __init__(self, storage, field_name):

        self._storage = storage
        self._field_name = field_name


class BaseModel(metaclass=ABCMeta):

    @property
    @abstractmethod
    def storage(self):
        pass

    @property
    @abstractmethod
    def fields(self):
        pass

    def __init__(self):
        self._primary_key = 0

    def __getattr__(self, item):

        if item in self.fields:
            return SelectItem(storage=self.storage, field_name=item)

        return self.__getattribute__(item)

    def insert(self, data):

        self.storage[self._primary_key] = data
        self._primary_key += 1

    def get_by_id(self, primary_key):

        return self.storage[primary_key]


class Users(BaseModel):

    _fields = {'name', 'surname', 'email'}

    @property
    def storage(self):
        return self._storage

    @property
    def fields(self):
        return self._fields

    def __init__(self):
        super().__init__()
        self._storage = {}

