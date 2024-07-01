# Neste modulo são definidas as funções utilizadas do modulo main
import os
import pandas as pd

# define função para tratar e acessar os dados.

def concatenaDados():
    
    global arquivo_saida
    global diretorio_salvar
    global df
   

     # Define o caminho para a pasta onde deseja salvar o arquivo CSV
    diretorio_salvar = os.path.join(os.path.dirname(__file__), 'dados', 'csv_concatenado')
    arquivo_saida = os.path.join(diretorio_salvar, 'dados_concatenados.csv')
   
    # Verifica se o diretório existe e cria se não existir
    if not os.path.exists(diretorio_salvar):
        os.makedirs(diretorio_salvar)
    
    # Verifica se o arquivo de saída já existe
    if os.path.exists(arquivo_saida):
        print(f"O arquivo {arquivo_saida} já existe. Carregando o DataFrame a partir deste arquivo.")
        df = pd.read_csv(arquivo_saida, delimiter=',', low_memory= False)
        print(f"DataFrame carregado com sucesso. Total de linhas: {len(df)}")
        return df
           
   # Lista os arquivos dentro da pasta de origem dos CSVs
    diretorio_principal = os.path.dirname(__file__)
    pasta_csv_semestrais = os.path.join(diretorio_principal, 'dados', 'csv_semestrais')
    arquivos = os.listdir(pasta_csv_semestrais)
    print("Arquivos na pasta: ", arquivos)

    # Cria um DataFrame para armazenar os dados
    df_base = []
    
    # Varre todos os arquivos .csv e adiciona ao df_base.
    csv_processado = 0
    for arquivo in arquivos:
        if arquivo.endswith(".csv"):
           csv_processado += 1
           print("Arquivo analisado", arquivo)
           caminho = os.path.join(diretorio_principal, arquivo)
           print("Caminho do arquivo: ", caminho)
           df = pd.read_csv(caminho, delimiter=';',low_memory= False)
           print("Total de linhas do arquivo", len(df))
           df_base.append(df)

    # Concatena todos os DataFrames e um único.
    df = pd.concat(df_base, ignore_index=True)
    print("Base de dados criada, total de:", str(csv_processado), "Arquivos adicionados.")
    print(f"Total de linhas do DataFrame, {len(df)}, \n\n{df.describe()}, \n\n{df.info()} ")

    # Salva o DataFrame em um arquivo CSV na pasta especificada
    df.to_csv(arquivo_saida, index=False)
    print(f"DataFrame salvo como CSV em: {arquivo_saida}")

    return df

def atualizaDados():

    # Verifica se o arquivo de saída já existe e remove o mesmo
    if os.path.exists(arquivo_saida):
        os.remove(arquivo_saida)

        # Atualiza os dados através do metodo concatenaDados
        concatenaDados()

def infoDF():

    # Exibe informações sobre o DataFrame antes da conversão
    print("Informações do DataFrame antes da conversão:")
    print(df.info())

def convertValorFloat(): 

    # Converte a coluna 'Valor de Venda' para float
    df['Valor de Venda'] = df['Valor de Venda'].str.replace(',', '.').astype(float)
    return df

def convertDate():
    # Converte a coluna 'Data da Coleta' para o formato de Data 
    df['Data da Coleta'] = pd.to_datetime(df['Data da Coleta'], dayfirst=True)
    return df
    
###def limparDados():
    print("Iniciando a limpeza do dados...")
    
    valores_nulos_antes = df.isnull().sum()
    print("\nValores nulos por coluna antes da limpeza:")
    print(valores_nulos_antes)
    
    
###def limpar_Dados():
    print("Iniciando a limpeza dos dados...")

    # Levantar o número de valores nulos por coluna antes da limpeza
    valores_nulos_antes = df.isnull().sum()
    print("\nValores nulos por coluna antes da limpeza:")
    print(valores_nulos_antes)

    # Remover linhas com células vazias
    df = df.dropna()

    # Verificar e remover valores NaT
    df = df[df['Data da Coleta'].notna()]

    # Levantar o número de valores nulos por coluna após a limpeza
    valores_nulos_depois = df.isnull().sum()
    print("\nValores nulos por coluna após a limpeza:")
    print(valores_nulos_depois)

    print("Dados limpos com sucesso.")
    return df

