from timeit import default_timer as timer
import copy
from pip._vendor.distlib.compat import raw_input


class Node:
    def __init__(self, info, h):
        self.info = info
        self.h = h

    def __str__(self):
        string = ""
        for i in range(len(self.info)):
            for j in range(len(self.info[i])):
                string += self.info[i][j]
            string += "\n"
        return string

    def __repr__(self):
        string = ""
        for i in range(len(self.info)):
            for j in range(len(self.info[i])):
                string += self.info[i][j]
            string += "\n"
        string += "\n"
        return string


class Problem:
    def __init__(self, start=None):
        if start is None:
            start = START
        self.nodeStart = Node(start, float("inf"))
        self.ROWS = len(start)
        self.COLUMNS = len(start[0])
        self.EMPTY = '#'


class NodParcurgere:
    problem = None

    def __init__(self, nodeGraph, parent=None, g=0, f=None):
        self.nodeGraph = nodeGraph
        self.parent = parent
        self.g = g
        if f is None:
            self.f = self.g + self.nodeGraph.h
        else:
            self.f = f

    def graphPath(self):
        nodeC = self
        path = [nodeC]
        while nodeC.parent is not None:
            path = [nodeC.parent] + path
            nodeC = nodeC.parent
        return path

    def containsInPath(self, node):
        nodeC = self
        while nodeC.parent is not None:
            if node.info == nodeC.nodeGraph.info:
                return True
            nodeC = nodeC.parent
        return False

    """ Returns the unique elements from the current nodeGraph. """

    def unique(self, screen):
        unique = []
        for i in range(self.problem.ROWS):
            for j in range(self.problem.COLUMNS):
                if screen[i][j] != self.problem.EMPTY:
                    unique.append(screen[i][j])
        unique = set(unique)
        return len(unique)

    """ Returns the total number of colored elements from the current node. """

    def totalColoredSquares(self, screen):
        total = 0
        for i in range(self.problem.ROWS):
            for j in range(self.problem.COLUMNS):
                if screen[i][j] != self.problem.EMPTY:
                    total += 1
        return total

    def heuristic(self, newScreen):
        if HEURISTIC == 1:
            # The number of distinct colored elements (admissible)
            return self.unique(newScreen)

        if HEURISTIC == 2:
            # The number of distinct colored elements * total number of colored elements / total number of elements
            return self.unique(newScreen) * self.totalColoredSquares(newScreen) / (
                        self.problem.ROWS * self.problem.COLUMNS)

        if HEURISTIC == 3:
            # The total number of colored elements
            return self.totalColoredSquares(newScreen)

    def extend(self):

        """ A recursive function to replace color of the given element
            and all adjacent same colored elements with EMPTY. """

        def floodFill(screen, x, y, color, surrounding):
            # base cases
            if x < 0 or x >= self.problem.ROWS or y < 0 or y >= self.problem.COLUMNS:
                return
            if screen[x][y] != color:
                return
            if screen[x][y] == self.problem.EMPTY:
                return

            # replace the color at (x, y)
            screen[x][y] = self.problem.EMPTY

            # memorize all surroundings of (x, y)
            surrounding.append(screen[x][y])

            # recur for north, east, south and west
            floodFill(screen, x + 1, y, color, surrounding)
            floodFill(screen, x - 1, y, color, surrounding)
            floodFill(screen, x, y + 1, color, surrounding)
            floodFill(screen, x, y - 1, color, surrounding)

        """ All the elements above EMPTY "fall" into the places left vacant. """

        def fall(screen):
            for j in range(self.problem.COLUMNS):
                column = [screen[i][j] for i in range(len(screen))]
                for k in range(len(column)):
                    if column[k] == self.problem.EMPTY:
                        column.pop(k)
                        column[:0] = self.problem.EMPTY
                for k in range(len(column)):
                    screen[k][j] = column[k]

        """ If we have an empty column between columns, 
            the columns in the right move to the left. """

        def toTheLeft(screen):
            for j in range(self.problem.COLUMNS - 1, -1, -1):
                column = set([screen[i][j] for i in range(len(screen))])
                if len(column) == 1 and list(column)[0] == self.problem.EMPTY and j < self.problem.COLUMNS - 1:
                    for i in range(len(screen)):
                        screen[i][j], screen[i][j + 1] = screen[i][j + 1], screen[i][j]

        """ Total number of elements colored as the given element. """

        def total(screen, color):
            totalNumber = 0
            for i in range(self.problem.ROWS):
                for j in range(self.problem.COLUMNS):
                    if screen[i][j] == color:
                        totalNumber += 1
            return totalNumber

        # this is where the actual expansion begins
        successors = []
        for i in range(self.problem.ROWS):
            for j in range(self.problem.COLUMNS):

                screen = copy.deepcopy(self.nodeGraph.info)
                surrounding = []
                floodFill(screen, i, j, screen[i][j], surrounding)

                N = total(self.nodeGraph.info, self.nodeGraph.info[i][j])
                K = len(surrounding)
                cost = 1 + (N - K) / N

                heuristic = self.heuristic(screen)
                newNode = Node(screen, heuristic)
                if (newNode, cost) not in successors and len(surrounding) > 2:
                    fall(screen)
                    toTheLeft(screen)
                    successors.append((newNode, float("{:.2f}".format(cost))))

        return successors

    def scope(self):
        return self.unique(self.nodeGraph.info) == 0

    def __str__(self):
        parent = self.parent if self.parent is None else self.parent.nodeGraph.info
        return f"({self.nodeGraph}, parinte={parent}, f={self.f}, g={self.g})"


