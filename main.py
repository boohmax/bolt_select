import json
import argparse
import bolts

parser = argparse.ArgumentParser(
    description='''Program for select bolts with given parameters.
    Bolts GOST 7798-70. Nuts GOST 5915-70. Washers GOST 11371-78.
    Thread bevel GOST 10549-80.'''
    )
parser.add_argument(
    'size', type=int, help='Write size of bolt'
    )
parser.add_argument(
    'det1', type=int,
    help='Write width det1 of connecting details'
    )
parser.add_argument(
    'det2', type=int,
    help='Write width det2 of connecting details'
    )
parser.add_argument(
    '--thread', dest='thread', type=str, default='big',
    help='Write thread size of bolt, big or small'
    )
parser.add_argument(
    '--thread_entry', dest='thread_entry', type=bool, default=False,
    help='Thread entry in detail package, True or False')
parser.add_argument(
    '--washer_head', dest='washer_head', type=bool, default=True,
    help='Exsistance washer under bolt head, True or False'
    )
parser.add_argument(
    '--nuts_count', dest='nuts_count', type=int, default=2,
    help='Number of nuts, 2 or 1'
    )
args = parser.parse_args()

print(bolts.find_bolts_GOST_7798_70(
    args.size, args.det1, args.det2, args.thread, args.thread_entry,
    args.washer_head, args.nuts_count
)
)
