from collections import defaultdict
from itertools import chain
from math import floor

class DisjointSetStruct(object):
    def __init__(self):
        self.disjoint_sets = []

    def __iter__(self):
        return self.disjoint_sets.__iter__()

    def __contains__(self, element):
        return element in chain(map(lambda s: s.__iter__(), self.disjoint_sets))

    def make_set(self, obj):
        new_set = DisjointSet(obj)
        self.disjoint_sets.append(new_set)
        return new_set

class DisjointSetElement(object):
    def __init__(self, element, containing_set, next_elem=None):
        self.element = element
        self.containing_set = containing_set
        self.next_elem = next_elem

class DisjointSet(object):
    class DisjointSetIter(object):
        def __init__(self, disjoint_set):
            self.next = disjoint_set.head

        def __iter__(self):
            return self

        def __next__(self):
            if self.next is None:
                raise StopIteration
            current = self.next
            self.next = self.next.next_elem
            return current.element

    def __init__(self, element):
        self.head = DisjointSetElement(element, self)
        self.tail = self.head

    def __iter__(self):
        return self.DisjointSetIter(self)

    def union(self, other):
        self.tail.next_elem = other.head
        self.tail = other.tail

        current_node = other.head
        while current_node != None:
            current_node.containing_set = self
            current_node = current_node.next_elem

        other.head = None

        return self

class Point(object):
    def __init__(self, **kwargs):
        self.y0 = kwargs['y0']
        self.data = kwargs['data']

class PointGrouper(object):
    def __init__(self, **kwargs):
        self.tolerance = kwargs['tolerance']

    def group(self, points):
        if len(points) == 0:
            return []

        partitions = defaultdict(list)
        max_y = max(points, key=lambda pt: pt.y0).y0
        min_y = min(points, key=lambda pt: pt.y0).y0

        def partition_index(tolerance, y):
            return floor( (y - min_y) / (tolerance * 2) )

        acc = DisjointSetStruct()
        for point in points:
            new_set = acc.make_set(point)
            partitions[partition_index(self.tolerance, point.y0)].append(new_set.head)

        partitions_iter = iter(partitions.values())
        partition = next(partitions_iter)
        while partition is not None:
            next_partition = next(partitions_iter, None)

            for p1 in partition:
                for p2 in partition:
                    if p1.containing_set != p2.containing_set:
                        if abs(p1.element.y0 - p2.element.y0) < self.tolerance:
                            p1.containing_set.union(p2.containing_set)

                if next_partition is not None:
                    for p2 in next_partition:
                        if p1.containing_set != p2.containing_set:
                            if abs(p1.element.y0 - p2.element.y0) < self.tolerance:
                                p1.containing_set.union(p2.containing_set)
            partition = next_partition

        return list(filter(lambda disjoint_set: len(list(disjoint_set)) > 0, acc))