def infoPeriodo():

    # Organiza o dataframe em ordem crescente de data e seleciona as celulas com data inicia e a final do dataframe.
    df_sorted_data = df.sort_values(by='Data da Coleta', ascending= True)
    data_inicial = df_sorted_data.iloc[0, 11]
    data_final = df_sorted_data.iloc[-1, 11]

    print(df_sorted_data.tail(20))

    # Formatando as datas no formato (dia/mês/ano)
    data_inicial_formatada = data_inicial.strftime('%d/%m/%Y')
    data_final_formatada = data_final.strftime('%d/%m/%Y')

    # Infomora a data inicial e a final do dataframe
    print(f'A série historica começa em {data_inicial_formatada} e termina em {data_final_formatada}')
    return data_inicial, data_final

def concatenaEndereco():

    # Converte as colunas de interesse para strings
    df[['Nome da Rua', 'Numero Rua', 'Bairro', 'Municipio', 'Estado - Sigla']] = df[['Nome da Rua', 'Numero Rua', 'Bairro', 'Municipio', 'Estado - Sigla']].astype(str)
    
    # Concatenar colunas para formar o endereço completo
    df['Endereço'] = df[['Nome da Rua', 'Numero Rua', 'Bairro', 'Municipio', 'Estado - Sigla']].agg(', '.join, axis=1)
    
    return df

#def salvaDfCsv():
    # salva o data frame df_analise
    #df.to_csv('C:/python/senai/Combustivel/teste/arquivo_teste_gasolina.csv', index=False)

#def salvadfExcel():
    # salva o data frame df_analise
    #df.to_excel('C:/python/senai/Combustivel/teste/arquivo_teste_gasolina.xlsx', index=False)

def mediaVendaMunicipiosProduto():

    # Cria uma dataframe que contenham valores especificos na coluna 'Municipio' e que calcule a média por valor de venda 
    df_cidade = df[df['Municipio'].isin(['BOTUCATU', 'BAURU', 'AVARE', 'SAO PAULO']) & (df['Produto'] == 'GASOLINA')]
    df_mais_baratos = df_cidade.groupby(['Municipio', 'Produto'])['Valor de Venda'].mean().sort_values(ascending=True)
    df_mais_baratos = df_mais_baratos.reset_index()
    df_mais_baratos = df_mais_baratos.rename(columns={'Valor de Venda': 'Média do Valor de Venda (R$)'})
    print(f"\n Municípios em ordem crescente da Média do Valor de venda: \n\n {df_mais_baratos.head(5)}")
    
def mediaVendaMunicipiosProdutoDataInteresse():

    df_cidade = df[df['Municipio'].isin(['BOTUCATU', 'BAURU', 'AVARE', 'SAO PAULO']) & (df['Produto'] == 'GASOLINA')]
    df_cidade = df_cidade[(df_cidade['Data da Coleta'] >= (pd.to_datetime('10/05/2004', dayfirst=True))) & (df_cidade['Data da Coleta'] <= (pd.to_datetime ('29/06/2004', dayfirst=True))) ]
    df_mais_baratos = df_cidade.groupby(['Municipio', 'Produto'])['Valor de Venda'].mean().sort_values(ascending=True)
    df_mais_baratos = df_mais_baratos.reset_index()
    df_mais_baratos = df_mais_baratos.rename(columns={'Valor de Venda': 'Média do Valor de Venda (R$)'})
    print(df_mais_baratos.head(5))
    print(df_mais_baratos.describe())

def top5BaratosHistorico():

    df_cidade = df[(df['Municipio'] == 'BOTUCATU') & (df['Produto'] == 'GASOLINA')]
    df_mais_baratos = df_cidade.groupby(['Municipio', 'Produto', 'Revenda', 'Bandeira', 'Endereço'])['Valor de Venda'].mean().sort_values(ascending=True)
    df_mais_baratos = df_mais_baratos.reset_index()
    df_mais_baratos = df_mais_baratos.rename(columns={'Valor de Venda': 'Média do Valor de Venda (R$)'})
    print(df_mais_baratos.head(5))
    print(df_mais_baratos.describe())

   
def top5BaratosDataInteresse():

    df_cidade = df[(df['Municipio'] == 'BOTUCATU') & (df['Produto'] == 'GASOLINA')]
    df_cidade = df_cidade[(df_cidade['Data da Coleta'] >= (pd.to_datetime('10/05/2004', dayfirst=True))) & (df_cidade['Data da Coleta'] <= (pd.to_datetime ('29/06/2004', dayfirst=True))) ]
    df_mais_baratos = df_cidade.groupby(['Municipio', 'Produto', 'Revenda', 'Bandeira', 'Endereço'])['Valor de Venda'].mean().sort_values(ascending=True)
    df_mais_baratos = df_mais_baratos.reset_index()
    df_mais_baratos = df_mais_baratos.rename(columns={'Valor de Venda': 'Média do Valor de Venda (R$)'})
    print(df_mais_baratos.head(5))
    print(df_mais_baratos.describe())