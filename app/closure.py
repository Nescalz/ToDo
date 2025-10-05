
def make_counter():
    data_storage = {}
    
    def save_data_default(id, data): #Хранит начальный путь(Все папки и файлы)
        nonlocal data_storage
        data_storage[f"back{id}"] = [data]
        data_storage[f"{id}def"] = data 
        print(f"savedef {data_storage}")

    def save_data(id, data): #Хранит список значений которые дали кнопкам
        nonlocal data_storage
        data_storage[f"{id}"] = data 
        print(f"save {data_storage}")

    def add_back_data(id, data):
        nonlocal data_storage
        list_back = data_storage[f"back{id}"]
        list_back.append(data)
        data_storage[f"back{id}"] = list_back 
        print(f"addback {data_storage}")

    def remove_back_data(id):
        nonlocal data_storage
        list_back = data_storage[f"back{id}"]
        list_back.reverse()
        list_back.pop(0)
        list_back.reverse()
        data_storage[f"back{id}"] = list_back 
        print(f"removeback {data_storage}")
#Функции получения данных
    def give_data_default(id): 
        nonlocal data_storage
        print(f"givedef {data_storage}")
        return data_storage[f"{id}def"]
        
    def give_data(id):
        nonlocal data_storage
        print(f"give {data_storage}")
        return data_storage[f"{id}"]

    def give_back_data(id): 
        nonlocal data_storage
        print(f"back {data_storage}")
        return data_storage[f"back{id}"]
    return save_data_default, give_data_default, save_data, give_data, add_back_data, give_back_data, remove_back_data

