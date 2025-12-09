#Поиск элемента по индексу
def find_index(data: dict, index: int, prefix: str) -> dict:

    target_prefix = f"{prefix}{index}"
    for key, value in data.items():
        if key.startswith(target_prefix):
            return {key: value}

        if isinstance(value, dict):
            result = find_index(value, index, prefix)
            if result:
                return result
    return None

#Поиск прошлого элемента по индексу
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

#Удаялет элемент по индексу(включая вложения в элемент)
def remove_by_type_index(data: dict, target_index: int, target_type: str) -> dict:
    """
    Удаляет из data все ключи (на любом уровне вложенности), 
    которые начинаются с f"{target_type}{target_index}_".
    Сохраняет остальные ключи + структуру.
    """
    result = {}
    prefix = f"{target_type}{target_index}_"
    
    for key, value in data.items():
        if key.startswith(prefix):
            continue

        if isinstance(value, dict):
            result[key] = remove_by_type_index(value, target_index, target_type)
        else:
            result[key] = value

    return result

#Поиск папки для добавления в нее элемента
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

#Поиск занятых индексов и добавление в множество
def get_used_dir_indexes(node: dict, type):

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
#Добовление элемента
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

#Система цепочки файлов(Хлебные крошки)
def get_folder_path(data: dict, target_index: int):
    if target_index == "dir0": target_index=0

    def dfs(node, path):
        result = None
        for key, value in node.items():
            if key.startswith("dir") and "_" in key:
                idx_str, name = key[3:].split("_", 1)
                if not idx_str.isdigit():
                    continue
                idx = int(idx_str)
                new_path = path + [name]

                if idx == target_index:
                    return new_path  

                if isinstance(value, dict):
                    result = dfs(value, new_path)
                    if result is not None:
                        return result

            elif isinstance(value, dict):
                result = dfs(value, path)
                if result is not None:
                    return result

        return None  

    return dfs(data, [])




