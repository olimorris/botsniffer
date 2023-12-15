class Tree:
    """
    Produce a Python dictionary of the bot dependencies
    """

    def __init__(self, data):
        self.data = data
        self.tree = {}

    def grow(self, parent_bot):
        """
        Grow the tree
        """
        self.tree[parent_bot] = self._build_dependencies(parent_bot)
        return self.tree

    def _build_dependencies(self, bot):
        nested_deps = []
        for dep in self.data.get(bot, []):
            if dep in self.data:
                nested_deps.append({dep: self._build_dependencies(dep)})
            else:
                nested_deps.append({dep: []})
        return nested_deps
