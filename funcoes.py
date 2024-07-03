# Neste modulo são definidas as funções utilizadas no codigo main
import os
import pandas as pd

# define função para concatenar os dados semestrais e salvar um arquivo concatenado.
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
    
    # Verifica se o arquivo de saída já existe, se existir lê o arquivo e  o salva na memoria como dataframe "df"
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
           caminho = os.path.join(pasta_csv_semestrais, arquivo)
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
# Define função para atualizar o banco de dados caso seja inserido algum dado semestral novo.
def atualizaDados():

    # Verifica se o arquivo de saída já existe e remove o mesmo
    if os.path.exists(arquivo_saida):
        os.remove(arquivo_saida)

        # Atualiza os dados através do metodo concatenaDados
        return concatenaDados()

# Define a função que retona informações sobre o dataframe "df"
def infoDF():

    # Exibe informações sobre o DataFrame antes do tratamento
    print("\nInformações do DataFrame antes do tratamento:\n")
    print(df.info())

def infoDFLimpo(df_limpo):

    # Exibe informações sobre o DataFrame antes do tratamento
    print("\nInformações do DataFrame depois do tratamento:\n")
    print(df_limpo.info())
    
def convertValorFloat(): 

    # Converte a coluna 'Valor de Venda' para float
    df['Valor de Venda'] = df['Valor de Venda'].str.replace(',', '.').astype(float)

    return df

def convertDate():

    # Converte a coluna 'Data da Coleta' para o formato de Data 
    df['Data da Coleta'] = pd.to_datetime(df['Data da Coleta'], dayfirst=True, errors='coerce')

    return df

def concatenaEndereco():

    # Converte as colunas de interesse para strings
    df[['Nome da Rua', 'Numero Rua', 'Bairro', 'Municipio', 'Estado - Sigla']] = df[['Nome da Rua', 'Numero Rua', 'Bairro', 'Municipio', 'Estado - Sigla']].astype(str)
    
    # Concatenar colunas para formar o endereço completo
    df['Endereço'] = df[['Nome da Rua', 'Numero Rua', 'Bairro', 'Municipio', 'Estado - Sigla']].agg(', '.join, axis=1)
    
    return df

def tratamentoDados():

    global df_limpo

    infoDF()
    
    print("""\nIniciando o tratamento dos dados:\n- Conversão da coluna "Valor de Venda para Float"\n- Conversão da coluna "Data da Coleta para Data"\n- Criação da coluna "Endereço"\n- Tratamento das celulas com valores nulos\n""")

    convertValorFloat()

    convertDate()

    concatenaEndereco()
    
    # Realiza o levantamento de valores nulos por coluna antes da limpeza
    colunas_interesse = ['Produto', 'Valor de Venda','Data da Coleta']
    valores_nulos_antes = df[colunas_interesse].isnull().sum().reset_index()
    valores_nulos_antes.columns = ['Coluna', 'Valores Nulos']
    print("Valores nulos antes da limpeza:\n")
    print(valores_nulos_antes)

    # Remove as linhas com valores nulos nas colunas de interesse
    df_limpo = df.dropna(subset=colunas_interesse)

    # Realiza o levantamento de valores nulos por coluna após a limpeza
    valores_nulos_depois = df_limpo[colunas_interesse].isnull().sum().reset_index()
    valores_nulos_depois.columns = ['Coluna', 'Valores Nulos']
    print("\nValores nulos depois da limpeza:\n")
    print(valores_nulos_depois)
    print('\ntratamento dos dados concluído.\n')

    infoDFLimpo(df_limpo)
    
    return df_limpo
  
    
def infoPeriodo():

    # Organiza o dataframe em ordem crescente de data e seleciona as celulas com data inicia e a final do dataframe.
    df_sorted_data = df_limpo.sort_values(by='Data da Coleta', ascending= True)
    data_inicial = df_sorted_data.iloc[0, 11]
    data_final = df_sorted_data.iloc[-1, 11]
    
    # Formatando as datas no formato (dia/mês/ano)
    data_inicial_formatada = data_inicial.strftime('%d/%m/%Y')
    data_final_formatada = data_final.strftime('%d/%m/%Y')

    # Infomora a data inicial e a final do dataframe
    print(f'\nA série historica começa em {data_inicial_formatada} e termina em {data_final_formatada}\n')
    return data_inicial, data_final

