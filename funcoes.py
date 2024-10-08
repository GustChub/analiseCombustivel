# Neste modulo são definidas as funções utilizadas no codigo main
import os
import unidecode
import pandas as pd
import xlsxwriter
import gc
from datetime import datetime

# define função para concatenar os dados semestrais e salvar um arquivo concatenado.
def concatenaDados():
    
    # Define as variaveis globais
    global arquivo_saida
    global diretorio_salvar
    global df
   
    # Define o caminho para a pasta onde deseja salvar o arquivo CSV
    diretorio_salvar = os.path.join(os.path.dirname(__file__), 'dados', 'csv_concatenado')
    arquivo_saida = os.path.join(diretorio_salvar, 'dados_concatenados.csv')
   
    # Verifica se o diretório existe e cria se não existir
    if not os.path.exists(diretorio_salvar):
        os.makedirs(diretorio_salvar)
    
    # Verifica se o arquivo de saída já existe, se existir lê o arquivo e o salva na memoria como dataframe "df"
    if os.path.exists(arquivo_saida):
        print(f"O arquivo {arquivo_saida} já existe. Carregando o DataFrame a partir deste arquivo.")
        df = pd.read_csv(arquivo_saida, delimiter=',', low_memory= False)
        print(f"DataFrame carregado com sucesso. Total de linhas: {len(df)}")

        return df
           
   # Lista os arquivos dentro da pasta de origem dos CSVs
    diretorio_principal = os.path.dirname(__file__)
    pasta_csv_semestrais = os.path.join(diretorio_principal, 'dados', 'csv_semestrais')

    if not os.path.exists(pasta_csv_semestrais): #Verifica/Cria a pasta csv_semestrais
        os.makedirs(pasta_csv_semestrais)
        print(f"Salve os arquivos semestrais.csv na pasta {pasta_csv_semestrais} e reinicie o Script")
        exit()

    arquivos = os.listdir(pasta_csv_semestrais)
    print("Arquivos na pasta: ", arquivos)

    # Lista para armazenar os DataFrames carregados
    df_base = []

    # Itera sobre os arquivos na pasta
    for arquivo in os.listdir(pasta_csv_semestrais):
        if arquivo.endswith(".csv"):
            print("Arquivo analisado:", arquivo)
            caminho = os.path.join(pasta_csv_semestrais, arquivo)
            print("Caminho do arquivo:", caminho)
            
            # Define as colunas que você deseja carregar
            colunas_carregar = [
                'Regiao - Sigla', 'Estado - Sigla', 'Municipio', 'Revenda', 'CNPJ da Revenda',
                'Nome da Rua', 'Numero Rua', 'Bairro', 'Produto', 'Data da Coleta', 
                'Valor de Venda', 'Bandeira'
            ]
            
            # Carrega o arquivo CSV em chunks, apenas com as colunas especificadas
            df_chunk = pd.read_csv(caminho, delimiter=';', usecols=colunas_carregar, 
                                low_memory=False, encoding_errors="ignore", chunksize=100000, 
                                dtype=str)  # Carregar tudo como string
            
            for chunk in df_chunk:
                # Corrige os valores da coluna 'Valor de Compra'
                chunk['Valor de Venda'] = chunk['Valor de Venda'].str.replace(',', '.').astype(float)
                
                # Cria a nova coluna "Endereço" concatenando as colunas especificadas
                chunk['Endereço'] = chunk['Nome da Rua'] + ', ' + chunk['Numero Rua'] + ', ' + chunk['Bairro'] + ', ' + chunk['Municipio'] + ', ' + chunk['Estado - Sigla']
                
                # Remove as colunas que não são mais necessárias
                chunk = chunk.drop(columns=['Nome da Rua', 'Numero Rua', 'Bairro'])
                
                # Adiciona o chunk ao DataFrame base
                df_base.append(chunk)

    
    # Concatena todos os chunks em um único DataFrame
    df = pd.concat(df_base, ignore_index=True)

    # Libera a memória dos DataFrames intermediários
    del df_chunk
    del df_base

    # Método chamado para realizar a limpeza da memoria ram, limpando resquicios que as variaveis deletadas possam ter deixado.
    gc.collect()

    #df = pd.concat(df_base, ignore_index=True)
    print("\nBase de dados criada")
    print(f"Total de linhas do DataFrame: {len(df)} \nSalvando arquivo concatenado, aguarde") #\n\n{df.describe()}, \n\n{df.info()} ")

    # Salva o DataFrame em um arquivo CSV na pasta especificada
    df.to_csv(arquivo_saida, index=False)
    print(f"\nDataFrame salvo como CSV em: {arquivo_saida}")

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

