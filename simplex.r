##############################################################################################
#                                                                                            #
# Simplex.r                                                                                  #
#                                                                                            #
# Script didático para ensino de Pesquisa Operacional usando o Método Simplex na sua versão  #
# algébrica, escrito na linguagem R (ver R Project for Scientific Computing)                 #
#                                                                                            #
# Altere os 'ifs' no final do arquivo para habilitar a execucao dos modelos em questao,      #
# escritos na forma padrao.                                                                  #
#                                                                                            #
# Instituto Federal de Educação, Ciência e Tecnologia de Minas Gerais (IFMG) - Formiga/MG    #
#                                                                                            #
# Data       Autor        Comentarios                                                        #
# ========   ===========  =================================================================  #
# 19/11/14   Diego Mello  Versao Inicial. Trata apenas problemas sem degeneracao.            #
#                                                                                            #
##############################################################################################

##############################################################################################
#                                                                                            #
# Metodo Simplex                                                                             #
#                                                                                            #
# Resolve problemas de programação linear utilizando o método Simplex proposto por Dantzig   #
# em 1947. São informados a matriz de coeficientes 'A', o vetor de recursos 'b', o vetor de  #
# custos 'c', os indices de A que formam a base da solucao basica factivel inicial, os indi- #
# ces das variaveis nao-basicas, a dimensao de 'A' e o rotulo do problema em questao.        #
#                                                                                            #
##############################################################################################
Simplex <- function(A, b, c, IndicesBase, IndicesNaoBase, m, n, Titulo)
{
	Iteracao <- 0;

	print(A);
	print(b);
	print(c);

	# Exibe o titulo do problema
	cat('\n\n-------------------------------------------------------------\n');
	cat('Titulo: ', Titulo, '\n');
	cat('-------------------------------------------------------------\n');

	#
	# Laco principal da aplicacao: executa os 5 passos propostos por Bertsimas e Tsiksiklis para realizar
	# uma iteracao completa do método Simplex.
	#
	repeat
	{
		#
		# Passo 1: Calculando SBF inicial
		#

			# Exibe indices basicos e nao basicos da iteracao atual (apenas debug)
			cat('\nIteracao # ', Iteracao, '\n\n');
			cat('\tIndices Basicos    :');
			for(i in IndicesBase)
			{
				cat(' ', i);
			}
			cat('\n');
			cat('\tIndices Não Basicos:');
			for(i in IndicesNaoBase)
			{
				cat(' ', i);
			}
			cat('\n');

			# Cria o espaco reservado para a matriz basica B de dimensao m x m
			B <- matrix(rep(NA, m * m), m, m, byrow=T);

			# Copia as colunas que formam a base inicial
			for(j in 1:m)
			{
				# B_j <- A_{B(j)}
				B[,j] <- A[,IndicesBase[j]];
			}

			# Exibe a base (apenas debug)
			cat('\tBase: \n');
			for(i in 1:m)
			{
				cat('\t\t|');
				for(j in 1:m)
				{
					cat('\t', B[i,j]);
				}
				cat('\t|\n');
			}

			# Calcula a SBF inicial pelo produto da inversa de B com b
			BMenosUm <- solve(B);
			x <- BMenosUm %*% b;

			# Exibe a inversa da base (apenas debug)
			cat('\tBase^-1: \n');
			for(i in 1:m)
			{
				cat('\t\t|');
				for(j in 1:m)
				{
					cat('\t', BMenosUm[i,j]);
				}
				cat('\t|\n');
			}

			# Exibe a solucao básica factível da iteração corrente, apenas variáveis básicas (apenas debug)
			cat('\tSBF # ', Iteracao, ':\n');
			for(i in 1:m)
			{
				cat('\t\tx[', IndicesBase[i], '] = ', x[i], '\n');
			}

			# Exibe o valor da funcao objetivo
			Objetivo <- 0;
			for(i in 1:m)
			{
				Objetivo <- Objetivo + c[IndicesBase[i]]*x[i];
			}
			cat('\tObjetivo: ', Objetivo, '\n');

		#
		# Passo 2: Calculando os custos reduzidos dos indices nao basicos
		#

			# Para cada indice nao base, calcula o custo reduzido correspondente

			# Vetor de custo basico, i.e., parte de c que está relacionado com as variáveis básicas atuais
			CustoBase <- rep(NA, m);
			for(i in 1:m)
			{
				CustoBase[i] <- c[IndicesBase[i]];
			}

			# Exibe vetor de custo basico (apenas debug)
			cat('\tCusto Basico\n');
			for(i in 1:m)
			{
				cat('\t\tc_B[', IndicesBase[i], '] = ', CustoBase[i], '\n');
			}

			# Escolhe algum indice nao basico cujo custo reduzido e' negativo. Dentre os negativos, escolhe
			# o 'mais negativo'
			JotaEscolhido  <- -1;
			CustoEscolhido <- Inf;
			for(j in IndicesNaoBase)
			{
				print(A[,j]);

				# Calcula a j-esima direcao factivel pelo produto -B^{-1}A_j, apenas para debug
				Direcao <- -BMenosUm %*% A[,j];

				# Calcula o custo reduzido
				Custo = c[j] - t(CustoBase) %*% BMenosUm %*% A[,j];

				# Guarda um indice de direcao basica factivel com custo reduzido negativo, se houver
				if(Custo < 0)
				{
					# Verifica se a j-ésima direcao básica é a que contem o custo reduzido 'mais negativo'
					if(Custo < CustoEscolhido)
					{
						# Atualiza candidata a entrar na base
						JotaEscolhido  <- j;
						CustoEscolhido <- Custo;
					}
				}

				# Exibe a j-ésima direcao factivel (apenas para debug)
				cat('\tDirecao Factivel', j, ', Custo Reduzido = ', Custo, '\n');
				for(i in 1:m)
				{
					cat('\t\td_B[', IndicesBase[i], '] = ', Direcao[i], '\n');
				}
			}

			# Se nao encontrou nenhum indice com custo reduzido negativo, e' porque chegamos no otimo
			if(JotaEscolhido == -1)
			{
				# Exibe solucao ótima (apenas debug)
				ValObjetivo <- 0;
				for(i in 1:m)
				{
					ValObjetivo <- ValObjetivo + CustoBase[i] * x[i];
				}
				cat('\nObjetivo = ', ValObjetivo, '(encontrado na ', Iteracao, 'a. iteracao)\n\n')
				Solucao <- rep(0.0, n);
				for(i in 1:m)
				{
					Solucao[IndicesBase[i]] = x[i];
				}
				for(i in 1:n)
				{
					cat('x[', i, '] = ', Solucao[i], '\n');
				}
				cat('\n\n\n');

				return(x);
			}

			# Exibe quem entra na base
			cat('\tVariavel Entra Base: x[', JotaEscolhido, ']\n');

		#
		# Passo 3: Computa vetor u
		#

			# Não chegamos em uma solucao ótima ainda. Alguma variável básica deve sair da base para dar
			# lugar a entrada de uma variável não básica. Computa 'u' para verificar se solucao é ilimitada
			u <- BMenosUm %*% A[,JotaEscolhido];

			# Verifica se nenhum componente de u e' positivo
			ExistePositivo <- FALSE;
			for(i in 1:m)
			{
				if(u[i] > 0)
				{
					ExistePositivo <- TRUE;
				}
			}

			# Testa. Se não houver no vetor 'u' (sinal inverso da direcao factivel) nenhum componente
			# positivo, é porque o valor ótimo é - infinito.
			if(!ExistePositivo)
			{
				cat('\n\nCusto Otimo = -Infinito');
				return(rep(Inf, n));
			}

		#
		# Passo 4: Determina o valor de Theta
		#

			# Chuta um valor alto para o theta, e vai reduzindo de acordo com a razao x_i / u_i
			Theta   <- Inf;
			IndiceL <- -1;

			# Varre indices basicos determinando o valor de theta que garante factibilidade
			for(i in 1:m)
			{
				# Calcula a razao
				if(u[i] > 0)
				{
					# Calcula a razao
					Razao <- x[i] / u[i];

					# Atualiza a razao, pois encontramos um menor valor de theta
					if(Razao < Theta)
					{
						Theta   <- Razao;
						IndiceL <- IndicesBase[i];
					}
				}
			}

			# Exibe variavel que irá deixar a base (apenas debug)
			cat('\tVariavel  Sai  Base: x[', IndiceL, '], Theta = ', Theta, '\n');

		#
		# Passo 5: Atualiza variável básica e não-básica
		#

			# Calcula novo valor da nao-basica, e atualiza base
			for(i in 1:m)
			{
				# Se encontramos o L-ésimo indica da variável básica que deixará a base, substitui-a
				# pela variável não-básica correspondente à j-ésima direção factível de redução de custo
				if(IndicesBase[i] == IndiceL)
				{
					x[i] <- Theta;
					IndicesBase[i] <- JotaEscolhido;
				}
			}

			# Para as demais variáveis não básicas, apenas atualiza o índice de quem saiu da base (e
			# entrou no conjunto das não-básicas
			for(i in 1:(n-m))
			{
				if(IndicesNaoBase[i] == JotaEscolhido)
				{
					IndicesNaoBase[i] <- IndiceL;
				}
			}

		# Incrementa o numero da iteracao
		Iteracao <- Iteracao + 1;
	}

	# Retorna o vetor solucao
	return(x);
}


