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

edge_list = []
line_list = []
src = None
des = None
max_node = 0
file_pointer = open(file_name, 'r')
prob_graph = "chain_" + file_name
probabilistic_file_writer = open(prob_graph, 'w')
for line in file_pointer:
    if line.startswith("edge(") or line.startswith("line("):
        edges = line[line.find("(") + 1: line.find(")")]
        edge_tuple = edges.split(",")
        max_node = max(max_node, max(int(edge_tuple[0]), int(edge_tuple[1])))

        if line.startswith("edge("):
            # for edges
            edge_list.append((int(edge_tuple[0]), int(edge_tuple[1])))
        elif line.startswith("line("):
            # for lines
            line_list.append((int(edge_tuple[0]), int(edge_tuple[1])))

    elif line.startswith("first("):
        node = line[line.find("(") + 1: line.find(")")]
        src = int(node)

    elif line.startswith("last("):
        node = line[line.find("(") + 1: line.find(")")]
        des = int(node)

    else:
        probabilistic_file_writer.write(line)


# print("Max variable before probabilistic encoding: {0}".format(max_node))
num_nodes = max_node
# prob_list = [prob]
number_of_new_rules = 0
multiplication_factor = 0


independent_support = "IS_" + prob_graph
# abstract_graph = "abst_graph_" + file_name
# abstract_file_writer = open(abstract_graph, 'w')
IS_file_writer = open(independent_support, 'w')
IS_string = "c ind "
for index, edge in enumerate(edge_list):
    line = "{0} {1} {2}\n".format(edge[0], edge[1], prob)
    # abstract_file_writer.write(line)
    rule_string = "edge({0}, {1}).\n".format(edge[0], edge[1])
    probabilistic_file_writer.write(rule_string)

    if prob == 0.125:
        # introducing 2 new variables 
        new_var1 = max_node + 1
        new_var2 = max_node + 2
        # update new max_node
        max_node = max_node + 2
        rule_string = "{{ in({0}, {1}, 1); in({1}, {2}, 1); in({2},{3}, 1) }} :- edge({0}, {3}).\n"\
            .format(edge[0], new_var1, new_var2, edge[1])

        probabilistic_file_writer.write(rule_string)
        IS_string += "in({0},{1},1) in({1},{2},1) in({2},{3},1) ".format(edge[0], new_var1, new_var2, edge[1])
        rule_string = "in({0}, {3}) :- in({0}, {1}, 1), in({1}, {2}, 1), in({2},{3}, 1).\n"\
            .format(edge[0], new_var1, new_var2, edge[1])
        probabilistic_file_writer.write(rule_string)
        number_of_new_rules += 2
        multiplication_factor += 3

    elif prob == 0.25:
        # introducing 1 new variables 
        new_var1 = max_node + 1
        # update new max_node
        max_node = max_node + 1
        rule_string = "{{ in({0}, {1}, 1); in({1}, {2}, 1) }} :- edge({0}, {2}).\n"\
            .format(edge[0], new_var1, edge[1])

        probabilistic_file_writer.write(rule_string)
        IS_string += "in({0},{1},1) in({1},{2},1) ".format(edge[0], new_var1, edge[1])
        rule_string = "in({0}, {2}) :- in({0}, {1}, 1), in({1}, {2}, 1).\n"\
            .format(edge[0], new_var1, edge[1])
        probabilistic_file_writer.write(rule_string)
        number_of_new_rules += 2
        multiplication_factor += 2

    elif prob == 0.375:
        # introducing 1 new variables 
        new_var1 = max_node + 1
        # update new max_node
        max_node = max_node + 1
        rule_string = "{{ in({0}, {1}, 1); in({1}, {2}, 1); in({1},{2}, 2) }} :- edge({0}, {2}).\n"\
            .format(edge[0], new_var1, edge[1])

        probabilistic_file_writer.write(rule_string)
        IS_string += "in({0},{1},1) in({1},{2},1) in({1},{2},2) ".format(edge[0], new_var1, edge[1])
        rule_string = "in({0}, {2}) :- in({0}, {1}, 1), in({1}, {2}, 1).\n"\
            .format(edge[0], new_var1, edge[1])
        probabilistic_file_writer.write(rule_string)
        rule_string = "in({0}, {2}) :- in({0}, {1}, 1), in({1}, {2}, 2).\n"\
            .format(edge[0], new_var1, edge[1])
        probabilistic_file_writer.write(rule_string)
        number_of_new_rules += 3
        multiplication_factor += 3
    
    elif prob == 0.5:
        rule_string = "{{ in({0}, {1}, 1) }} :- edge({0}, {1}).\n"\
            .format(edge[0], edge[1])

        probabilistic_file_writer.write(rule_string)
        IS_string += "in({0},{1},1) ".format(edge[0], edge[1])
        rule_string = "in({0}, {1}) :- in({0}, {1}, 1).\n"\
            .format(edge[0], edge[1])

        probabilistic_file_writer.write(rule_string)
        number_of_new_rules += 2
        multiplication_factor += 1

    elif prob == 0.625:
        # introducing 1 new variables 
        new_var1 = max_node + 1
        # update new max_node
        max_node = max_node + 1
        rule_string = "{{ in({0}, {1}, 1); in({1}, {2}, 1); in({0}, {2}, 1) }} :- edge({0}, {2}).\n"\
            .format(edge[0], new_var1, edge[1])

        probabilistic_file_writer.write(rule_string)
        IS_string += "in({0},{1},1) in({1},{2},1) in({0},{2},1) ".format(edge[0], new_var1, edge[1])
        rule_string = "in({0}, {1}) :- in({0}, {1}, 1).\n"\
            .format(edge[0], edge[1])
        probabilistic_file_writer.write(rule_string)
        rule_string = "in({0}, {1}) :- in({0}, {1}, 1), in({1}, {2}, 1).\n"\
            .format(edge[0], new_var1, edge[1])
        probabilistic_file_writer.write(rule_string)
        number_of_new_rules += 3
        multiplication_factor += 3

    elif prob == 0.75:
        new_var1 = max_node + 1
        new_var2 = max_node + 2
        new_var3 = max_node + 3
        new_var4 = max_node + 4
        # update new max_node
        max_node = max_node + 4
        rule_string = "{{ in({2}, {3}, 1); in({4}, {5}, 1) }} :- edge({0}, {1}).\n"\
            .format(edge[0], edge[1], new_var1, new_var2, new_var3, new_var4)

        probabilistic_file_writer.write(rule_string)
        IS_string += "in({0},{1},1) in({2},{3},1) ".format(new_var1, new_var2, new_var3, new_var4)
        rule_string = "in({0}, {1}) :- in({2}, {3}, 1).\nin({0}, {1}) :- in({4}, {5}, 1).\n "\
            .format(edge[0], edge[1], new_var1, new_var2, new_var3, new_var4)
        probabilistic_file_writer.write(rule_string)
        number_of_new_rules += 3
        multiplication_factor += 2

    elif prob == 0.875:
        new_var1 = max_node + 1
        new_var2 = max_node + 2
        new_var3 = max_node + 3
        new_var4 = max_node + 4
        new_var5 = max_node + 5
        new_var6 = max_node + 6
        # update new max_node
        max_node = max_node + 6
        rule_string = "{{ in({2}, {3}, 1); in({4}, {5}, 1); in({6}, {7}, 1) }} :- edge({0}, {1}).\n"\
            .format(edge[0], edge[1], new_var1, new_var2, new_var3, new_var4, new_var5, new_var6)

        probabilistic_file_writer.write(rule_string)
        IS_string += "in({0},{1},1) in({2},{3},1) in({4},{5},1) "\
            .format(new_var1, new_var2, new_var3, new_var4, new_var5, new_var6)
        rule_string = "in({0}, {1}) :- in({2}, {3}, 1).\nin({0}, {1}) :- in({4}, {5}, 1).\nin({0}, {1}) :- in({6}, {7}, 1).\n"\
            .format(edge[0], edge[1], new_var1, new_var2, new_var3, new_var4, new_var5, new_var6)
        probabilistic_file_writer.write(rule_string)
        number_of_new_rules += 4
        multiplication_factor += 3

