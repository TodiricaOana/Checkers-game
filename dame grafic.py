# Todirica Oana-Andreea, grupa 244
import time
import copy
import pygame, sys


# aceasta functie deseneaza tabla de joc, colorata cu patratele maro si crem si pune piesele pe tabla, in functie
# de pozitiile pe care se afla piesele la starea curenta
def deseneaza_grid(display, tabla):
    w_gr = h_gr = 50

    # incarcam imaginile si le schimbam dimensiunea (dame si regi)
    alb_img = pygame.image.load('dama_alba.png')
    alb_img = pygame.transform.scale(alb_img, (w_gr, h_gr))
    negru_img = pygame.image.load('dama_neagra.png')
    negru_img = pygame.transform.scale(negru_img, (w_gr, h_gr))
    rege_alb_img = pygame.image.load('rege_alb.png')
    rege_alb_img = pygame.transform.scale(rege_alb_img, (w_gr, h_gr))
    rege_negru_img = pygame.image.load('rege_negru.png')
    rege_negru_img = pygame.transform.scale(rege_negru_img, (w_gr, h_gr))
    drt = []

    # desenam tabla de joc
    for linie in range(8):
        for coloana in range(8):
            patr = pygame.Rect(coloana * (w_gr + 1), linie * (h_gr + 1), w_gr, h_gr)
            drt.append(patr)

            if (linie % 2 == 0 and coloana % 2 == 1) or (linie % 2 == 1 and coloana % 2 == 0):
                pygame.draw.rect(display, (66, 46, 19), patr)
            else:
                pygame.draw.rect(display, (247, 228, 194), patr)
            if tabla[linie][coloana] != '#' and tabla[linie][coloana].culoare == 'n' and not tabla[linie][coloana].rege:
                display.blit(negru_img, (coloana * (w_gr + 1), linie * (h_gr + 1)))
            if tabla[linie][coloana] != '#' and tabla[linie][coloana].culoare == 'n' and tabla[linie][coloana].rege:
                display.blit(rege_negru_img, (coloana * (w_gr + 1), linie * (h_gr + 1)))
            if tabla[linie][coloana] != '#' and tabla[linie][coloana].culoare == 'a' and not tabla[linie][coloana].rege:
                display.blit(alb_img, (coloana * (w_gr + 1), linie * (h_gr + 1)))
            if tabla[linie][coloana] != '#' and tabla[linie][coloana].culoare == 'a' and tabla[linie][coloana].rege:
                display.blit(rege_alb_img, (coloana * (w_gr + 1), linie * (h_gr + 1)))
    pygame.display.flip()
    return drt

# aceasta functie coloreaza cu verde patratica pe care un jucator o selecteaza ca sa mute, daca poate muta de acolo
# si coloreaza cu verde patratelele in care poate muta, daca a selectat o patratica din care poate muta
def deseneaza_grid_selectat(display, tabla, linie_start, coloana_start, poz):
    w_gr = h_gr = 50

    alb_img = pygame.image.load('dama_alba.png')
    alb_img = pygame.transform.scale(alb_img, (w_gr, h_gr))
    negru_img = pygame.image.load('dama_neagra.png')
    negru_img = pygame.transform.scale(negru_img, (w_gr, h_gr))
    rege_alb_img = pygame.image.load('rege_alb.png')
    rege_alb_img = pygame.transform.scale(rege_alb_img, (w_gr, h_gr))
    rege_negru_img = pygame.image.load('rege_negru.png')
    rege_negru_img = pygame.transform.scale(rege_negru_img, (w_gr, h_gr))
    drt = []

    # salvam pozitiile in care se poate muta din linie start si coloana start
    mutari_colorate = []
    for p in poz:
        if linie_start == p[0] and coloana_start == p[1]:
            mutari_colorate.append([p[2], p[3]])

    for linie in range(8):
        for coloana in range(8):
            ok = False
            patr = pygame.Rect(coloana * (w_gr + 1), linie * (h_gr + 1), w_gr, h_gr)
            drt.append(patr)

            # daca linie start si coloana start sunt pozitii valide din care se poate muta, coloram cu verde patratica
            for p in poz:
                if linie_start == linie and coloana_start == coloana and linie_start == p[0] and coloana_start == p[1]:
                    pygame.draw.rect(display, (40, 153, 59), patr)
                    ok = True

            # coloram cu verde si patratelele in care se poate muta din acea pozitie
            for mut in mutari_colorate:
                if linie == mut[0] and coloana == mut[1]:
                    pygame.draw.rect(display, (40, 153, 59), patr)
                    ok = True

            # coloram cu maro si crem celelalte patratele
            if not ok:
                if (linie % 2 == 0 and coloana % 2 == 1) or (linie % 2 == 1 and coloana % 2 == 0):
                    pygame.draw.rect(display, (66, 46, 19), patr)
                else:
                    pygame.draw.rect(display, (247, 228, 194), patr)
            if tabla[linie][coloana] != '#' and tabla[linie][coloana].culoare == 'n' and not tabla[linie][coloana].rege:
                display.blit(negru_img, (coloana * (w_gr + 1), linie * (h_gr + 1)))
            if tabla[linie][coloana] != '#' and tabla[linie][coloana].culoare == 'n' and tabla[linie][coloana].rege:
                display.blit(rege_negru_img, (coloana * (w_gr + 1), linie * (h_gr + 1)))
            if tabla[linie][coloana] != '#' and  tabla[linie][coloana].culoare == 'a' and not tabla[linie][coloana].rege:
                display.blit(alb_img, (coloana * (w_gr + 1), linie * (h_gr + 1)))
            if tabla[linie][coloana] != '#' and tabla[linie][coloana].culoare == 'a' and tabla[linie][coloana].rege:
                display.blit(rege_alb_img, (coloana * (w_gr + 1), linie * (h_gr + 1)))
    pygame.display.flip()
    return drt