# Define a função que retona informações sobre o dataframe "df_limpo"
def infoDFLimpo(df_limpo):

    # Exibe informações sobre o DataFrame antes do tratamento
    print("\nInformações do DataFrame depois do tratamento:\n")
    print(df_limpo.info())
    
def convertDate():

    # Converte a coluna 'Data da Coleta' para o formato de Data 
    df['Data da Coleta'] = pd.to_datetime(df['Data da Coleta'], dayfirst=True, errors='coerce')

    return df

def tratamentoDados():

    global df_limpo

    # Imprime informação dos tipos de dadados de cada coluna do daframe, antes do tratamento.
    infoDF()
    
    # Informa quais os tratamento de dados serão aplicados.
    print("\nIniciando o tratamento dos dados, aguarde.")
    
    # Chama o método que converte a coluna "Data da Coleta" para valores de data.
    convertDate()
        
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

    global data_inicial, data_final, data_inicial_formatada, data_final_formatada

    # Organiza o dataframe em ordem crescente de data e seleciona as celulas com data inicia e a final do dataframe.
    df_sorted_data = df_limpo.sort_values(by='Data da Coleta', ascending= True)
    data_inicial = df_sorted_data.iloc[0, 6] 
    data_final = df_sorted_data.iloc[-1, 6] 
    
    # Formatando as datas no formato (dia/mês/ano)
    data_inicial_formatada = data_inicial.strftime('%d/%m/%Y')
    data_final_formatada = data_final.strftime('%d/%m/%Y')

    # Infomora a data inicial e a final do dataframe
    print(f'\nA série historica começa em {data_inicial_formatada} e termina em {data_final_formatada}')
    
    return data_inicial, data_final, data_inicial_formatada, data_final_formatada

# Definir a classe EstatisticaBasica que herda atributos da clase .describe do pandas
class EstatisticaBasica:
    def __init__(self, df):

        self.df = df  # Armazena o DataFrame fornecido na instância da classe

    def describe_pt(self):
        # Gera as estatísticas descritivas utilizando o método describe do pandas
        desc = self.df.describe()
        
        # Traduzir os índices das estatísticas descritivas para português
        translation = {
            'count': 'Contagem das linhas:',
            'mean': 'Média da consulta:',
            'std': 'Desvio Padrão dos valores das médias da consulta:',
            'min': 'Mínimo da consulta:',
            '25%': '25% dos valores da consulta estão abaixo de:',
            '50%': '50% dos valores da consulta estão abaixo de:',
            '75%': '75% dos valores da consulta estão abaixo de:',
            'max': 'Máximo da consulta:'
        }

        # Formatando os valores para usar vírgula em vez de ponto decimal
        formatted_desc = desc.apply(lambda x: f"{x:.6f}".replace('.', ','))
        formatted_desc.rename(index=translation, inplace=True)

        return formatted_desc  # Retorna o DataFrame com as estatísticas descritivas formatadas

def coletarPeriodoUsuario():

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

