import re
import os
from typing import Literal, Union
from collections import defaultdict


DB_FILE_NAME = 'data.txt'

classes = ['ФизическоеЛицо', 'Клиент', 'Инспектор',
           'Договор', 'ДоговорИнспектора', 'ДоговорКлиента',
           'Организация', 'ДоговорСОгранизацией',
           'ОрганизацияДоговорСОгранизацией', 'Заявка',
           'Услуга', 'УслугаЗаявки', 'ДоговорЗаявки']


class CustomClassWithRepr():
    def __repr__(self):
        text = self.__class__.__name__
        text += '('
        for index, attribute_name in enumerate(self.__slots__):
            if index:
                text += ', '
            text += f'{attribute_name}={repr(getattr(self, attribute_name))}'

        text += ')'
        return text


class ФизическоеЛицо(CustomClassWithRepr):
    __slots__ = ['ID', 'ФИО']
    __types__ = ['int', 'str']

    AUTOINCREMENT_ATTR_NAME = 'ID'

    def __init__(self, ID: int, ФИО: str):
        self.ФИО = ФИО
        self.ID = ID


class Клиент(ФизическоеЛицо):
    __slots__ = ['ID_клиента', 'ФИО', 'номер_паспорта',
                 'СНИЛС']
    __types__ = ['int', 'str', 'str', 'str']

    AUTOINCREMENT_ATTR_NAME = 'ID_клиента'

    def __init__(self, ID_клиента: int, ФИО: str,
                 номер_паспорта: str, СНИЛС: str):
        self.ID_клиента = ID_клиента
        self.номер_паспорта = номер_паспорта
        self.СНИЛС = СНИЛС
        self.ФИО = ФИО


class Инспектор(ФизическоеЛицо):
    __slots__ = ['ID_инспектора', 'ФИО']
    __types__ = ['int', 'str']

    AUTOINCREMENT_ATTR_NAME = 'ID_инспектора'

    def __init__(self, ID_инспектора: int, ФИО: str):
        self.ID_инспектора = ID_инспектора
        self.ФИО = ФИО


class Договор(CustomClassWithRepr):
    __slots__ = ['ID_договора', 'дата_договора', 'дата_окончания_договора']
    __types__ = ['int', 'str', 'str']

    AUTOINCREMENT_ATTR_NAME = 'ID_договора'

    def __init__(self, ID_договора: int, дата_договора: str,
                 дата_окончания_договора: str):
        self.ID_договора = ID_договора
        self.дата_договора = дата_договора
        self.дата_окончания_договора = дата_окончания_договора


class ДоговорИнспектора(CustomClassWithRepr):
    __slots__ = ['ID_договор_инспектора', 'ID_инспектора', 'ID_договора']
    __types__ = ['int', 'int', 'int']

    FOREIGN_KEYS_DICT = {
        __slots__[1]: 'Инспектор',
        __slots__[2]: 'Договор',
    }

    AUTOINCREMENT_ATTR_NAME = 'ID_договор_инспектора'

    def __init__(self, ID_договор_инспектора: int,
                 ID_инспектора: int, ID_договора: int):
        self.ID_инспектора = ID_инспектора
        self.ID_договора = ID_договора
        self.ID_договор_инспектора = ID_договор_инспектора


class ДоговорКлиента(CustomClassWithRepr):
    __slots__ = ['ID_договор_клиента', 'ID_клиента', 'ID_договора']
    __types__ = ['int', 'int', 'int']

    FOREIGN_KEYS_DICT = {
        __slots__[1]: 'Клиент',
        __slots__[2]: 'Договор',
    }

    AUTOINCREMENT_ATTR_NAME = 'ID_договор_клиента'

    def __init__(self, ID_договор_клиента: int,
                 ID_клиента: int, ID_договора: int):
        self.ID_клиента = ID_клиента
        self.ID_договора = ID_договора
        self.ID_договор_клиента = ID_договор_клиента


class Организация(CustomClassWithRepr):
    __slots__ = ['ID_организации', 'НаименованиеОрганизации',
                 'АктивнаяОрганизация']
    __types__ = ['int', 'str', 'bool']

    AUTOINCREMENT_ATTR_NAME = 'ID_организации'

    def __init__(self, ID_организации: int, НаименованиеОрганизации: str,
                 АктивнаяОрганизация: bool):
        self.ID_организации = ID_организации
        self.НаименованиеОрганизации = НаименованиеОрганизации
        self.АктивнаяОрганизация = АктивнаяОрганизация


class ДоговорСОгранизацией(CustomClassWithRepr):
    __slots__ = ['ID_договора', 'дата_заключения', 'дата_окончания',
                 'наименования_договора']
    __types__ = ['int', 'str', 'str', 'str']

    AUTOINCREMENT_ATTR_NAME = 'ID_договора'

    def __init__(self, ID_договора: int, дата_заключения: str,
                 дата_окончания: str, наименования_договора: str):
        self.ID_договора = ID_договора
        self.дата_заключения = дата_заключения
        self.дата_окончания = дата_окончания
        self.наименования_договора = наименования_договора


