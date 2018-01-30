import pandas as pd
import matplotlib.pyplot as plt

'''
Objectif de ce code : 
Avoir une vision globale des émissions de CO2 au niveau monde
- Evolution entre 1960 et 2014
- Part de chaque type d'énergie dans les émissions de CO2
- Part de chaque secteur dans les émissions de CO2
'''

################################
#    I - IMPORT DES DONNEES    #
################################

data = pd.read_csv('C:\\Users\\mcoug\\Dropbox\\Etude de cas iAdvize\\Data\\WDI\\WDIData.csv', sep=',')
country_series = pd.read_csv('C:\\Users\\mcoug\\Dropbox\\Etude de cas iAdvize\\Data\\WDI\\WDICountry-Series.csv', sep=',')
country = pd.read_csv('C:\\Users\\mcoug\\Dropbox\\Etude de cas iAdvize\\Data\\WDI\\WDICountry.csv', sep=',')
footnote = pd.read_csv('C:\\Users\\mcoug\\Dropbox\\Etude de cas iAdvize\\Data\\WDI\\WDIFootNote.csv', sep=',')
series_1= pd.read_csv('C:\\Users\\mcoug\\Dropbox\\Etude de cas iAdvize\\Data\\WDI\\WDISeries.csv', sep=',')
series_time = pd.read_csv('C:\\Users\\mcoug\\Dropbox\\Etude de cas iAdvize\\Data\\WDI\\WDISeries-Time.csv', sep=',')

#####################################################
#    II - ANALYSE PRELIMINAIRE AU NIVEAU MONDIAL    #
#####################################################


# 1 - EVOLUTION DE L'EMISSION DE CO2 AU NIVEAU MONDE DE 1960 A 2014

# On ne garde que les données Monde

world = data[data['Country Code'] == 'WLD']

# On ne garde que les données concernant les émissions de CO2

world_co2_emission = world[world['Indicator Code'] == 'EN.ATM.CO2E.KT']

# On nettoie la table pour ne garder que les champs qui nous intéresse

world_co2_emission.drop(['Country Code','Indicator Name','Indicator Code','2015','2016','2017','Unnamed: 62'],axis=1,inplace=True)

# Représentation graphique des données

world_co2_emission.set_index('Country Name').T.plot()


# 2 - PART DE CHAQUE TYPE D'ENERGIE DANS LES EMISSIONS DE CO2 EN 2014

# On crée une table pour chaque type d'énergie avec les données correspondantes sur 2014
# Puis on renomme le champ avec le nom du type d'énergie 

def type_energie(nom,code):
     
    table_energie = world[data['Indicator Code'] == code]
    table_energie = table_energie[['Country Name','2014']]
    table_energie.rename(columns={"2014": "{0}".format(nom)}, inplace=True)
    return table_energie

gaseous_fuel=type_energie('gaseous_fuel','EN.ATM.CO2E.GF.ZS')
liquid_fuel=type_energie('liquid_fuel','EN.ATM.CO2E.LF.ZS')
solid_fuel=type_energie('solid_fuel','EN.ATM.CO2E.SF.ZS')

# On crée la table avec les données sur les 3 types d'énergie

part_energie_dans_emission=pd.merge(pd.merge(gaseous_fuel,liquid_fuel,on='Country Name'),solid_fuel,on='Country Name')

# On ajoute un champ 'Other' pour avoir une somme égale à 100%

part_energie_dans_emission["other"] = 100-(part_energie_dans_emission["gaseous_fuel"]+part_energie_dans_emission["liquid_fuel"]+part_energie_dans_emission["solid_fuel"])

# Représentation graphique des données

part_energie_dans_emission.plot.barh()

# 3 - PART DE CHAQUE SECTEUR DANS LES EMISSIONS DE CO2

# On crée une table pour chaque secteur avec les données correspondantes sur 2014
# Puis on renomme le champ avec le nom du secteur

def secteurs(nom,code):
     
    table_secteurs = world[data['Indicator Code'] == code]
    table_secteurs = table_secteurs[['Country Name','2014']]
    table_secteurs.rename(columns={"2014": "{0}".format(nom)}, inplace=True)
    return table_secteurs

buildings=secteurs('buildings','EN.CO2.BLDG.ZS')
electricity=secteurs('electricity and heat production','EN.CO2.ETOT.ZS')
industries=secteurs('industries and construction','EN.CO2.MANF.ZS')
transport=secteurs('transport','EN.CO2.TRAN.ZS')
other=secteurs('other','EN.CO2.OTHX.ZS')

# On crée la table avec les données sur les 5 secteurs

part_secteurs_dans_emission=buildings.merge(electricity,on='Country Name').merge(industries,on='Country Name').merge(transport,on='Country Name').merge(other,on='Country Name')

# Représentation graphique des données

labels = 'buildings', 'electricity', 'industries', 'transport','other'
plt.pie(part_secteurs_dans_emission.set_index('Country Name').T,autopct='%.0f%%',labels=labels,shadow=True, radius=0.5)



