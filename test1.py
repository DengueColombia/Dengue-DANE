import pandas as pd
import numpy as np
import jellyfish as jf
from functions import function1, function2

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

state_code = 5
#####################################################################################################
# Se van a encontrar las variables posibles en el archivo de 'Personas' y 'Viviendas'
#####################################################################################################

s = function1(people_data,viv_data)

#######################################################################################
# Ahora se va a calcular el numero de hospitales por km2 y el numero de hogares por km2
#######################################################################################

s[:,24:26] = function2(state_code, municipality_data, health_providers_data, municipality_area_data, houses_data)
# Redondeamos todos los resultados a dos decimales y se escriben como porcentaje
s[:,1:] = np.round(s[:,1:]*100,2)
# Se ajustan los codigos de cada municipio para el merge final
s[:,0] = s[:,0] + state_code*1000

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
