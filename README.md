# Análise de Preços de Combustíveis utilizando Python e Pandas

Este repositório apresenta um módulo Python desenvolvido para analisar grandes volumes de dados (big data) de preços de combustíveis. Utilizando séries temporais desde 2004, o módulo abrange dados de todo o território nacional, disponibilizados pela ANP (Agência Nacional do Petróleo).

A análise visa fornecer ao usuário informações estatísticas com o objetivo de ajudá-lo a escolher postos com preços mais baixos de combustível em sua cidade. Além disso, permite a comparação de preços entre cidades e a exportação dos resultados em formato .xlsx.

## Instalação

Para começar, clone o repositório e instale as dependências necessárias:

```bash
git clone https://github.com/GustChub/analiseCombustivel
cd analiseCombustivel
pip install pandas xlsxwriter unidecode
```

## Como Usar

1. **Baixe os Dados:**
   - Faça o download dos arquivos .csv semestrais de interesse no site [dados.gov.br](https://dados.gov.br/dados/conjuntos-dados/serie-historica-de-precos-de-combustiveis-e-de-glp).

2. **Organize os Dados:**
   - Coloque os arquivos .csv na pasta `dados/csv_semestrais` do repositório clonado.

3. **Execute o Script:**
   - Execute o arquivo `main.py` no seu ambiente Python.
   - Aguarde o término do tratamento dos dados e escolha a análise desejada.

4. **Exporte os Resultados:**
   - Caso deseje, exporte a consulta realizada. Os arquivos serão gerados na pasta `dados/consulta`.

## Requisitos de Hardware

Para executar o script de análise de preços de combustíveis de forma eficiente, recomenda-se que sua máquina atenda aos seguintes requisitos mínimos:

- Pelo menos 24 GB de memória RAM disponível.

Certifique-se de que sua máquina atende a esses requisitos para garantir um desempenho adequado durante o processamento dos dados.