for index, edge in enumerate(line_list):
    # line = "{0} {1} {2}\n".format(edge[0], edge[1], 0.99)
    line = "{0} {1} {2}\n".format(edge[0], edge[1], 0.5)
    # abstract_file_writer.write(line)

    rule_string = "edge({0}, {1}).\n".format(edge[0], edge[1])
    IS_string += "in({0},{1},1) ".format(edge[0], edge[1])
    probabilistic_file_writer.write(rule_string)

    # rule_string = "in({0}, {1}) :- edge({0}, {1}).\n"\
    #         .format(edge[0], edge[1])
    rule_string = "{{ in({0}, {1}, 1) }} :- edge({0}, {1}).\n"\
            .format(edge[0], edge[1])
    probabilistic_file_writer.write(rule_string)

    rule_string = "in({0}, {1}) :- in({0}, {1}, 1).\n"\
            .format(edge[0], edge[1])

    probabilistic_file_writer.write(rule_string)
    number_of_new_rules += 2
    multiplication_factor += 1

# putting source and desination
rule_string = "last({0}).\n".format(des)
probabilistic_file_writer.write(rule_string)
# abstract_file_writer.write(rule_string)

rule_string = "first({0}).\n".format(src)
probabilistic_file_writer.write(rule_string)
# abstract_file_writer.write(rule_string)
IS_file_writer.write(IS_string + "0\n")

probabilistic_file_writer.close()
# abstract_file_writer.close()
IS_file_writer.close()

# print("Max variable after probabilistic encoding: {0}".format(max_node))
print("Number of new rules added: {0}".format(number_of_new_rules))
print("The multiplication factor: {0}".format(multiplication_factor))
file_pointer.close()