def mediaVendaMunicipiosProduto():

    # Cria uma série booleana para as cidades
    cidades_selecionadas = df_limpo['Municipio'].isin(['BOTUCATU', 'BAURU', 'AVARE', 'SAO PAULO'])
    
    # Cria uma série booleana para o produto
    produto_selecionado = df_limpo['Produto'] == 'GASOLINA'
    
    # Combina as duas condições
    condicao = cidades_selecionadas & produto_selecionado
    
    # Aplica a condição ao DataFrame
    df_cidade = df_limpo[condicao]
    
    # Calcula a média por valor de venda
    df_mais_baratos = df_cidade.groupby(['Municipio', 'Produto'])['Valor de Venda'].mean().sort_values(ascending=True)
    df_mais_baratos = df_mais_baratos.reset_index()
    df_mais_baratos = df_mais_baratos.rename(columns={'Valor de Venda': 'Média do Valor de Venda (R$)'})
    
    # Imprime o resultado
    print(f"\n Municípios em ordem crescente da Média do Valor de venda: \n\n {df_mais_baratos.head(5)}")

    
def mediaVendaMunicipiosProdutoDataInteresse():
    # Cria uma série booleana para as cidades
    cidades_selecionadas = df_limpo['Municipio'].isin(['BOTUCATU', 'BAURU', 'AVARE', 'SAO PAULO'])
    
    # Cria uma série booleana para o produto
    produto_selecionado = df_limpo['Produto'] == 'GASOLINA'
    
    # Combina as duas condições
    condicao = cidades_selecionadas & produto_selecionado
    
    # Aplica a condição ao DataFrame
    df_cidade = df_limpo[condicao]
    
    # Filtra por data de interesse
    df_cidade = df_cidade[(df_cidade['Data da Coleta'] >= pd.to_datetime('10/05/2004', dayfirst=True)) & 
                          (df_cidade['Data da Coleta'] <= pd.to_datetime('29/06/2004', dayfirst=True))]
    
    # Calcula a média por valor de venda
    df_mais_baratos = df_cidade.groupby(['Municipio', 'Produto'])['Valor de Venda'].mean().sort_values(ascending=True)
    df_mais_baratos = df_mais_baratos.reset_index()
    df_mais_baratos = df_mais_baratos.rename(columns={'Valor de Venda': 'Média do Valor de Venda (R$)'})
    
    # Imprime o resultado
    print(df_mais_baratos.head(5))
    print(df_mais_baratos.describe())

def top5BaratosHistorico():
    # Cria uma série booleana para a cidade
    cidade_selecionada = df_limpo['Municipio'] == 'BOTUCATU'
    
    # Cria uma série booleana para o produto
    produto_selecionado = df_limpo['Produto'] == 'GASOLINA'
    
    # Combina as duas condições
    condicao = cidade_selecionada & produto_selecionado
    
    # Aplica a condição ao DataFrame
    df_cidade = df_limpo[condicao]
    
    # Calcula a média por valor de venda
    df_mais_baratos = df_cidade.groupby(['Municipio', 'Produto', 'Revenda', 'Bandeira', 'Endereço'])['Valor de Venda'].mean().sort_values(ascending=True)
    df_mais_baratos = df_mais_baratos.reset_index()
    df_mais_baratos = df_mais_baratos.rename(columns={'Valor de Venda': 'Média do Valor de Venda (R$)'})
    
    # Imprime o resultado
    print(df_mais_baratos.head(5))
    print(df_mais_baratos.describe())

   
def top5BaratosDataInteresse():
    # Cria uma série booleana para a cidade
    cidade_selecionada = df_limpo['Municipio'] == 'BOTUCATU'
    
    # Cria uma série booleana para o produto
    produto_selecionado = df_limpo['Produto'] == 'GASOLINA'
    
    # Combina as duas condições
    condicao = cidade_selecionada & produto_selecionado
    
    # Aplica a condição ao DataFrame
    df_cidade = df_limpo[condicao]
    
    # Filtra por data de interesse
    df_cidade = df_cidade[(df_cidade['Data da Coleta'] >= pd.to_datetime('10/05/2004', dayfirst=True)) & 
                          (df_cidade['Data da Coleta'] <= pd.to_datetime('29/06/2004', dayfirst=True))]
    
    # Calcula a média por valor de venda
    df_mais_baratos = df_cidade.groupby(['Municipio', 'Produto', 'Revenda', 'Bandeira', 'Endereço'])['Valor de Venda'].mean().sort_values(ascending=True)
    df_mais_baratos = df_mais_baratos.reset_index()
    df_mais_baratos = df_mais_baratos.rename(columns={'Valor de Venda': 'Média do Valor de Venda (R$)'})
    
    # Imprime o resultado
    print(df_mais_baratos.head(5))
    print(df_mais_baratos.describe())