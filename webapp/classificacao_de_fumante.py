import pandas                  as pd
import streamlit               as st
import joblib
import inflection
import seaborn                 as sns
import numpy                   as np
from sklearn.compose           import ColumnTransformer
from sklearn.preprocessing     import OneHotEncoder
from sklearn.pipeline          import Pipeline

st.write("""
# MENZOIL WEBAPP - Classificação de pessoas fumantes ou não fumantes
""")

st.sidebar.title('Options')
radio_button = st.sidebar.radio('Select:', ['Upload de tabela', 'Input de Dados'])
best_model = joblib.load( 'C:/Users/leo_m/Repos/Projeto Menzoil/model/model_menzoil.pkl' )

if radio_button == 'Upload de tabela':
    try:
        st.write("""
        ### Para classificar as pessoas carregue o arquivo CSV:
        """)
        uploaded_file = st.file_uploader("")
            
        df_raw = pd.read_csv(uploaded_file)
        df_etl = df_raw.copy()

        # classificaçao_corporal
        df_etl['Classificaçao_corporal'] = df_etl['IMC'].apply( lambda x: 'thinness' if x < 18.5  else 'normal' if (x >= 18.5) & (x < 24.9) else 'overweight' if (x >= 24.9) & (x < 30) else 'obese' )

        # fase_da_vida
        df_etl['Fase_da_vida'] = df_etl['Idade'].apply( lambda x: 'kid' if x < 12  else 'teenager' if (x >= 12) & (x < 18) else 'adult' if (x >= 18) & (x < 60) else 'elderly' )

        # regiao_geral
        df_etl['Regiao_geral'] = df_etl['Regiao'].apply( lambda x: 'south' if (x == 'southwest') or (x == 'southeast')  else 'north')

        df1 = df_etl.copy()

        cols_old = ['Idade', 'Sexo', 'IMC', 'Filhos', 'Regiao', 'Custos', 'Classificaçao_corporal', 'Fase_da_vida', 'Regiao_geral']

        snakecase = lambda x: inflection.underscore( x )

        cols_new = list( map( snakecase, cols_old ) )

        # rename
        df1.columns = cols_new

        df3 = df1.copy()

        y_preds = best_model.predict(df3)
        y_preds = pd.DataFrame(data = y_preds)
        y_preds = y_preds.rename(columns={0: 'Fumante'})
        y_preds = y_preds.Fumante.map(lambda x: 'yes' if x == 1 else 'no')
        y_preds = pd.DataFrame(data = y_preds)

        df_test = pd.concat( [df_raw, y_preds], axis=1)
        st.dataframe(df_test)

    except:
        
        st.stop()


elif radio_button == 'Input de Dados':

    with st.form("unit_form"):
        st.write("""
        ### Preencha com os dados do caso:
        """)
        idade = st.slider("Idade", min_value=1, max_value=100, value=18)
        sexo = st.selectbox('Sexo', ('male', 'female'))
        imc = st.number_input("IMC", value=15.0, step=0.1, format="%.4f")
        filhos = st.slider("Filhos", min_value=0, max_value=10, value=0)
        regiao = st.selectbox('Região', ('southwest', 'southeast', 'northwest', 'northeast'))
        custos = st.number_input("Custos", value=1100.0, step=0.1, format="%.5f")
        

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            df = pd.DataFrame([[idade, sexo, imc, filhos, regiao, custos]], columns=['Idade', 'Sexo', 'IMC', 'Filhos', 'Regiao', 'Custos'])
            print(df)
            # classificaçao_corporal
            df['Classificaçao_corporal'] = df['IMC'].apply( lambda x: 'thinness' if x < 18.5  else 'normal' if (x >= 18.5) & (x < 24.9) else 'overweight' if (x >= 24.9) & (x < 30) else 'obese' )

            # fase_da_vida
            df['Fase_da_vida'] = df['Idade'].apply( lambda x: 'kid' if x < 12  else 'teenager' if (x >= 12) & (x < 18) else 'adult' if (x >= 18) & (x < 60) else 'elderly' )

            # regiao_geral
            df['Regiao_geral'] = df['Regiao'].apply( lambda x: 'south' if (x == 'southwest') or (x == 'southeast')  else 'north')


            cols_old = ['Idade', 'Sexo', 'IMC', 'Filhos', 'Regiao', 'Custos', 'Classificaçao_corporal', 'Fase_da_vida', 'Regiao_geral']

            snakecase = lambda x: inflection.underscore( x )

            cols_new = list( map( snakecase, cols_old ) )

            # rename
            df.columns = cols_new
            

            y_preds = best_model.predict(df)
            y_preds = pd.DataFrame(data = y_preds)
            y_preds = y_preds.rename(columns={0: 'Fumante'})
            y_preds = y_preds.Fumante.map(lambda x: 'yes' if x == 1 else 'no')
            y_preds = pd.DataFrame(data = y_preds)

            cols_old = ['idade', 'sexo', 'imc', 'filhos', 'regiao', 'custos', 'classificaçao_corporal', 'fase_da_vida', 'regiao_geral']

            snakecase = lambda x: inflection.humanize( x )

            cols_new = list( map( snakecase, cols_old ) )

            # rename
            df.columns = cols_new
                    

            df_test = pd.concat( [df[['Idade', 'Sexo','Imc','Filhos','Regiao','Custos']], y_preds], axis=1)
            st.dataframe(df_test)
