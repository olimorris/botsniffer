from treelib import Tree


class Formatter:
    """
    Format the bot output
    """

    def __init__(self, data):
        self.data = data
        self.counter = 0
        self.tree = Tree()

    def to_tree(self, parent_bot):
        """
        Format to a tree using the treelib library
        """
        self.tree.create_node(parent_bot, parent_bot)
        self._add_nodes(parent_bot, self.data[parent_bot], parent_id=parent_bot)

        return self

    def _add_nodes(self, parent_name, children, parent_id=None):
        if isinstance(children, list):
            for child in children:
                for key, value in child.items():
                    child_id = f"{key}_{self.counter}"  # Create a unique ID
                    self.counter += 1
                    self.tree.create_node(key, child_id, parent=parent_id)
                    self._add_nodes(key, value, parent_id=child_id)
        elif isinstance(children, dict):
            for key, value in children.items():
                child_id = f"{key}_{self.counter}"  # Create a unique ID
                self.counter += 1
                self.tree.create_node(key, child_id, parent=parent_id)
                self._add_nodes(key, value, parent_id=child_id)

    def prune(self, max_depth):
        """
        Prune the tree to a specified depth
        """
        self._prune_node(self.tree.root, 0, max_depth)
        return self

    def _prune_node(self, node_id, current_depth, max_depth):
        if current_depth >= max_depth:
            self.tree.remove_node(node_id)
        else:
            child_ids = [child.identifier for child in self.tree.children(node_id)]
            for child_id in child_ids:
                self._prune_node(child_id, current_depth + 1, max_depth)
