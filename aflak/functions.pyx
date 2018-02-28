import numpy as np
cimport numpy as np
cimport cython

from pyqtgraph.Qt import QtGui


ctypedef struct POINT_t:
    int x
    int y

cdef inline POINT_t north(POINT_t node):
    cdef POINT_t p
    p.x = node.x
    p.y = node.y - 1
    return p


cdef inline POINT_t south(POINT_t node):
    cdef POINT_t p
    p.x = node.x
    p.y = node.y + 1
    return p


cdef inline POINT_t west(POINT_t node):
    cdef POINT_t p
    p.x = node.x - 1
    p.y = node.y
    return p


cdef inline POINT_t east(POINT_t node):
    cdef POINT_t p
    p.x = node.x + 1
    p.y = node.y
    return p

# np.ndarray[dtype=np.float, ndim=2]
@cython.boundscheck(False)
def floodfill(img, node_, predicate):
    cdef POINT_t firstNode
    firstNode.x = node_[0]
    firstNode.y = node_[1]
    cdef np.ndarray[dtype=np.int8_t, ndim=2] mask = np.zeros((img.shape[0], img.shape[1]), dtype=np.int8)
    mask[firstNode.x, firstNode.y] = 1
    cdef list queue = [firstNode]
    cdef POINT_t node, N, S, W, E, nextNode
    while len(queue) > 0:
        node = queue.pop()
        N = north(node)
        S = south(node)
        W = west(node)
        E = east(node)
        for nextNode in [N, S, W, E]:
            if (nextNode.x < 0 or nextNode.x >= img.shape[0] or
                    nextNode.y < 0 or nextNode.y >= img.shape[1]):
                continue
            if (not mask[nextNode.x, nextNode.y]) and predicate(img[nextNode.x, nextNode.y]):
                mask[nextNode.x, nextNode.y] = 1
                queue.append(nextNode)
    return mask.view(dtype=np.bool)


@cython.boundscheck(False)
def getPath(np.ndarray[np.uint8_t, cast=True, ndim=2] mask):
    """
    Return the path of the countour of a boolean numpy 2d-array.
    """
    cdef int imax = mask.shape[0]
    cdef int jmax = mask.shape[1]
    cdef int i, j
    path = QtGui.QPainterPath()
    for i in range(imax):
        for j in range(jmax):
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


def makeArrowPath(headLen, tipAngle, tailLen, tailWidth):
    """
    Make arrow path for which origin is the extremity of the arrow's tail.
    """
    headWidth = headLen * np.tan(tipAngle * 0.5 * np.pi/180.)
    path = QtGui.QPainterPath()
    path.moveTo(0, 0)
    path.lineTo(0, -tailWidth/2)
    path.lineTo(-tailLen, -tailWidth/2)
    path.lineTo(-tailLen, -tailWidth/2 - headWidth/2)
    path.lineTo(-tailLen - headLen, 0)
    path.lineTo(-tailLen, tailWidth/2 + headWidth/2)
    path.lineTo(-tailLen, tailWidth/2)
    path.lineTo(0, tailWidth/2)
    path.lineTo(0, 0)
    return path
