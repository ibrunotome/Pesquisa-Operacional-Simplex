# Quantidade de hectares a serem plantados
var Milho 	>= 0;
var Soja 	>= 0;
var Tomate 	>= 0;

# Funcao objetivo de maximizacao do lucro de acordo com a lucratividade
# por hectare apurada em cada cultura, esses valores foram obtidos
# com o calculo "ganho estimado - custo estimado" por hectare
#
# Area maxima para plantacao: 120 hectares, porem, o tempo de cultivo
# para o milho eh de 180 dias, para a soja sao 120 dias, e para o tomate
# 150 dias. Logo, pode-se plantar, milho 2x ao ano, soja 3x ao ano, e tomate
# 2.3x ao ano.
#
# Limitando-se (por pedido do Luis) a plantacao de tomate a 1 hectare, dos 120,
# e o milho a 66 hectares dos 120, sobram 53 hectares para a soja, dos 120. A
# partir dai pode-se criar o conceito de rotacao das culturas. Logo em um
# ano, totalizam-se 360 hectares disponiveis para a plantacao.
maximize lucro: 4340*Milho*2 + 1380*Soja*3 + 36000*Tomate*2.3;

# Area maxima para plantacao de milho eh de 66 hectares, como o tempo de
# cultivo eh de 180 dias, pode-se plantar milho 2x ao ano (2x66 = 132), sem
# prejuizo para a terra, pois pode-se rotacionar o local de plantio.
AreaMaximaMilho: 	Milho	<= 132; # Plantar 2x = 2x66 hectares
AreaMinimaMilho:	Milho	>= 66;	# Plantar 1x = 1x66 hectares

# Area maxima para plantacao de soja eh de 53 hectares, como o tempo de
# cultivo eh de 120 dias, pode-se plantar soja 3x ao ano (3x53 = 159), sem
# prejuizo para a terra, pois pode-se rotacionar o local de plantio.
AreaMaximaSoja: 	Soja	<= 159; # Plantar 3x = 3x53 hectares
AreaMinimaSoja:		Soja	>= 53; 	# Plantar 1x = 1x53 hectares

# Area maxima para plantacao de tomate eh de 1 hectare (devido ao risco, o
# investimento eh alto (+ de 70 mil reais por hectare, e existe o risco de
# perda por falta de demanda, como aconteceu este ano)), como o tempo de
# cultivo eh de 150 dias, pode-se plantar soja 2.3x ao ano (2.3x1 = 2.3),
# arredondamos para 3.
AreaMaximaTomate: 	Tomate	<= 3; # Plantar 2.3x = 2.3x1 hectares
AreaMinimaTomate:	Tomate	>= 1; # Plantar 1x = 1x1 hectare

# Investimento disponivel para a plantacao anual = 1000000
MaximoInvestimento: 2860*Milho + 3520*Soja + 36490*Tomate <= 1000000;

solve;

display lucro, MaximoInvestimento, Milho, Soja, Tomate;
