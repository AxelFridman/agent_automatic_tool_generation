import functions_utils
import inspect
import os
def sum_list_odd_index_elements(lst):
    total = 0
    for i in range(0, len(lst), 2):
        total += lst[i]
    return total

#res = "sv@calling:ag1@hola"
#print(res.split("@calling:")[1].split("@")[0])
functions_dict = {name: obj for name, obj in inspect.getmembers(functions_utils, inspect.isfunction)}

print(functions_dict)
print(os.getcwd())
