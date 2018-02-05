import pandas as pd
import numpy as np

'''
Objectif de ce code : 
Identifier les variables intéressantes pour le groupement des pays en fonction
de leurs caractéristiques (clustering)
- Suppression des indicateurs mal renseignés (avec de nombreuses valeurs manquantes)
- Identification des variables à prendre en compte dans le clustering
(grâce à des matrices de corrélations pour éviter la redondance d'information avec la donnée d'émission)
'''

################################
#    I - IMPORT DES DONNEES    
################################

data = pd.read_csv('C:\\etude_cas_mcougul\\data\\WDIData.csv', sep=',')
country = pd.read_csv('C:\\etude_cas_mcougul\\data\\WDICountry.csv', sep=',')
series_1= pd.read_csv('C:\\etude_cas_mcougul\\data\\WDISeries.csv', sep=',')

###################################################################
#    II - MATRICE DE CORRELATIONS SUR L'ENSEMBLE DES INDICATEURS    
###################################################################


# 1 - Identification des indicateurs bien renseignés (avec pas trop de valeurs manquantes)

# On compte le nombre de fois où l'indicateur est renseigné (sur l'ensemble des pays)
# Ce comptage se fait sur chaque date

check_indic = data.groupby("Indicator Name").count()

# On nettoie les données en supprimant les champs inutiles

check_indic.drop(['Country Name','Country Code', 'Indicator Code', 'Unnamed: 62'],axis=1, inplace=True)

# On supprime 1960 et 2017 car il y a très peu de données renseignées pour ces 2 dates

check_indic.drop(['1960','2017'],axis=1, inplace=True)

# On calcule un "taux de renseignement" pour chaque indicateur

check_indic["taux ok"] = np.mean(check_indic,axis=1) / 264

# On ne garde que les indicateurs avec un taux >= 60%

kpi_ok = check_indic[check_indic["taux ok"]>=0.6]
kpi_ok=kpi_ok[["taux ok"]]

# On perd beaucoup d'indicateurs => essayons en ne prenant que sur les 20 dernières années
# (là où les données sont les mieux renseignées)

# On supprime les dates de 1961 à 1993

list_date_drop = ['1961','1962','1963','1964','1965','1966','1967','1968','1969','1970',
                  '1971','1972','1973','1974','1975','1976','1977','1978','1979',	'1980',	
                  '1981','1982','1983','1984','1985','1986','1987','1988','1989','1990',
                  '1991','1992','1993']

for i in list_date_drop:
    check_indic.drop([i],axis=1, inplace=True)
    
# On recalcule notre "taux de renseignement" pour chaque indicateur
    
check_indic.drop(["taux ok"],axis=1, inplace=True)
check_indic["taux ok"] = np.mean(check_indic,axis=1) / 264

# On ne garde que les variables avec un taux >= 60%

kpi_ok_bis = check_indic[check_indic["taux ok"]>=0.6]
kpi_ok_bis=kpi_ok_bis[["taux ok"]]


# 2 - Création de la matrice de corrélations sur l'ensemble des indicateurs retenus
# On va travailler ici sur les émissions par personne afin de s'affranchir de
# l'effet du nombre d'habitants sur les émissions de CO2

#On ne garde que les données concernant les indicateurs retenus

prepa_matrice_corr = pd.merge(data,kpi_ok_bis,left_on='Indicator Name', right_index=True)

# On ne garde ensuite que le pays, le nom du kpi et sa valeur pour 2014

prepa_matrice_corr=prepa_matrice_corr[['Country Name', 'Indicator Name', '2014']]

# On transpose cette table pour avoir une ligne par pays

prepa_matrice_corr_pivot = prepa_matrice_corr.pivot_table(index=['Country Name'], columns='Indicator Name')

# On construit la matrice de corrélations

correlations=prepa_matrice_corr_pivot.corr()


#########################################################################
#    III - MATRICE DE CORRELATIONS SUR UN NOMBRE RESTREINT D'INDICATEURS    
#########################################################################

# Afin de faciliter la lecture et ensuite l'interprétation des groupes de pays que l'on
# va créer, on se restreint aux données environnementales concernant les émissions et
# la production d'énergie

# On ne garde donc que les indicateurs avec assez peu de corrélation avec la variable
# d'émissions de CO2 par personne afin d'éviter la redondance d'information dans le modèle

# On ne garde alors que les indicateurs avec une corrélation comprise entre -45% et 45% environ

# Afin d'éviter les redondances d'information au sein de toutes ces données, on refait une matrice
# de corrélation

# A noter que la copie dans mon code d'un grand nombre d'indicateurs entre '' n'est 
# pas fait à la main mais via une formule excel !

