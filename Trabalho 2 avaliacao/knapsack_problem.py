#Dependências
from recordclass import recordclass
#pip install recordclass

import heapq
import numpy as np
import scipy.stats

import random
import time

#Calculo da média e Intervalo de confiança
def mean_confidence_interval(data, confidence=0.99):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h

#Auxilia no registro dos testes ==> output.txt
def write(row,filename):
    row = [str(w) for w in row]
    output = open("{}.txt".format(filename),"a")#append mode
    output.write(','.join(row)+"\n")
    output.close()    

#Gera os conjuntos de dados e roda o teste
def roda_teste(itens,R,algoritmo,output):
    
    header = ['modelo','tempo_medio','inferior','superior']
    write(header,output)
    
    run_time = []
    
    for item in itens:
        for r in R:
            for i in range(50):
                #Gera os dados dos itens
                v_lista = [random.randint(1,r) for x in range(0,item)]
                p_lista = [random.randint(1,r) for y in range(0,item)]
                c = int(sum(p_lista)/2)
                start_time = time.time()
                result = algoritmo(c,v_lista,p_lista)
                run_time.append(time.time()-start_time)
                if(i == 49):
                    media, inferior, superior = mean_confidence_interval(run_time, confidence=0.99)
                    modelo = '{}_{}i_{}'.format(output,item,r)
                    write([modelo,media,inferior,superior],output)
                    run_time = []

#Gera os conjuntos de dados e roda o teste para o Força Bruta
def roda_teste_bruteforce(itens,R):
    
    output = 'bruteforce'
    header = ['modelo','tempo_medio','inferior','superior']
    write(header,output)
    
    run_time = []
    
    for item in itens:
        for r in R:
            for i in range(50):
                #Gera os dados dos itens
                v_lista = [random.randint(1,r) for x in range(0,item)]
                p_lista = [random.randint(1,r) for y in range(0,item)]
                c = int(sum(p_lista)/2)
                start_time = time.time()
                result = knapsack_brute_force(c, v_lista, p_lista, item)
                run_time.append(time.time()-start_time)
                if(i == 49):
                    media, inferior, superior = mean_confidence_interval(run_time, confidence=0.99)
                    modelo = '{}_{}i_{}'.format(output,item,r)
                    write([modelo,media,inferior,superior],output)
                    run_time = []


def knapsack_brute_force(cap, valores, pesos, n):
    if n == 0 or cap == 0:
        return 0
    
    if (pesos[n-1] > cap):
        return knapsack_brute_force(cap, valores, pesos, n-1)
    
    else:
        return max(valores[n-1] + knapsack_brute_force(cap-pesos[n-1], valores, pesos, n-1),
                   knapsack_brute_force(cap, valores, pesos, n-1))


def knapsack_greedy(cap,valores,pesos):
    pesoCum = 0
    mochila = {}
    
    itens = [(v,p) for v, p in zip(valores, pesos)]
    itens = sorted(itens, key=lambda x: x[0]/x[1], reverse=True)
    
    for item in itens:
        if (item[1]+pesoCum) <= cap:
            mochila[item] = 1
            pesoCum+=item[1]
        else:
            mochila[item] = 0
            
    return mochila

def knapsack_dynamic(cap, valores, peso):
    n = len(valores)
    matriz = [[0 for x in range(cap + 1)] for x in range(n + 1)]
    for c in range(cap + 1):
        for i in range(n + 1):
            if(i == 0 or c == 0):
                matriz[i][c] = 0
            elif (peso[i-1] <= c):
                matriz[i][c] = max(valores[i-1] + matriz[i-1][c-peso[i-1]],
                            matriz[i-1][c])
            else:
                matriz[i][c] = matriz[i-1][c]
    return (matriz[n][cap])

#Branch and Bound

No = recordclass('No', 'nivel valor peso bound itens')

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]
    
    def empty(self):
        if (len(self._queue) == 0):
            return True
        else:
            return False

    def length(self):
        return len(self._queue)

def knapsack_branch_bound(cap,valores,pesos):


    itens = [(v,p) for v, p in zip(valores, pesos)]
    itens = sorted(itens, key=lambda x: x[0]/x[1], reverse=True)  
    
    n = len(itens)
    
    v = No(nivel = -1, valor = 0, peso = 0, bound = 0, itens = [])
    v.bound = upperbound(v, cap, n , itens)
    
    Q = PriorityQueue()
    
    Q.push(v, v.bound)

    valorMax = 0    
    melhorSolucao = 0
    
    while not Q.empty():

        v = Q.pop()
        if (v.bound > valorMax):
            u = No(nivel = None, peso = None, valor = None, bound = None, itens = [])       
            u.nivel = v.nivel + 1
            u.peso = v.peso + itens[u.nivel][1]
            u.valor = v.valor + itens[u.nivel][0]
            u.itens = list(v.itens)       
            u.itens.append(itens[u.nivel])
        
            if (u.peso <= cap and u.valor > valorMax):
                valorMax = u.valor
                melhorSolucao = u
        
            u.bound = upperbound(u, cap, n, itens)
                
            if (u.bound > valorMax):
                Q.push(u, u.bound)
                
            u = No(nivel = None, peso = None, valor = None, bound = None, itens = [])
            u.nivel = v.nivel + 1
            u.peso = v.peso
            u.valor = v.valor
            u.itens = list(v.itens)
      
            u.bound = upperbound(u, cap, n, itens)

            if (u.bound > valorMax):
                Q.push(u, u.bound)
    
    return melhorSolucao
    
def upperbound(no, cap, n, itens):
    if (no.peso >= cap):
        return 0
    else:
        result = no.valor
        j = no.nivel + 1
        pesoCum = no.peso
        
        while (j < n and pesoCum + itens[j][1] <= cap):
            pesoCum = pesoCum + itens[j][1]
            result = result + itens[j][0]
            j = j + 1
        
        k = j
        if (k <= n - 1):
            result = result + (cap - pesoCum)*itens[k][0]/itens[k][1]
        
        return result

#############################################################################
###                              TESTES                                   ###
#############################################################################

#Força Bruta Recursivo

#itens = [10,15,20,25]
#R = [100,1000,10000]

#roda_teste_bruteforce(itens,R)

#Guloso
#itens = [10000,20000,30000,40000,50000,60000,70000,80000,90000,100000]
#R = [100,1000,10000]

#roda_teste(itens,R,knapsack_greedy,'greedy')

#Dinâmico
#itens = [100,200,300]
#R = [100,1000,10000]

#roda_teste(itens,R,knapsack_dynamic,'dynamic')

#BranchBound
#itens = [1000,5000,10000,15000,20000,25000]
#R = [1000,10000]

#roda_teste(itens,R,knapsack_branch_bound,'branch_bound')