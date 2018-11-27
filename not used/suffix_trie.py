from copy import deepcopy
# creates nodes and provides a
# convenient interface for the suffix trie
# this was intended to replace substring however has
# been abandoned as substring was replaced by
# coincidence index instead


class trie_node:

    # upon initialization the set the character
    # and make a child $ to terminate the string
    # and set the depth to 0
    def __init__(self, character):
        self.character = character
        self.children = ["$"]
        self.depth = 0

    # add another node or another string to the tree
    def add_child(self, child):
        # create a new node if child is a string
        child = trie_node(child) if isinstance(child, str) else deepcopy(child)

        # update the depth the root of the child tree
        # and then all children of the new child if they exist
        for node in child.get_each():
            node.depth += self.depth + 1

        # update the chilren list
        if self.children == ["$"]:
            self.children = [child]
        else:
            self.children.append(child)

    # return the list of children
    def get_children(self):
        return self.children

    # return the character at the node
    def get_character(self):
        return self.character

    # generator to return every node
    # from the parent down to its leaves
    def get_each(self):

        # yield the parent
        yield self

        # yield each of the children
        for child in self.children:
            if not (child == "$"):
                yield from child.get_each()

    # string representation of the node down to its leaves
    # complete with tabbing to represent depth
    def __str__(self):
        string = ""
        for child in self.get_each():
            if not (child == "$"):
                string += child.depth * "\t" + child.character
            string += "\n"
        return string


if __name__ == "__main__":
    # this is going to be fun

    suffix_trie2 = trie_node('d')
    suffix_trie2.add_child('b')
    suffix_trie2.add_child('c')
    suffix_trie2.add_child('d')
    suffix_trie2.add_child('e')

    suffix_trie = trie_node('c')
    suffix_trie.add_child('b')
    suffix_trie.add_child('c')
    suffix_trie.add_child('d')
    suffix_trie.add_child('e')
    suffix_trie.add_child(suffix_trie2)

    temp_suffix_trie = trie_node('g')
    temp_suffix_trie.add_child('f')
    temp_suffix_trie.add_child('h')
    temp_suffix_trie.add_child('j')
    temp_suffix_trie.add_child('k')

    temp2_suffix_trie = trie_node('r')
    temp2_suffix_trie.add_child('f')
    temp2_suffix_trie.add_child('h')
    temp2_suffix_trie.add_child('j')
    temp2_suffix_trie.add_child('k')

    for i in suffix_trie.get_each():
        if i.get_character() == 'e':
            i.add_child(temp_suffix_trie)

    add_list = []
    for i in suffix_trie.get_each():
        if i.get_character() == 'k':
            add_list.append(i)
    for i in add_list:
        i.add_child(temp2_suffix_trie)
    print(suffix_trie)
