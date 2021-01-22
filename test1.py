import pandas as pd
import numpy as np
import jellyfish as jf

# Función para quitar tildes
def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s

# Función para encontrar similitud entre palabras que son iguales pero se han escrito distinto
def name_matcher(original_matriz,matriz_to_merge,column_with_nan_spaces):
    # Combino los dataframes por nombre del municipio
    final_with_errors = pd.merge(original_matriz, matriz_to_merge, on='Municipality', how='outer')
    # Tomo los municipios que no obtuvieron coincidencia por nombre
    matriz_with_wrong_names = final_with_errors.iloc[n:,:]
    matriz_with_blanks = final_with_errors[np.isnan(final_with_errors[column_with_nan_spaces])]
    for i in matriz_with_wrong_names['Municipality']:
        score = 0
        winner = ''
        for j in matriz_with_blanks['Municipality']:
            if jf.jaro_winkler_similarity(i, j) >= score:
                score = jf.jaro_winkler_similarity(i, j)
                winner = j
        print(f'{i} was replaced for {winner}')
        matriz_to_merge.loc[matriz_to_merge['Municipality']==i,'Municipality'] = winner

# Función para verificar el tamaño de la matriz
def size_error(matriz_after_merge, n):
    if matriz_after_merge.shape[0] == n:
        print("No hay errores")
    else:
        print("Hubo algún error")

#####################################################################################################
# Paths of Files
#####################################################################################################

# This file is too big to upload it to the repository. Change the path to your local file 'People'
people_file_path = "D:/UNIVERSIDAD/DANE Dengue/Git Repositorios/CNPV2018_5PER_A2_05.CSV"

houses_file_path = "D:/UNIVERSIDAD/DANE Dengue/Git Repositorios/CNPV2018_2HOG_A2_05.CSV"
viv_file_path = "D:/UNIVERSIDAD/DANE Dengue/Git Repositorios/CNPV2018_1VIV_A2_05.CSV"
dengue_data_file = "Data_Files/DANE_Dengue_Data_2015_2019.csv"
health_providers_file = "Data_Files/Health_Providers.csv"
municipality_area_file = "Data_Files/Municipality_Area.csv"

#####################################################################################################
# Reading the csv files
#####################################################################################################

people_data = pd.read_csv(people_file_path, usecols=['U_MPIO', 'P_EDADR', 'PA1_GRP_ETNIC', 'CONDICION_FISICA',
                                                    'P_ALFABETA', 'P_NIVEL_ANOSR', 'P_TRABAJO', 'P_SEXO'])
houses_data = pd.read_csv(houses_file_path, usecols=['U_MPIO','COD_ENCUESTAS'])
viv_data = pd.read_csv(viv_file_path, usecols=['U_MPIO', 'VA1_ESTRATO', 'VB_ACU', 'VF_INTERNET'])
municipality_data = pd.read_csv(dengue_data_file, usecols=['State code','Municipality code', 'Municipality'])
health_providers_data = pd.read_csv(health_providers_file, usecols=['depa_nombre', 'muni_nombre','nombre_prestador'])
municipality_area_data = pd.read_csv(municipality_area_file)

#####################################################################################################
# Inicio del codigo
#####################################################################################################

# Número de municipios en el archivo
n = len(people_data['U_MPIO'].unique())

# Crear matriz de salida
s = np.zeros((n,26))

# Poner código de municipio en primera columna de matriz de salida
s[:,0] = people_data['U_MPIO'].unique()

#####################################################################################################
# Se van a encontrar las variables posibles en el archivo de 'Personas'
#####################################################################################################

