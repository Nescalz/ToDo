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