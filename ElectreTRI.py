#!/usr/bin/python
# -*- coding: UTF-8 -*-


from random import randint
from random import choice


def main():

	print "\nTrabalho de Tópicos Avançados I\n"

	print "Pesquisa: Preferência de Cidades\n"

	print "Determinar a ordem das cidades em que voce moraria, atribuindo notas de 1 a 10:"
	print "Sendo 10 para o critério que você considera de maior importância e 1 para o que você considera de menor importância \n"


	print "Resultados:\n"

	cidades=[
		'Rio de Janeiro',
		'Sao Paulo',
		'Belo Horizonte',
		'Brasilia',
		'Salvador',
		]

	nAlternativas= 5 #Linhas
	nCriterios = 5 #Colunas

	vetorPesos=[0.1, 0.1, 0.2, 0.3, 0.3]
	#Peso 0.1 - Indústria
	#Peso 0.1 - Tráfego
	#Peso 0.2 - Turismo
	#Peso 0.3 - Segurança
	#Peso 0.3 - Custo de vida

	#indice de concordancia
	c = 0.65
	#indice de discordancia
	d = 0.35
	#limite de preferência
	p = 2.0
	#limite de indiferença
	q = 1.0
	#limite de veto
	v = 1.0
	#lambda de corte
	lamb = 1.0

	# Classes ordenadas

	classes = ['Excelente', 'Bom', 'Regular', 'Ruim', 'Péssimo']
	limites= []
	numeros = 8.0

	for i in range(len(classes)):
		limites_linhas= []
		for j in range(nCriterios):
			limites_linhas.append(numeros)
		limites.append(limites_linhas)	
		print classes[i], limites[i]
		numeros -= 2.0

	print "\n \n"
	# bordas= [[8.0, 8.0, 8.0, 8.0, 8.0]
	# 	[6.0, 6.0, 6.0, 6.0, 6.0],
	# 	[4.0, 4.0, 4.0, 4.0, 4.0],
	# 	[2.0, 2.0, 2.0, 2.0, 2.0]
	# 	]	

	tabela = geraTabelaPagamento(nAlternativas, nCriterios)

	print "Critério 1: Indútria"
	print "Critério 2: Tráfego"
	print "Critério 3: Turismo"
	print "Critério 4: Segurança"
	print "Critério 5: Custo de vida\n"

	for i in range(nAlternativas):
		print tabela[i], cidades[i]

	print "\n\nMétodo Electre TRI\n"

	mConcordanciaAB = matrizConcordanciaTRI(cidades, tabela, nAlternativas, nCriterios, vetorPesos, p, q, limites)
	mConcordanciaBA = matrizConcordanciaTRI(cidades, limites, nAlternativas, nCriterios, vetorPesos, p, q, tabela)

	mDiscordanciaAB = matrizDiscordanciaTRI(cidades, tabela, nAlternativas, nCriterios, vetorPesos, p, v, limites)
	mDiscordanciaBA = matrizDiscordanciaTRI(cidades, limites, nAlternativas, nCriterios, vetorPesos, p, v,tabela)
	# mDiscordancia = matrizDisconcordancia(cidades, tabela, nAlternativas, nCriterios, vetorPesos, p, v)

	# mCredibilidade = matrizCredibilidade(cidades, nAlternativas, nCriterios, mConcordancia, mDiscordancia)

	# destilacao(cidades, nAlternativas, nCriterios, mCredibilidade)

	# subordinacao = matrizSubordinacao(cidades, tabela, nAlternativas, nCriterios, p, v, mCredibilidade, lamb)

	print "\n"

def geraTabelaPagamento(nAlternativas, nCriterios):
	matriz = []
	for i in range(nAlternativas):
		linha = []
		for j in range(nCriterios):
			achounumero = 0
			colunaatual = []
			for k in range(i):
				colunaatual.append(matriz[k][j])
			while (achounumero == 0):
				num = choice([1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 10.0])
				if num in colunaatual:
					continue
				else:
					achounumero = 1
			linha.append(num)
		matriz.append(linha)
	return matriz