def strNodeInfo(list):
    string = ""
    for node in list:
        string += str(node.nodeGraph)
        string += "h = {}\n".format(node.nodeGraph.h)
        string += "Cost: " + str(node.g - node.parent.g) if node.g != 0 else ""
        string += "\n\n"
    string += "{} moves were made at a cost of {}".format(len(list) - 1, list[-1].f)
    return string


def inList(list, node):
    for i in range(len(list)):
        if list[i].nodeGraph.info == node.info:
            return list[i]
    return None


def AStar():
    rootNode = NodParcurgere(NodParcurgere.problem.nodeStart)

    if rootNode.scope():
        print("Initial state = final state")
        writeToTxt("Initial state = final state")
        return

    open = [rootNode]
    closed = []

    while len(open) > 0:
        nodeCurrent = open.pop(0)
        closed.append(nodeCurrent)

        if nodeCurrent.scope():
            break

        for successor, cost in nodeCurrent.extend():
            if not nodeCurrent.containsInPath(successor):
                nodeC = inList(closed, successor)
                gSuccessor = nodeCurrent.g + cost
                fSuccessor = gSuccessor + successor.h

                if nodeC is not None:
                    if fSuccessor < nodeC.f:
                        closed.remove(nodeC)
                        nodeC.parent = nodeCurrent
                        nodeC.g = gSuccessor
                        nodeC.f = fSuccessor
                        nodeSearch = nodeC
                else:
                    nodeC = inList(open, successor)
                    if nodeC is not None:
                        if fSuccessor < nodeC.f:
                            open.remove(nodeC)
                            nodeC.parent = nodeCurrent
                            nodeC.g = gSuccessor
                            nodeC.f = fSuccessor
                            nodeSearch = nodeC

                    else:
                        nodeSearch = NodParcurgere(successor, nodeCurrent, gSuccessor)
                    open.append(nodeSearch)
        open.sort(key=lambda node: (node.f, -node.g))

    print("\n------------------ Conclusion -----------------------")

    if len(open) == 0:
        print("Open List is empty, there is no path from root node to scope node")
        writeToTxt("Open List is empty, there is no path from root node to scope node")
    else:
        print("Minimum cost path:\n" + strNodeInfo(nodeCurrent.graphPath()))
        writeToTxt("Minimum cost path:\n" + strNodeInfo(nodeCurrent.graphPath()))


def menu():
    global HEURISTIC
    global INDEX

    print("1. Input file that has no solutions")
    print("2. Initial state = final state")
    print("3. Input file with a minimum cost path of length 3-5")
    print("4. Input file with a minimum cost path of length greater than 5")

    while True:
        value = raw_input("Select the input file: ")
        try:
            value = int(value)
        except ValueError:
            print("Valid number, please")
            continue
        if 1 <= value <= 4:
            break
        else:
            print("Valid range, please: 1-4")

    INDEX = value
    readFromTxt(value)

    print("\nHeuristics:")
    print("1. The number of distinct colored elements (admissible)")
    print(
        "2. The number of distinct colored elements * total number of colored elements / total number of elements (admissible)")
    print("3. The total number of colored elements")

    while True:
        value = raw_input("Select the input file: ")
        try:
            value = int(value)
        except ValueError:
            print("Valid number, please")
            continue
        if 1 <= value <= 3:
            break
        else:
            print("Valid range, please: 1-3")

    HEURISTIC = value
    print(" ---- Heuristic {} ---- \n".format(HEURISTIC))
    writeToTxt(" ---- Heuristic {} ---- \n".format(HEURISTIC))


def readFromTxt(index):
    global START
    try:
        file = open("input_{}.txt".format(index), "r")
        fileObj = file.readlines()

        START = []
        for i in range(len(fileObj)):
            row = []
            for j in range(len(fileObj[i])):
                row.append(fileObj[i][j])
            row.pop(-1) if row[-1] == "\n" else None
            START.append(row)
    except:
        print("Something went wrong")
    finally:
        file.close()


def writeToTxt(data):
    try:
        file = open("output_{}.txt".format(INDEX), "a")
        file.write(data)
    except:
        print("Something went wrong when writing to the file")
    finally:
        file.close()


if __name__ == "__main__":
    menu()
    start = timer()
    problem = Problem()
    NodParcurgere.problem = problem
    AStar()
    end = timer()
    print("Execution time: {}".format(end - start))
    writeToTxt("\nExecution time: {}\n\n".format(end - start))
    writeToTxt("____________________________________________\n\n")
