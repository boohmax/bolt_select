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
    size, det1, det2, thread='big', thread_entry=False,
    washer_head=True, washer_nuts=True, nuts_count=2
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
                + int(washer_nuts)*washer_width + nuts_count*nut_width
                )

            thread_position = (
                bolt['bolt_length']
                - bolt['thread_length']
                )

            package_full = (
                int(washer_head)*washer_width
                + det1 + det2 + int(washer_nuts)*washer_width
                )

        if result and thread == "big":
            thread_remain = (
                2 * bolt["thread_size_big"] + bolt['thread_bevel_big']
                )
        elif result and thread == "small" and bolt.get('thread_bevel_small'):
            thread_remain = (
                2 * bolt["thread_size_small"] + bolt['thread_bevel_small']
                )
        else:
            thread_remain = (
                2 * bolt["thread_size_big"] + bolt['thread_bevel_big']
                )

        if result:
            result = (length + thread_remain) < bolt['bolt_length']

        if result and thread_entry is False:
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

    for bolt in bolts_list:
        if thread == 'small' and bolt.get('thread_size_small') is None:
            print('The calculation use \'big\' thread size')

    return bolts_list


def find_bolts_GOST_7798_70(
    size, det1, det2,
    thread='big', thread_entry=False,
    washer_head=True, washer_nuts=True, nuts_count=2
):
    '''Select bolts for given package
Check result for normal condition, 2 washers 2 nuts
>>> [bolt['bolt_length'] for bolt in find_bolts_GOST_7798_70(\
size=16, det1=10, det2=8)]
[60]

Check result without washer under bolt head
>>> [bolt['bolt_length'] for bolt in find_bolts_GOST_7798_70(\
size=16, det1=8, det2=8, washer_head=False)]
[55]

Check result with two washers under nuts
>>> [bolt['bolt_length'] for bolt in find_bolts_GOST_7798_70(\
size=16, det1=10, det2=10, washer_nuts=2)]
[65]

Check result for small size of thread
>>> [bolt['bolt_length'] for bolt in find_bolts_GOST_7798_70(\
size=16, det1=8, det2=6, thread='small')]
[55]

Check result when thread entry allowed
>>> [bolt['bolt_length'] for bolt in find_bolts_GOST_7798_70(\
size=10, det1=2, det2=2, thread_entry=True)]
[30]

Check result when thread entry allowed and use one nut
>>> [bolt['bolt_length'] for bolt in find_bolts_GOST_7798_70(\
size=10, det1=2, det2=2, thread_entry=True, nuts_count=1)]
[25, 30]

Check result when all positional parameters are specified
>>> [bolt['bolt_length'] for bolt in find_bolts_GOST_7798_70(\
size=10, det1=2, det2=2, thread='small', thread_entry=True,\
nuts_count=1, washer_head=False)]
[20, 25, 30]

Check result when give incorrect size of bolt
>>> [bolt['bolt_length'] for bolt in find_bolts_GOST_7798_70(\
size=13, det1=2, det2=2, thread='small', thread_entry=True,\
nuts_count=1, washer_head=False)]
[]
'''
    return find_bolts(
        data_bolts, data_nuts, data_washers,
        size, det1, det2,
        thread, thread_entry, washer_head, washer_nuts, nuts_count
        )