liste_kpi = ['Access to electricity (% of population)',
'CO2 emissions from gaseous fuel consumption (% of total)',
'CO2 emissions from electricity and heat production, total (% of total fuel combustion)',
'Access to electricity, urban (% of urban population)',
'CO2 intensity (kg per kg of oil equivalent energy use)',
'Electricity production from natural gas sources (% of total)',
'Electricity production from oil, gas and coal sources (% of total)',
'CO2 emissions (kg per 2010 US$ of GDP)',
'Energy use (kg of oil equivalent) per $1,000 GDP (constant 2011 PPP)',
'CO2 emissions from gaseous fuel consumption (kt)',
'Electricity production from renewable sources, excluding hydroelectric (kWh)',
'Electricity production from nuclear sources (% of total)',
'CO2 emissions from liquid fuel consumption (kt)',
'Energy intensity level of primary energy (MJ/$2011 PPP GDP)',
'CO2 emissions (kt)',
'CO2 emissions from solid fuel consumption (% of total)',
'CO2 emissions from solid fuel consumption (kt)',
'Electricity production from coal sources (% of total)',
'Electricity production from oil sources (% of total)',
'Electricity production from renewable sources, excluding hydroelectric (% of total)',
'CO2 emissions from manufacturing industries and construction (% of total fuel combustion)',
'Alternative and nuclear energy (% of total energy use)',
'CO2 emissions from residential buildings and commercial and public services (% of total fuel combustion)',
'GDP per unit of energy use (PPP $ per kg of oil equivalent)',
'GDP per unit of energy use (constant 2011 PPP $ per kg of oil equivalent)',
'CO2 emissions from other sectors, excluding residential buildings and commercial and public services (% of total fuel combustion)',
'Energy imports, net (% of energy use)',
'CO2 emissions from liquid fuel consumption (% of total)',
'CO2 emissions from transport (% of total fuel combustion)',
'Electric power transmission and distribution losses (% of output)',
'Renewable electricity output (% of total electricity output)',
'Electricity production from hydroelectric sources (% of total)',
'Combustible renewables and waste (% of total energy)']

matrice_corr_light = prepa_matrice_corr[prepa_matrice_corr['Indicator Name'] == 'CO2 emissions (metric tons per capita)']

for i in liste_kpi:
    ajout_kpi = prepa_matrice_corr[prepa_matrice_corr['Indicator Name'] == i]
    matrice_corr_light = pd.concat([matrice_corr_light,ajout_kpi])

matrice_corr_light = matrice_corr_light.pivot_table(index=['Country Name'], columns='Indicator Name')

import seaborn as sns
corr = matrice_corr_light.corr()
sns.heatmap(corr, 
            xticklabels=corr.columns.values,
            yticklabels=corr.columns.values)

# Lorsque 2 variables sont très corrélées, on supprime une des 2 pour éviter la redondance
# Après cet exercice, on obtient les indicateurs suivants (avec lesquels on refait le même exercice)

#########################################################################
#    IV - MATRICE DE CORRELATIONS SUR LES INDICATEURS RETENUS
#########################################################################


liste_kpi = ['CO2 emissions from gaseous fuel consumption (% of total)',
'CO2 emissions from electricity and heat production, total (% of total fuel combustion)',
'CO2 emissions from solid fuel consumption (% of total)',
'CO2 emissions from transport (% of total fuel combustion)',
'Alternative and nuclear energy (% of total energy use)',
'CO2 emissions from residential buildings and commercial and public services (% of total fuel combustion)',
'CO2 emissions from other sectors, excluding residential buildings and commercial and public services (% of total fuel combustion)',
'CO2 emissions from liquid fuel consumption (% of total)',
'Combustible renewables and waste (% of total energy)',
'GDP per unit of energy use (PPP $ per kg of oil equivalent)',
'Energy imports, net (% of energy use)',
'Electric power transmission and distribution losses (% of output)']

matrice_corr_light = prepa_matrice_corr[prepa_matrice_corr['Indicator Name'] == 'CO2 emissions (metric tons per capita)']

for i in liste_kpi:
    ajout_kpi = prepa_matrice_corr[prepa_matrice_corr['Indicator Name'] == i]
    matrice_corr_light = pd.concat([matrice_corr_light,ajout_kpi])

matrice_corr_light = matrice_corr_light.pivot_table(index=['Country Name'], columns='Indicator Name')

import seaborn as sns
corr = matrice_corr_light.corr()
sns.heatmap(corr, 
            xticklabels=corr.columns.values,
            yticklabels=corr.columns.values)

# Nous avons donc obtenu les indicateurs que nous allons utiliser dans notre clustering