class ОрганизацияДоговорСОгранизацией(CustomClassWithRepr):
    __slots__ = ['ID', 'ID_организации', 'ID_договора']
    __types__ = ['int', 'int', 'int']

    FOREIGN_KEYS_DICT = {
        __slots__[1]: 'Договор',
    }

    AUTOINCREMENT_ATTR_NAME = 'ID'

    def __init__(self, ID: int, ID_организации, ID_договора):
        self.ID = ID
        self.ID_организации = ID_организации
        self.ID_договора = ID_договора


class Заявка(CustomClassWithRepr):
    __slots__ = ['ID_заявки', 'комментарий', 'стоимость', 'телефон',
                 'тип_услуги']
    __types__ = ['int', 'str', 'int', 'str', 'str']

    AUTOINCREMENT_ATTR_NAME = 'ID_заявки'

    def __init__(self, ID_заявки: int, комментарий: str, стоимость: int,
                 телефон: str, тип_услуги: str):
        self.ID_заявки = ID_заявки
        self.комментарий = комментарий
        self.стоимость = стоимость
        self.телефон = телефон
        self.тип_услуги = тип_услуги


class Услуга(CustomClassWithRepr):
    __slots__ = ['ID_услуги', 'наименование_услуги', 'стоимость_услуги']
    __types__ = ['int', 'str', 'str']

    AUTOINCREMENT_ATTR_NAME = 'ID_услуги'

    def __init__(self, ID_услуги: int, наименование_услуги: str,
                 стоимость_услуги: int):
        self.ID_услуги = ID_услуги
        self.наименование_услуги = наименование_услуги
        self.стоимость_услуги = стоимость_услуги


class УслугаЗаявки(CustomClassWithRepr):
    __slots__ = ['ID', 'ID_услуги', 'ID_заявки']
    __types__ = ['int', 'int', 'int']

    FOREIGN_KEYS_DICT = {
        __slots__[1]: 'Услуга',
        __slots__[2]: 'Заявка',
    }

    AUTOINCREMENT_ATTR_NAME = 'ID'

    def __init__(self, ID: int, ID_услуги: str, ID_заявки: int):
        self.ID = ID
        self.ID_услуги = ID_услуги
        self.ID_заявки = ID_заявки


class ДоговорЗаявки(CustomClassWithRepr):
    __slots__ = ['ID', 'ID_заявки', 'ID_договора']
    __types__ = ['int', 'int', 'int']

    FOREIGN_KEYS_DICT = {
        __slots__[1]: 'Заявка',
        __slots__[2]: 'Договор',
    }

    AUTOINCREMENT_ATTR_NAME = 'ID'

    def __init__(self, ID: int, ID_заявки: str, ID_договора: int):
        self.ID = ID
        self.ID_заявки = ID_заявки
        self.ID_договора = ID_договора


class FileDBManager():
    def __init__(self, file_name):
        self.file_name = file_name

    def load(self) -> dict[str, list]:
        result = defaultdict(list)
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as file:
                for line in file.readlines():
                    if not line.strip():
                        continue

                    class_name = line[:line.find('(')]
                    result.setdefault(class_name, [])
                    result[class_name].append(eval(line))

        return result

    def save_to_file(self, objects):
        with open(self.file_name, 'w') as file:
            for obj in objects:
                file.write(repr(obj))
                file.write('\n')


def find_all_re(class_name: str, attr_name: str,
                pattern: str, limit=None) -> list[object]:
    result = []
    for obj in data[class_name]:
        if re.match(pattern, str(getattr(obj, attr_name))):
            result.append(obj)

        if limit and len(result) == limit:
            break

    return result


def find_all(class_name: str, attr_name: str,
             value, limit=None) -> list[object]:
    result = []
    for obj in data[class_name]:
        if getattr(obj, attr_name) == value:
            result.append(obj)

        if limit and len(result) == limit:
            break

    return result


def get_id_list(class_name) -> list[int]:
    result = []
    for obj in data[class_name]:
        result.append(getattr(obj, obj.AUTOINCREMENT_ATTR_NAME))

    return result


def get_input(value_range,
              value_type: Union[Literal['int'], Literal['str'],
                                Literal['bool']] = str):
    print('Введите(для отмены введите X): ')
    while True:
        value = input()
        if value == 'X':
            return None

        if value_type is int:
            try:
                value = int(value)
            except ValueError:
                print('Введите корректное значение!')

        if value not in value_range:
            print('Введите корректное значение!')
        else:
            break

    return value


