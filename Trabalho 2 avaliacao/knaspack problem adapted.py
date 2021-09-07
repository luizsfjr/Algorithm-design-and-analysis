def knapSack(matriz, cap, peso, valores):
	n = len(valores)
	for c in range(cap + 1):
		for i in range(n + 1):
			if(i == 0 or c == 0):
				matriz[i][c] = 0
			elif (peso[i-1] <= c):
				matriz[i][c] = max(valores[i-1] + matriz[i-1][c-peso[i-1]],
							    matriz[i-1][c])
			else:
				matriz[i][c] = matriz[i-1][c]
	return (matriz[n][cap],matriz)

# Main
valores = [60, 100, 120]
pesos = [1, 2, 3]
cap = 5
matriz = [[0 for x in range(cap + 1)] for x in range(len(valores) + 1)]
valor_maximo, matriz = knapSack(matriz, cap, pesos, valores)
print(valor_maximo)
print(matriz)