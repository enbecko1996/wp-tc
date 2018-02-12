import os


class Node:
    def __init__(self, name, option, layer, parent, is_head=False):
        self.name = name
        self.option = option
        self.layer = layer
        self.parent = parent
        self.is_head = is_head
        self.children = []
        self.exec_nodes = []

    def force_add_on_layer(self, parent_ident, name_ident, layer, option):
        if self.layer + 1 == layer:
            self.children.append(Node(name_ident, option, self.layer + 1, self))
        else:
            for c in self.children:
                c.force_add_on_layer(parent_ident, name_ident, layer, option)

    def add_new_group(self, parent_ident, name_ident, layer, option):
        if self.layer + 1 == layer and (parent_ident == self.name or parent_ident == "all"
                                        or ("$name$" in parent_ident
                                            and parent_ident.replace("$name$", self.name.replace(parent_ident.replace("$name$", ""), "")) == self.name)):
            self.children.append(Node(name_ident, option, self.layer + 1, self))
        elif self.layer < layer and parent_ident == self.name:
            self.force_add_on_layer(parent_ident, name_ident, layer, option)
        else:
            for c in self.children:
                c.add_new_group(parent_ident, name_ident, layer, option)

    def force_add_exec_on_layer(self, parent_ident, name_ident, order, option):
        if len(self.children) == 0:
            self.exec_nodes.append(Node(name_ident, option, order, self))
        else:
            for c in self.children:
                c.force_add_exec_on_layer(parent_ident, name_ident, order, option)

    def add_new_exec_group(self, parent_ident, name_ident, order, option):
        if len(self.children) == 0 and (parent_ident == self.name or parent_ident == "all"
                or ("$name$" in parent_ident
                and parent_ident.replace("$name$", self.name.replace(parent_ident.replace("$name$", ""), "")) == self.name)):
            self.exec_nodes.append(Node(name_ident, option, order, self))
        elif parent_ident == self.name:
            self.force_add_exec_on_layer(parent_ident, name_ident, order, option)
        else:
            for c in self.children:
                c.add_new_exec_group(parent_ident, name_ident, order, option)

    def make_dirs(self, cur_dir):
        cur_dir += "/" + self.name
        if len(self.children) == 0:
            if not os.path.exists(cur_dir):
                os.makedirs(cur_dir)
        else:
            for c in self.children:
                c.make_dirs(cur_dir)

    def make_def(self, cur_dir, cur_def):
        cur_dir += "/" + self.name
        cur_def = cur_def.replace("{" + str(self.layer) + "}\n", self.option)
        if self.option == "$name$\n":
            cur_def = cur_def.replace("$name$", self.name)
        if len(self.children) == 0:
            lines = cur_def.split("\n")
            for l_i in range(len(lines)):
                line = lines[l_i]
                if line.startswith("$file_cont$="):
                    file = open(line.replace("$file_cont$=", ""), "r")
                    lines[l_i] = file.read()
            out_def = open(cur_dir + "/def.def", "w")
            for line in lines:
                line += "\n"
                out_def.write(line)
        else:
            for c in self.children:
                c.make_def(cur_dir, cur_def)

    def make_exec(self, cur_dir, cur_exec):
        cur_dir += "/" + self.name
        if len(self.children) == 0:
            print(self.exec_nodes)
            for exec_node in self.exec_nodes:
                print("{" + str(exec_node.layer) + "}\n")
                cur_exec = cur_exec.replace("{" + str(exec_node.layer) + "}\n", exec_node.option)
            out_exec = open(cur_dir + "/exec.sh", "w")
            out_exec.write(cur_exec)
        else:
            for c in self.children:
                c.make_exec(cur_dir, cur_exec)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.name + ", children: " + str(self.children)


class HeadNode(Node):
    def __init__(self, name, option):
        super().__init__(name, option, layer=1, parent=None)
