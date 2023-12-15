import json


class Counter:
    def __init__(self, data):
        self.data = data
        self.bots = {}

    def count(self):
        self._count_values(self.data)
        return self

    def sort(self, descending=True):
        return dict(
            sorted(self.bots.items(), key=lambda item: item[1], reverse=descending)
        )

    def _count_values(self, node):
        if isinstance(node, dict):
            for value in node.values():
                self._count_values(value)
        elif isinstance(node, list):
            for item in node:
                if isinstance(item, str):
                    self.bots[item] = self.bots.get(item, 0) + 1
                else:
                    self._count_values(item)

    def save2file(self, path):
        with open(path, "w") as f:
            json.dump(self.sort(), f, indent=4)