def matrizConcordancia(cidades, tabela, nAlternativas, nCriterios, vetorPesos, p, q):
    	print "\nMatriz de Concordância Global\n"

    	somaPesos = 0
    	mConcordancia = []

    	for x in range(len(vetorPesos)):
    		somaPesos += vetorPesos[x]

    	#Laço para alternativa a ser comparada
    	for i in range(nAlternativas):
    		linha = []
    		#Laço para o criterio a ser comparado
    		for j in range(len(tabela[i])):
    			#Laço para percorrer matriz
    			somatorioW = 0
    			for y in range(nCriterios):
    				valor = 0
    				if tabela[i][y] > (tabela[j][y] - q):
    					valor = 1
    				else:
    					if tabela[i][y] <= (tabela[j][y] - p):
    						valor = 0
    						#print tabela[i][y], tabela[j][y], q, tabela[j][y] - q
    					else:
    						somatorioW += vetorPesos[y] * ((p-(tabela[i][y]- tabela[j][y]))/p-q)
    				if valor == 1:
    					somatorioW += vetorPesos[y]
    			result = 1.0/somaPesos * somatorioW
    			linha.append(round(result, 2))
    			#print result
    		mConcordancia.append(linha)
    		print mConcordancia[i], cidades[i]
    	return mConcordancia

def matrizConcordanciaTRI(cidades, tabela, nAlternativas, nCriterios, vetorPesos, p, q, limites):
    	print "\nMatriz de Concordância Global\n"

    	somaPesos = 0
    	mConcordancia = []
    	mConcordancia = []
    	# mConcordanciaAB = []
    	# mConcordanciaBA = []
    	mConcordanciaParcial= []
    	# mConcordanciaParcialAB = []
    	# mConcordanciaParcialBA = []

    	for x in range(len(vetorPesos)):
    		somaPesos += vetorPesos[x]



    	for i in range(nAlternativas):
    		linha = []
    		for j in range(len(tabela[i])):
    			valor = 0.0
    			if (limites[i][j] - tabela[i][j]) >= p:
    				valor = 0.0
    			elif (limites[i][j] - tabela[i][j]) < q:
    				valor = 1.0
    			else:
    				valor = (p + tabela[i][j] - limites[i][j]) / (p - q)
    			linha.append(valor)
    			print(valor)
    		mConcordanciaParcial.append(linha)

    	# for in in range(nAlternativas):
    	# 	linha = []
    	# 	for j in range(len(limites[i])):
    	# 		valor = 0
    	# 		if (tabela[i][j] - limites[i][j]) >= p:
    	# 			valor = 0
    	# 		else if (tabela[i][j] - limites[i][j]) < q:
    	# 			valor = 1
    	# 		else:
    	# 			valor = (p + limites[i][j] - tabela[i][j] ) / (p - q)
    	# 		linha.append(valor)
    	# 	mConcordanciaParcialBA.append(linha)

    	for i in range(nAlternativas):
    		linha = []
    		for j in range(len(mConcordanciaParcial)):
    			linha.append(somaPesos * (mConcordanciaParcial[i][j] / somaPesos))
    		mConcordancia.append(linha)
    		print mConcordancia[i], cidades[i]

    	return mConcordancia

    	# #Laço para alternativa a ser comparada
    	# for i in range(nAlternativas):
    	# 	linha = []
    	# 	#Laço para o criterio a ser comparado
    	# 	for j in range(len(tabela[i])):
    	# 		#Laço para percorrer matriz
    	# 		somatorioW = 0
    	# 		for y in range(nCriterios):
    	# 			valor = 0
    	# 			if tabela[i][y] > (tabela[j][y] - q):
    	# 				valor = 1
    	# 			else:
    	# 				if tabela[i][y] <= (tabela[j][y] - p):
    	# 					valor = 0
    	# 					#print tabela[i][y], tabela[j][y], q, tabela[j][y] - q
    	# 				else:
    	# 					somatorioW += vetorPesos[y] * ((p-(tabela[i][y]- tabela[j][y]))/p-q)
    	# 			if valor == 1:
    	# 				somatorioW += vetorPesos[y]
    	# 		result = 1.0/somaPesos * somatorioW
    	# 		linha.append(round(result, 2))
    	# 		#print result
    	# 	mConcordancia.append(linha)
    	# 	print mConcordancia[i], cidades[i]
    	# return mConcordancia

