import json

file_bolts = open("data_bolts.json")
data_bolts = json.load(file_bolts)
file_bolts.close()

file_nuts = open("data_nuts.json")
data_nuts = json.load(file_nuts)
file_nuts.close()

file_washers = open("data_washers.json")
data_washers = json.load(file_washers)
file_washers.close()

def find_bolts(
    data_bolts, data_nuts, data_washers,
    size, det1, det2,
    thread='big', thread_entry=False, washer_head=True, nuts_count=2
):
    
    bolts_list = []
    
    for washer in data_washers:
        if washer['washer_size'] == size:
            washer_width = washer['washer_width']
            
    for nut in data_nuts:
        if nut['nut_size'] == size:
            nut_width = nut['nut_width']
            
    for bolt in data_bolts:
        result = bolt['bolt_size'] == size

        if result:
            length = (
                int(washer_head)*washer_width + det1 + det2
                + washer_width + nuts_count*nut_width
                )

            thread_position = (
                bolt['bolt_length']
                - bolt['thread_length']
                )

            package_full = (
                int(washer_head)*washer_width
                + det1 + det2 + washer_width
                )

        if result and thread == "big":
            thread_remain = (
                2 * bolt["thread_size_big"] + bolt['thread_bevel_big']
                )                
        elif result and thread == "small" and bolt.get('thread_bevel_small'):
            thread_remain = (
                2 * bolt["thread_size_small"] + bolt['thread_bevel_small']
                )

        if result:
            result = (length + thread_remain) < bolt['bolt_length']
            
        if result and thread_entry == False:
            result = (
                thread_position >
                package_full - washer_width - 5 and
                thread_position >
                package_full - washer_width - det2/2 and
                thread_position < package_full
                )
            
        if result and thread_entry:
            result = thread_position < package_full

        if result:
            bolts_list.append(bolt)
    return bolts_list


def find_bolts_GOST_7798_70(
    size, det1, det2,
    thread='big', thread_entry=False, washer_head=True, nuts_count=2
):
    '''Select bolts for given package
>>> [bolt['bolt_length'] for bolt in select_bolts(\
[{"bolt_size":16, "bolt_length":50, "thread_size_big":2,\
"thread_size_small":1.5, "thread_length":38},\
{"bolt_size":16, "bolt_length":55, "thread_size_big":2,\
"thread_size_small":1.5, "thread_length":38},\
{"bolt_size":16, "bolt_length":60, "thread_size_big":2,\
"thread_size_small":1.5, "thread_length":38}],\
[{"nut_size":16,"nut_width":14.8, "nut_diameter":26.2}],\
[{"washer_size":16, "washer_width":3, "washer_diameter":30}],\
[{"thread_step":1.5, "thread_bevel":1.6},\
{"thread_step":2, "thread_bevel":2}],\
size=16, det1=10, det2=8)]
[60]

>>> [bolt['bolt_length'] for bolt in select_bolts(\
[{"bolt_size":16, "bolt_length":50, "thread_size_big":2,\
"thread_size_small":1.5, "thread_length":38},\
{"bolt_size":16, "bolt_length":55, "thread_size_big":2,\
"thread_size_small":1.5, "thread_length":38},\
{"bolt_size":16, "bolt_length":60, "thread_size_big":2,\
"thread_size_small":1.5, "thread_length":38}],\
[{"nut_size":16,"nut_width":14.8, "nut_diameter":26.2}],\
[{"washer_size":16, "washer_width":3, "washer_diameter":30}],\
[{"thread_step":1.5, "thread_bevel":1.6},\
{"thread_step":2, "thread_bevel":2}],\
size=16, det1=8, det2=8, washer_head=0)]
[55]

>>> [bolt['bolt_length'] for bolt in select_bolts(\
[{"bolt_size":16, "bolt_length":50, "thread_size_big":2,\
"thread_size_small":1.5, "thread_length":38},\
{"bolt_size":16, "bolt_length":55, "thread_size_big":2,\
"thread_size_small":1.5, "thread_length":38},\
{"bolt_size":16, "bolt_length":60, "thread_size_big":2,\
"thread_size_small":1.5, "thread_length":38}],\
[{"nut_size":16,"nut_width":14.8, "nut_diameter":26.2}],\
[{"washer_size":16, "washer_width":3, "washer_diameter":30}],\
[{"thread_step":1.5, "thread_bevel":1.6},\
{"thread_step":2, "thread_bevel":2}],\
size=16, det1=8, det2=6, thread='small')]
[55]

>>> [bolt['bolt_length'] for bolt in select_bolts(\
[{"bolt_size":10, "bolt_length":20, "thread_size_big":1.5,\
"thread_size_small":1.25, "thread_length":20},\
{"bolt_size":10, "bolt_length":25, "thread_size_big":1.5,\
"thread_size_small":1.25, "thread_length":25},\
{"bolt_size":10, "bolt_length":30, "thread_size_big":1.5,\
"thread_size_small":1.25, "thread_length":30}],\
[{"nut_size":10, "nut_width":8.4, "nut_diameter":17.6}],\
[{"washer_size":10, "washer_width":2, "washer_diameter":20}],\
[{"thread_step":1.5, "thread_bevel":1.6},\
{"thread_step":1.25, "thread_bevel":1.6}],\
size=10, det1=2, det2=2, thread_entry='yes')]
[30]

>>> [bolt['bolt_length'] for bolt in select_bolts(\
[{"bolt_size":10, "bolt_length":20, "thread_size_big":1.5,\
"thread_size_small":1.25, "thread_length":20},\
{"bolt_size":10, "bolt_length":25, "thread_size_big":1.5,\
"thread_size_small":1.25, "thread_length":25},\
{"bolt_size":10, "bolt_length":30, "thread_size_big":1.5,\
"thread_size_small":1.25, "thread_length":30}],\
[{"nut_size":10, "nut_width":8.4, "nut_diameter":17.6}],\
[{"washer_size":10, "washer_width":2, "washer_diameter":20}],\
[{"thread_step":1.5, "thread_bevel":1.6},\
{"thread_step":1.25, "thread_bevel":1.6}],\
size=10, det1=2, det2=2, thread_entry='yes', nuts_count=1)]
[25, 30]

>>> [bolt['bolt_length'] for bolt in select_bolts(\
[{"bolt_size":10, "bolt_length":20, "thread_size_big":1.5,\
"thread_size_small":1.25, "thread_length":20},\
{"bolt_size":10, "bolt_length":25, "thread_size_big":1.5,\
"thread_size_small":1.25, "thread_length":25},\
{"bolt_size":10, "bolt_length":30, "thread_size_big":1.5,\
"thread_size_small":1.25, "thread_length":30}],\
[{"nut_size":10, "nut_width":8.4, "nut_diameter":17.6}],\
[{"washer_size":10, "washer_width":2, "washer_diameter":20}],\
[{"thread_step":1.5, "thread_bevel":1.6},\
{"thread_step":1.25, "thread_bevel":1.6}],\
size=10, det1=2, det2=2, thread='small', thread_entry='yes',\
nuts_count=1, washer_head=0)]
[20, 25, 30]

>>> [bolt['bolt_length'] for bolt in select_bolts(\
[], [], [], [],\
size=16, det1=10, det2=10)]
[]
'''
    return find_bolts(
        data_bolts, data_nuts, data_washers,
        size, det1, det2,
        thread, thread_entry, washer_head, nuts_count
        )