# Iterar por cada municipio para encontrar P_EDADR de 0 a 4 años (osea valor en 1)
for i in range(0,n):
    # Número de personas del municipio s[i,0] Y del rango de edad "1"
    aux1 = len(people_data[(people_data['U_MPIO']==s[i,0]) & (people_data['P_EDADR']==1) ])
    # Llevar a porcentaje dividiendo por el total de personas del municipio
    aux2 = aux1/ len(people_data[people_data['U_MPIO']==s[i,0]])
    #print(aux2)
    #aux2 = np.round(aux2*100,2) #comentar esta línea para archivo final, solo por visualización de print
    # guardar en matriz de salida
    s[i,1] = aux2

    # Para encontrar P_EDADR de 4 a 15 años (osea valor en 2 y 3)
    # Número de personas del municipio s[i,0] Y del rango de edad "2"
    aux1 = len(people_data[(people_data['U_MPIO']==s[i,0]) & (people_data['P_EDADR']==2) ])
    # Número de personas del municipio s[i,0] Y del rango de edad "2" y "3"
    aux1 = aux1 + len(people_data[(people_data['U_MPIO']==s[i,0]) & (people_data['P_EDADR']==3) ])
    # Llevar a porcentaje dividiendo por el total de personas del municipio
    aux2 = aux1/ len(people_data[people_data['U_MPIO']==s[i,0]])
    # guardar en matriz de salida
    s[i,2] = aux2

    # Para encontrar P_EDADR de 15 a 29 años (osea valor en 4, 5 y 6)
    # Número de personas del municipio s[i,0] Y del rango de edad "4"
    aux1 = len(people_data[(people_data['U_MPIO']==s[i,0]) & (people_data['P_EDADR']==4) ])
    # Número de personas del municipio s[i,0] Y del rango de edad "4" y "5"
    aux1 = aux1 + len(people_data[(people_data['U_MPIO']==s[i,0]) & (people_data['P_EDADR']==5) ])
    # Número de personas del municipio s[i,0] Y del rango de edad "4", "5" y "6"
    aux1 = aux1 + len(people_data[(people_data['U_MPIO']==s[i,0]) & (people_data['P_EDADR']==6) ])
    # Llevar a porcentaje dividiendo por el total de personas del municipio
    aux2 = aux1/ len(people_data[people_data['U_MPIO']==s[i,0]])
    # guardar en matriz de salida
    s[i,3] = aux2

    # Para encontrar P_EDADR de mayores a 30 años (osea valor >= 7)
    # Número de personas del municipio s[i,0] Y de los rangos de edades mayores o iguales a "7"
    aux1 = len(people_data[(people_data['U_MPIO']==s[i,0]) & (people_data['P_EDADR']>=7) ])
    # Llevar a porcentaje dividiendo por el total de personas del municipio
    aux2 = aux1/ len(people_data[people_data['U_MPIO']==s[i,0]])
    # guardar en matriz de salida
    s[i,4] = aux2

    # Para encontrar PA1_GRP_ETNIC población afrocolombiana suponiendo que sería
    # Negro, mulato, afrodescendiente, afrocolombiano, raizal y palenquero (valores 3, 4 y 5)
    # Número de personas del municipio s[i,0] y afrocolombianas "3", "4" y "5"
    aux1 = len(people_data[(people_data['U_MPIO']==s[i,0]) & ((people_data['PA1_GRP_ETNIC']==3) | (people_data['PA1_GRP_ETNIC']==4) | (people_data['PA1_GRP_ETNIC']==5))])
    # Llevar a porcentaje dividiendo por el total de personas del municipio
    aux2 = aux1/ len(people_data[people_data['U_MPIO']==s[i,0]])
    # guardar en matriz de salida
    s[i,5] = aux2

    # Para encontrar PA1_GRP_ETNIC población indigena (valor 1)
    # Número de personas del municipio s[i,0] e indigenas "1"
    aux1 = len(people_data[(people_data['U_MPIO']==s[i,0]) & (people_data['PA1_GRP_ETNIC']==1)])
    # Llevar a porcentaje dividiendo por el total de personas del municipio
    aux2 = aux1/ len(people_data[people_data['U_MPIO']==s[i,0]])
    # guardar en matriz de salida
    s[i,6] = aux2

    # Para encontrar CONDICION_FISICA personas con dificultades en su vida diaria (osea valor en 1)
    # Número de personas del municipio s[i,0] y condicion fisica "1"
    aux1 = len(people_data[(people_data['U_MPIO']==s[i,0]) & (people_data['CONDICION_FISICA']==1) ])
    # Llevar a porcentaje dividiendo por el total de personas del municipio
    aux2 = aux1/ len(people_data[people_data['U_MPIO']==s[i,0]])
    # guardar en matriz de salida
    s[i,7] = aux2

    # Para encontrar P_ALFABETA personas que no saben leer ni escribir (o sea valor en 2)
    # Número de personas del municipio s[i,0] y no saben leer ni escribir "2"
    aux1 = len(people_data[(people_data['U_MPIO']==s[i,0]) & (people_data['P_ALFABETA']==2) ])
    # Llevar a porcentaje dividiendo por el total de personas del municipio
    aux2 = aux1/ len(people_data[people_data['U_MPIO']==s[i,0]])
    # guardar en matriz de salida
    s[i,8] = aux2

    # Para encontrar 'P_NIVEL_ANOSR' personas con educación secundaria/superior (o sea valor entre 3 y 9)
    # Número de personas del municipio s[i,0] y con educación secundaria/superior ">=3" & "<=9"
    aux1 = len(people_data[(people_data['U_MPIO']==s[i,0]) & (people_data['P_NIVEL_ANOSR']>=3) & (people_data['P_NIVEL_ANOSR']<=9)])
    # Llevar a porcentaje dividiendo por el total de personas del municipio
    aux2 = aux1/ len(people_data[people_data['U_MPIO']==s[i,0]])
    # guardar en matriz de salida
    s[i,9] = aux2

    # Para encontrar 'P_TRABAJO' personas empleadas (o sea valor 1 y 3)
    # Número de personas del municipio s[i,0] y empleadas "1" & "3"
    aux1 = len(people_data[(people_data['U_MPIO']==s[i,0]) & ((people_data['P_TRABAJO']==1) | (people_data['P_TRABAJO']==3))])
    # Llevar a porcentaje dividiendo por el total de personas del municipio
    aux2 = aux1/ len(people_data[people_data['U_MPIO']==s[i,0]])
    # guardar en matriz de salida
    s[i,10] = aux2

    # Para encontrar 'P_TRABAJO' personas desempleadas (o sea valor 2 y 4)
    # Número de personas del municipio s[i,0] y empleadas "2" & "4"
    aux1 = len(people_data[(people_data['U_MPIO']==s[i,0]) & ((people_data['P_TRABAJO']==2) | (people_data['P_TRABAJO']==4))])
    # Llevar a porcentaje dividiendo por el total de personas del municipio
    aux2 = aux1/ len(people_data[people_data['U_MPIO']==s[i,0]])
    # guardar en matriz de salida
    s[i,11] = aux2

    # Para encontrar 'P_TRABAJO' personas con oficios domesticos (o sea valor 7)
    # Número de personas del municipio s[i,0] y con oficios domesticos "7"
    aux1 = len(people_data[(people_data['U_MPIO']==s[i,0]) & (people_data['P_TRABAJO']==7)])
    # Llevar a porcentaje dividiendo por el total de personas del municipio
    aux2 = aux1/ len(people_data[people_data['U_MPIO']==s[i,0]])
    # guardar en matriz de salida
    s[i,12] = aux2

    # Para encontrar 'P_TRABAJO' personas jubiladas (o sea valor 5)
    # Número de personas del municipio s[i,0] y jubiladas "5"
    aux1 = len(people_data[(people_data['U_MPIO']==s[i,0]) & (people_data['P_TRABAJO']==5)])
    # Llevar a porcentaje dividiendo por el total de personas del municipio
    aux2 = aux1/ len(people_data[people_data['U_MPIO']==s[i,0]])
    # guardar en matriz de salida
    s[i,13] = aux2

    # Número de personas del municipio s[i,0] y sexo ==1 hombre o ==2 mujer
    aux1 = len(people_data[(people_data['U_MPIO']==s[i,0]) & (people_data['P_SEXO']==1)])
    # Llevar a porcentaje dividiendo por el total de personas del municipio
    aux2 = aux1/ len(people_data[people_data['U_MPIO']==s[i,0]])
    # guardar en matriz de salida
    s[i,14] = aux2 #Hombres

    # Número de personas del municipio s[i,0] y sexo ==1 hombre o ==2 mujer
    aux1 = len(people_data[(people_data['U_MPIO']==s[i,0]) & (people_data['P_SEXO']==2)])
    # Llevar a porcentaje dividiendo por el total de personas del municipio
    aux2 = aux1/ len(people_data[people_data['U_MPIO']==s[i,0]])
    # guardar en matriz de salida
    s[i,15] = aux2 #Mujeres

    # Para agua
    aux1 = len(viv_data[(viv_data['U_MPIO']==s[i,0]) & (viv_data['VB_ACU']==2)])
    # Llevar a porcentaje dividiendo por el total de personas del municipio
    aux2 = aux1/ len(viv_data[viv_data['U_MPIO']==s[i,0]])
    # guardar en matriz de salida
    s[i,16] = aux2

    # Para internet
    aux1 = len(viv_data[(viv_data['U_MPIO']==s[i,0]) & (viv_data['VF_INTERNET']==2)])
    # Llevar a porcentaje dividiendo por el total de personas del municipio
    aux2 = aux1/ len(viv_data[viv_data['U_MPIO']==s[i,0]])
    # guardar en matriz de salida
    s[i,17] = aux2

