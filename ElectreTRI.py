#!/usr/bin/python
# -*- coding: UTF-8 -*-


from random import randint
from random import choice
from collections import defaultdict


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
		'Florianopolis',
		]

	nAlternativas= len(cidades) #Linhas
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
	print 'Limite de Preferência', p
	print '\n'
	#limite de indiferença
	q = 1.0
	print 'Limite de Indiferença', q
	print '\n'

	#limite de veto
	v = 1.0
	print 'Limite de Veto', v
	print '\n'

	#lambda de corte
	lamb = 0.7
	print 'Lambda de Corte', lamb
	print '\n'

	# Classes ordenadas

	classes = ['Excelente', 'Bom', 'Regular', 'Ruim', 'Pessimo']

	limites= []
	numeros = 8.0

	for i in range(len(classes)):
		limites_linhas= []
		for j in range(nCriterios):
			limites_linhas.append(numeros)
		limites.append(limites_linhas)	
		print limites[i], classes[i]
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

	mConcordanciaAB = matrizConcordanciaTRI(cidades, classes, tabela, nAlternativas, nCriterios, vetorPesos, p, q, limites, 0)
	mConcordanciaBA = matrizConcordanciaTRI(cidades, classes, tabela, nAlternativas, nCriterios, vetorPesos, p, q, limites, 1)

	mDiscordanciaAB = matrizDiscordanciaTRI(cidades, classes, tabela, nAlternativas, nCriterios, vetorPesos, p, v, limites, 0)
	mDiscordanciaBA = matrizDiscordanciaTRI(cidades, classes, tabela, nAlternativas, nCriterios, vetorPesos, p, v, limites, 1)
	# mDiscordancia = matrizDisconcordancia(cidades, tabela, nAlternativas, nCriterios, vetorPesos, p, v)

	mCredibilidadeAB = matrizCredibilidadeTRI(cidades, nAlternativas, nCriterios, mConcordanciaAB, mDiscordanciaAB, limites)
	mCredibilidadeBA = matrizCredibilidadeTRI(cidades, nAlternativas, nCriterios, mConcordanciaBA, mDiscordanciaBA, limites)
	# mCredibilidade = matrizCredibilidade(cidades, nAlternativas, nCriterios, mConcordancia, mDiscordancia)

	# destilacao(cidades, nAlternativas, nCriterios, mCredibilidade)

	subordinacao = matrizSubordinacao(cidades, tabela, nAlternativas, nCriterios, p, v, mCredibilidadeAB, mCredibilidadeBA, lamb, classes)

	classificacaoPessimista(cidades, nAlternativas, nCriterios, subordinacao, classes, limites)	
	classificacaoOtimista(cidades, nAlternativas, nCriterios, subordinacao, classes, limites)	

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

def matrizConcordanciaTRI(cidades, classes, tabela, nAlternativas, nCriterios, vetorPesos, p, q, limites, inverte):
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


    	if (inverte == 0):
	    	for i in range(nAlternativas):
	    		linha = []
	    		for j in range(nCriterios):
	    			somatorio = 0
	    			for k in range(len(classes)):
		    			valor = 0.0
		    			# print(k, j)
		    			if (limites[k][j] - tabela[i][j]) >= p:
		    				valor = 0.0
		    			elif (limites[k][j] - tabela[i][j]) < q:
		    				valor = 1.0
		    			else:
		    				valor += (p + tabela[i][j] - limites[k][j]) / (p - q)
		    			somatorio += valor
	    			linha.append(round(somatorio,2))
	    			# print(valor)
	    		mConcordancia.append(linha)
	    		print(mConcordancia[i], cidades[i])
    	else:
	    	for i in range(len(classes)):
	    		linha = []
	    		for j in range(nAlternativas):
	    			somatorio = 0
	    			for k in range(nCriterios):
	    				valor = 0.0
		    			# print(k, j)
		    			if (tabela[j][k] - limites[i][k]) >= p:
		    				valor = 0.0
		    			elif (tabela[j][k] - limites[i][k]) < q:
		    				valor = 1.0
		    			else:
		    				valor += (p + tabela[j][k] - limites[i][k]) / (p - q)
		    			somatorio += valor
	    			linha.append(round(somatorio,2))
	    		mConcordancia.append(linha)
	    		print(mConcordancia[i], classes[i])


    	return mConcordancia


