from timeit import default_timer as timer

NR_LINII = 3
NR_COLOANE = 3

class Nod:
    def __init__(self, info, h):
        self.info = info
        self.h = h

    def __str__(self):
        sir = "\n"
        for i in range(NR_LINII):
            for j in range(NR_COLOANE):
                sir += str(self.info[NR_COLOANE * i + j]) + " "
            sir += "\n"
        return sir

    def __repr__(self):
        sir = "\n"
        for i in range(NR_LINII):
            for j in range(NR_COLOANE):
                sir += str(self.info[NR_COLOANE * i + j]) + " "
            sir += "\n"
        return sir

class Arc:
    def __init__(self, capat, varf, cost):
        self.capat = capat
        self.varf = varf
        self.cost = cost

class Problema:
    def __init__(self, start = [2, 4, 3, 8, 7, 5, 1, 0, 6], scop = [1, 2, 3, 4, 5, 6, 7, 8, 0]):
        self.nod_start = Nod(start, float("inf"))
        self.nod_scop = scop

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
        while nod_c:
            if nod_c.nod_graf.info == nod.info:
                return True
            nod_c = nod_c.parinte
        return False

    def interschimba(self, indice1, indice2, l):
        l_nou = list(l)
        l_nou[indice1], l_nou[indice2] = l_nou[indice2], l_nou[indice1]
        return l_nou

    def distanta_hamilton(self, elem, i_elem, j_elem, reprezentare):
        nr = reprezentare.index(elem)
        i_scop = nr / NR_COLOANE
        j_scop = nr % NR_COLOANE
        return abs(i_scop - i_elem) + abs(j_scop - j_elem)

    def euristica_h(self, reprez_nod):
        euristica = 0
        for i in range(len(reprez_nod)):
            i_elem = i / NR_COLOANE
            j_elem = i % NR_COLOANE
            if (reprez_nod[i] != 0):
                euristica += self.distanta_hamilton(reprez_nod[i], i_elem, j_elem, self.problema.nod_scop)
        return euristica

    def expandeaza(self):
        nodCurent = self
        nod = self.nod_graf
        indice_0 = nod.info.index(0)
        linie_0 = int(indice_0 / NR_COLOANE)
        coloana_0 = int(indice_0 % NR_COLOANE)
        l_succesori = []

        if linie_0 >= 1:
            poz_noua = (linie_0 - 1) * NR_COLOANE + coloana_0
            reprez_noua = self.interschimba(indice_0, poz_noua, nod.info)
            euristica = self.euristica_h(reprez_noua)
            nod_nou = Nod(reprez_noua, euristica)
            if not nodCurent.contine_in_drum(nod_nou):
                l_succesori.append((nod_nou, 1))

        if linie_0 <= 1:
            poz_noua = (linie_0 + 1) * NR_COLOANE + coloana_0
            reprez_noua = self.interschimba(indice_0, poz_noua, nod.info)
            euristica = self.euristica_h(reprez_noua)
            nod_nou = Nod(reprez_noua, euristica)
            if not nodCurent.contine_in_drum(nod_nou):
                l_succesori.append((nod_nou, 1))

        if coloana_0 >= 1:
            poz_noua = linie_0 * NR_COLOANE + coloana_0 - 1
            reprez_noua = self.interschimba(indice_0, poz_noua, nod.info)
            euristica = self.euristica_h(reprez_noua)
            nod_nou = Nod(reprez_noua, euristica)
            if not nodCurent.contine_in_drum(nod_nou):
                l_succesori.append((nod_nou, 1))

        if coloana_0 <= 1:
            poz_noua = linie_0 * NR_COLOANE + coloana_0 + 1
            reprez_noua = self.interschimba(indice_0, poz_noua, nod.info)
            euristica = self.euristica_h(reprez_noua)
            nod_nou = Nod(reprez_noua, euristica)
            if not nodCurent.contine_in_drum(nod_nou):
                l_succesori.append((nod_nou, 1))

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

    while len(open) > 0:
        nod_curent = open.pop(0)
        closed.append(nod_curent)
        if nod_curent.test_scop():
            break
        for succesor, cost in nod_curent.expandeaza():
            if (not nod_curent.contine_in_drum(succesor)):
                nod_c = in_lista(closed, succesor)
                g_succesor = nod_curent.g + cost
                f = g_succesor + succesor.h

                if nod_c is not None:
                    if (f < nod_curent.f):
                        nod_c.parinte = nod_curent
                        nod_c.g = g_succesor
                        nod_c.f = f
                else:
                    nod_c = in_lista(open, succesor)
                    if nod_c is not None:
                        if nod_c.g > g_succesor:
                            nod_c.parinte = nod_curent
                            nod_c.g = g_succesor
                            nod_c.f = f
                    else:
                        nod_cautare = NodParcurgere(succesor, nod_curent, g_succesor)
                        open.append(nod_cautare)

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