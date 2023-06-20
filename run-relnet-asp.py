import argparse
import os
import random
accepted_range = [0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875]
parser = argparse.ArgumentParser()
parser.add_argument('-i','--i', help='input asp file', required=True)
parser.add_argument('-p', '--p', default=True, required=0.125,
                    help='edge probability, prob (-p) should be from values: {0}'.format(accepted_range))
args = parser.parse_args()

file_name = args.i
prob = float(args.p)

if prob not in accepted_range:
    print("prob should be from values: {0}".format(accepted_range))
    prob = 0.125
    print("Using prob value = 0.125")

os.system('python add_chain_formula.py -i {0} -p 0.125 > result_{0}'.format(file_name))
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

