from copy import deepcopy
# creates nodes and provides a
# convenient interface for the suffix trie


class trie_node:

    # upon initialization the set the character
    # and make a child $ to terminate the string
    def __init__(self, character):
        self.character = character
        self.children = ["$"]
        self.depth = 0

    def add_child(self, child):
        node = trie_node(child) if isinstance(child, str) else child

        for child in node.get_each():
            child.depth += self.depth + 1

        if self.children == ["$"]:
            self.children = [node]
        else:
            self.children.append(node)

    def get_children(self):
        return self.children

    def get_character(self):
        return self.character

    def get_each(self):
        yield self

        for child in self.children:
            if not (child == "$"):
                yield from child.get_each()

    def __str__(self):
        string = ""
        for child in self.get_each():
            if not (child == "$"):
                string += child.depth * "\t" + child.character
            string += "\n"
        return string


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
        i.add_child(deepcopy(temp_suffix_trie))

add_list = []
for i in suffix_trie.get_each():
    if i.get_character() == 'k':
        add_list.append(i)
for i in add_list:
    i.add_child(deepcopy(temp2_suffix_trie))
print(suffix_trie)
