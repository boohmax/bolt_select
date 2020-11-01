def select_bolts(data_bolts, data_nuts,
    data_washers, size=20, det1=10, det2=10,
    thread='big', washer_head=1, nuts_count=2):

    bolts_list = []

    for washer in data_washers:
        if washer['washer_size'] == size:
            washer_width = washer['washer_width']

    for nut in data_nuts:
        if nut['nut_size'] == size:
            nut_width = nut['nut_width']
    
    for bolt in data_bolts:
        result = True

        nonlocal washer_width
        nonlocal nut_width

        length = washer_head*washer_width + det1 + det2
        + washer_width + nuts_count*nut_width

        thread_inner = bolt['bolt_length']\
        - washer_head*washer_width\
        - det1 - det2\
        - bolt['thread_length']

        thread_outer = bolt['bolt_length']\
        - washer_head*washer_width\
        - det1 - det2 - washer_width\
        - bolt['thread_length']

        if thread == "big":
            thread_remain = 2 * bolt["thread_size_big"]
        else:
            thread_remain = 2 * bolt["thread_size_small"]
  
        if (bolt['bolt_size'] == size) and\
            (length + thread_remain < bolt['bolt_length']) and\
            (thread_inner < 5 and thread_inner < det2/2) and\
            (thread_inner > 0 or thread_outer > 0):
            result = True

        if result:
            bolts_list.append(bolt)
    return bolts_list
