import numpy as np

from pyqtgraph.Qt import QtGui


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


def getPath(mask):
    """
    Return the path of the countour of a boolean numpy 2d-array.
    """
    path = QtGui.QPainterPath()
    for i in range(mask.shape[0]):
        for j in range(mask.shape[1]):
            # Draw vertical lines
            if i == 0:  # Border first
                if mask[i, j]:
                    path.moveTo(i, j)
                    path.lineTo(i, j + 1)
            elif i == mask.shape[0] - 1:
                if mask[i, j]:
                    path.moveTo(i + 1, j)
                    path.lineTo(i + 1, j + 1)
            else:
                if mask[i, j] != mask[i + 1, j]:
                    path.moveTo(i + 1, j)
                    path.lineTo(i + 1, j + 1)
            # Draw horizontal lines
            if j == 0:  # Border first
                if mask[i, j]:
                    path.moveTo(i, j)
                    path.lineTo(i + 1, j)
            elif j == mask.shape[1] - 1:
                if mask[i, j]:
                    path.moveTo(i, j + 1)
                    path.lineTo(i + 1, j + 1)
            else:
                if mask[i, j] != mask[i, j + 1]:
                    path.moveTo(i, j + 1)
                    path.lineTo(i + 1, j + 1)
    return path