def matrizDiscordanciaTRI(cidades, tabela, nAlternativas, nCriterios, vetorPesos, p, v, limites):
	print "\nMatrizes de Discordância  por Alternativa\n"
	mDiscordancia = []

	for i in range(nAlternativas):
		linha = []
		for j in range(len(limites[i])):
			valor = 0.0
			if(limites[i][j] - tabela[i][j]) < p:
				valor = 0.0
			elif(limites[i][j] - tabela[i][j]) >= v:
				valor = 1.0
			else:
				valor= (limites[i][j] - tabela[i][j] - p) / (v - p)
			linha.append(valor)
		mDiscordancia.append(linha)
		print mDiscordancia[i], cidades[i]

def matrizDisconcordancia(cidades, tabela, nAlternativas, nCriterios, vetorPesos, p, v):
	print "\nMatrizes de Discordância  por Critério\n"

	matrizesDiscordancia = []

	#Laço para alternativa a ser comparada
	for i in range(nAlternativas):
		mDiscordancia = []
		print "\nCritério",i+1
		#Laço para o criterio a ser comparado
		for j in range(len(tabela[i])):
			linha = []
			#Laço para percorrer matriz
			for y in range(nCriterios):
				if i==y or j==y:
					linha.append(0)
				else:
					if tabela[i][y] > (tabela[j][y] - p):
						linha.append(0)
					else:
						if tabela[i][y] < (tabela[j][y] - v):
							linha.append(1)
							#print tabela[i][y], tabela[j][y], q, tabela[j][y] - q
						else:
							result = ((tabela[i][y] - tabela[j][y] - p)/v-p)
							linha.append(round(result, 2))
			#print result
			mDiscordancia.append(linha)

		for x in range(len(mDiscordancia[j])):
			print mDiscordancia[x], cidades[x]

		matrizesDiscordancia.append(mDiscordancia)

	#print matrizesDiscordancia[3][4][0]

	return matrizesDiscordancia

def matrizCredibilidade(cidades, nAlternativas, nCriterios, mConcordancia, mDiscordancia):
	print "\n\nMatriz de Credibilidade\n"

	matrizCredibilidade = []

	for i in range(nAlternativas):
		linha = []
		for j in range(len(mConcordancia[i])):
			indiceDiscordanciaMaior = False

			for k in range(nCriterios):
				if (mDiscordancia[k][i][j] > mConcordancia[i][j]):
					indiceDiscordanciaMaior = True
			#print indiceDiscordanciaMaior
			if (indiceDiscordanciaMaior):
				resultado1 = 1.0
				for k in range(nCriterios):
					resultado1 *= round(((1.0-mDiscordancia[k][i][j])/(1.0-mConcordancia[i][j])), 2)
				resultado2 = mConcordancia[i][j] * resultado1
				#print resultado2
				linha.append(resultado2)
			else:
				linha.append(mConcordancia[i][j])
			#print linha
		matrizCredibilidade. append(linha)

	for x in range(nAlternativas):
		print matrizCredibilidade[x], cidades[x]

	return matrizCredibilidade

def matrizSubordinacao(cidades, tabela, nAlternativas, nCriterios, p, v, mCredibilidade, lamb):
	print "\n\nRelação de Subordinação \n"	
	subordinacao = []

	# for i in range(nAlternativas):
	# 	for j in range(len(mCredibilidade[i])):


main()
