import json
import argparse
import function

parser = argparse.ArgumentParser(
    description='Program for select bolts with given parameters'
    )
'''parser.add_argument('catalog_bolts')
parser.add_argument('catalog_nuts')
parser.add_argument('catalog_washers')
'''
parser.add_argument(
    '--size', dest='size', type=int, help='Write size of bolt'
    )
parser.add_argument(
    '--det1', dest='det1', type=int,
    help='Write det1 size of connecting details'
    )
parser.add_argument(
    '--det2', dest='det2', type=int,
    help='Write det2 size of connecting details'
    )
parser.add_argument(
    '--thread', dest='thread', type=str, default='big',
    help='Write thread size of bolt'
    )
parser.add_argument(
    '--washer', dest='washer', type=int, default=1,
    help='Exsistance washer under bolt head'
    )
parser.add_argument(
    '--nuts', dest='nuts', type=int, default=2,
    help='Number of nuts'
    )
args = parser.parse_args()

file_bolts = open("data_bolts.json")
data_bolts = json.load(file_bolts)
file_bolts.close()

file_nuts = open("data_nuts.json")
data_nuts = json.load(file_nuts)
file_nuts.close()

file_washers = open("data_washers.json")
data_washers = json.load(file_washers)
file_washers.close()

print(function.select_bolts(data_bolts, data_nuts, data_washers,
    args.size, args.det1, args.det2, args.thread, args.washer, args.nuts
    )
)
