def find_index(data: dict, index: int, prefix: str) -> dict:
    """
    Ищет в словаре data ключ, который начинается с prefix + индекс,
    например prefix="dir", index=2 -> ищем ключ начинающийся с "dir2".
    Если найден, возвращает его значение и ключ.
    Иначе возвращает {} или None.
    """
    target_prefix = f"{prefix}{index}"
    for key, value in data.items():
        if key.startswith(target_prefix):
            return {key: value}

        if isinstance(value, dict):
            result = find_index(value, index, prefix)
            if result:
                return result
    return None

def find_parent_index(data: dict, target_index: int, kind: str):
    target_prefix = f"{kind}{target_index}_"
    
    def recurse(curr: dict, parent_key: str = None):
        for key, value in curr.items():
            if key.startswith(target_prefix):
                if parent_key is None:
                    return None
                if parent_key.startswith("dir"):
                    try:
                        return int(parent_key[len("dir"):].split("_",1)[0])
                    except:
                        return None
                return None
            if key.startswith("dir") and isinstance(value, dict):
                res = recurse(value, key)
                if res is not None:
                    return res
        return None
    
    return recurse(data)

def remove_by_type_index(data: dict, target_index: int, target_type: str) -> dict:
    """
    Удаляет из data все ключи (на любом уровне вложенности), 
    которые начинаются с f"{target_type}{target_index}_".
    Сохраняет остальные ключи + структуру.
    """
    result = {}
    prefix = f"{target_type}{target_index}_"
    
    for key, value in data.items():
        # если ключ с нужным префиксом — пропускаем
        if key.startswith(prefix):
            continue

        # если значение — dict, рекурсивно очищаем
        if isinstance(value, dict):
            result[key] = remove_by_type_index(value, target_index, target_type)
        else:
            result[key] = value

    return result




def make_unique_key(existing_keys, prefix: str):
    """
    Сгенерировать ключ вида prefix + уникальное число, которого нет в existing_keys.
    """
    i = 0
    while True:
        key = f"{prefix}{i}"
        if key not in existing_keys:
            return key
        i += 1

def find_folder_dict(data: dict, target_index: int):
    target_prefix = f"{target_index}"
    print(target_prefix)
    
    def recurse(curr: dict, path="root"):
        for key, val in curr.items():
            if key.startswith(target_prefix):
                return val
            if isinstance(val, dict):
                found = recurse(val, f"{path}->{key}")
                if found is not None:
                    return found
        return None
    
    return recurse(data)



def get_used_dir_indexes(node: dict, type):
    """Рекурсивно собирает все индексы, которые уже заняты в ключах dirX_."""
    used = set()
    for key, val in node.items():
        if key.startswith(type):
            rest = key[len(type):]
            if "_" in rest:
                idx_str = rest.split("_", 1)[0]
                if idx_str.isdigit():
                    used.add(int(idx_str))
        if isinstance(val, dict):
            used.update(get_used_dir_indexes(val, type))
    return used

def add_to_folder(data: dict, parent_index: int, item_type: str, name, value={}):
    parent = find_folder_dict(data, parent_index)
    if parent is None:
        raise KeyError(f"Папка {parent_index} не найдена.")

    prefix = item_type

    used_indexes = get_used_dir_indexes(data, item_type)

    new_index = 0
    while new_index in used_indexes:
        new_index += 1

    new_key = f"{prefix}{new_index}_{name}"
    print(new_key)
    parent[new_key] = {} if item_type == "dir" else f"{value}"

    return data, new_index


#Тест функция
def build_paths(data: dict):
    #Префиксы элементов словаря
    prefix_dir = "dir"
    prefix_file = "text"
    """
    Преобразует вложенный словарь data в список путей строк.
    parent_parts — список уже пройденных частей пути (без префиксов).
    prefix_dir — префикс для папок (по умолчанию "dir").
    prefix_file — префикс для файлов (по умолчанию "text").
    
    Возвращает список строк вида "main -> МатьДИР -> apachi22".
    """
    parent_parts = []
    paths = []
    for key, value in data.items():
        if "_" in key:
            kind, name = key.split("_", 1)
        else:
            kind, name = key, ""
        if kind.startswith(prefix_dir):
            new_parent = parent_parts + [ name ]
            if isinstance(value, dict):
                paths.extend(build_paths(value))
            else:
                paths.append(" -> ".join(new_parent + [ str(value) ]))
        elif kind.startswith(prefix_file):
            path = parent_parts + [ name ]
            paths.append(" -> ".join(path))
        else:
            path = parent_parts + [ key ]
            if isinstance(value, dict):
                paths.extend(build_paths(value))
            else:
                paths.append(" -> ".join(path))
    return paths