def coletarCombustivel():

    # Cria uma serie com so valores únicos da coluna combustível
    combustiveis_validos = df_limpo['Produto'].unique().tolist()
    
    while True:

        try:
            # Solicita ao usuário o combustível de interesse
            combustivel = input(f"Escreva um combustível desejado - {combustiveis_validos}: ").strip().upper()
            
            # Previne que o usuário deixe o campo vazio.
            if len(combustivel) == 0:
                raise ValueError("\nPor favor insira um Combustível.\n")
            
            # Verifica se o combustível escolhido existe na serie de combustíveis validos
            if combustivel not in combustiveis_validos:
                raise ValueError("Combustível inválido. Por favor, insira um combustível válido.")
            
            return combustivel
        
        except ValueError as e:
            # Imprime a mensagem de erro e continua o loop
            print(e)


def coletarCidades():
    
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

def coletarUmaCidade():

    # Obtém a lista de cidades possíveis a partir do DataFrame
    cidades_possiveis = df_limpo['Municipio'].unique().tolist()
    
    while True:
        try:
            # Solicita ao usuário que insira o nome de uma cidade, retira espaços da entrada e converte para maiúsculas.
            cidade = input("\nDigite o nome da cidade: ").strip().upper()

            # Normaliza a entrada do usuário: remove acentos e substitui 'Ç' por 'C'
            cidade_normalizada = unidecode.unidecode(cidade).replace('Ç', 'C')
            
            # Verifica se a cidade inserida está na lista de cidades possíveis
            cidades_possiveis_normalizadas = [unidecode.unidecode(c).replace('ç', 'c').upper() for c in cidades_possiveis]
            if cidade_normalizada not in cidades_possiveis_normalizadas:
                raise ValueError(f"\n'{cidade}' não é uma cidade válida. Por favor, insira uma cidade válida.\n")
            
            # Se a cidade for válida, retorna a cidade normalizada
            return cidade_normalizada
        
        except ValueError as e:
            # Imprime a mensagem de erro e continua o loop
            print(e)

