class DisjointSetForest:
    def __init__(self, elements):
        self._core = _DisjointSetForestCore()
        self.element_to_id = {}
        self.id_to_element = {}
        for element in elements:
            eid = self._core.make_set()
            self.element_to_id[element] = eid
            self.id_to_element[eid] = element

    def find_set(self, element):
        return self.id_to_element[
            self._core.find_set(
                self.element_to_id[element]
            )
        ]

    def union(self, x, y):
        x_id = self.element_to_id[x]
        y_id = self.element_to_id[y]
        self._core.union(x_id, y_id)

    def in_same_set(self, x, y):
        return self.find_set(x) == self.find_set(y)


class _DisjointSetForestCore:
    def __init__(self):
        self._parent = []
        self._rank = []
        self._size_of_set = []

    def make_set(self):
        x = len(self._parent)
        self._parent.append(None)
        self._rank.append(0)
        self._size_of_set.append(1)
        return x

    def find_set(self, x):
        try:
            parent = self._parent[x]
        except IndexError:
            raise ValueError(f"{x} is not in the collection.")

        if parent is None:
            return x

        root = self.find_set(parent)
        self._parent[x] = root
        return root

    def union(self, x, y):
        x_rep = self.find_set(x)
        y_rep = self.find_set(y)

        if x_rep == y_rep:
            return

        if self._rank[x_rep] > self._rank[y_rep]:
            self._parent[y_rep] = x_rep
            self._size_of_set[x_rep] += self._size_of_set[y_rep]
        else:
            self._parent[x_rep] = y_rep
            self._size_of_set[y_rep] += self._size_of_set[x_rep]
            if self._rank[x_rep] == self._rank[y_rep]:
                self._rank[y_rep] += 1


def slc(graph, d, k):
    nodes = list(graph.nodes)
    n = len(nodes)

    if not 1 <= k <= n:
        raise ValueError("k must be between 1 and the number of graph nodes")

    dsf = DisjointSetForest(nodes)
    number_of_clusters = n

    for u, v in sorted(graph.edges, key=d):
        if not dsf.in_same_set(u, v):
            dsf.union(u, v)
            number_of_clusters -= 1
            if number_of_clusters == k:
                break

    if number_of_clusters != k:
        raise ValueError("the graph does not contain enough edges to form k clusters")

    clusters = {}
    for node in nodes:
        root = dsf.find_set(node)
        clusters.setdefault(root, set()).add(node)

    return frozenset(frozenset(cluster) for cluster in clusters.values())