#ciclo while permite categorizar los seis estratos existentes
mun = 1
while (mun < 7):
    for i in range(0,n):
        estrato = len(viv_data[(viv_data['U_MPIO']==s[i,0]) & (viv_data['VA1_ESTRATO']==mun)])
        # Llevar a porcentaje dividiendo por el total de personas del municipio
        estrato = estrato/ len(viv_data[viv_data['U_MPIO']==s[i,0]])
        # guardar en matriz de salida
        s[i,17+mun] = estrato
    mun += 1

#######################################################################################
# Ahora se va a calcular el numero de hospitales por km2
#######################################################################################

# Selecciono los municipios de Antioquia y borro la columna de codigo de estado
matriz = municipality_data[municipality_data['State code']==5]
del matriz['State code']
# Se itera cada municipio, se cambia a MAYUSCULAS y se quitan tildes. Tambien se dejan los codigos de cada
# municipio igual a como los presenta el DANE (solo decenas y unidades)
for i in range(0,len(matriz['Municipality'])):
    matriz.loc[i,'Municipality'] = normalize(matriz.loc[i,'Municipality'].upper())
    matriz.loc[i,'Municipality code'] = matriz.loc[i,'Municipality code'] - 5000

# Cuento cuantos prestadores hay por municipio
table = health_providers_data[['muni_nombre']].groupby('muni_nombre').size()
# Creo dos listas, una con los nombres de los municipios y la otra con sus cantidades de prestadores
municipios = table.index.values
hospitales = table.values
# Creo un dataframe con los anteriores datos para hacer mas facil el merge
diccionario = {'Municipality':municipios, 'Hospitals':hospitales}
prestadores = pd.DataFrame(data=diccionario)