# Exemplo de execucao (Reddy Mikks)
if(1)
{
	A <- matrix(c(
		 6, 4, 1, 0, 0, 0,
		 1, 2, 0, 1, 0, 0,
		-1, 1, 0, 0, 1, 0,
		 0, 1, 0, 0, 0, 1
	), 4, 6, byrow=T);
	b <- c(24, 6, 1, 2);
	c <- c(-5, -4, 0, 0, 0, 0);
	solucao <- Simplex(A, b, c, c(3,4,5,6), c(1,2), 4, 6, 'Reddy Mikks');
}

# Exemplo de Execucao
if(1)
{
	A <- matrix(c(
		 1, 1, 1, 1,
		 2, 0, 3, 4
	), 2, 4, byrow=T);
	b <- c(2, 2);
	c <- c(-3, 1, 1, 1);
	solucao <- Simplex(A, b, c, c(3,4), c(2,1), 2, 4, 'Exemplo Qualquer');
}

# Exemplo de Execucao (http://www.iepg.unifei.edu.br/arnaldo/ensino/pos/mba/TURMA2/po/aulas/aula_04/Simplex.pdf)
if(1)
{
	A <- matrix(c(
		 2, 1, 1, 0, 0,
		 1, 1, 0, 1, 0,
		 1, 0, 0, 0, 1
	), 3, 5, byrow=T);
	b <- c(100, 80, 40);
	c <- c(-3, -2, 0, 0, 0);
	solucao <- Simplex(A, b, c, c(3,4,5), c(1,2), 3, 5, 'Unifei');
}

# Exemplo: Goldbarg, pagina 104)
if(1)
{
	A <- matrix(c(
		 1, 0, 1, 0, 0,
		 0, 1, 0, 1, 0,
		 3, 2, 0, 0, 1
	), 3, 5, byrow=T);
	b <- c(4, 6, 18);
	c <- c(-3, -5, 0, 0, 0);
	solucao <- Simplex(A, b, c, c(3,2,5), c(1,4), 3, 5, 'Goldbarg (pag 104)');
}

# Exemplo Motores
if(1)
{
	A <- matrix(c(
		  1,  0,   0,  1,  0,   0, 0, 0,
		  0,  1,   0,  0,  1,   0, 0, 0,
		  0,  0,   1,  0,  0,   1, 0, 0,
		  1,  2, 0.5,  0,  0,   0, 1, 0,
		2.5,  1,   4,  0,  0,   0, 0, 1
	), 5, 8, byrow=T);
	b <- c(3000, 2500, 500, 6000, 10000);
	c <- c(50, 90, 120, 65, 92, 140, 0, 0, 0);
	solucao <- Simplex(A, b, c, c(4,5,6,7,8), c(1,2,3), 5, 8, 'Produzir ou Comprar Motores [Lachtermarcher]');
}
