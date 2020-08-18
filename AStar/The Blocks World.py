import copy
from timeit import default_timer as timer

class Nod:
    def __init__(self, info, h):
        self.info = info
        self.h = h

    def __str__(self):
        return "({}, h={})".format(self.info, self.h)

    def __repr__(self):
        return f"({self.info}, h={self.h})"


class Arc:
    def __init__(self, capat, varf, cost):
        self.capat = capat
        self.varf = varf
        self.cost = cost

class Problema:
    def __init__(self, start = [['a'], ['c', 'b'], ['d']], scop = [['b', 'c'], [], ['d', 'a']]):
        self.nod_start = Nod(start, float("inf"))
        self.nod_scop = scop
        self.noduri = [self.nod_start]
        self.arce = []

    def cauta_nod_nume(self, info):
        for nod in self.noduri:
            if nod.info == info:
                return nod
        return None

class NodParcurgere:
    problema = None
    def __init__(self, nod_graf, parinte = None, g = 0, f = None):
        self.nod_graf = nod_graf
        self.parinte = parinte
        self.g = g
        if f is None:
            self.f = self.g + self.nod_graf.h
        else:
            self.f = f

    def drum_arbore(self):
        nod_c = self
        drum = [nod_c]
        while nod_c.parinte is not None:
            drum = [nod_c.parinte] + drum
            nod_c = nod_c.parinte
        return drum

    def contine_in_drum(self, nod):
        nod_c = self
        while nod_c.parinte is not None:
            if nod.info == nod_c.nod_graf.info:
                return True
            nod_c = nod_c.parinte
        return False

    def euristica_h(self, info):
        dictionar_info = {}
        for i in range(len(info)):
            for j in range(len(info[i])):
                dictionar_info[info[i][j]] = (i, j)
        dictionar_nod_scop = {}
        for i in range(len(self.problema.nod_scop)):
            for j in range(len(self.problema.nod_scop[i])):
                dictionar_nod_scop[self.problema.nod_scop[i][j]] = (i, j)
        euristica = 0
        for i in dictionar_info:
            if dictionar_info[i] != dictionar_nod_scop[i]:
                euristica += 1
        return euristica

    def expandeaza(self):
        l_succesori = []
        for i in range(len(self.nod_graf.info)):
            if len(self.nod_graf.info[i]) > 0:
                for j in range(len(self.nod_graf.info)):
                    if i != j:
                        info_intermediar = copy.deepcopy(self.nod_graf.info)
                        bloc = info_intermediar[i].pop()
                        info_intermediar[j].append(bloc)
                        h = self.euristica_h(info_intermediar)
                        nod = Nod(info_intermediar, h)
                        if self.problema.cauta_nod_nume(info_intermediar) is None:
                            self.problema.noduri.append(nod)
                        self.problema.arce.append((self.nod_graf, nod, 1))
                        l_succesori.append((nod, 1))
        return l_succesori

    def test_scop(self):
        return self.nod_graf.info == self.problema.nod_scop

    def __str__(self):
        parinte = self.parinte if self.parinte is None else self.parinte.nod_graf.info
        return f"({self.nod_graf}, parinte={parinte}, f={self.f}, g={self.g})"

def str_info_noduri(l):
    sir = "["
    for x in l:
        sir += str(x) + " "
    sir += "]"
    return sir

def afis_succesori_cost(l):
    sir = ""
    for (x, cost) in l:
        sir += "\nnod: " + str(x) + ", cost arc: " + str(cost)
    return sir

def in_lista(l, nod):
    for i in range(len(l)):
        if l[i].nod_graf.info == nod.info:
            return l[i]
    return None

def a_star():
    rad_arbore = NodParcurgere(NodParcurgere.problema.nod_start)
    open = [rad_arbore]
    closed = []

    while open:
        print(str_info_noduri(open))
        nod_curent = open.pop(0)
        closed.append(nod_curent)
        if nod_curent.test_scop():
            break
        for succesor, cost in nod_curent.expandeaza():
            nod_open = in_lista(open, succesor)
            nod_closed = in_lista(closed, succesor)
            g_nou = nod_curent.g + cost

            if nod_open:
                if g_nou < nod_open.g:
                    nod_open.g = g_nou
                    nod_open.f = g_nou + nod_open.nod_graf.h
                    nod_open.parinte = nod_curent

            elif nod_closed:
                f_nou = g_nou + nod_closed.nod_graf.h

                if f_nou < nod_closed.f:
                    nod_closed.g = g_nou
                    nod_closed.f = f_nou + nod_closed.nod_graf.h
                    nod_closed.parinte = nod_curent
                    open.append(nod_closed)
            else:
                nod_nou = NodParcurgere(succesor, nod_curent, g_nou)
                open.append(nod_nou)
        open.sort(key = lambda nod: (nod.f, -nod.g))

    print("\n------------------ Concluzie -----------------------")

    if (len(open) == 0):
        print("Lista open e vida, nu avem drum de la nodul start la nodul scop")
    else:
        print("Drum de cost minim: " + str_info_noduri(nod_curent.drum_arbore()))

if __name__ == "__main__":
    problema = Problema()
    NodParcurgere.problema = problema
    start = timer()
    a_star()
    end = timer()
    print("Timp de executie: {}".format(end - start))