from timeit import default_timer as timer

class Nod:
    def __init__(self, info, h):
        self.info = info
        self.h = h

    # def __str__(self):
    #     return "({}, h={})".format(self.info, self.h)

    def __str__(self):
        return "Pe malul din vest: {} misionari si {} canibali. " \
               "Pe malul din est: {} misionari si {} canibali. " \
               "Barca se afla pe malul din {}".format(self.info[0], self.info[1], self.info[2], self.info[3], self.info[4])

    def __repr__(self):
        return f"({self.info}, h={self.h})"

class Problema:
    def __init__(self, N = 3, M = 2, mal = "est"):
        self.N = N
        self.M = M
        nod_E = (0, 0, N, N, "est")
        nod_V = (N, N, 0, 0, "vest")

        start = nod_E if mal == "est" else nod_V
        scop = nod_V if mal == "est" else nod_E

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
        while nod_c.parinte is not None:
            if nod.info == nod_c.nod_graf.info:
                return True
            nod_c = nod_c.parinte
        return False

    def euristica_h(self, info):
        return (info[2] + info[3]) // (self.problema.M - 1)           # Timp de executie: 0.00046660000000000104
        # return 2 * self.problema.N - (info[0] + info[1])            # cate persoane nu sunt pe malul final (vest), Timp de executie: 0.0003282000000000007

    def expandeaza(self):

        def testConditie(nrCan, nrMis):
            return nrMis == 0 or nrMis >= nrCan

        l_succesori = []
        mal_curent = self.nod_graf.info[-1]
        if mal_curent == "est":
            nrMis_malCurent = self.nod_graf.info[2]
            nrCan_malCurent = self.nod_graf.info[3]
            nrMis_malOpus = self.nod_graf.info[0]
            nrCan_malOpus = self.nod_graf.info[1]
        else:
            nrMis_malCurent = self.nod_graf.info[0]
            nrCan_malCurent = self.nod_graf.info[1]
            nrMis_malOpus = self.nod_graf.info[2]
            nrCan_malOpus = self.nod_graf.info[3]

        for nrMis_barca in range(nrMis_malCurent + 1):
            for nrCan_barca in range(nrCan_malCurent + 1):
                if nrMis_barca + nrCan_barca == 0 or nrMis_barca + nrCan_barca > self.problema.M:
                    continue
                if not testConditie(nrCan_barca, nrMis_barca):
                    continue
                nrMis_malCurent_nou = nrMis_malCurent - nrMis_barca
                nrCan_malCurent_nou = nrCan_malCurent - nrCan_barca
                if not testConditie(nrCan_malCurent_nou, nrMis_malCurent_nou):
                    continue
                nrMis_malOpus_nou = nrMis_malOpus + nrMis_barca
                nrCan_malOpus_nou = nrCan_malOpus + nrCan_barca
                if not testConditie(nrCan_malOpus_nou, nrMis_malOpus_nou):
                    continue
                if mal_curent == "est":
                    info_nou = [nrMis_malOpus_nou, nrCan_malOpus_nou, nrMis_malCurent_nou, nrCan_malCurent_nou, "vest"]
                else:
                    info_nou = [nrMis_malCurent_nou, nrCan_malCurent_nou, nrMis_malOpus_nou, nrCan_malOpus_nou, "est"]
                euristica = self.euristica_h(info_nou)
                nod = Nod(info_nou, euristica)
                l_succesori.append((nod, 1))
        return l_succesori

    def test_scop(self):
        for i in range(len(self.nod_graf.info)):
            if self.nod_graf.info[i] != self.problema.nod_scop[i]:
                return False
        return True

    def __str__(self):
        parinte = self.parinte if self.parinte is None else self.parinte.nod_graf.info
        return f"({self.nod_graf}, parinte={parinte}, f={self.f}, g={self.g})"

def str_info_noduri(l):
    sir = ""
    for i in range(len(l)):
        if i < len(l) - 1 is not None:
            nr_misionari_barca = abs(l[i].nod_graf.info[0] - l[i + 1].nod_graf.info[0])
            nr_canibali_barca = abs(l[i].nod_graf.info[1] - l[i + 1].nod_graf.info[1])
            sir += str(l[i].nod_graf) + " de unde pleaca {} misionari si {} canibali spre malul din {}."\
                .format( nr_misionari_barca, nr_canibali_barca, l[i + 1].nod_graf.info[-1]) + "\n"
        else:
            sir += str(l[i].nod_graf) + ". Destinatie finala."
    return sir

# def str_info_noduri(l):
#     sir = "["
#     for x in l:
#         sir += str(x) + "\n"
#     sir += "]"
#     return sir

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
        print("Drum de cost minim:\n" + str_info_noduri(nod_curent.drum_arbore()))


if __name__ == "__main__":
    problema = Problema()
    NodParcurgere.problema = problema
    start = timer()
    a_star()
    end = timer()
    print("Timp de executie: {}".format(end - start))