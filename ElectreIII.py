#!/usr/bin/python
# -*- coding: UTF-8 -*-


from random import randint
from random import choice


def main():

	print "\nTrabalho de Tópicos Avançados I\n"

	print "Pesquisa: Preferência de Cidades\n"

	print "Determinar a ordem das cidades em que voce moraria, atribuindo notas de 1 a 9:"
	print "Sendo 9 para o critério que você considera de maior importância e 1 para o que você considera de menor importância \n"


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
	q = 1.5
	#limite de veto
	v = 1.0

	tabela = geraTabelaPagamento(nAlternativas, nCriterios)

	print "Critério 1: Indútria"
	print "Critério 2: Tráfego"
	print "Critério 3: Turismo"
	print "Critério 4: Segurança"
	print "Critério 5: Custo de vida\n"

	for i in range(nAlternativas):
		print tabela[i], cidades[i]

	print "\n\nMétodo Electre III\n"

	mConcordancia = matrizConcordancia(cidades, tabela, nAlternativas, nCriterios, vetorPesos, p, q)

	mDiscordancia = matrizDisconcordancia(cidades, tabela, nAlternativas, nCriterios, vetorPesos, p, v)

	mCredibilidade = matrizCredibilidade(cidades, nAlternativas, nCriterios, mConcordancia, mDiscordancia)

	destilacao(cidades, nAlternativas, nCriterios, mCredibilidade)

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
				num = choice([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])
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


def destilacao(cidades, nAlternativas, nCriterios, mCredibilidade):
	print "\n\nDestilação\n"

	destilacaoAscendente = []



	for i in range(len(mCredibilidade)):
		mCredibilidade[i].append(cidades[i])

	#print len(mCredibilidade)

	fim = False
	while (fim==False):

		#print mCredibilidade

		lAst = lambdaAsterisco(lambdaMaxima(mCredibilidade, nAlternativas))

		vetorSelecionadas = determinaAlternativaAscendente(mCredibilidade, lAst, cidades)

		for k in range(len(vetorSelecionadas)):
			for i in range(len(mCredibilidade)):
				if (vetorSelecionadas[k][0] == mCredibilidade[i][len(mCredibilidade)]):
					for j in range(len(mCredibilidade)):
						for g in range(len(mCredibilidade)):
							if (i == j or i == g):
								mCredibilidade[j][g] = []




		zero = True
		for n in range(len(vetorSelecionadas)):
			if 0 != vetorSelecionadas[n][1]:
				zero = False
		if (zero):
			i = 0
			while (i < len(vetorSelecionadas)):
				achou = False
				for n in range(len(destilacaoAscendente)):
					#print vetorSelecionadas[i][0], destilacaoAscendente[n][0]
					if(vetorSelecionadas[i][0] == destilacaoAscendente[n][0]):
						achou = True
				if (achou ==False):
					destilacaoAscendente.append(vetorSelecionadas[i])
				i+=1
		else:
			for n in range(len(vetorSelecionadas)):
				destilacaoAscendente.append(vetorSelecionadas[n])

		fim = True
		for k in range(len(mCredibilidade)):
			for i in range(len(mCredibilidade)):
				if mCredibilidade[k][i] != []:
					fim = False

	print destilacaoAscendente


def determinaAlternativaAscendente(mCredibilidade, lAst, cidades):


	matrizOrdenacao = []
	for i in range(len(mCredibilidade)):
		linha = []
		for j in range(len(mCredibilidade)):
				if (mCredibilidade[i][j] >= lAst) and mCredibilidade[i][j] != []:
					linha.append(1)
				else:
					linha.append(0)

		matrizOrdenacao.append(linha)
	#print matrizOrdenacao, "\n"

	# Vetor Qualificacao
	matrizQualificacao = []
	for i in range(len(matrizOrdenacao)):
		vetorQualificacao = []
		valorLinha = 0
		valorColuna = 0
		for j in range(len(matrizOrdenacao)):
			for k in range(len(matrizOrdenacao[i])):
				if i == j:
					valorLinha += matrizOrdenacao[j][k]
				if i == k:
					valorColuna += matrizOrdenacao[j][k]
		resultado = valorLinha - valorColuna
		vetorQualificacao.append(cidades[i])
		vetorQualificacao.append(resultado)
		matrizQualificacao.append(vetorQualificacao)
	#print matrizQualificacao

	matrizQualificacao.sort(key=lambda x: x[1], reverse = True)

	vet = []
 	for i in range(len(matrizOrdenacao)):
		vet.append(matrizQualificacao[i][1])

	maiorIndice = max(vet)
	#Pegando as alternativas de maiores indices
	altMaior = []
	for i in range(len(matrizOrdenacao)):
		if (matrizQualificacao[i][1] == maiorIndice):
			altMaior.append(matrizQualificacao[i])

	return altMaior
