def conteiner():
    dict_data = {}
    def add_data(id, data):
        nonlocal dict_data
        dict_data[id] = data
        
    def give_data(id):
        nonlocal dict_data
        return dict_data[id]
    
    return add_data, give_data