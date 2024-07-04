import os
import pandas as pd
import funcoes as fn

# Retira o limite de carcateres vizualizados no teriminal quando é imprimido o dataframe. 
pd.set_option('display.max_colwidth', None)

# Roda a função de concatenar os dados semestrais, cria o datframe como as informações e salva um CSV concatenado.
fn.concatenaDados()

# Roda a função de tratamento dos dados.
fn.tratamentoDados()

# Informa o periodo inicial e final da série histórica.
fn.infoPeriodo()

while True:

    # Solicita a Analise de dados desjada:
    escolha = input(f"""\nEscolha a Analise de dados desejada:\n 1 - Comparação entre cidades do preço médio do combustivel para toda série histórica\n 2 - Comparação entre cidades do preço médio do combustivel para o periodo de interesse\n 3 - Endereço dos Postos com o preço médio do combustivel mais baratos para toda série histórica\n 4 - Endereço dos Postos com o preço médio do combustivel mais baratos para o perido de interesse\n 5 - Sair\n""")

    match escolha:
        case "1":
            combustivel = fn.coletar_combustivel()
            
            cidades = fn.coletar_cidades()

            fn.mediaVendaMunicipiosProduto(cidades, combustivel)

        case "2":

            # Desempacota as variaveis que informam inicio da série histórica e final da série histórica.
            data_inicial, data_final, data_inicial_formatada, data_final_formatada = fn.infoPeriodo()

            # Desempacota as variaveis que informam inicio do periodo de interesse e final do periodo de interesse.
            data_inicial_usuario_dt, data_final_usuario_dt = fn.coletar_periodo_usuario(data_inicial, data_final, data_inicial_formatada, data_final_formatada)

            combustivel = fn.coletar_combustivel()
            
            cidades = fn.coletar_cidades()

            fn.mediaVendaMunicipiosProdutoDataInteresse(cidades, combustivel, data_inicial_usuario_dt, data_final_usuario_dt)

        case "3":
            fn.top5BaratosHistorico()

            fn.top5BaratosDataInteresse()
        
        case "5":
            break