'''
	if len(altMaior) > 1:
		novaMatriz=[]
		for k in range(len(altMaior)):
			for i in range(len(mCredibilidade)):
				if (altMaior[k][0] == mCredibilidade[i][len(mCredibilidade)]):
					for j in range(len(mCredibilidade)):
						for g in range(len(mCredibilidade)):
							if (i == j or i == g):
								mCredibilidade[j][g] = []

		#print mCredibilidade
		try:
			determinaAlternativaAscendente(mCredibilidade, lAst, cidades)
		except:
			print ''
'''

def lambdaMaxima(mCredibilidade, nAlternativas):

	#print mCredibilidade

	lMax = 0
	for i in range(len(mCredibilidade)):
		for j in range(len(mCredibilidade)):
			if (i!=j) and (mCredibilidade[i][j] != []):
				if(mCredibilidade[i][j] > lMax):
					lMax = mCredibilidade[i][j]
	#print lMax
	return lMax

def lambdaAsterisco(lMax):

	lAst = lMax - (0.3 - 0.15*lMax)

	return lAst








'''
def matrizOrdenacao(cidades, nAlternativas, nCriterios, mCredibilidade):
	print "\n\nDestilação\n"

	# P - Preferência Forte
	# Q - Preferência Fraca
	# I - Indiferença
	# R - Incomparabilidade
	# S - Superação

	#lambda máxima

	#print lambdaMaxima(mCredibilidade, nAlternativas)

	#lMax = lambdaMaxima(mCredibilidade, nAlternativas)

	#print lambdaAsterisco(lMax)

	destilacaoAscendente = []
	i = 0
	while (i < nAlternativas):
		print mCredibilidade
		lAst = lambdaAsterisco(lambdaMaxima(mCredibilidade, nAlternativas))

		vetorSelecionadas = []
		vetorSelecionadas = determinaAlternativaAscendente(mCredibilidade, lAst, cidades)

		indices = []
		for k in range(len(vetorSelecionadas)):
			indices.append(cidades.index(vetorSelecionadas[k][0]))
		#print indices
		for j in range(len(indices)):
			mCredibilidade[indices[j]] = []

		print vetorSelecionadas
		destilacaoAscendente.append(vetorSelecionadas)

		i += 1
		#mCredibilidade = []



def determinaAlternativaAscendente(mCredibilidade, lAst, cidades):

	matrizOrdenacao = []
	for i in range(len(mCredibilidade)):
		 if (mCredibilidade[i] != []):
			linha = []
			for j in range(len(mCredibilidade)):
				if (mCredibilidade[i][j] >= lAst):
					linha.append(1)
				else:
					linha.append(0)

			matrizOrdenacao.append(linha)
	#print matrizOrdenacao

	# Vetor Qualificacao
	matrizQualificacao = []
	for i in range(len(matrizOrdenacao)):
		vetorQualificacao = []
		valorLinha = 0
		valorColuna = 0
		for j in range(len(matrizOrdenacao)):
			for k in range(len(matrizOrdenacao[i])):
				if i == j:
					valorLinha += matrizOrdenacao[j][k]
				if i == k:
					valorColuna += matrizOrdenacao[j][k]
		resultado = valorLinha - valorColuna
		vetorQualificacao.append(cidades[i])
		vetorQualificacao.append(resultado)
		matrizQualificacao.append(vetorQualificacao)

	matrizQualificacao.sort(key=lambda x: x[1], reverse = True)

	vet = []
 	for i in range(len(matrizOrdenacao)):
		vet.append(matrizQualificacao[i][1])

	maiorIndice = max(vet)
	#Pegando as alternativas de maiores indices
	altMaior = []
	for i in range(len(matrizOrdenacao)):
		if (matrizQualificacao[i][1] == maiorIndice):
			altMaior.append(matrizQualificacao[i])

	#Desempate

	if len(altMaior) > 1:
		indices = []
		for k in range(len(altMaior)):
			indices.append(cidades.index(altMaior[k][0]))
		#print indices
		for j in range(len(indices)):
			mCredibilidade[indices[j]] = []
		#print len(mCredibilidade)
		try:
			determinaAlternativaAscendente(mCredibilidade, lAst, cidades)
		except:
			print ''
	print "\n", matrizQualificacao
	#print vet, maiorIndice
	return altMaior

def lambdaMaxima(mCredibilidade, nAlternativas):

	lMax = 0
	for i in range(nAlternativas):
		for j in range(nAlternativas):
			if (i!=j) and (mCredibilidade[i] != []):
				if(mCredibilidade[i][j] > lMax):
					lMax = mCredibilidade[i][j]
	return lMax

def lambdaAsterisco(lMax):

	lAst = lMax - (0.3 - 0.15*lMax)

	return lAst

'''
'''
def determinaAlternativa(cidades, vetorSelecionadas, mCredibilidade):
	escolhida = 0
	for i in range (len(vetorSelecionadas)-1):
		j=1
		for j in range (len(vetorSelecionadas)-1):
			alt1 = cidades.index(vetorSelecionadas[i][0])
			alt2 = cidades.index(vetorSelecionadas[j][0])
			if (mCredibilidade[alt1][alt2] > mCredibilidade[alt2][alt1]) and (mCredibilidade[alt1][alt2] > escolhida):
					escolhida = alt1
			else:
				if (mCredibilidade[alt1][alt2] < mCredibilidade[alt2][alt1]) and (mCredibilidade[alt2][alt1] > escolhida):
					escolhida = alt2

	print escolhida
	print cidades[escolhida]
'''
'''
	matrizOrdenacao = []
	vetorQualificacao = []


	# Matriz Ordenação
	for i in range(nAlternativas):
		linha = []
		for j in range(len(mCredibilidade[i])):
			if (mCredibilidade[i][j] >= l):
				linha.append(1)
			else:
				linha.append(0)

		matrizOrdenacao.append(linha)

	for x in range(nAlternativas):
		print matrizOrdenacao[x], cidades[x]


	# Vetor Qualificacao
	for i in range(nAlternativas):
		valorLinha = 0
		valorColuna = 0
		for j in range(len(matrizOrdenacao[i])):
			for k in range(len(matrizOrdenacao[i])):
				if i == j:
					valorLinha += matrizOrdenacao[j][k]
				if i == k:
					valorColuna += matrizOrdenacao[j][k]
		resultado = valorLinha - valorColuna
		vetorQualificacao.append(resultado)

	print "\n", vetorQualificacao

	# Ordenação Otimista
	matrizOtimista =[]

	#Preenchendo matriz
	for i in range(nAlternativas):
		linha=[]
		linha.append(cidades[i])
		linha.append(vetorQualificacao[i])
		linha.append(False) #Incomparabilidade
		matrizOtimista.append(linha)

	print matrizOtimista

	matrizOtimista.sort(key=lambda x: x[1], reverse = True)

	print matrizOtimista

	#Criterio de Desempate Ascendente
	for i in range(nAlternativas):
		for j=1  in range(nAlternativas):
			if (matrizOtimista[i][1] == matrizOtimista[j][1]):
				print i, j
				matrizDesempate = []
				valor1 = cidades.index(matrizOtimista[i][0])
				valor2 = cidades.index(matrizOtimista[j][0])
				print valor1, valor2
				matrizDesempate.append(matrizOrdenacao[valor1])
				matrizDesempate.append(matrizOrdenacao[valor2])

	print matrizDesempate




for i in range(nAlternativas):
	for j in range(nAlternativas):
		if (i!=j):
			if((mCredibilidade[i][j] > lAst) and (mCredibilidade[i][j] > mCredibilidade[j][i])):
				lForte = 0
				lFraco = 0
				linha = []
				for k in range(nAlternativas):
					if (mCredibilidade[i][k]>lMax):
						lForte +=1
					else:
						lFraco +=1
				linha.append(cidades[i])
				linha.append(lForte-lFraco)
				vetorSelecionadas.append(linha)



'''

main()