def matrizDiscordanciaTRI(cidades, classes, tabela, nAlternativas, nCriterios, vetorPesos, p, v, limites, inverte):
	print "\nMatrizes de Discordância  por Alternativa\n"
	mDiscordancia = []

	if (inverte == 0):
		for i in range(nAlternativas):
			linha = []
			for j in range(nCriterios):
				resultado = 0
				for k in range(len(classes)):
					valor = 0.0
					if(limites[k][j] - tabela[i][j]) < p:
						valor = 0.0
					elif(limites[k][j] - tabela[i][j]) >= v:
						valor = 1.0
					else:
						valor += round((limites[k][j] - tabela[i][j] - p) / (v - p), 2)
					resultado += valor
				linha.append(round(resultado, 2))
			mDiscordancia.append(linha)
			print mDiscordancia[i], cidades[i]
	else:
		for in range(len(classes)):
			linha = []
			for j in range(nAlternativas):
				resultado = 0
				for k in range(nCriterios):
					valor = 0.0
					if(tabela[j][j] - limites[i][k]) < p:
						valor = 0.0
					elif(tabela[j][j] - limites[i][k]) >= v:
						valor = 1.0
					else:
						valor += round((limites[k][j] - tabela[i][j] - p) / (v - p), 2)
					resultado += valor
					linha.append(round(resultado, 2))
			mDiscordancia.append(linha)
			print mDiscordancia[i], cidades[i]


	return mDiscordancia

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

def matrizCredibilidadeTRI(cidades, nAlternativas, nCriterios, mConcordancia, mDiscordancia, limites):
	print "\n\nMatriz de Credibilidade\n"

	matrizCredibilidade = []
	mCredibilidade= []

	for i in range(nAlternativas):
		linha=[]
		for j in range(len(limites[i])):
			valor = 1
			if(mDiscordancia[i][j] > mConcordancia[i][j]):
				valor = 1.0
			elif(mConcordancia[i][j] == 1.0):
				valor = 1.0
			else:
				# print mDiscordancia[i][j], mConcordancia[i][j]
				for k in range(nCriterios):
					valor *= ((1 - mDiscordancia[i][k]) / (1 - mConcordancia[i][j]))
			linha.append(round(mConcordancia[i][j] * valor, 2))		
		mCredibilidade.append(linha)
		print(mCredibilidade[i], cidades[i])

	return mCredibilidade
	# for i in range(nAlternativas):
	# 	linha = []
	# 	for j in range(len(mConcordancia[i])):
	# 		indiceDiscordanciaMaior = False

	# 		for k in range(nCriterios):
	# 			if (mDiscordancia[k][i][j] > mConcordancia[i][j]):
	# 				indiceDiscordanciaMaior = True
	# 		#print indiceDiscordanciaMaior
	# 		if (indiceDiscordanciaMaior):
	# 			resultado1 = 1.0
	# 			for k in range(nCriterios):
	# 				resultado1 *= round(((1.0-mDiscordancia[k][i][j])/(1.0-mConcordancia[i][j])), 2)
	# 			resultado2 = mConcordancia[i][j] * resultado1
	# 			#print resultado2
	# 			linha.append(resultado2)
	# 		else:
	# 			linha.append(mConcordancia[i][j])
	# 		#print linha
	# 	matrizCredibilidade. append(linha)

	# for x in range(nAlternativas):
	# 	print matrizCredibilidade[x], cidades[x]

	# return matrizCredibilidade

def matrizSubordinacao(cidades, tabela, nAlternativas, nCriterios, p, v, mCredibilidadeAB, mCredibilidadeBA, lamb, classes):
	print "\n\nRelação de Subordinação \n"	
	subordinacao = []

	#0 - Indiferença
	#1 - ASB
	#2 - BSA
	#3 - !ASB AND !BSA

	for i in range(nAlternativas):
		linha = []
	 	for j in range(len(mCredibilidadeAB[i])):
	 		valor = 0
	 		if(mCredibilidadeAB[i][j] >= lamb) and (mCredibilidadeBA[i][j] >= lamb):
	 			valor = 0
	 		elif (mCredibilidadeAB[i][j] >= lamb) and not(mCredibilidadeBA[i][j] >= lamb):
	 			valor = 1
	 		elif not(mCredibilidadeAB[i][j] >= lamb) and (mCredibilidadeBA[i][j] >= lamb):
	 			valor = 2
	 		elif not(mCredibilidadeAB[i][j] >= lamb) and not(mCredibilidadeBA[i][j] >= lamb):
	 			valor = 3
	 		linha.append(valor)
	 		print cidades[i], valor, classes[j]
	 	subordinacao.append(linha)

	return subordinacao

def classificacaoPessimista(cidades, nAlternativas, nCriterios, subordinacao, classes, limites):
	print "\n\n Classificação Pessimista \n"
	classificacao = defaultdict(list)


	for i in range(nAlternativas):	
		linha = []
		for j in range(len(classes)):
			# print j
			if(subordinacao[i][j] < 2):
				break
		if(j < len(classes)):
			classificacao[classes[j+1]].append(cidades[i])	
		else:
			classificacao[classes[j]].append(cidades[i])	
	print(classificacao)

def classificacaoOtimista(cidades, nAlternativas, nCriterios, subordinacao, classes, limites):
	print "\n\n Classificação Otimista \n"
	classificacao = defaultdict(list)


	for i in range(nAlternativas):	
		linha = []
		for j in reversed(range(len(classes))):
			# print j
			if(subordinacao[i][j] < 2):
				break
		classificacao[classes[j]].append(cidades[i])	

	print(classificacao)




main()