def exportarParaExcel(df_mais_baratos, estatisticas_basicas, titulo_resultado):

    try:
        # Pergunta se o usuário deseja salvar a consulta
        deseja_salvar_consulta = input("\nDeseja exportar a consulta? S/N: ").strip().upper()
        
        if deseja_salvar_consulta == "S":

            # Criar o diretório dados/consulta se não existir
            caminho_pasta = os.path.dirname(__file__) + '\dados\consulta'

            if not os.path.exists(caminho_pasta):
                os.makedirs(caminho_pasta)
            
            # Nome do arquivo com a data e hora atual
            nome_arquivo = datetime.now().strftime('%Y%m%d_%H%M%S') + '.xlsx'
            caminho_arquivo = os.path.join(caminho_pasta, nome_arquivo)
            
            # Criar um escritor de Excel usando pandas ExcelWriter
            with pd.ExcelWriter(caminho_arquivo, engine='xlsxwriter') as writer:
                # Adicionar abas
                df_mais_baratos.to_excel(writer, sheet_name='Consulta combustível', index=False, startrow=2)
                estatisticas_basicas.describe_pt().to_excel(writer, sheet_name='Estatísticas descritivas', startrow=2)
                
                # Escrever a informação sobre o que a consulta se refere na primeira linha de cada aba
                worksheet1 = writer.sheets['Consulta combustível']
                worksheet1.write(0, 0, titulo_resultado)
                
                worksheet2 = writer.sheets['Estatísticas descritivas']
                worksheet2.write(0, 0, "Estatística descritiva da consulta")
            
            print(f'Dados exportados com sucesso para: {caminho_arquivo}')

        # Informa que o arquivo não foi exportado e finaliza o loop.
        elif deseja_salvar_consulta == "N":
            print("Consulta não exportada.")

        # Informa que o arquivo não foi exportado e finaliza o loop.
        else:
            print("Opção inválida. Consulta não exportada.")
    
    except Exception as e:
        # Imprime a mensagem de erro e continua o loop
        print(f"Ocorreu um erro ao exportar os dados para Excel: {str(e)}")

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
    df_mais_baratos = df_mais_baratos.rename(columns={'Valor de Venda': 'Média do Valor de Venda (R$/l)', 'Estado - Sigla': 'Estado'})

    # Cria uma instância da classe EstatisticaBasica imprime as estatísticas descritivas em português
    estatisticas_basicas = EstatisticaBasica(df_mais_baratos['Média do Valor de Venda (R$/l)'])

    # Formata os valores para usar vírgula em vez de ponto decimal em df_mais_baratos
    df_mais_baratos['Média do Valor de Venda (R$/l)'] = df_mais_baratos['Média do Valor de Venda (R$/l)'].apply(lambda x: f"{x:.6f}".replace('.', ','))
    
    # Imprime o resultado
    print(f"\nMunicípios em ordem crescente da Média do Valor de venda para toda a série histórica de {data_inicial_formatada} a {data_final_formatada}:\n\n {df_mais_baratos.head(5)}")

    # imprime as estatísticas descritivas do resultado
    print(f"\nEstatistíca descritiva da consulta:\n\n{estatisticas_basicas.describe_pt()}")

    # Cria o titulo do arquivo de resultados para ser salvo
    titulo_resultado = f"Municípios em ordem crescente da Média do Valor de venda para toda a série histórica de {data_inicial_formatada} a {data_final_formatada}"

    # Pergunta se o usuário deseja salvar a consulta
    exportarParaExcel(df_mais_baratos, estatisticas_basicas, titulo_resultado)

    
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
    df_mais_baratos = df_cidade.groupby(['Municipio', 'Estado - Sigla', 'Produto'])['Valor de Venda'].mean().sort_values(ascending=True)
    df_mais_baratos = df_mais_baratos.reset_index()
    df_mais_baratos = df_mais_baratos.rename(columns={'Valor de Venda': 'Média do Valor de Venda (R$/l)', 'Estado - Sigla': 'Estado'})

    # Cria uma instância da classe EstatisticaBasica imprime as estatísticas descritivas em português
    estatisticas_basicas = EstatisticaBasica(df_mais_baratos['Média do Valor de Venda (R$/l)'])

    # Formata os valores para usar vírgula em vez de ponto decimal em df_mais_baratos
    df_mais_baratos['Média do Valor de Venda (R$/l)'] = df_mais_baratos['Média do Valor de Venda (R$/l)'].apply(lambda x: f"{x:.6f}".replace('.', ','))
    
    # Imprime o resultado
    print(f"\n Municípios em ordem crescente da Média do Valor de venda, analisados para o período de {data_inicial_usuario_dt.strftime('%d/%m/%Y')} a {data_final_usuario_dt.strftime('%d/%m/%Y')}:\n\n {df_mais_baratos.head(5)}\n")
    
    # imprime as estatísticas descritivas do resultado
    print(f"\nEstatistíca descritiva da consulta:\n\n{estatisticas_basicas.describe_pt()}")

    # Cria o titulo do arquivo de resultados para ser salvo
    titulo_resultado = f"Municípios em ordem crescente da Média do Valor de venda, analisados para o período de {data_inicial_usuario_dt.strftime('%d/%m/%Y')} a {data_final_usuario_dt.strftime('%d/%m/%Y')}"

    # Pergunta se o usuário deseja salvar a consulta
    exportarParaExcel(df_mais_baratos, estatisticas_basicas, titulo_resultado)

