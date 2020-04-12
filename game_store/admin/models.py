from abc import ABCMeta, abstractmethod
import pdb

class SelectItem:

    def __init__(self, storage, field_name):

        self._storage = storage
        self._field_name = field_name

    def query(self, pred):
        find_data = {}
        for id, elem in self._storage.items():
            if self._field_name in elem and pred(elem[self._field_name]):
                find_data[id] = elem
        # pdb.set_trace()  #if smth goes wrong(debug)
        return find_data.values()


    def fetchone(self, pred):
        for item in self.query(pred=pred):
            return item


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

        data.update({self.primary_field_name: self._primary_key})
        self.storage[self._primary_key] = data
        self._primary_key += 1

    def get_by_id(self, primary_key):

        if self.storage[primary_key]['active']:
            return self.storage[primary_key]

class Users(BaseModel):

    _fields = {'user_id', 'name', 'surname', 'email', 'password', 'status', 'active'}

    @property
    def storage(self):
        return self._storage

    @property
    def fields(self):
        return self._fields

    @property
    def primary_field_name(self):
        return 'user_id'

    def __init__(self):
        super().__init__()
        self._storage = {}

    def insert(self, data):
        data['active'] = True
        super().insert(data)

    def hide(self, primary_key):
        self._storage[primary_key]['active'] = False

    def search(self, field, key):
        result = SelectItem(self._storage, field)
        return result.query(lambda x: x == key)


class Roles(BaseModel):

    _fields = {'id, name'}

    @property
    def storage(self):
        return self._storage

    @property
    def fields(self):
        return self._fields

    @property
    def primary_field_name(self):
        return 'role_id'

    def __init__(self):
        super().__init__()
        self._storage = {}

    def delete(self, primary_key):
        del self._storage[primary_key]


class Resources(BaseModel):

    _fields = {'resources_id, name'}

    @property
    def storage(self):
        return self._storage

    @property
    def fields(self):
        return self._fields

    @property
    def primary_field_name(self):
        return 'resources_id'

    def __init__(self):
        super().__init__()
        self._storage = {}


class UserRoles(BaseModel):

    _fields = {'ur_id, name'}

    @property
    def storage(self):
        return self._storage

    @property
    def fields(self):
        return self._fields

    @property
    def primary_field_name(self):
        return 'ur_id'

    def __init__(self):
        super().__init__()
        self._storage = {}
