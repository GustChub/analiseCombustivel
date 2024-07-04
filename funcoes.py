# Neste modulo são definidas as funções utilizadas no codigo main
import os
import unidecode
import pandas as pd
from datetime import datetime

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
    
    return data_inicial, data_final, data_inicial_formatada, data_final_formatada

def coletar_periodo_usuario(data_inicial, data_final, data_inicial_formatada, data_final_formatada):

    while True:
        try:
            # Solicita ao usuário que insira a data inicial e final no formato correto
            data_inicial_usuario = input(f"Digite a data inicial do periodo de analise (dd/mm/yyyy) posterior a {data_inicial_formatada}: ").strip()
            data_final_usuario = input(f"Digite a data final do periodo de analise (dd/mm/yyyy) anterior a {data_final_formatada}: ").strip()
            
            # Converte as datas para o formato datetime
            data_inicial_usuario_dt = datetime.strptime(data_inicial_usuario, '%d/%m/%Y')
            data_final_usuario_dt = datetime.strptime(data_final_usuario, '%d/%m/%Y')
            
            # Verifica se as datas estão dentro do período válido
            if data_inicial_usuario_dt < data_inicial or data_final_usuario_dt > data_final:
                raise ValueError(f"As datas devem estar entre {data_inicial.strftime('%d/%m/%Y')} e {data_final.strftime('%d/%m/%Y')}.")
            
            if data_inicial_usuario_dt > data_final_usuario_dt:
                raise ValueError("A data inicial deve ser anterior ou igual à data final.")
            
            # Se as datas forem válidas, retorna-as
            return data_inicial_usuario_dt, data_final_usuario_dt
        
        except ValueError as e:
            # Imprime a mensagem de erro e continua o loop
            print(f"Erro: {e}. Por favor, tente novamente.")

def coletar_combustivel():
    combustiveis_validos = df_limpo['Produto'].unique().tolist()
    
    while True:
        try:
            combustivel = input(f"Escreva um combustível desejado - {combustiveis_validos}: ").strip().upper()
            
            if combustivel not in combustiveis_validos:
                raise ValueError("Combustível inválido. Por favor, insira um combustível válido.")
            
            return combustivel
        
        except ValueError as e:
            print(e)


def coletar_cidades():
    # Obtém a lista de cidades possíveis a partir do DataFrame
    cidades_possiveis = df_limpo['Municipio'].unique().tolist()
    
    # Lista para armazenar as cidades válidas inseridas pelo usuário
    cidades = []

    while True:
        try:
            # Solicita ao usuário que insira o nome de uma cidade , retira espaços da entrada e converte para maiúsculas.
            cidade = input("\nDigite o nome da cidade (ou aperte Enter para adicionar outra, ou deixe em branco e aperte Enter para finalizar):\n ").strip().upper()
            
            # Normaliza a entrada do usuário: remove acentos e substitui 'Ç' por 'C'
            cidade_normalizada = unidecode.unidecode(cidade).replace('Ç', 'C')
            
            # Verifica se a entrada está vazia para finalizar a coleta
            if cidade_normalizada == "":
                break
            
            # Verifica se a cidade inserida está na lista de cidades possíveis
            cidades_possiveis_normalizadas = [unidecode.unidecode(c).replace('ç', 'c').upper() for c in cidades_possiveis]
            if cidade_normalizada not in cidades_possiveis_normalizadas:
                raise ValueError(f"\n'{cidade}' não é uma cidade válida. Por favor, insira uma cidade válida.\n")
            
            # Adiciona a cidade à lista
            cidades.append(cidade_normalizada)
        
        except ValueError as e:
            # Imprime a mensagem de erro e continua o loop
            print(e)
    
    return cidades

def mediaVendaMunicipiosProduto(cidades, combustivel):

    # Cria uma série booleana para as cidades
    cidades_selecionadas = df_limpo['Municipio'].isin(cidades)
    
    # Cria uma série booleana para o produto
    produto_selecionado = df_limpo['Produto'] == combustivel
    
    # Combina as duas condições
    condicao = cidades_selecionadas & produto_selecionado
    
    # Aplica a condição ao DataFrame
    df_cidade = df_limpo[condicao]
    
    # Calcula a média por valor de venda
    df_mais_baratos = df_cidade.groupby(['Municipio', 'Estado - Sigla', 'Produto'])['Valor de Venda'].mean().sort_values(ascending=True)
    df_mais_baratos = df_mais_baratos.reset_index()
    df_mais_baratos = df_mais_baratos.rename(columns={'Valor de Venda': 'Média do Valor de Venda (R$)', 'Estado - Sigla': 'Estado'})
    
    # Imprime o resultado
    print(f"\n Municípios em ordem crescente da Média do Valor de venda para toda série histórica: \n\n {df_mais_baratos.head(5)}")

    
def mediaVendaMunicipiosProdutoDataInteresse(cidades, combustivel, data_inicial_usuario_dt, data_final_usuario_dt):
    # Cria uma série booleana para as cidades
    cidades_selecionadas = df_limpo['Municipio'].isin(cidades)
    
    # Cria uma série booleana para o produto
    produto_selecionado = df_limpo['Produto'] == combustivel
    
    # Combina as duas condições
    condicao = cidades_selecionadas & produto_selecionado
    
    # Aplica a condição ao DataFrame
    df_cidade = df_limpo[condicao]
     
    # Filtra por data de interesse
    df_cidade = df_cidade[(df_cidade['Data da Coleta'] >= pd.to_datetime(data_inicial_usuario_dt, dayfirst=True)) & 
                          (df_cidade['Data da Coleta'] <= pd.to_datetime(data_final_usuario_dt, dayfirst=True))]
    
    # Calcula a média por valor de venda
    df_mais_baratos = df_cidade.groupby(['Municipio', 'Produto'])['Valor de Venda'].mean().sort_values(ascending=True)
    df_mais_baratos = df_mais_baratos.reset_index()
    df_mais_baratos = df_mais_baratos.rename(columns={'Valor de Venda': 'Média do Valor de Venda (R$)'})
    
    # Imprime o resultado
    print(f"\n Municípios em ordem crescente da Média do Valor de venda, analisados para o periodo de {data_inicial_usuario_dt} a {data_final_usuario_dt}:\n {df_mais_baratos.head(5)}")
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