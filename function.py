def select_bolts(data_bolts, data_nuts,
    data_washers, size, det1, det2,
    thread='big', washer_head=1, nuts_count=2):
    '''

    '''

    bolts_list = []
    washer_width = None
    nut_width = None
    length = None
    thread_inner = None
    thread_outer = None
    thread_remain = None


    for washer in data_washers:
        if washer['washer_size'] == size:
            washer_width = washer['washer_width']

    for nut in data_nuts:
        if nut['nut_size'] == size:
            nut_width = nut['nut_width']
    
    for bolt in data_bolts:
        result = True
        
        if bolt['bolt_size'] == size:
            length = washer_head*washer_width + det1 + det2
            + washer_width + nuts_count*nut_width

        if bolt['thread_length'] != '':
            thread_inner = bolt['bolt_length']\
            - washer_head*washer_width\
            - det1 - det2\
            - bolt['thread_length']

        if bolt['thread_length'] != '':
            thread_outer = bolt['bolt_length']\
            - washer_head*washer_width\
            - det1 - det2 - washer_width\
            - bolt['thread_length']

        if thread == "big":
            thread_remain = 2 * bolt["thread_size_big"]
        else:
            thread_remain = 2 * bolt["thread_size_small"]
  
        if result:
            result = (length + thread_remain) < bolt['bolt_length']

        if result:
            result = thread_inner < 5 and thread_inner < det2/2

        if result:
            result = thread_inner > 0 or thread_outer > 0

        if result:
            bolts_list.append(bolt)
    return bolts_list
