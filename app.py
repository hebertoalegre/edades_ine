import os
import pandas as pd
from tqdm import tqdm

grupo_etario = ['Total']+ [f'{i} a {i+4}' for i in range(0,100, 5)] + ['100 o más']
route = os.path.abspath('data')

files = os.listdir(route)


grupo = []
edad = []

for file in tqdm(files):
    if file.endswith('.xlsx'):

        df = pd.read_excel(os.path.join(route, file), sheet_name='Población total', header=6)
        dpt = file.split('-')[1] if file.split('-')[1] not in ('El', 'Santa', 'San', 'Alta', 'Baja') else file.split('-')[1] + ' ' + file.split('-')[2]

        for row, t in zip([0, 123, 246],['ambos', 'hombres', 'mujeres']):
            dfi = df.iloc[row:row+123]

            #POR GRUPO ETARIO
            dfg = dfi[dfi[df.columns[0]].isin(grupo_etario)]
            dfg = dfg.set_index(df.columns[0]).dropna(axis=0, how='any').stack().reset_index()
            dfg.columns = ['edad', 'ano', 'poblacion']
            dfg['departamento'] = dpt
            dfg['sector'] = t

            #POR EDAD 
            dfe = dfi[~dfi[df.columns[0]].isin(grupo_etario[:-1])]
            dfe = dfe.set_index(df.columns[0]).dropna(axis=0, how='any').stack().reset_index()
            dfe.columns = ['edad', 'ano', 'poblacion']
            dfe['departamento'] = dpt
            dfe['sector'] = t

            grupo.append(dfg)
            edad.append(dfe)



df_grupo = pd.concat(grupo, axis=0)
df_edad = pd.concat(edad, axis=0)


df_grupo.to_excel(os.path.join(os.path.abspath('outputs'), 'grupo_etario.xlsx'), index=False)
df_edad.to_excel(os.path.join(os.path.abspath('outputs'), 'edad.xlsx'), index=False)


