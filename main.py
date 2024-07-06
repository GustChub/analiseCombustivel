import os
import pandas as pd
import funcoes as fn

# Retira o limite de caracteres vizualizados no teriminal, quando é imprimido o dataframe. 
pd.set_option('display.max_colwidth', None)

# Roda a função de concatenar os dados semestrais, cria o dataframe e salva um CSV concatenado.
fn.concatenaDados()

# Roda a função de tratamento dos dados.
fn.tratamentoDados()

# Informa o periodo inicial e final da série histórica.
fn.infoPeriodo()

while True:

    # Solicita a Analise de dados desjada:
    print("""\nEscolha a Analise de dados desejada:\n 1 - Comparação entre cidades do preço médio do combustivel para toda série a histórica\n 2 - Comparação entre cidades do preço médio do combustivel para o período de interesse\n 3 - Postos com o preço médio do combustivel mais baratos para toda série a histórica\n 4 - Postos com o preço médio do combustivel mais baratos para o perído de interesse\n 5 - Sair\n""")
    escolha = input("Opção: ")

    match escolha:
        case "1":

            # Atribui a combustivel a escolha do usuário retornada pela função 'fn.coletarCombustivel()'
            combustivel = fn.coletarCombustivel()
            
            # Atribui a cidades a escolha do municipio de interesse do usuário retornada pela função 'fn.coletarCidades()'
            cidades = fn.coletarCidades()

            # Imprimi os resultado das Médias do valor do combustível para o municipio em toda série histórica
            fn.mediaVendaMunicipiosProduto(cidades, combustivel)

        case "2":

            # Desempacota as variaveis que informam inicio do periodo de interesse e final do periodo de interesse.
            data_inicial_usuario_dt, data_final_usuario_dt = fn.coletarPeriodoUsuario()

            # Atribui a combustivel a escolha do usuário retornada pela função 'fn.coletarCombustivel()'
            combustivel = fn.coletarCombustivel()

            # Atribui a cidades a escolha do municipio de interesse do usuário retornada pela função 'fn.coletarCidades()'
            cidades = fn.coletarCidades()

            # Imprimi os resultado das Médias do valor do combustível para o municipio em toda série histórica
            fn.mediaVendaMunicipiosProdutoDataInteresse(cidades, combustivel, data_inicial_usuario_dt, data_final_usuario_dt)

        case "3":

            combustivel = fn.coletarCombustivel()

            cidade = fn.coletarUmaCidade()

            fn.top5BaratosHistorico(cidade, combustivel)

        case "4":

            # Desempacota as variaveis que informam inicio do periodo de interesse e final do periodo de interesse.
            data_inicial_usuario_dt, data_final_usuario_dt = fn.coletarPeriodoUsuario()

            combustivel = fn.coletarCombustivel()
            
            cidade = fn.coletarUmaCidade()

            fn.top5BaratosDataInteresse(cidade, combustivel, data_inicial_usuario_dt, data_final_usuario_dt)
        
        case "5":
            break

        case _ :
            print('Entrada inválida, ecolha um número de 1 a 5')