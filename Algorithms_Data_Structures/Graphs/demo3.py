import yaml
import ast


def get_data():
    f = open("input.yml", "r")
    data = yaml.load(f)
    f.close()

    lst_values = (data['edges'])

    lst_invalid_values = []
    lst_invalid_paths = data['invalid_paths']
    for path in lst_invalid_paths:
        new_item = ast.literal_eval(path)
        lst_invalid_values.append((new_item))

    lst_new_values = []

    for item in lst_values:
        new_item = ast.literal_eval(item)
        lst_new_values.append((new_item))

    return lst_new_values, lst_invalid_values


class Node:
    def __init__(self, node_name, num):
        self.name = node_name
        self.id = num
        self.children_nodes = {}

    def __str__(self):
        return str(self.name) + ' children: ' + str([x.name for x in self.children_nodes])

    def add_child(self, child_node, weight=0):
        self.children_nodes[child_node] = weight

    def get_child_connections(self):
        return self.children_nodes.keys()

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        if neighbor in self.children_nodes:
            return self.children_nodes[neighbor]


class Graph:
    def __init__(self):
        self.dct_nodes = {}
        self.num_nodes = 0

    def add_node(self, node_name):
        self.num_nodes = self.num_nodes + 1
        if node_name not in self.dct_nodes:
            new_node = Node(node_name, self.num_nodes)
            self.dct_nodes[node_name] = new_node
            return new_node
        else:
            print('Node already present in Graph')

    def get_node(self, node_name):
        if node_name in self.dct_nodes:
            return self.dct_nodes[node_name]
        else:
            return None

    def get_total_nodes(self):
        return self.num_nodes

    def add_edge(self, start, end, weight=1):
        if start not in self.dct_nodes:
            self.add_node(start)
        if end not in self.dct_nodes:
            self.add_node(end)
        self.dct_nodes[start].add_child(self.dct_nodes[end], weight)

    def get_all_start_nodes(self):
        # All the nodes in the Graph
        set_of_node_names = set(self.dct_nodes)

        # Iterating over the Graph and getting the Connection Node names
        for node_name in self.dct_nodes:
            connected_node_names = self.get_all_child_connections(node_name)
            set_connected_node_names = set(connected_node_names)

            # Getting the final set of nodes which doesnt appear in connected nodes
            set_of_node_names -= set_connected_node_names
            # This gives the list of start nodes in the graph as they dont appear in connected nodes
        self.start_nodes = list(set_of_node_names)
        return self.start_nodes

    def get_all_end_nodes(self):
        lst_end_nodes = []
        for node_name in self.dct_nodes:
            if not self.dct_nodes[node_name].get_child_connections():
                lst_end_nodes.append(node_name)
        self.end_nodes = lst_end_nodes
        return self.end_nodes

    def get_weight(self, node1_name, node2_name):
        node1 = self.get_node(node1_name)
        node2 = self.get_node(node2_name)
        weight = node1.get_weight(node2)
        return weight if weight else 0

    def get_all_child_connections(self, node_name):
        node = self.get_node(node_name)
        connected_node_names = []
        for connected_node in node.get_child_connections():
            connected_node_names.append(connected_node.get_name())
        return connected_node_names

    def find_paths_between_nodes(self, start, end, loop_count=1, path=[]):
        paths = []
        if start not in self.dct_nodes or end not in self.dct_nodes:
            return paths

        path = path + [start]

        if start == end:
            return [path]

        for node in self.get_all_child_connections(start):
            # if node not in path:
            if path.count(node) < loop_count:
                newpaths = self.find_paths_between_nodes(node, end, loop_count, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    def find_shortest_path(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if start not in self.dct_nodes:
            return None
        shortest = None
        for node in self.get_all_child_connections(start):
            if node not in path:
                newpath = self.find_shortest_path(node, end, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest

    def find_all_paths(self):
        lst_all_paths = []
        start_nodes = self.get_all_start_nodes()
        end_nodes = self.get_all_end_nodes()
        for start_node in start_nodes:
            for end_node in end_nodes:
                path = self.find_paths_between_nodes(start_node, end_node)
                lst_all_paths.extend(path)
        return lst_all_paths

    def get_valid_coverage_old(self, lst_invalid_paths):
        lst_all_paths = self.find_all_paths()
        set_all_paths = set(tuple(path) for path in lst_all_paths)
        set_invalid_paths = set(tuple(path) for path in lst_invalid_paths)
        valid_paths = set_all_paths - set_invalid_paths

        valid_paths = list(list(path) for path in valid_paths)
        return valid_paths

    def get_valid_coverage(self, lst_invalid_paths):
        lst_str_invalid_paths = self.convert_lst_str(lst_invalid_paths)
        lst_str_graph_paths = self.convert_lst_str(self.find_all_paths())
        lst_str_valid_paths = lst_str_graph_paths.copy()

        for str_invalid_path in lst_str_invalid_paths:
            for str_graph_path in lst_str_graph_paths:
                out = str_graph_path.find(str_invalid_path)
                if out >= 0:
                    if str_graph_path in lst_str_valid_paths:
                        lst_str_valid_paths.remove(str_graph_path)

        lst_valid_paths = self.convert_str_lst(lst_str_valid_paths)
        return lst_valid_paths

    def convert_lst_str(self, lst_of_items):
        lst_str_items = []
        for item in lst_of_items:
            str_item = ''.join(item)
            lst_str_items.append(str_item)
        return lst_str_items

    def convert_str_lst(self, lst_str_items):
        lst_items = []
        for item in lst_str_items:
            lst_items.append(list(item))
        return lst_items

    def clone(self, src_node_name, target_node_name):
        src_node = Node(src_node_name, self.num_nodes + 1)
        self.dct_nodes[src_node_name] = src_node
        target_node = self.get_node(target_node_name)

        # Assign the children of target_node to the src_node along the weights
        src_node.children_nodes = target_node.children_nodes.copy()

        # Assign the parents of target_node to the src_node along with the weights
        parent_node_names = self.get_parent_node_names(target_node_name)
        for parent_name in parent_node_names:
            weight = self.get_weight(parent_name, target_node_name)
            self.add_edge(parent_name, src_node_name, weight)

        return src_node

    def get_parent_node_names(self, child_node_name):
        lst_parent_nodes_names = []
        for node_name in self.dct_nodes:
            if child_node_name in self.get_all_child_connections(node_name):
                lst_parent_nodes_names.append(node_name)
        return lst_parent_nodes_names

    def get_node_id_from_name(self, node_name):
        node = self.get_node(node_name)
        return node.get_id()

    def construct_mapping_dcts_ids_names(self):
        self.dct_name_id = {}
        self.dct_id_name = {}
        for name in self.dct_nodes:
            node = self.get_node(name)
            id = node.get_id()
            self.dct_name_id[name] = id
            self.dct_id_name[id] = name
        return self

    def get_all_node_names(self):
        return list(self.dct_nodes.keys())


if __name__ == '__main__':
    cyle_count = 2
    g = Graph()
    input_datas, invalid_paths = get_data()

    for data in input_datas:
        g.add_edge(*data)

    # print(g.get_all_start_nodes())
    # print(g.get_all_end_nodes())
    #
    # print(g.get_weight('a', 'b'))
    # print(g.get_all_child_connections('b'))
    #
    # #
    #
    # print('>' * 100)
    # print(g.find_paths_between_nodes('a', 'f'))
    # print('>' * 100)
    #
    # from functools import partial
    #
    # print('Path with One loop >>>>>>')
    # find_paths_between_nodes_with_no_loop = partial(g.find_paths_between_nodes, loop_count=1, path=[])
    # print(find_paths_between_nodes_with_no_loop('a', 'f'))
    # print('>' * 100)
    #
    # print('Path with Two loops >>>>>>')
    # find_paths_between_nodes_with_one_loop = partial(g.find_paths_between_nodes, loop_count=2, path= [])
    # print(find_paths_between_nodes_with_one_loop('a', 'f'))
    # print('>' * 100)
    # print(g.find_shortest_path('a', 'f'))

    print(g.find_all_paths())

    # invalid_paths = [['a', 'b', 'd', 'e', 'f'], ['a', 'c', 'd', 'e', 'f']]
    # invalid_paths = [('a', 'b', 'd', 'e', 'f'), ('a', 'c', 'd', 'e', 'f')]

    print(g.get_valid_coverage(invalid_paths))

    # print('>>> Cloning Node w as c  >>>>')
    # g.clone('w', 'c')
    #
    # print(g.get_weight('c', 'f'))
    # print(g.get_weight('w', 'f'))
    # #
    # print(g.find_paths_between_nodes('a', 'w'))
    # print(g.find_paths_between_nodes('a', 'c'))
    #
    #
    # #
    # g.construct_mapping_dcts_ids_names()
    #
    # print(g.get_node_id_from_name('b'))
    # print(g.get_node_id_from_name('w'))
    #
    # print(g.dct_id_name)
    # print(g.dct_name_id)
    #
    # print(g.get_node('a'))