def top5BaratosHistorico(cidade, combustivel):
    # Cria uma série booleana para a cidade
    cidade_selecionada = df_limpo['Municipio'] == cidade
    
    # Cria uma série booleana para o produto
    produto_selecionado = df_limpo['Produto'] == combustivel
    
    # Combina as duas condições
    condicao = cidade_selecionada & produto_selecionado
    
    # Aplica a condição ao DataFrame
    df_cidade = df_limpo[condicao]
    
    # Calcula a média por valor de venda
    df_mais_baratos = df_cidade.groupby(['Produto', 'Revenda', 'Bandeira', 'Endereço'])['Valor de Venda'].mean().sort_values(ascending=True)
    df_mais_baratos = df_mais_baratos.reset_index()
    df_mais_baratos = df_mais_baratos.rename(columns={'Valor de Venda': 'Média do Valor de Venda (R$/l)'})

    # Cria uma instância da classe EstatisticaBasica imprime as estatísticas descritivas em português
    estatisticas_basicas = EstatisticaBasica(df_mais_baratos['Média do Valor de Venda (R$/l)'])

    # Formata os valores para usar vírgula em vez de ponto decimal em df_mais_baratos
    df_mais_baratos['Média do Valor de Venda (R$/l)'] = df_mais_baratos['Média do Valor de Venda (R$/l)'].apply(lambda x: f"{x:.6f}".replace('.', ','))
    
    # Imprime o resultado
    print(f"\nPostos em ordem crescente da Média do Valor de venda para toda a série histórica de {data_inicial_formatada} a {data_final_formatada}:\n\n{df_mais_baratos.head(5)}\n")
    
    # imprime as estatísticas descritivas do resultado
    print(f"\nEstatistíca descritiva da consulta:\n\n{estatisticas_basicas.describe_pt()}")

    # Cria o titulo do arquivo de resultados para ser salvo
    titulo_resultado = f"Postos com o preço médio do combustivel mais baratos para a cidade de interesse em toda a série histórica {data_inicial_formatada} a {data_final_formatada}"

    # Pergunta se o usuário deseja salvar a consulta
    exportarParaExcel(df_mais_baratos, estatisticas_basicas, titulo_resultado) 
   
def top5BaratosDataInteresse(cidade, combustivel, data_inicial_usuario_dt, data_final_usuario_dt):
    # Cria uma série booleana para a cidade
    cidade_selecionada = df_limpo['Municipio'] == cidade
    
    # Cria uma série booleana para o produto
    produto_selecionado = df_limpo['Produto'] == combustivel
    
    # Combina as duas condições
    condicao = cidade_selecionada & produto_selecionado
    
    # Aplica a condição ao DataFrame
    df_cidade = df_limpo[condicao]
    
    # Filtra por data de interesse
    df_cidade = df_cidade[(df_cidade['Data da Coleta'] >= pd.to_datetime(data_inicial_usuario_dt, dayfirst=True)) & 
                          (df_cidade['Data da Coleta'] <= pd.to_datetime(data_final_usuario_dt, dayfirst=True))]
    
    # Calcula a média por valor de venda
    df_mais_baratos = df_cidade.groupby(['Produto', 'Revenda', 'Bandeira', 'Endereço'])['Valor de Venda'].mean().sort_values(ascending=True)
    df_mais_baratos = df_mais_baratos.reset_index()
    df_mais_baratos = df_mais_baratos.rename(columns={'Valor de Venda': 'Média do Valor de Venda (R$/l)'})
    
    # Cria uma instância da classe EstatisticaBasica imprime as estatísticas descritivas em português
    estatisticas_basicas = EstatisticaBasica(df_mais_baratos['Média do Valor de Venda (R$/l)'])

    # Formata os valores para usar vírgula em vez de ponto decimal em df_mais_baratos
    df_mais_baratos['Média do Valor de Venda (R$/l)'] = df_mais_baratos['Média do Valor de Venda (R$/l)'].apply(lambda x: f"{x:.6f}".replace('.', ','))

    # Imprime o resultado
    print(f"\nPostos com o preço médio do combustivel mais baratos para o período {data_inicial_usuario_dt.strftime('%d/%m/%Y')} a {data_final_usuario_dt.strftime('%d/%m/%Y')}:\n{df_mais_baratos.head(5)}\n")
    
    # imprime as estatísticas descritivas do resultado
    print(f"\nEstatistíca descritiva da consulta:\n\n{estatisticas_basicas.describe_pt()}")

    # Cria o titulo do arquivo de resultados para ser salvo
    titulo_resultado = f"Postos com o preço médio do combustivel mais baratos para a cidade e período de interesse {data_inicial_usuario_dt.strftime('%d/%m/%Y')} a {data_final_usuario_dt.strftime('%d/%m/%Y')}"

    # Pergunta se o usuário deseja salvar a consulta
    exportarParaExcel(df_mais_baratos, estatisticas_basicas, titulo_resultado)
    