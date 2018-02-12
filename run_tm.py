import os

from Nodes import HeadNode

combined = open("combined.def", "r").read()
var1 = combined.find("####")
var2 = combined.find("####", var1 + 1)
def1 = combined.find("+++", var2 + 1)
def2 = combined.find("---", def1 + 1)
exec1 = combined.find("##", def2 + 1)
exec2 = combined.find("##", exec1 + 1)

var_dec = combined[var1 + 5:var2]
def_dec = combined[def1 + 4:def2]
exec_dec = combined[exec1 + 3:exec2]


def add_node(parent_ident, name_ident, l, opt):
    if parent_ident == "head":
        head_nodes.append(HeadNode(name_ident, opt))
    else:
        for h in head_nodes:
            h.add_new_group(parent_ident, name_ident, l, opt)


def add_exec_node(parent_ident, name_ident, orde, opt):
    for h in head_nodes:
        h.add_new_exec_group(parent_ident, name_ident, orde, opt)


defined_vars = {}
lines = var_dec.split("\n")
for line in lines:
    s1 = line.find("$")
    if s1 >= 0:
        s2 = line.find("$", s1 + 1)
        key = line[s1:s2 + 1]
        value = line.replace(key + "=", "")
        defined_vars[key] = value


#
# CREATE DEF NODES
#
head_nodes = []
o1 = def_dec.find("{")
layer = 0
rep_def = def_dec
while o1 >= 0:
    layer += 1
    o2 = def_dec.find("}", o1 + 1)
    rep_def = rep_def.replace(def_dec[o1:o2 + 1], "{" + str(layer) + "}")
    grp = def_dec[o1 + 1:o2]
    so1 = grp.find("[")
    while so1 >= 0:
        so2 = grp.find("]", so1 + 1)
        subgrp = grp[so1 + 1:so2]
        p_def1 = subgrp.find("(")
        p_def2 = subgrp.find(")", p_def1 + 1)
        p_def = subgrp[p_def1 + 1:p_def2]
        n_def1 = subgrp.find("(", p_def2 + 1)
        n_def2 = subgrp.find(")", n_def1 + 1)
        n_def = subgrp[n_def1 + 1:n_def2]
        option = subgrp[n_def2 + 1:]
        if "$name$" in n_def:
            names = option.split(",")
            n_def_base = n_def
            for name in names:
                n_def = n_def_base.replace("$name$", name)
                option = name
                add_node(p_def, n_def.replace("\n", ""), layer, "$name$\n")
        else:
            add_node(p_def, n_def, layer, option)
        so1 = grp.find("[", so1 + 1)
    o1 = def_dec.find("{", o1 + 1)

for key in defined_vars.keys():
    rep_def = rep_def.replace(key, defined_vars[key])

replaceable_def = open("rep.def", "w")
replaceable_def.write(rep_def)

#
# CREATE EXEC NODES
#
o1 = exec_dec.find("{")
order = 0
rep_exec = exec_dec
while o1 >= 0:
    order += 1
    o2 = exec_dec.find("}", o1 + 1)
    rep_exec = rep_exec.replace(exec_dec[o1:o2 + 1], "{" + str(order) + "}")
    grp = exec_dec[o1 + 1:o2]
    so1 = grp.find("[")
    while so1 >= 0:
        so2 = grp.find("]", so1 + 1)
        subgrp = grp[so1 + 1:so2]
        p_def1 = subgrp.find("(")
        p_def2 = subgrp.find(")", p_def1 + 1)
        p_def = subgrp[p_def1 + 1:p_def2]
        n_def1 = subgrp.find("(", p_def2 + 1)
        n_def2 = subgrp.find(")", n_def1 + 1)
        n_def = subgrp[n_def1 + 1:n_def2]
        option = subgrp[n_def2 + 1:]
        if "$name$" in n_def:
            names = option.split(",")
            n_def_base = n_def
            for name in names:
                n_def = n_def_base.replace("$name$", name)
                option = name
                add_exec_node(p_def, n_def.replace("\n", ""), order, option)
        else:
            add_exec_node(p_def, n_def, order, option)
        so1 = grp.find("[", so1 + 1)
    o1 = exec_dec.find("{", o1 + 1)

for key in defined_vars.keys():
    rep_exec = rep_exec.replace(key, defined_vars[key])

replaceable_exec = open("rep.exec", "w")
replaceable_exec.write(rep_exec)

print(head_nodes)

for h in head_nodes:
    h.make_dirs(os.curdir)
    h.make_def(os.curdir, rep_def)
    h.make_exec(os.curdir, rep_exec)
