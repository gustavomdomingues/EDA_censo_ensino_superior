import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import missingno as msno
from yellowbrick.features import PCA

@st.cache()
def ler_arquivo(caminho):
	#arquivo = pd.read_csv(caminho, encoding='latin')
	df_chunk = pd.read_csv("./DM_ALUNO_LIMPO.csv", encoding='latin', chunksize=300000)
	chunk_lista = []
	for chunk in df_chunk:
		chunk_lista.append(chunk)
		break
	df = pd.concat(chunk_lista)
	return df

#@st.cache()
#def ler_arquivo_completo():
#	df_chunk = pd.read_csv("./dados_2016/DM_ALUNO.CSV", sep="|", encoding='latin', chunksize=400000)
#	chunk_lista = []
#	for chunk in df_chunk:
#		chunk_lista.append(chunk)
#		break
#	df = pd.concat(chunk_lista)
#	return df

def main():

	pagina = st.sidebar.selectbox("Escolha uma opção:", ['Introdução', 'Resultados', 'Ferramentas Utilizadas','Análise Geral', 'Análise Individual', 'Análise Desvinculados/Concluintes','PCA', 'Possíveis melhorias'])

	st.header('Gustavo Domingues')

	if (pagina == 'Introdução'):

		st.markdown('### O objetivo deste projeto é explorar a base de dados do censo da educação superior de 2018 feito pelo Inep.')
		st.write(' --- ')
		st.markdown('__Utilize o menu à esquerda para navegar por diferentes partes do projeto.__')

		st.write('As estapas de trabalho foram as seguintes:')

		st.write('1. Ler detalhadamente o dicionários de dados.')
		st.write('2. Aprender e aplicar a leitura de grandes arquivos no Pandas.')
		st.write('3. Analisar as estatísticas gerais da base de dados utilizando o Jupyter Notebook.')
		st.write('4. Analisar as estatísticas e conteúdo das variáveis individualmente.')
		st.write('5. Analisar as características que levaram à conclusão ou ao desvínculo em 2016.')
		st.write('6. Armazenar o conteúdo do projeto em aplicação Streamlit publicada no Heroku.')


	elif (pagina == 'Resultados'):
		st.write(' --- ')
		st.write("### Resultados")

		st.write('Abaixo estão descritas hipóteses levantadas e validadas durante esta análise.')

		st.write('**Hipótese 1:** Estudantes de cursos de Exatas têm MAIOR taxa de desvínculo.')

	elif (pagina == 'Ferramentas Utilizadas'):
		
		st.write(' --- ')

		st.markdown('### Ferramentas utilizadas:')

		st.write('1. **Python**: linguagem utilizada.')
		st.write('2. **Jupyter Notebook**: rascunho das análises.')
		st.write('3. **Streamlit**: framework para criação da aplicação web.')
		st.write('4. **Heroku**: hospedagem do aplicativo para acesso público.')
		st.write('5. **Missigno, Seaborn, Altair**: visualização de dados.')
		st.write('6. **Pandas**: manipulação de dados.')
		st.write('7. **Yellowbrick**: PCA.')
		
	elif (pagina == 'Análise Geral'):
		st.write(' --- ')
		dados_chunk = ler_arquivo("./DM_ALUNO_LIMPO.csv") #ler_arquivo_completo()

		st.write('Tamanho do arquivo: ', dados_chunk.shape)
		#st.write('Tipo dos dados (a maioria dos campos categóricos já foi convertida para labels numéricos): ', dados_chunk.dtypes)
		#st.write('Variaveis não numéricas (a maior parte é campo de descrição): ', (dados_chunk.select_dtypes(include=[np.object])).columns)

		colunas_interessantes = ['CO_IES','CO_CATEGORIA_ADMINISTRATIVA', 'CO_CURSO', 'CO_TURNO_ALUNO', 'CO_GRAU_ACADEMICO',
                             'CO_MODALIDADE_ENSINO', 'CO_NIVEL_ACADEMICO', 'CO_OCDE',
                              'CO_OCDE_AREA_GERAL', 'CO_OCDE_AREA_ESPECIFICA', 'CO_OCDE_AREA_DETALHADA', 'CO_ALUNO_CURSO',
                              'CO_ALUNO_CURSO_ORIGEM', 'CO_ALUNO', 'CO_COR_RACA_ALUNO', 'IN_SEXO_ALUNO', 'NU_IDADE_ALUNO',
                              'CO_NACIONALIDADE_ALUNO', 'CO_UF_NASCIMENTO', 'CO_MUNICIPIO_NASCIMENTO', 'IN_ALUNO_DEF_TGD_SUPER',
                              'CO_ALUNO_SITUACAO', 'QT_CARGA_HORARIA_TOTAL', 'QT_CARGA_HORARIA_INTEG', 'IN_RESERVA_RENDA_FAMILIAR',
                              'IN_FINANC_ESTUDANTIL', 'IN_APOIO_SOCIAL', 'IN_ATIVIDADE_EXTRACURRICULAR', 'CO_TIPO_ESCOLA_ENS_MEDIO',
                              'IN_ALUNO_PARFOR', 'CO_SEMESTRE_REFERENCIA', 'IN_MOBILIDADE_ACADEMICA', 'IN_MATRICULA', 'IN_CONCLUINTE', 'IN_INGRESSO_TOTAL',
                              'IN_INGRESSO_VAGA_NOVA', 'ANO_INGRESSO']

		st.write('Optei por utilizar somente as variáveis abaixo, por intuição (substituindo uma eventual pessoa de negócios):')
		st.dataframe(colunas_interessantes)

		dados_limpo = dados_chunk #ler_arquivo("./DM_ALUNO_LIMPO.csv")

		st.write("A maioria dos campos possui nenhum ou poucos valores nulos, o que indica boa qualidade da base. Os campos com muitos valores nulos ainda assim serão mantidos, pois o próprio valor nulo tem significado.")
		st.write(msno.matrix(dados_limpo.sample(100000)))
		st.pyplot()
		
		st.write("A correlação entre valores nulos pode indicar variáveis com origem similar (como as categorias da OCDE).")
		st.write(msno.heatmap(dados_limpo))
		st.pyplot()

		st.write("A correlação de spearman pode indicar relações de significado.")
		st.write(sns.heatmap(dados_limpo.sample(100000).corr(method='spearman')))
		st.pyplot()
		

	elif (pagina == 'Análise Individual'):
		st.write(' --- ')
		dados_chunk = ler_arquivo("./DM_ALUNO_LIMPO.csv") #ler_arquivo_completo()
		
		opcoes_feature =  dados_chunk.columns
		feature_escolhido = st.selectbox("Escolha uma feature:", opcoes_feature)

		if ((dados_chunk[feature_escolhido].dtype == int) | (dados_chunk[feature_escolhido].dtype == float )):
			if (dados_chunk[feature_escolhido].nunique() < 10):
				st.write(sns.distplot(dados_chunk[feature_escolhido].dropna().astype(int), kde=False))
				st.pyplot()

		else:
			st.bar_chart(dados_chunk[feature_escolhido].value_counts())

		st.write('Algumas estatísticas para entender melhor a variável:')
		if (dados_chunk[feature_escolhido].nunique() < 10):
			st.write(dados_chunk[feature_escolhido].astype('object').describe())	
		else:
			st.write(dados_chunk[feature_escolhido].describe())
		st.write('Primeiras 5 linhas (para ter uma noção do que tem no dataset):')
		st.write(dados_chunk[feature_escolhido].head())
		st.write('Últimas 5 linhas:')
		st.write(dados_chunk[feature_escolhido].tail())

		
	elif (pagina == 'Análise Desvinculados/Concluintes'):
		dados_cru = ler_arquivo("./DM_ALUNO_LIMPO.csv")
		dados_encerraram2016_completo = dados_cru[(dados_cru.CO_ALUNO_SITUACAO == 4) | (dados_cru.CO_ALUNO_SITUACAO == 6)]

		st.write("Meu objetivo é entender quais características impactam na não conclusão do curso. Resolvi analisar a populção de estudantes que se desligaram de sua instituição em 2016 e averiguar as taxas de concluintes e de desvínculos.")
		st.write(' --- ')
		opcoes_feature = ['Area de estudo', 'Turno', 'Grau academico', 'Modalidade de ensino', 'Raça', 'Sexo', 'Deficiência/Superdotação', 'Baixa renda', 'Escola que cursou o ensino medio']
		feature_escolhido = st.selectbox("Escolha uma feature:", opcoes_feature)
		
		dicionario = {'Turno': 'CO_TURNO_ALUNO', 'Area de estudo': 'CO_OCDE_AREA_GERAL', 'Grau academico': 'CO_GRAU_ACADEMICO', 'Modalidade de ensino': 'CO_MODALIDADE_ENSINO', 'Raça': 'CO_COR_RACA_ALUNO', 'Sexo': 'IN_SEXO_ALUNO', 'Deficiência/Superdotação': 'IN_ALUNO_DEF_TGD_SUPER', 'Baixa renda': 'IN_RESERVA_RENDA_FAMILIAR', 'Escola que cursou o ensino medio':'CO_TIPO_ESCOLA_ENS_MEDIO'}

		if (feature_escolhido in opcoes_feature):

			dados_encerraram2016 = dados_encerraram2016_completo.groupby([dicionario[feature_escolhido],'CO_ALUNO_SITUACAO'], as_index=False)['CO_ALUNO_CURSO'].count()
			dados_encerraram2016.columns = [feature_escolhido, 'Situacao', 'Quantidade']
			dados_encerraram2016.replace({'Situacao': {4: 'Desvinculado', 6: 'Concluinte'}}, inplace=True)
			
			dados_encerraram2016[feature_escolhido] = dados_encerraram2016[feature_escolhido].astype(str)
			grafico_barras_empilhadas = alt.Chart(dados_encerraram2016).mark_bar().encode(x=alt.X(feature_escolhido, sort=alt.EncodingSortField(field="Quantidade", op="sum", order='ascending')), y='Quantidade',color='Situacao')
			st.altair_chart(grafico_barras_empilhadas, use_container_width=True)
		
			dados_encerraram2016.columns = [feature_escolhido, 'Situacao', 'Porcentagem']
			grafico_barras_normalizado = alt.Chart(dados_encerraram2016).mark_bar().encode(x=alt.X('Porcentagem', sort=alt.EncodingSortField(field="Porcentagem", op="sum", order='ascending'), stack="normalize"),y=feature_escolhido,color='Situacao')
			st.altair_chart(grafico_barras_normalizado, use_container_width=True)  

	
	elif (pagina == 'PCA'):
		st.write(' --- ')
		dados_limpo = ler_arquivo("./DM_ALUNO_LIMPO.csv")
		dados_encerraram2016_completo = dados_limpo[(dados_limpo.CO_ALUNO_SITUACAO == 4) | (dados_limpo.CO_ALUNO_SITUACAO == 6)]


		opcoes_pca = ['CO_CATEGORIA_ADMINISTRATIVA', 'CO_TURNO_ALUNO', 'CO_GRAU_ACADEMICO','CO_MODALIDADE_ENSINO','CO_NIVEL_ACADEMICO','CO_OCDE_AREA_GERAL','CO_COR_RACA_ALUNO', 'IN_SEXO_ALUNO', 'NU_IDADE_ALUNO','IN_ALUNO_DEF_TGD_SUPER','QT_CARGA_HORARIA_TOTAL', 'IN_RESERVA_RENDA_FAMILIAR','CO_TIPO_ESCOLA_ENS_MEDIO','CO_SEMESTRE_REFERENCIA']
		
		colunas_pca = st.multiselect('Quais características você quer utilizar no PCA para avaliar a importância para conclusão/desvínculo: ', options=opcoes_pca, default=opcoes_pca)

		if (len(colunas_pca) > 1):
			X = dados_encerraram2016_completo[colunas_pca]
			y = dados_encerraram2016_completo.IN_CONCLUINTE
			visualizer = PCA(scale=True, proj_features=True)
			visualizer.fit_transform(X.fillna(-1), y)
			st.write(visualizer.show())
			st.pyplot()


	elif (pagina == 'Possíveis melhorias'):
		st.write(' --- ')

		st.write('Algumas possíveis melhorias que não executei ainda neste projeto:')

		st.write('1. Ler detalhadamente o dicionários de dados.')
		
	


if __name__ == '__main__':
    main()