# executam mutarea de pe pozitia start pe pozitia finala
def muta(tabla, poz_start, poz_finala):
    tabla[poz_finala[0]][poz_finala[1]] = tabla[poz_start[0]][poz_start[1]]
    tabla[poz_start[0]][poz_start[1]] = '#'

    # verificam daca am ajuns in capatul opus, pentru a face piesa rege
    if poz_finala[0] == 0 and tabla[poz_finala[0]][poz_finala[1]] != '#' and tabla[poz_finala[0]][poz_finala[1]].culoare == 'n':
        tabla[poz_finala[0]][poz_finala[1]].rege = True

    if poz_finala[0] == 7 and tabla[poz_finala[0]][poz_finala[1]] != '#' and tabla[poz_finala[0]][poz_finala[1]].culoare == 'a':
        tabla[poz_finala[0]][poz_finala[1]].rege = True

    # daca am facut o saritura, 'mancam' piesa peste care sarim (punem simbolul gol in patratica)
    if (poz_start[0] - poz_finala[0]) % 2 == 0:
        tabla[(poz_start[0] + poz_finala[0]) // 2][(poz_start[1] + poz_finala[1]) // 2] = '#'
        Joc.SARITURA = True


# clasa ce retine culoarea unei piese si daca e rege sau nu
class Piesa:
    def __init__(self, culoare, rege):
        self.culoare = culoare
        self.rege = rege

    def __str__(self):
        if not self.rege:
            return self.culoare
        else:
            if self.culoare == 'a':
                return 'A'
            else:
                return 'N'


class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    NR_COLOANE = 8
    NR_LINII = 8
    SIMBOLURI_JUC = ['n', 'a']
    JMIN = None
    JMAX = None
    GOL = '#'
    SARITURA = False
    SARITURA_DUBLA = False
    POSIBILITATI = []
    TIP_SCOR = 1

    def __init__(self, tabla=None):
        if tabla is not None:
            self.matr = tabla
        else:
            self.matr = [
                ['#', Piesa('a', False), '#', Piesa('a', False), '#', Piesa('a', False), '#', Piesa('a', False)],
                [Piesa('a', False), '#', Piesa('a', False), '#', Piesa('a', False), '#', Piesa('a', False), '#'],
                ['#', Piesa('a', False), '#', Piesa('a', False), '#', Piesa('a', False), '#', Piesa('a', False)],
                ['#', '#', '#', '#', '#', '#', '#', '#'],
                ['#', '#', '#', '#', '#', '#', '#', '#'],
                [Piesa('n', False), '#', Piesa('n', False), '#', Piesa('n', False), '#', Piesa('n', False), '#'],
                ['#', Piesa('n', False), '#', Piesa('n', False), '#', Piesa('n', False), '#', Piesa('n', False)],
                [Piesa('n', False), '#', Piesa('n', False), '#', Piesa('n', False), '#', Piesa('n', False), '#']
            ]

    def final(self, juc):
        # daca nu mai sunt mutari posibile, pierde cel care nu mai are mutari
        poz = self.mutari_posibile(juc)
        if len(poz) == 0:
            if juc == self.JMIN:
                return self.JMAX
            else:
                return self.JMIN

        # daca nu mai sunt piese pe tabla, pierde cel care nu mai are piese
        jmin_scor = self.numar_piese(self.JMIN)
        jmax_scor = self.numar_piese(self.JMAX)
        if jmin_scor == 0:
            return self.JMAX
        elif jmax_scor == 0:
            return self.JMIN

        return False   # sau 'False' daca nu s-a terminat jocul

    # aceasta functie returneaza daca saritura peste o piesa opusa este posibila
    # parametrii sunt pozitia de unde se pleaca, piesa peste care se sare si pozitia pe care ar trebui sa ajunga piesa care sare
    def saritura_posibila(self, poz_start, obstacol, poz_finala):
        # verificam sa nu iesim din tabla
        if poz_finala[0] < 0 or poz_finala[0] > 7 or poz_finala[1] < 0 or poz_finala[1] > 7:
            return False

        # verificam daca exista piesa peste care sarim
        if self.matr[obstacol[0]][obstacol[1]] == '#':
            return False

        # verificam sa nu existe deja o piesa pe pozitia pe care vrem sa sarim
        if self.matr[poz_finala[0]][poz_finala[1]] != '#':
            return False

        # pentru piese negre
        if self.matr[poz_start[0]][poz_start[1]].culoare == 'n':
            # daca nu e rege, merge doar in sus
            if not self.matr[poz_start[0]][poz_start[1]].rege and poz_finala[0] > poz_start[0]:
                return False
            # trebuie sa sara peste o piesa opusa
            if self.matr[obstacol[0]][obstacol[1]].culoare != 'a':
                return False
            return True

        # pentru piese albe
        if self.matr[poz_start[0]][poz_start[1]].culoare == 'a':
            # daca nu e rege, merge doar in jos
            if not self.matr[poz_start[0]][poz_start[1]].rege and poz_finala[0] < poz_start[0]:
                return False
            # trebuie sa sara peste o piesa de culoare opusa
            if self.matr[obstacol[0]][obstacol[1]].culoare != 'n':
                return False
            return True

    # aceasta functie verifica daca putem face o mutare din poz_start in poz_finala
    def mutare_posibila(self, poz_start, poz_finala):
        # verificam sa nu iesim din tabla
        if poz_finala[0] < 0 or poz_finala[0] > 7 or poz_finala[1] < 0 or poz_finala[1] > 7:
            return False

        # verificam sa nu existe deja o piesa pe pozitia pe care vrem sa ajungem
        if self.matr[poz_finala[0]][poz_finala[1]] != '#':
            return False

        # pentru piese negre
        # daca nu e rege, merge doar in sus
        if not self.matr[poz_start[0]][poz_start[1]].rege and self.matr[poz_start[0]][poz_start[1]].culoare == 'n':
            if poz_finala[0] > poz_start[0]:
                return False
            return True

        # pentru piese albe
        # daca nu e rege, merge doar in jos
        if not self.matr[poz_start[0]][poz_start[1]].rege and self.matr[poz_start[0]][poz_start[1]].culoare == 'a':
            if poz_finala[0] < poz_start[0]:
                return False
            return True

        # daca e rege, poate merge si inapoi si inainte (daca e liber)
        if self.matr[poz_start[0]][poz_start[1]].rege:
            return True

    # aceasta functie returneaza o lista cu urmatoarele mutari posibile alea unui jucator
    def mutari_posibile(self, juc):
        mutari = []

        if Joc.SARITURA_DUBLA:
            mutari = Joc.POSIBILITATI

        else:
            # verificam daca se pot face sarituri
            for linie in range(self.NR_LINII):
                for coloana in range(self.NR_COLOANE):
                    if self.matr[linie][coloana] != '#' and self.matr[linie][coloana].culoare == juc:
                        if self.saritura_posibila([linie, coloana], [linie + 1, coloana + 1], [linie + 2, coloana + 2]):
                            mutari.append([linie, coloana, linie + 2, coloana + 2])
                        if self.saritura_posibila([linie, coloana], [linie - 1, coloana + 1], [linie - 2, coloana + 2]):
                            mutari.append([linie, coloana, linie - 2, coloana + 2])
                        if self.saritura_posibila([linie, coloana], [linie + 1, coloana - 1], [linie + 2, coloana - 2]):
                            mutari.append([linie, coloana, linie + 2, coloana - 2])
                        if self.saritura_posibila([linie, coloana], [linie - 1, coloana - 1], [linie - 2, coloana - 2]):
                            mutari.append([linie, coloana, linie - 2, coloana - 2])

            if len(mutari) != 0:
                Joc.SARITURA = True
            else:
                # verificam daca se pot face mutari
                for linie in range(self.NR_LINII):
                    for coloana in range(self.NR_COLOANE):
                        if self.matr[linie][coloana] != '#' and self.matr[linie][coloana].culoare == juc:
                            if self.mutare_posibila([linie, coloana], [linie + 1, coloana + 1]):
                                mutari.append([linie, coloana, linie + 1, coloana + 1])
                            if self.mutare_posibila([linie, coloana], [linie - 1, coloana + 1]):
                                mutari.append([linie, coloana, linie - 1, coloana + 1])
                            if self.mutare_posibila([linie, coloana], [linie + 1, coloana - 1]):
                                mutari.append([linie, coloana, linie + 1, coloana - 1])
                            if self.mutare_posibila([linie, coloana], [linie - 1, coloana - 1]):
                                mutari.append([linie, coloana, linie - 1, coloana - 1])

        return mutari

    # aceasta functie returneaza o lista cu tablele dupa actionarea mutarilor
    def mutari(self, juc):
        l_mutari = []

        mutari = self.mutari_posibile(juc)

        for linie_start, coloana_start, linie_finala, coloana_finala in mutari:
            tabla_noua = copy.deepcopy(self.matr)
            muta(tabla_noua, [linie_start, coloana_start], [linie_finala, coloana_finala])
            l_mutari.append(Joc(tabla_noua))

        return l_mutari

    # aceasta functie calculeaza scorul, numarand piesele de joc ramase pe tabla pentru un jucator
    # daca piesa e dama, acorda punctajul 10, daca piesa e rege acorda punctajul 100
    # aceasta functie ajuta la estimarea scorului cat mai prielnic pentru JMAX, deoarece jocul se termina atunci cand
    # nu mai sunt mutari sau cand un jucator ramane fara piese, asa ca JMAX va cauta sa aiba cat mai multe piese
    # pe tabla de joc, pentru ca JMIN sa ramana fara piese primul, cat si sa faca regi, pentru a primi puncte bonus.
    def numar_piese(self, juc):
        regi = 0
        piese = 0
        for linie in range(8):
            for coloana in range(8):
                if self.matr[linie][coloana] != '#' and self.matr[linie][coloana].culoare == juc:
                    if self.matr[linie][coloana].rege:
                        regi += 1
                    else:
                        piese += 1
        return regi * 100 + piese * 10

    # euristica este diferenta dintre scorurile jucatorilor
    def fct_euristica1(self):
        return self.numar_piese(Joc.JMAX) - self.numar_piese(Joc.JMIN)

    # aceasta functie numara cate piese a mancat un jucator adversarului
    # aceasta functie ajuta la estimarea scorului cat mai prielnic pentru JMAX, deoarece jocul se termina atunci cand
    # nu mai sunt mutari sau cand un jucator ramane fara piese, asa ca JMAX va cauta sa manance cat mai multe piese
    # de-ale adversarului cu scopul de a-l lasa fara piese, pentru a castiga
    def numar_piese_mancate(self, juc):
        piese = 0

        if juc == self.JMAX:
            juc_opus = self.JMIN
        else:
            juc_opus = self.JMAX

        for linie in range(8):
            for coloana in range(8):
                if self.matr[linie][coloana] != '#' and self.matr[linie][coloana].culoare == juc_opus:
                    piese += 1

        # din total scadem nr de piese de pe tabla ale adversarului si ne dau piese mancate
        piese_mancate = 12 - piese
        return 10 * piese_mancate

    # functia euristica este diferenta dintre piesele mancate
    def fct_euristica2(self):
        return self.numar_piese_mancate(Joc.JMAX) - self.numar_piese_mancate(Joc.JMIN)

    def estimeaza_scor(self, adancime, jucator):
        t_final = self.final(jucator)
        if t_final == Joc.JMAX:
            return 9999 + adancime
        elif t_final == Joc.JMIN:
            return -9999 - adancime
        elif t_final == 'remiza':
            return 0
        else:
            if self.TIP_SCOR == 1:
                return self.fct_euristica1()
            else:
                return self.fct_euristica2()


    def __str__(self):
        sir = '  '
        for nr_col in range(self.NR_COLOANE):
            sir += str(nr_col) + ' '
        sir += '\n'

        for lin in range(self.NR_LINII):
            sir += (str(lin) + ' ' + " ".join([str(x) for x in self.matr[lin]]) + "\n")
        return sir


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu
    configuratiile posibile in urma mutarii unui jucator
    """

    ADANCIME_MAX = None

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, scor=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent

        # adancimea in arborele de stari
        self.adancime = adancime

        # scorul starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.scor = scor

        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None

    def jucator_opus(self):
        if self.j_curent == Joc.JMIN:
            return Joc.JMAX
        else:
            return Joc.JMIN

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.j_curent)
        juc_opus = self.jucator_opus()
        l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]

        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "(Juc curent: " + self.j_curent + ")\n"
        return sir


""" Algoritmul MinMax """


def min_max(stare):
    if stare.adancime == 0 or stare.tabla_joc.final(stare.j_curent):
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime, stare.j_curent)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutari_scor = [min_max(mutare) for mutare in stare.mutari_posibile]

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu scorul maxim
        stare.stare_aleasa = max(mutari_scor, key=lambda x: x.scor)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu scorul minim
        stare.stare_aleasa = min(mutari_scor, key=lambda x: x.scor)

    stare.scor = stare.stare_aleasa.scor
    return stare


def alpha_beta(alpha, beta, stare):
    if stare.adancime == 0 or stare.tabla_joc.final(stare.j_curent):
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime, stare.j_curent)
        return stare

    if alpha >= beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Joc.JMAX:
        scor_curent = float('-inf')

        for mutare in stare.mutari_posibile:
            # calculeaza scorul
            stare_noua = alpha_beta(alpha, beta, mutare)

            if scor_curent < stare_noua.scor:
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor
            if alpha < stare_noua.scor:
                alpha = stare_noua.scor
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        scor_curent = float('inf')

        for mutare in stare.mutari_posibile:
            stare_noua = alpha_beta(alpha, beta, mutare)

            if scor_curent > stare_noua.scor:
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor

            if beta > stare_noua.scor:
                beta = stare_noua.scor
                if alpha >= beta:
                    break

    stare.scor = stare.stare_aleasa.scor

    return stare


def afis_daca_final(stare_curenta, jucator):
    final = stare_curenta.tabla_joc.final(jucator)
    if final:
        if final == "remiza":
            print("Remiza!")
        else:
            if Joc.TIP_SCOR == 1:
                print("A castigat " + final + " cu scorul: " + str(stare_curenta.tabla_joc.numar_piese(final)))
            else:
                print("A castigat " + final + " cu scorul: " + str(stare_curenta.tabla_joc.numar_piese_mancate(final)))
        return True

    return False

# aceasta functie returneaza pozitia pe care a sarit un jucator, daca a sarit, -1 altfel
# primeste matricea initiala, matricea dupa mutare si jucatorul si returneaza pozitia pe care s-a sarit
def pozitii_diferite (matrice1, matrice2, juc):
    for linie in range(8):
        for coloana in range(8):
            if matrice2[linie][coloana] != '#' and matrice2[linie][coloana].culoare == juc and matrice1[linie][coloana] == '#':
                return linie, coloana
    return -1, -1

# aceasta functie verifica daca un jucator a efectuat o saritura
# primeste matricea initiala, matricea dupa mutare si jucatorul si returneaza daca s-a putut sari
def a_sarit(matrice1, matrice2, juc):
    poz = []
    for linie in range(8):
        for coloana in range(8):
            if (matrice1[linie][coloana] != '#' and matrice1[linie][coloana].culoare == juc and matrice2[linie][coloana] == '#') \
                    or (matrice2[linie][coloana] != '#' and matrice2[linie][coloana].culoare == juc and matrice1[linie][coloana] == '#'):
                poz.append(linie)
                poz.append(coloana)

    if len(poz) == 4:
        if abs(poz[0] - poz[2]) == 2:
            return True
    return False

# aceasta functie ia coordonatele unui clic si le transforma in coordonate de matrice
def clic(patratele, joc_timp_inceput, stare_curenta, nr_mutari_JMAX, nr_mutari_JMIN, s):
    for event in pygame.event.get():
        # daca se apasa pe x, se termina jocul si se afiseaza informatii
        if event.type == pygame.QUIT:
            joc_timp_final = int(round(time.time() * 1000))
            timp_joc = joc_timp_final - joc_timp_inceput
            print(f"Jocul a durat {int(timp_joc)} milisecunde")
            if Joc.TIP_SCOR == 1:
                print(f"Scor pentru {Joc.JMAX}: {stare_curenta.tabla_joc.numar_piese(Joc.JMAX)}")
                print(f"Scor pentru {Joc.JMIN}: {stare_curenta.tabla_joc.numar_piese(Joc.JMIN)}")
            else:
                print(f"Scor pentru {Joc.JMAX}: {stare_curenta.tabla_joc.numar_piese_mancate(Joc.JMAX)}")
                print(f"Scor pentru {Joc.JMIN}: {stare_curenta.tabla_joc.numar_piese_mancate(Joc.JMIN)}")
            print(f"Nr mutari {Joc.JMAX}: {nr_mutari_JMAX}")
            print(f"Nr mutari {Joc.JMIN}: {nr_mutari_JMIN}")
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            for np in range(len(patratele)):
                # daca clicul se afla pe una din patratele
                if patratele[np].collidepoint(pos):
                    # afla linia si coloana corespunzatoare matricei
                    linie = np // 8
                    coloana = np % 8
                    if s == 1:
                        print("linie start = " + str(linie))
                        print("coloana_start = " + str(coloana))
                    else:
                        print("linie final = " + str(linie))
                        print("coloana final = " + str(coloana))
                    return linie, coloana
    return -1, -1

def main():
    # initializare algoritm
    raspuns_valid = False
    tip_algoritm = None
    tip_interfata = None

    while not raspuns_valid:
        tip_algoritm = input("Algoritmul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-beta\n ")
        if tip_algoritm in ['1', '2']:
            raspuns_valid = True
        else:
            print("Nu ati ales o varianta corecta.")

    # initializare ADANCIME_MAX
    raspuns_valid = False
    while not raspuns_valid:
        print("Alege dificultatea")
        print("\t1 = Usor")
        print("\t2 = Mediu")
        print("\t3 = Greu")

        dificultate = int(input())

        if dificultate == 1:
            Stare.ADANCIME_MAX = 3
            raspuns_valid = True
        elif dificultate == 2:
            Stare.ADANCIME_MAX = 4
            raspuns_valid = True
        elif dificultate == 3:
            Stare.ADANCIME_MAX = 5
            raspuns_valid = True
        else:
            print("Dificultate invalida")

    raspuns_valid = False
    while not raspuns_valid:
        print("Cum doresti sa se calculeze scorul?")
        print("\t1 = Numararea pieselor de pe tabla cu punctaj bonus pe regi")
        print("\t2 = Numararea pieselor pe care le-ai 'mancat'")
        scor = input()
        if scor in ['1', '2']:
            Joc.TIP_SCOR = scor
            raspuns_valid = True
        else:
            print("Nu ati ales o varianta corecta.")

    # initializare jucatori
    [s1, s2] = Joc.SIMBOLURI_JUC.copy()  # lista de simboluri posibile
    raspuns_valid = False
    while not raspuns_valid:
        Joc.JMIN = str(input("Doriti sa jucati cu {} sau cu {}? ".format(s1, s2)))
        if Joc.JMIN in Joc.SIMBOLURI_JUC:
            raspuns_valid = True
        else:
            print("Raspunsul trebuie sa fie {} sau {}.".format(s1, s2))
    Joc.JMAX = s1 if Joc.JMIN == s2 else s2

    raspuns_valid = False
    while not raspuns_valid:
        print("Doresti sa joci in consola sau cu interfata grafica?")
        print("\t1 = Consola")
        print("\t2 = Interfata grafica")

        tip_interfata = int(input())

        if tip_algoritm in ['1', '2']:
            raspuns_valid = True
        else:
            print("Nu ati ales o varianta corecta.")

    # initializare tabla
    tabla_curenta = Joc()
    print("Tabla initiala")
    print(str(tabla_curenta))

    # creare stare initiala
    stare_curenta = Stare(tabla_curenta, Joc.SIMBOLURI_JUC[0], Stare.ADANCIME_MAX)

    joc_timp_inceput = int(round(time.time() * 1000))

    nr_mutari_JMAX = 0
    nr_mutari_JMIN = 0

    if tip_interfata == 2:
        # setari interf grafica
        pygame.init()
        pygame.display.set_caption('Dame')
        ecran = pygame.display.set_mode(size=(408, 408))

        patratele = deseneaza_grid(ecran, tabla_curenta.matr)

    while True:
        if stare_curenta.j_curent == Joc.JMIN:
            print("Randul dumneavoastra: \n")
            # testez daca jocul a ajuns intr-o stare finala
            # si afisez un mesaj corespunzator in caz ca da
            if afis_daca_final(stare_curenta, Joc.JMIN):
                break

            t_inainte = int(round(time.time() * 1000))

            # muta jucatorul
            raspuns_valid = False
            exit = False

            poz = stare_curenta.tabla_joc.mutari_posibile(Joc.JMIN)
            print(
                "Pozitii posibile(primele doua sunt cele pe care se afla piesa si urmatoarele sunt cele in care se doreste sa ajunga piesa - linia si coloana):  ")
            for p in poz:
                print("[(", p[0], ", ", p[1], ")", " -> (", p[2], ", ", p[3], ")] ")
            print()

            linie_start = -1
            coloana_start = -1
            linie_finala = -1
            coloana_finala = -1

            while not raspuns_valid:
                if tip_interfata == 2:

                    # daca e primul clic, se iau coordonatele de unde se muta o piese
                    if linie_start == -1 and coloana_start == -1:
                        linie_start, coloana_start = clic(patratele, joc_timp_inceput, stare_curenta, nr_mutari_JMAX, nr_mutari_JMIN, 1)
                        patratele = deseneaza_grid_selectat(ecran, stare_curenta.tabla_joc.matr, linie_start, coloana_start, poz)
                    else:
                        # daca se da clic a doua oara, se iau coordonatele unde se muta o piesa
                        linie_finala, coloana_finala = clic(patratele, joc_timp_inceput, stare_curenta, nr_mutari_JMAX, nr_mutari_JMIN, 2)

                    if [linie_start, coloana_start, linie_finala, coloana_finala] in poz:
                        raspuns_valid = True

                    # daca nu s-au dat clicuri pe pozitii corecte, se mai permite odata
                    elif linie_finala != -1 and coloana_finala != -1:
                        print("Coordonate gresite, mutarile sunt imposibile. Mai incercati odata!")
                        linie_start = -1
                        coloana_start = -1
                        linie_finala = -1
                        coloana_finala = -1

                else:
                    # jucam in consola
                    linie_start = input("linie start = ")

                    if linie_start == "exit":
                        exit = True
                        break

                    coloana_start = input("coloana start = ")

                    if coloana_start == "exit":
                        exit = True
                        break

                    linie_finala = input("linie finala = ")

                    if linie_finala == "exit":
                        exit = True
                        break

                    coloana_finala = input("coloana finala = ")

                    if coloana_finala == "exit":
                        exit = True
                        break

                    # verificam daca datele sunt corecte
                    if linie_start.isdigit() and coloana_start.isdigit() and linie_finala.isdigit() and coloana_finala.isdigit():
                        if [int(linie_start), int(coloana_start), int(linie_finala), int(coloana_finala)] in poz:
                            raspuns_valid = True
                        else:
                            print("Pozitie invalida. Nu puteti muta in aceasta pozitie.")
                    else:
                        print("Pozitie invalida. Pozitia trebuie sa fie un numar intreg.")

            if exit:
                break

            # datele sunt corecte, mutam
            muta(stare_curenta.tabla_joc.matr, [int(linie_start), int(coloana_start)], [int(linie_finala), int(coloana_finala)])
            nr_mutari_JMIN += 1

            # afisarea starii jocului in urma mutarii utilizatorului
            print("\nTabla dupa mutarea jucatorului")
            print(str(stare_curenta))

            if tip_interfata == 2:
                patratele = deseneaza_grid(ecran, stare_curenta.tabla_joc.matr)

            t_dupa = int(round(time.time() * 1000))
            print("Jucatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")

            if Joc.TIP_SCOR == 1:
                print(f"Scor pentru {Joc.JMIN}: {stare_curenta.tabla_joc.numar_piese(Joc.JMIN)} \n")
            else:
                print(f"Scor pentru {Joc.JMIN}: {stare_curenta.tabla_joc.numar_piese_mancate(Joc.JMIN)} \n")

            Joc.SARITURA_DUBLA = False
            Joc.POSIBILITATI.clear()

            # daca s-a realizat o saritura, verificam daca se mai poate face una din aceeasi pozitie si lasam randul aceluiasi jucator
            if Joc.SARITURA:
                Joc.SARITURA = False
                poz2 = stare_curenta.tabla_joc.mutari_posibile(Joc.JMIN)
                if Joc.SARITURA:
                    for p in poz2:
                        # aici verific daca saritura ce ar urma se face din pozitia in care a ajuns piesa ce a mancat inainte
                        if int(linie_finala) == p[0] and int(coloana_finala) == p[1]:
                            stare_curenta.j_curent = Joc.JMIN
                            Joc.SARITURA_DUBLA = True
                            Joc.POSIBILITATI.append(p)
                    if not Joc.SARITURA_DUBLA:
                        # Daca nu se mai poate face inca o saritura, schimb jucatorul cu cel opus
                        stare_curenta.j_curent = stare_curenta.jucator_opus()
                        Joc.SARITURA = False
                else:
                    stare_curenta.j_curent = stare_curenta.jucator_opus()
                    Joc.SARITURA = False
            else:
                stare_curenta.j_curent = stare_curenta.jucator_opus()
                Joc.SARITURA = False



        # --------------------------------
        else:  # jucatorul e JMAX (calculatorul)
            if afis_daca_final(stare_curenta, Joc.JMAX):
                break

            print("Randul calculatorului: \n")
            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))
            if tip_algoritm == '1':
                stare_actualizata = min_max(stare_curenta)
            else:
                stare_actualizata = alpha_beta(-5000, 5000, stare_curenta)

            # verific daca s-a efectuat o saritura
            if a_sarit(stare_curenta.tabla_joc.matr, stare_actualizata.stare_aleasa.tabla_joc.matr, stare_curenta.j_curent):
                # aceste variabile retin pozitiile in care a sarit piesa
                linie_finala, coloana_finala = pozitii_diferite(stare_curenta.tabla_joc.matr,
                                                                stare_actualizata.stare_aleasa.tabla_joc.matr,
                                                                stare_curenta.j_curent)
                Joc.SARITURA = True
            else:
                Joc.SARITURA = False

            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            nr_mutari_JMAX += 1

            print("Tabla dupa mutarea calculatorului:")
            print(str(stare_curenta))

            if tip_interfata == 2:
                patratele = deseneaza_grid(ecran, stare_curenta.tabla_joc.matr)

            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")

            if Joc.TIP_SCOR == 1:
                print(f"Scor pentru {Joc.JMAX}: {stare_curenta.tabla_joc.numar_piese(Joc.JMAX)}\n")
            else:
                print(f"Scor pentru {Joc.JMAX}: {stare_curenta.tabla_joc.numar_piese_mancate(Joc.JMAX)}\n")

            Joc.SARITURA_DUBLA = False
            Joc.POSIBILITATI.clear()

            # daca s-a realizat o saritura, verificam daca se mai poate face una din aceeasi pozitie si lasam randul aceluiasi jucator
            if Joc.SARITURA:
                Joc.SARITURA = False
                poz2 = stare_curenta.tabla_joc.mutari_posibile(Joc.JMAX)
                if Joc.SARITURA:
                    for p in poz2:
                        # aici verific daca saritura ce ar urma se face din pozitia in care a ajuns piesa ce a mancat inainte
                        if linie_finala == p[0] and coloana_finala == p[1]:
                            stare_curenta.j_curent = Joc.JMAX
                            Joc.SARITURA_DUBLA = True
                            Joc.POSIBILITATI.append(p)
                    if not Joc.SARITURA_DUBLA:
                        # Daca nu se mai poate face inca o saritura, schimb jucatorul cu cel opus
                        stare_curenta.j_curent = stare_curenta.jucator_opus()
                        Joc.SARITURA = False
                else:
                    stare_curenta.j_curent = stare_curenta.jucator_opus()
                    Joc.SARITURA = False
            else:
                stare_curenta.j_curent = stare_curenta.jucator_opus()
                Joc.SARITURA = False


    joc_timp_final = int(round(time.time() * 1000))
    timp_joc = joc_timp_final - joc_timp_inceput
    print(f"Jocul a durat {int(timp_joc)} milisecunde")
    if Joc.TIP_SCOR == 1:
        print(f"Scor pentru {Joc.JMAX}: {stare_curenta.tabla_joc.numar_piese(Joc.JMAX)}")
        print(f"Scor pentru {Joc.JMIN}: {stare_curenta.tabla_joc.numar_piese(Joc.JMIN)}")
    else:
        print(f"Scor pentru {Joc.JMAX}: {stare_curenta.tabla_joc.numar_piese_mancate(Joc.JMAX)}")
        print(f"Scor pentru {Joc.JMIN}: {stare_curenta.tabla_joc.numar_piese_mancate(Joc.JMIN)}")
    print(f"Nr mutari {Joc.JMAX}: {nr_mutari_JMAX}")
    print(f"Nr mutari {Joc.JMIN}: {nr_mutari_JMIN}")
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
