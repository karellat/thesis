import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import kendalltau
import pandas as pd
import seaborn as sns
import argparse
import sys, os
import fnmatch

parser = argparse.ArgumentParser()
parser.add_argument('-es', help='<Required> give csv with es generations', required=True)
parser.add_argument('-de', help='<Required> give csv with de generations', required=True)
args = parser.parse_args()

es_data = np.genfromtxt(args.es, delimiter=";")
es_df = pd.DataFrame(data={'Generace': es_data[:, 0], 'Fitness': es_data[:, 1]})
es_df['EA'] = "ES"

de_data = np.genfromtxt(args.de,delimiter=";")
de_df = pd.DataFrame(data={'Generace': de_data[:,0], 'Fitness': de_data[:,1]})
de_df['EA'] = "DE"

df = pd.concat([de_df,es_df])
df["Generace"] = round(df["Generace"]/100)

df = df.groupby(by=["Generace","EA"], as_index=False).mean()
sns.factorplot(x="Generace", y="Fitness", hue="EA", data=df, size=10, kind="bar", palette="muted")
sns.despine(offset=10, trim=True)

plt.savefig("ESvsDE.pdf",bbox_inches='tight', format='pdf', dpi=500)
