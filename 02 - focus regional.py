import pandas as pd
import matplotlib.pyplot as plt

'''
Objectif de ce code : 
Avoir une vision globale des émissions de CO2 par région
- Part de chaque région dans les émissions de CO2 (en 2014)
- Top 20 des pays avec les émissions les plus importantes (en 2014)
- Moyenne des émissions de CO2 par personne et par région
- Emissions de CO2 par personne pour les 20 plus gros pollueurs identifiés précédemment
(comparaison entre 1994 et 2014 pour voir les tendances par pays)
'''


################################
#    I - IMPORT DES DONNEES    
################################

data = pd.read_csv('C:\\etude_cas_mcougul\\data\\WDIData.csv', sep=',')
country = pd.read_csv('C:\\etude_cas_mcougul\\data\\WDICountry.csv', sep=',')


######################################################
#    II - ANALYSE PRELIMINAIRE AU NIVEAU REGIONAL
#            SUR LES EMISSIONS DE CO2 GLOBALES    
######################################################


# 1 - On supprime les données agrégées par groupe dans les data initiales
# On réintégrera la notion de groupes de pays par la suite 

# On ne garde que les données des émissions de CO2

data_co2_pays=data[data['Indicator Code'] == 'EN.ATM.CO2E.KT']

# On supprime les groupes de pays pour avoir une table contenant uniquement les pays

liste = ['ARB','CSS','CEB','EAR','EAS','EAP','TEA','EMU','ECS','ECA','TEC','EUU','FCS','HPC',
'HIC','IBD','IBT','IDB','IDX','IDA','LTE','LCN','LDC','LAC','TLA',' UN classification','LMY','LIC',
'LMC','MEA','MNA','TMN','MIC','NAC','INX','OED','OSS','PSS','PST','PRE','SST','SAS','TSA','SSF',
'SSA','TSS','UMC','WLD']

for i in liste:
    data_co2_pays=data_co2_pays[data_co2_pays['Country Code'] != i]

# On ajoute à ces infos, la région du pays 

country_groupes = country[["Country Code","Region"]]

data_groupe_pays=pd.merge(data_co2_pays,country_groupes, on =["Country Code"], how='inner')

data_groupe_pays.drop(['Country Code','Indicator Name','Indicator Code','2015','2016','2017','Unnamed: 62'],axis=1,inplace=True)


# 2 - Calcul de la part de chaque région dans les émissions de CO2 pour 2014

# Calcul de la part en faisant : somme de chaque groupe / somme totale

gb = data_groupe_pays.groupby('Region')['2014']
data_groupe_pays['part_groupe'] = gb.transform('sum') / data_groupe_pays['2014'].sum()

emission_par_groupe = data_groupe_pays.groupby(['Region'])['part_groupe'].first()

# Représentation graphique

labels = 'East Asia & Pacific', 'Europe & Central Asia', 'Latin America & Caribbean', 'Middle East & North Africa','North America','South Asia','Sub-Saharan Africa'
plt.pie(emission_par_groupe,autopct='%.0f%%',labels=labels,shadow=True, radius=0.5)

# 3 - TOP 20 des pays avec les émissions de CO2 les plus importantes

# On utilise la table data_co2_pays qui contient les émissions de CO2 par pays
# On la trie par ordre décroissant et on ne garde que les 20 premières observations

sort_2014 = data_co2_pays.sort_values(['2014'],ascending = False, na_position='last')
sort_2014_20best=sort_2014[['Country Name', '2014']].head(20)

# Représentation graphique

sort_2014_20best.plot(kind='bar', x='Country Name')


######################################################
#    III - ANALYSE PRELIMINAIRE AU NIVEAU REGIONAL
#          SUR LES EMISSIONS DE CO2 PAR PERSONNE    
######################################################

# 1 - Table avec les données d'émission de CO2 par personne en 1994 et 2014
# On prend ces 2 dates pour voir l'évolution en 20 ans => voir si certains pays baissent leurs émissions par personne

data_co2_per_capita=data[data['Indicator Code'] == 'EN.ATM.CO2E.PC']
data_co2_per_capita=data_co2_per_capita[["Country Name","Country Code","1994","2014"]]

# On supprime les groupes de pays pour avoir une table contenant uniquement les pays

liste = ['ARB','CSS','CEB','EAR','EAS','EAP','TEA','EMU','ECS','ECA','TEC','EUU','FCS','HPC',
'HIC','IBD','IBT','IDB','IDX','IDA','LTE','LCN','LDC','LAC','TLA',' UN classification','LMY','LIC',
'LMC','MEA','MNA','TMN','MIC','NAC','INX','OED','OSS','PSS','PST','PRE','SST','SAS','TSA','SSF',
'SSA','TSS','UMC','WLD']

for i in liste:
    data_co2_per_capita=data_co2_per_capita[data_co2_per_capita['Country Code'] != i]

# On ajoute à ces infos, la région du pays

country_groupes = country[["Country Code","Region"]]

co2_per_capita_groupe=pd.merge(data_co2_per_capita,country_groupes, on =["Country Code"], how='inner')

# 2 - Analyse de l'émission moyenne par personne pour chaque région

co2_per_capita_groupe['mean_per_capita'] = co2_per_capita_groupe.groupby('Region')['2014'].transform('mean')

emission_par_capita_groupe = co2_per_capita_groupe.groupby(['Region'])['mean_per_capita'].first()

# Représentation graphique

emission_par_capita_groupe.plot(kind='bar')

# 3 - Emissions de CO2 par personne pour les 20 plus gros pollueurs identifiés précédemment
# (avec comparaison entre 1994 et 2014)

co2_per_capita_gros_pollueurs = pd.merge(data_co2_per_capita, sort_2014_20best, on = ["Country Name"], how='inner')
co2_per_capita_gros_pollueurs.drop(["2014_y"], axis=1, inplace = True)
co2_per_capita_gros_pollueurs.rename(columns={"2014_x":"2014"}, inplace=True)

# Représentation graphique

co2_per_capita_gros_pollueurs.sort_values(['2014'],ascending = False, na_position='last').plot.bar(x="Country Name")




