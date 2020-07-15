from copy import deepcopy
import numpy as np
import random

#estado_final = [[0,1,2],
 #               [3,4,5],
  #              [6,7,8]]

estado_final = [[1,2,3],
                [4,5,6],
                [7,8,0]]

def is_solvable(estado_inicial):
    tiles = [x[i] for x in estado_inicial for i in range(3)]
    count = 0

    for i in range(8):
        for j in range(i + 1, 9):
            if tiles[j] and tiles[i] and tiles[i] > tiles[j]:
                count += 1

    return count % 2 == 0

def cria_8puzzle():
    x = []
    while len(x) < 9:
        a = random.randint(0, 8)
        if a in x:
            pass
        else:
            x.append(a)
    problema = np.array(x).reshape((3, 3))
    if is_solvable(problema) == False:
        return False, problema
    else:
        return True, problema

#bol, estado_inicial = cria_8puzzle()
#while bol != True:
    #bol, estado_inicial = cria_8puzzle()




class puzzle:

    def __init__(self, estado, pai):
        self.estado = estado
        self.pai = pai
        self.h = 0
        self.g = 0
        self.f = 0 #h(x) + g(x)

    # def manhattan(self):
    #     h = 0
    #     for i in range(3):
    #         for j in range(3):
    #             x, y = divmod(self.estado[i][j], 3)
    #             h += abs(x-i) + abs(y-j)
    #     return h
    def manhattan(self):
        h =0
        for i in range(9):
            row_final, col_final = np.where(np.array(estado_final) == i)
            row_atual, col_atual = np.where(np.array(self.estado) == i)
            h+= abs(row_atual - row_final) + abs(col_atual - col_final)
        return h

def move_function(curr):
    curr = curr.estado
    for i in range(3):
        for j in range(3):
            if curr[i][j] == 0:
                #Pegando onde está o 0
                x, y = i, j
                break
    q = []
    if x-1 >= 0:
        b = deepcopy(curr)
        b[x][y]=b[x-1][y]
        b[x-1][y]=0
        #Cria um novo nó, sendo ele o filho do curr
        succ = puzzle(b, curr)
        q.append(succ)
    if x+1 < 3:
        b = deepcopy(curr)
        b[x][y]=b[x+1][y]
        b[x+1][y]=0
        succ = puzzle(b, curr)
        q.append(succ)
    if y-1 >= 0:
        b = deepcopy(curr)
        b[x][y]=b[x][y-1]
        b[x][y-1]=0
        succ = puzzle(b, curr)
        q.append(succ)
    if y+1 < 3:
        b = deepcopy(curr)
        b[x][y]=b[x][y+1]
        b[x][y+1]=0
        succ = puzzle(b, curr)
        q.append(succ)
    return q

def find_best(openList):
    #A gente começa pegando o custo do primeiro elemento da lista
    f = openList[0].f
    index = 0
    for i, item in enumerate(openList): #O enumerate tanto percorre sobre os itens (item) como também o conta(i), ou seja, pega o indice.
        if(item.f < f):
            f = item.f
            index = i
    return openList[index], index

def AStar(start_Node):
    openList = []
    closedList = []

    #Inicia a lista:
    openList.append(start_Node)

    found = False
    #Enquanto a lista não estiver vazia:
    while openList:
        print(len(openList), len(closedList))

        #Pega o estado de menor custo
        node, index = find_best(openList)
        #Remove este da lista e coloca na lista de ja explroados
        openList.pop(index)

        #A gente vai inserir este bem no começo, devido a logica da linha 104
        closedList.append([])
        closedList[0+1:] = closedList[0:-1]
        closedList[0] = node

        if node.estado == estado_final:
            return node

        else:#Caso contrario, a gente continua a procurar
            new_nodes = move_function(node)

            for filho in new_nodes:
                #Ja vamos corrigir os custos deste nós:
                filho.g = node.g + 1 #é o custo do nó pai + 1
                filho.h = filho.manhattan()
                filho.f = filho.g + filho.h
                filho.pai = node

                #Agora vamos ver se este será ou não adicionado a lista
                ok = True
                for i, no in enumerate(closedList):
                    if filho.estado == no.estado:
                        if filho.f > no.f: #Então, a gente não deve adicionar nada a fila
                            ok = False
                        break

                if ok: #se ok = True, então é porque, ou não existe um elemento igual na closed, ou este novo tem menor custo
                    in_open= False
                    for i, no in enumerate(openList):
                        if filho.estado == no.estado:
                            in_open = True
                            if filho.f < no.f:#Se ele existir na openList e seu custo for menor do que o que está lá
                                #Entao a gente "substitui" este existente pelo novo
                                openList[i] = filho
                            break

                    if not in_open: #Se o in_open == false, isto é não tenha encontrado nada igual na open list
                        openList.append(filho)

    return None

problema = [[2,3,6],
            [1,0,7],
            [4,8,5]]

start = puzzle(problema, None)

result = AStar(start)
noofMoves = 0

if result == None:
    print ("No solution")
else:
    print(np.array(result.estado).reshape(3,3))
    t=result.pai
    while t:
        noofMoves += 1
        print("   /", "\\")
        print("    || ")
        print(np.array(t.estado).reshape(3,3))
        t=t.pai
print ("Length: ", noofMoves)