# Mayusculas y quito tildes
for i in range(0,len(prestadores['Municipality'])):
    prestadores.loc[i,'Municipality'] = normalize(prestadores.loc[i,'Municipality'].upper())

# Busco los municipios que no coincidieron en nombre y los combino con su municipio respectivo
name_matcher(matriz, prestadores, 'Hospitals')
# Hago el merge definitivo
final = pd.merge(matriz, prestadores, on='Municipality', how='outer')
# Compruebo que todos los municipios hayan encontrado su pareja, observando el tamaño de la matriz de salida
size_error(final, n)
# Cambio los NaN por cero
final.fillna(0, inplace=True)

# Selecciono los municipios de Antioquia en el archivo 'Municipality_Area' y reinicio los indices del dataframe
area = municipality_area_data[municipality_area_data['Departamento']=='Antioquia']
area.index = range(len(area.index))
# Cambio el nombre de la columna para el merge y elimino la columna de departamento
area.rename(columns={'Municipio':'Municipality'}, inplace=True)
del area['Departamento']

# Mayusculas y quito tildes
for i in range(0,len(area['Municipality'])):
    area.loc[i,'Municipality'] = normalize(area.loc[i,'Municipality'].upper())

# Busco los municipios que no coincidieron en nombre y los combino con su municipio respectivo
name_matcher(final, area, 'Area (km2)')
# Hago el merge definitivo
final_2 = pd.merge(final, area, on='Municipality', how='outer')
# Compruebo que todos los municipios hayan encontrado su pareja, observando el tamaño de la matriz de salida
size_error(final_2, n)
# Cambio los NaN por cero
final_2.fillna(0, inplace=True)