def get_attr_input(attr_name: str,
                   attr_type: Union[Literal['int'], Literal['str'],
                                    Literal['bool']] = str):
    while True:
        print(f'{attr_name}: {attr_type} = ', end='')
        try:
            value = eval(attr_type)(input())
        except ValueError:
            print('Введите корректное значение')
        else:
            break

    return value


class Main():
    def class_display(self, class_name):
        os.system('cls')
        print(class_name)
        print('1. Посмотреть записи')
        print('2. Поиск записей')
        print('3. Добавить новую запись')
        print('4. Удалить запись')
        value = get_input([1, 2, 3, 4], int)
        if value is None:
            self.menu()
            return

        if value == 1:
            self.display_objects(class_name)
        elif value == 2:
            self.find_objects(class_name)
        elif value == 3:
            self.create_new_object(class_name)
        elif value == 4:
            self.delete_object(class_name)

    def display_objects(self, class_name):
        print('Записи:\n')
        for obj in data[class_name]:
            print(obj)

        print()
        print('Для продолжения нажмите...')
        input()
        self.class_display(class_name)

    def find_objects(self, class_name):
        print('По какому столбцу хотите сделать поиск?')
        cls = globals()[class_name]
        attrs = cls.__slots__.copy()
        for index, attr_name in enumerate(attrs, 1):
            print(f'{index}. {attr_name}')

        index = get_input(list(range(1, len(attrs)+1)), int)
        if index is None:
            self.class_display(class_name)
            return

        attr_name = attrs[index-1]
        print('Введите шаблон(можно использовать регулярные выражения)')
        pattern = get_attr_input(attr_name, 'str')
        objects = find_all_re(class_name, attr_name, pattern)
        print('Найденные записи:\n')
        if objects:
            for obj in objects:
                print(obj)
        else:
            print('Ничего не найдено.')

        print()
        print('Для продолжения нажмите...')
        input()
        self.class_display(class_name)

    def create_new_object(self, class_name):
        cls = globals()[class_name]
        attrs = cls.__slots__.copy()
        types = cls.__types__.copy()
        types.pop(attrs.index(cls.AUTOINCREMENT_ATTR_NAME))
        attrs.remove(cls.AUTOINCREMENT_ATTR_NAME)
        attr_dict = {}
        for attr_name, attr_type in zip(attrs, types):
            if attr_name.startswith('ID'):
                print(f'\nВыберите из списка {attr_name}:\n')
                foreign_key_class_name = cls.FOREIGN_KEYS_DICT[attr_name]
                for obj in data[foreign_key_class_name]:
                    print(obj)

                if not data[foreign_key_class_name]:
                    print('Список пуст!')
                    print()
                    print('Для продолжения нажмите...')
                    input()
                    self.class_display(class_name)
                    return

                print()
                id_list = get_id_list(foreign_key_class_name)
                while True:
                    value = get_attr_input(attr_name, attr_type)
                    attr_dict[attr_name] = value
                    if value not in id_list:
                        print('Введите корректное значение!')
                    else:
                        break

            else:
                value = get_attr_input(attr_name, attr_type)
                attr_dict[attr_name] = value

        if data[class_name]:
            last_row_id = getattr(data[class_name][-1],
                                  cls.AUTOINCREMENT_ATTR_NAME)
        else:
            last_row_id = 0

        attr_dict[cls.AUTOINCREMENT_ATTR_NAME] = last_row_id+1
        obj = cls(**attr_dict)
        data[class_name].append(obj)
        print('Успешно добавлено!')
        print('Для продолжения нажмите...')
        input()
        self.class_display(class_name)

    def delete_object(self, class_name):
        cls = globals()[class_name]
        print('Введите', cls.AUTOINCREMENT_ATTR_NAME)
        id_list = get_id_list(class_name)
        id = get_input(id_list, int)
        if id:
            for index, obj in enumerate(data[class_name]):
                if getattr(obj, cls.AUTOINCREMENT_ATTR_NAME) == id:
                    data[class_name].pop(index)
                    print('Успешно удалено!')
                    break

        print('Для продолжения нажмите...')
        input()
        self.class_display(class_name)

    def menu(self):
        os.system('cls')
        print('Список таблиц:')
        for index, class_name in enumerate(classes, 1):
            print(f'{index}. {class_name}')

        print(f'{index+1}. Сохранить и выйти')
        index = get_input(list(range(1, len(classes)+2)), int)
        if index:
            if index == len(classes)+1:
                self.save()
            else:
                self.class_display(classes[index-1])

    def save(self):
        objects = []
        for obj_list in data.values():
            objects.extend(obj_list)

        db.save_to_file(objects)

    def run(self):
        self.menu()


if __name__ == "__main__":
    db = FileDBManager(DB_FILE_NAME)
    data = db.load()
    main = Main()
    main.run()
