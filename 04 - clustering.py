import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


'''
Objectif de ce code : 
Construire des groupes de pays présentant les mêmes caractéristiques (sur 2014)
Nous avons pris le parti ici de se focaliser sur des caractéristiques environnementale

- Construction de la segmentation avec la méthode K-means 
- Interprétation des clusters identifiés
'''

################################
#    I - IMPORT DES DONNEES    
################################

data = pd.read_csv('C:\\etude_cas_mcougul\\data\\WDIData.csv', sep=',')
country = pd.read_csv('C:\\etude_cas_mcougul\\data\\WDICountry.csv', sep=',')
series_1= pd.read_csv('C:\\etude_cas_mcougul\\data\\WDISeries.csv', sep=',')


###################################
#    II - PREPARATION DES DONNEES    
###################################

# On filtre les data sur les pays 

data_pays=data[['Country Code','Country Name','Indicator Code','2014']]

liste = ['ARB','CSS','CEB','EAR','EAS','EAP','TEA','EMU','ECS','ECA','TEC','EUU','FCS','HPC',
'HIC','IBD','IBT','IDB','IDX','IDA','LTE','LCN','LDC','LAC','TLA',' UN classification','LMY','LIC',
'LMC','MEA','MNA','TMN','MIC','NAC','INX','OED','OSS','PSS','PST','PRE','SST','SAS','TSA','SSF',
'SSA','TSS','UMC','WLD']

for i in liste:
    data_pays=data_pays[data_pays['Country Code'] != i]
    

# On garde uniquement les indicateurs qui nous intéresse pour la clusterisation
# cf. les indicateurs identifiés précédemment

list_kpis = ['EN.ATM.CO2E.GF.ZS',
'EN.CO2.ETOT.ZS',
'EN.ATM.CO2E.SF.ZS',
'EN.CO2.TRAN.ZS',
'EG.USE.COMM.CL.ZS',
'EN.CO2.BLDG.ZS',
'EN.CO2.OTHX.ZS',
'EN.ATM.CO2E.LF.ZS',
'EG.USE.CRNW.ZS']

data_pays_clustering=data_pays[data_pays["Indicator Code"]=='EN.ATM.CO2E.PC']
data_pays_clustering.drop(['Indicator Code'],axis=1,inplace=True)
data_pays_clustering.rename(columns={'2014':'EN.ATM.CO2E.PC'},inplace = True)

for i in list_kpis:
    ajout_kpi=data_pays[data_pays["Indicator Code"]==i]
    ajout_kpi.drop(['Country Name'], axis=1, inplace = True)
    data_pays_clustering = pd.merge(data_pays_clustering,ajout_kpi,on=['Country Code'],how='inner')
    data_pays_clustering.drop(['Indicator Code'],axis=1,inplace=True)
    data_pays_clustering.rename(columns={'2014':i} ,inplace = True)  


# Suppression des valeurs manquantes

data_pays_clustering=data_pays_clustering.dropna(axis=0)

# Table finale

x = data_pays_clustering.drop(["Country Name","Country Code"],axis=1)


###################################
#    III - CLUSTERISATION
###################################

# 1 - On utilise la méthode elbow pour trouver le nombre optimal de clusters

from sklearn.cluster import KMeans
from sklearn import cluster
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters = i, init = 'k-means++', random_state = 0)
    kmeans.fit(x)
    wcss.append(kmeans.inertia_) #attribut inertia_ qui est en fait le calcul de wcss
plt.plot(range(1, 11), wcss) #plot(abscisse, ordonnée) => range(1,11) pour avoir chaque nb entre 1 et 10
plt.title('La méthode Elbow')
plt.xlabel('Nombre de clusters')
plt.ylabel('WCSS')
plt.show()

# 2 - K-means 
kmeans = cluster.KMeans(n_clusters=4,init = 'k-means++',random_state=0)
kmeans.fit(x)
y_kmeans = kmeans.predict(x)

# index triés des groupes
idk = np.argsort(kmeans.labels_)
# affichage des observations et leurs groupes
classe=pd.DataFrame(kmeans.labels_[idk],x.index[idk])

# 3 - Fusion avec les données

clustering=pd.merge(data_pays_clustering,classe,left_index=True,right_index=True)
clustering.rename(columns={'EN.ATM.CO2E.GF.ZS' : 'CO2 emissions from gaseous fuel',
'EN.CO2.ETOT.ZS' : 'CO2 emissions from elec and heat prod',
'EN.ATM.CO2E.SF.ZS' : 'CO2 emissions from solid fuel',
'EN.CO2.TRAN.ZS' : 'CO2 emissions from transport',
'EG.USE.COMM.CL.ZS' : 'Alternative and nuclear energy',
'EN.CO2.BLDG.ZS' : 'CO2 emissions from buildings',
'EN.CO2.OTHX.ZS' : 'CO2 emissions from other sectors',
'EN.ATM.CO2E.LF.ZS' : 'CO2 emissions from liquid fuel',
'EG.USE.CRNW.ZS' : 'Combustible renewables and waste',
'EN.ATM.CO2E.PC' : 'emission co2 capita'},inplace=True)

###################################
#    IV - INTERPRETATION
###################################

# On crée des indices de sur ou sous représentation basés sur la moyenne tous pays confondus
# (base 100 => si l'indice est égal à 100 pour une classe, cela veut dire que la moyenne de 
# la classe = moyenne tous pays confondus)

gb=clustering.groupby(kmeans.labels_)
interpret_groups = gb.mean() / clustering.mean() * 100
interpret_groups.rename(columns={'EN.ATM.CO2E.GF.ZS' : 'CO2 emissions from gaseous fuel',
'EN.CO2.ETOT.ZS' : 'CO2 emissions from elec and heat prod',
'EN.ATM.CO2E.SF.ZS' : 'CO2 emissions from solid fuel',
'EN.CO2.TRAN.ZS' : 'CO2 emissions from transport',
'EG.USE.COMM.CL.ZS' : 'Alternative and nuclear energy',
'EN.CO2.BLDG.ZS' : 'CO2 emissions from buildings',
'EN.CO2.OTHX.ZS' : 'CO2 emissions from other sectors',
'EN.ATM.CO2E.LF.ZS' : 'CO2 emissions from liquid fuel',
'EG.USE.CRNW.ZS' : 'Combustible renewables and waste',
'EN.ATM.CO2E.PC' : 'emission co2 capita'},inplace=True)

# Nombre de pays par cluster

clustering["Country Name"].groupby(kmeans.labels_).count()

###################################
#    V - VISUALISATION
###################################

clustering["classe"]=clustering.iloc[:, -1].values

colors = {0:'blue', 1:'red', 2:'green', 3:'black'}

clustering.plot.scatter(x='CO2 emissions from solid fuel', y='CO2 emissions from gaseous fuel', c=clustering["classe"].apply(lambda x: colors[x]))
clustering.plot.scatter(x='CO2 emissions from gaseous fuel', y='Combustible renewables and waste', c=clustering["classe"].apply(lambda x: colors[x]))

