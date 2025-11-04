def find_index(data: dict, index: int, prefix: str) -> dict:
    print(11123)
    print(data)
    print(index)
    print(prefix)
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