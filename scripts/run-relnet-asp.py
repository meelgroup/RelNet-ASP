import argparse, tempfile
import os
import random
parser = argparse.ArgumentParser()
parser.add_argument('-i','--i', help='input asp file', required=True)
args = parser.parse_args()

file_name = args.i
with tempfile.NamedTemporaryFile(dir=".", delete=False) as f:
    temp_file = f.name
    os.system("cp {0} {1}".format(args.i, temp_file))
    input_file = os.path.basename(temp_file)

os.system('python add_chain_formula.py -i {0} > result_{0}'.format(input_file))
os.system('./approxasp --sparse --conf 0.35 --useind IS_chain_{0} --asp chain_{0} >> result_{0}'.format(input_file))

print("### Countering finished, parsing output ###")
print("Detailed output in file: result_{0}".format(input_file))
mul = None
m = None
n = None

for line in open("result_{0}".format(input_file)):
    if line.startswith("The multiplication factor:"):
        mul = int(line.split()[-1])
        print("The multiplication factor: 2^{0}".format(mul))

    elif line.startswith("After the iteration, the (median) number of solution:") or line.startswith("The exact number of solution:"):
        l = line.split()
        m = int(l[-5])
        n = int(l[-1])


if m != None and n != None and mul != None:
    print("The number of answer sets: {0} X 2^{1}".format(m,n))
    print("The network reliability: {0} X 2^{1} / 2^{2}".format(m,n,mul))
else:
    print("Error")
    print("Detailed output in file: result_{0}".format(input_file))
os.system("rm -f {0} IS_chain_{0} chain_{0}".format(input_file))

