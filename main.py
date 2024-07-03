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

# Solicita a Analise de dados desjada:
escolha = input(f"""\nEscolha a Analise de dados desejada:\n 1 - Comparação entre cidades do preço médio do combustivel para toda série histórica\n 2 - Comparação entre cidades do preço médio do combustivel para o periodo de interesse\n 3 - Endereço dos Postos com o preço médio do combustivel mais baratos para toda série histórica\n 4 - Endereço dos Postos com o preço médio do combustivel mais baratos para o perido de interesse\n""")

fn.mediaVendaMunicipiosProduto()

fn.mediaVendaMunicipiosProdutoDataInteresse()

fn.top5BaratosHistorico()

fn.top5BaratosDataInteresse()