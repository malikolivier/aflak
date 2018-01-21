import numpy as np


def north(node):
    return (node[0], node[1] - 1)


def south(node):
    return (node[0], node[1] + 1)


def west(node):
    return (node[0] - 1, node[1])


def east(node):
    return (node[0] + 1, node[1])


def toIntTuple(arraylike):
    return int(arraylike[0]), int(arraylike[1])


def floodfill(img, node, predicate):
    firstNode = toIntTuple(node)
    mask = np.zeros(img.shape, dtype=bool)
    mask[firstNode] = True
    queue = [firstNode]
    while len(queue) > 0:
        node = queue.pop()
        N = north(node)
        S = south(node)
        W = west(node)
        E = east(node)
        for nextNode in [N, S, W, E]:
            if (nextNode[0] < 0 or nextNode[0] >= img.shape[0] or
                    nextNode[1] < 0 or nextNode[1] >= img.shape[1]):
                continue
            if (not mask[nextNode]) and predicate(img[nextNode]):
                mask[nextNode] = True
                queue.append(nextNode)
    return mask
