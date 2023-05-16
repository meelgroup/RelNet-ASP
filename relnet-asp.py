import os, argparse, json

parser = argparse.ArgumentParser()
parser.add_argument('-i','--i', help='input asp file', required=True)
parser.add_argument('-s','--s', help='independent support file', required=True)
args = parser.parse_args()

input = args.i
IS_file = args.s
dir_name = os.path.dirname(input)
file_name = os.path.basename(input)

counter_result = "counter_" + file_name

factors = open('factor.json') # the cyclic result is herewith
factor_result = json.load(factors)
def parse_factor_from_json(file):
    key = file
    if key in factor_result:
        return factor_result[key]
    return None

factor = parse_factor_from_json(file_name)
if factor == None:
    print("========= Have no num (division factor) !!! ==========")
    print("========= Please specify num/division factor !!! ==========")
    exit(0)
else:
    print("========= The num is {0} !!! ==========".format(factor))
    print("We divide the number of answer sets by 2^{0}".format(factor))

print("========= Invoking ASP counter !!! ==========")
os.system('./approxasp --sparse --conf 0.35 --useind {0} --asp {1} > {2}'.format(IS_file, input, counter_result))

reliability = None
quo = None
exp = None
for line in open(counter_result, 'r'):
    if line.startswith("After the iteration, the (median) number of solution:") or \
        line.startswith("The exact number of solution"):
        l = line.split()
        quo = int(l[-5])
        exp = int(l[-1])

if quo != None:
    print("========= ASP Counting done !!! ==========")
    print("The number of answer sets is {0} X 2 ^ {1}".format(quo, exp))
    print("========= Computing Reliability !!! ==========")
    reliability = quo / 2 ** (factor - exp)
    print("The reliability is {0}".format(reliability))
else:
    print("ApproxASP timeouted !!!")

print("The log of ApproxASP: {0}".format(counter_result))
