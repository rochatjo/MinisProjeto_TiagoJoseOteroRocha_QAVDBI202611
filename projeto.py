import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#1. Carregando os dados
df = pd.read_csv('E:\SCTEC\CarreiraTech_TrilhaAnalisedeDados\MiniProjeto\BaseVarejo.csv')
print(df.head())

# 2. Identificando colunas fantasma (geradas por delimitadores extras no CSV)
colunas_fantasmas = [col for col in df.columns if 'Unnamed' in col]
print(f"Colunas fantasmas encontradas: {colunas_fantasmas}")

# Remove as colunas fantasmas para não poluírem a análise de nulos reais
df_ajustado = df.dropna(how='all', axis=1)

print("\n--- VALORES NULOS POR COLUNA (REAL) ---")
print(df_ajustado.isnull().sum())

print("\n--- DUPLICATAS ---")
print(f"Total de linhas 100% duplicadas: {df_ajustado.duplicated().sum()}")

print("\n--- POSSÍVEIS INCONSISTÊNCIAS ---")
# Verificando se há categorias vazias ou com espaços em branco na coluna PR_CAT
print("Categorias únicas de produtos:")
print(df_ajustado['PR_CAT'].unique())

#Código Limpeza mínima
# Verificando se a conversão de data gera algum erro (datas inválidas viram NaT)
datas_convertidas = pd.to_datetime(df_ajustado['DATA'], format='%d/%m/%Y', errors='coerce')
print(f"Datas inválidas encontradas: {datas_convertidas.isna().sum()}")

#Remoção preventiva de colunas fantasma criadas por ponto e vírgula extras (;;;;)
df = df.dropna(how='all', axis=1)

print(f"Dimensões originais do DataFrame: {df.shape[0]} linhas e {df.shape[1]} colunas.\n")

# --- ETAPA 1: TRATAMENTO DE VALORES NULOS ---
# Verificando a quantidade de nulos antes do tratamento
print("Nulos antes do tratamento:")
print(df.isnull().sum())

#Decisão: Remoção das linhas com valores nulos (Justificativa abaixo)
df_limpo = df.dropna()


# --- ETAPA 2: ELIMINAÇÃO DE DUPLICATAS RELEVANTES ---
# Verificando duplicatas exatas considerando todas as colunas reais de transação
duplicadas_antes = df_limpo.duplicated().sum()
print(f"\nLinhas duplicadas exatas encontradas: {duplicadas_antes}")

#Removendo as duplicatas e mantendo a primeira ocorrência
df_limpo = df_limpo.drop_duplicates()


# --- ETAPA 3: AJUSTE DOS TIPOS DE DADOS ---
# Convertendo a coluna DATA de texto (object) para datetime
df_limpo['DATA'] = pd.to_datetime(df_limpo['DATA'], format='%d/%m/%Y')

# Verificando o resultado final dos tipos de dados
print("\nTipos de dados finais das colunas:")
print(df_limpo.dtypes)

print(f"\nDimensões finais após a limpeza: {df_limpo.shape[0]} linhas.")

#3.Gerando estatísticas

#Limpeza rápida (remover valores nulos na coluna de filhos para não distorcer o cálculo)
df_limpo = df.dropna(subset=['CL_FHL'])

#Calcular cada estatística descritiva individualmente
media = df_limpo['CL_FHL'].mean()
mediana = df_limpo['CL_FHL'].median()
desvio_padrao = df_limpo['CL_FHL'].std()
maximo = df_limpo['CL_FHL'].max()
minimo = df_limpo['CL_FHL'].min()
contagem = df_limpo['CL_FHL'].count()

#Como a moda pode retornar mais de um valor (caso haja empate), pegamos o primeiro valor encontrado [.iloc[0]]
moda = df_limpo['CL_FHL'].mode().iloc[0]

#Exibir o relatório formatado
print("--- ESTATÍSTICAS DESCRITIVAS: FILHOS DO CLIENTE (CL_FHL) ---")
print(f"Média:         {media:.2f}")
print(f"Mediana:       {mediana:.2f}")
print(f"Desvio Padrão: {desvio_padrao:.2f}")
print(f"Moda:          {int(moda)}")
print(f"Mínimo:        {int(minimo)}")
print(f"Máximo:        {int(maximo)}")
print(f"Contagem:      {int(contagem)} clientes válidos")


#4. Padrões de grupamento

print("\n--- MATRIZ DE COMPRAS: CATEGORIA VS GÊNERO ---")
# Criando uma tabela dinâmica (Pivot Table)
tabela_dinamica = pd.pivot_table(
    df, 
    index='PR_CAT',       # O que vai nas linhas
    columns='CL_GENERO',  # O que vai nas colunas
    aggfunc='size',       # Função de agregação (contagem de registros)
    fill_value=0          # Substitui valores nulos por 0 caso um gênero nunca tenha comprado uma categoria
)

# Adiciona uma coluna de Total para facilitar a ordenação e análise
tabela_dinamica['Total'] = tabela_dinamica['F'] + tabela_dinamica['M']
print(tabela_dinamica.sort_values(by='Total', ascending=False))

#Visualisação Gráfico de Barras utilizando Seaborn

plt.figure(figsize=(10, 6))
# Criando um gráfico de barras cruzando Categoria (X) e Contagem, segmentado por Gênero (hue)
sns.countplot(data=df, x='PR_CAT', hue='CL_GENERO', order=df['PR_CAT'].value_counts().index)

plt.title('Volume de Compras por Categoria e Gênero')
plt.xlabel('Categoria do Produto')
plt.ylabel('Quantidade de Itens Comprados')
plt.xticks(rotation=45) # Rotaciona os nomes das categorias para não embolar
plt.tight_layout()
plt.show()

