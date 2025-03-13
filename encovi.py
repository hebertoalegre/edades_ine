import os 
import pyreadstat



file = os.path.abspath('data\personas.sav')
df, meta = pyreadstat.read_sav(file, apply_value_formats=True)  
personas = df[['NO_HOGAR']].reset_index().groupby(['NO_HOGAR']).count().to_dict()['index']


file = os.path.abspath('data\prestamos.sav')


df, meta = pyreadstat.read_sav(file, apply_value_formats=True)  
df = df[['DEPTO', 'NO_HOGAR','FACTOR', 'P17A01', 'P17A03', 'P17A05','P17A06']]
df = df[((df['P17A01']=='SI')|(df['P17A05']=='SI'))]
df['PERSONAS'] = df['NO_HOGAR'].map(personas)
df['EXPANSION'] = df['PERSONAS'] * df['FACTOR']
df['CREDITOS'] = df['P17A06']/df['PERSONAS']
df['TOTAL'] = df['EXPANSION'] * df['CREDITOS']
df = df.groupby('DEPTO')[['TOTAL', 'EXPANSION']].sum().reset_index()
df['P'] = df['TOTAL']/df['EXPANSION']

print(df)
# print(df.sum())

