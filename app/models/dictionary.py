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
    Возвращает новую структуру, где удалены все элементы, ключ которых начинается
    с f"{target_type}{target_index}_".
    """
    result = {}
    prefix = f"{target_type}{target_index}_"
    for key, value in data.items():
        if key.startswith(prefix):
            continue

        if isinstance(value, dict):
            cleaned = remove_by_type_index(value, target_type, target_index)

            if cleaned:
                result[key] = cleaned
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

def add_to_folder(data: dict, target_type: str, target_index: int,
                  add_type: str, name: str, value=None) -> bool:
    """
    Ищет во вложенной структуре папку с ключом, начинающимся с f"{target_type}{target_index}_".
    Если находит — добавляет туда:
      - подпапку (если add_type == "dir"), пустую dict
      - или текст (если add_type == "text"), ключ->value

    Возвращает True, если вставка произошла, иначе False.
    """
    prefix = f"{target_type}{target_index}_"

    for key, val in data.items():
        if key.startswith(prefix):
            # Found target folder — вставляем
            if not isinstance(val, dict):
                # несовместимо — не папка
                return False
            # генерируем уникальный ключ
            existing = set(val.keys())
            if add_type == "dir":
                newkey = make_unique_key(existing, f"{target_type}")
                val[newkey] = {}
            elif add_type == "text":
                newkey = make_unique_key(existing, f"{add_type}")
                val[newkey] = value
            else:
                raise ValueError("add_type must be 'dir' or 'text'")
            return True
        else:
            # если значение — dict, рекурсивно погружаемся
            if isinstance(val, dict):
                if add_to_folder(val, target_type, target_index, add_type, name, value):
                    return True

    return False


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