# Creo una lista con la cantidad de hospitales por km2 en orden de codigo municipal
m = final_2['Hospitals'].values / final_2['Area (km2)'].values
# Se agrega a la matriz final
s[:,24] = m

#######################################################################################
# Ahora se va a calcular el numero de hogares por km2
#######################################################################################

# Creo dos listas, una para el numero de hogares y la otra para los codigos de cada municipio
hogares_por_municipio = []
codigos_de_municipio = s[:,0]
# Itero y encuentro el numero de hogares por municipio
for i in range(0,n):
    hogares_por_municipio.append(len(houses_data[houses_data['U_MPIO'] == s[i,0]]['COD_ENCUESTAS'].unique()))
# Creo un diccionario para crear el dataframe
diccionario = {'Municipality code':codigos_de_municipio, 'Houses':hogares_por_municipio}
# Creo el dataframe
houses = pd.DataFrame(data=diccionario)
# Hago merge con la matriz llamada 'final_2' usada anteriormente, mediante el codigo de municipio
final_3 = pd.merge(final_2, houses, on='Municipality code', how='outer')
# Compruebo el tamaño de la matriz final
size_error(final_3, n)
# Creo una lista con la cantidad de hogares por km2 en orden de codigo municipal
m = final_3['Houses'].values / final_3['Area (km2)'].values
# Se agrega a la matriz final
s[:,25] = m
# Redondeamos todos los resultados a dos decimales y se escriben como porcentaje
s[:,1:] = np.round(s[:,1:]*100,2)
# Se ajustan los codigos de cada municipio para el merge final
s[:,0] = s[:,0] + 5000

#####################################################################################################
# Merging with the main file
#####################################################################################################
columns_names = ['Municipality code',
                'Age 0-4 (%)',
                'Age 5-14 (%)',
                'Age 15-29 (%)',
                'Age >30 (%)',
                'Afrocolombian Population (%)',
                'Indian Population (%)',
                'People with Disabilities (%)',
                'People who cannot read or write (%)',
                'Secondary/Higher Education (%)',
                'Employed population (%)',
                'Unemployed population (%)',
                'People doing housework (%)',
                'Retired people (%)',
                'Men (%)',
                'Women (%)',
                'Households without water access (%)',
                'Households without internet access (%)',
                'Building stratification 1 (%)',
                'Building stratification 2 (%)',
                'Building stratification 3 (%)',
                'Building stratification 4 (%)',
                'Building stratification 5 (%)',
                'Building stratification 6 (%)',
                'Number of hospitals per Km2',
                'Number of houses per Km2']
main_file = pd.read_csv(dengue_data_file)
DANE_Dengue_Data_Variables = pd.DataFrame(s, columns = columns_names)
final_file = pd.merge(main_file, DANE_Dengue_Data_Variables, on='Municipality code', how='outer')
# Optimization
final_file['Municipality code'] = final_file['Municipality code'].apply(int)
final_file['Municipality code'] = pd.to_numeric(final_file['Municipality code'], downcast='integer')
# Creating the csv file
final_file.to_csv('DANE_Dengue_Data_Variables.csv', index=False)
print(final_file)
