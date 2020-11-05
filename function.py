def select_bolts(
    data_bolts, data_nuts,
    data_washers, size=None, det1=None, det2=None,
    thread='big', thread_entry='no', washer_head=1, nuts_count=2
):
    '''

    '''

    bolts_list = []

    if size is not None and det1 is not None and det2 is not None:
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

                thread_inner = (bolt['bolt_length']
                                - washer_head*washer_width
                                - det1 - det2
                                - bolt['thread_length'])

                thread_outer = (bolt['bolt_length']
                                - washer_head*washer_width
                                - det1 - det2
                                - bolt['thread_length'])

                if thread == "big":
                    thread_remain = 2 * bolt["thread_size_big"]

                if thread == "small" and bolt['thread_size_small'] != '':
                    thread_remain = 2 * bolt["thread_size_small"]

                if result:
                    result = (length + thread_remain) < bolt['bolt_length']

                if result and thread_entry == 'no':
                    result = thread_inner > -5 and thread_inner > -det2/2

                if result and thread_entry == 'no' or thread_entry == 'yes':
                    result = (
                        thread_inner < 0 or thread_outer > 0 and
                        thread_outer < washer_width
                        )

                if result and bolt['thread_length'] == bolt['bolt_length']:
                    bolt['thread_warning'] = 'резьба на всю длину болта'

                if result:
                    bolts_list.append(bolt)
    return bolts_list
