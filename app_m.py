import os
import pandas as pd
from tqdm import tqdm

grupo_etario = ['Total']+ [f'{i} a {i+4}' for i in range(0,100, 5)] + ['100 o más']
route = os.path.abspath('data/municipal')

# archivos guardados
files = os.listdir(route)

# hojas por archivo
grupo = []
edad = []
for file in tqdm(files):

    file = os.path.join(route, file)
    xls = pd.ExcelFile(file)


    for sheet in xls.sheet_names:

        df = pd.read_excel(os.path.join(route, file), sheet_name=sheet, header=7)
        dpt = file.split('\\')[-1].split('-')[1] if file.split('-')[1] not in ('El', 'Santa', 'San', 'Alta', 'Baja') else file.split('-')[1] + ' ' + file.split('-')[2]
        mun = sheet
        
     
        for row, t in zip([0, 87, 174], ['ambos', 'hombres', 'mujeres']):
            dfi = df.iloc[row:row+87]

            #POR GRUPO ETARIO
            dfg = dfi[dfi[df.columns[0]].isin(grupo_etario)]
            dfg = dfg.set_index(df.columns[0]).dropna(axis=0, how='any').stack().reset_index()
            dfg.columns = ['edad', 'ano', 'poblacion']
            dfg['departamento'] = dpt.replace('.xlsx', '')
            dfg['municipio'] = mun
            dfg['sector'] = t

            #POR EDAD 
            dfe = dfi[~dfi[df.columns[0]].isin(grupo_etario[:-1])]
            dfe = dfe.set_index(df.columns[0]).dropna(axis=0, how='any').stack().reset_index()
            dfe.columns = ['edad', 'ano', 'poblacion']
            dfe['departamento'] = dpt.replace('.xlsx', '')
            dfe['municipio'] = mun 
            dfe['sector'] = t

            grupo.append(dfg)
            edad.append(dfe)


df_grupo = pd.concat(grupo, axis=0)
df_edad = pd.concat(edad, axis=0)

print(df_edad)
print(df_grupo)


df_grupo.to_csv(os.path.join(os.path.abspath('outputs'), 'grupo_etario_municipal.csv'), index=False, sep=',')
df_edad.to_csv(os.path.join(os.path.abspath('outputs'), 'edad_municapal.csv'), index=False, sep=',')