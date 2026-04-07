import argparse
import os
import random
parser = argparse.ArgumentParser()
parser.add_argument('-i','--i', help='input asp file', required=True)
parser.add_argument('-k', '--k', default=1, required=True,
                    help='the value of k (must be odd)')
parser.add_argument('-m', '--m', default=3, required=True,
                    help='the value of m')
args = parser.parse_args()

file_name = args.i

frac_k = int(args.k)
frac_m = int(args.m)

if frac_k == 0 or frac_k % 2 == 0:
    print("The k value must be odd, otherwise, the fraction k / 2^m can be reduced.")
    print("Exit")
    exit(0)

if frac_m == 0:
    print("The m value must be greater than 0")
    print("Exit")
    exit(0)

if frac_k > 2 ** frac_m:
    print("The condition k <= 2^m must hold")
    print("Exit")
    exit(0)

os.system('python add_chain_formula.py -i {0} -k {1} -m {2} > result_{0}'.format(file_name, frac_k, frac_m))
os.system('./approxasp --sparse --conf 0.35 --useind IS_chain_{0} --asp chain_{0} >> result_{0}'.format(file_name))

print("### Countering finished, parsing output ###")
print("Detailed output in file: result_{0}".format(file_name))
mul = None
m = None
n = None

for line in open("result_{0}".format(file_name)):
    if line.startswith("The multiplication factor:"):
        mul = int(line.split()[-1])
        print("The multiplication factor: 2^{0}".format(mul))

    elif line.startswith("After the iteration, the (median) number of solution:"):
        l = line.split()
        m = int(l[-5])
        n = int(l[-1])


print("The number of answer sets: {0} X 2^{1}".format(m,n))
print("The network reliability: {0} X 2^{1} / 2^{2}".format(m,n,mul))

