import matplotlib.pyplot as ptl
import numpy as np
from scipy.stats import kendalltau
import pandas as pd
import seaborn as sns
import argparse
import sys, os
import fnmatch


paths = []
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', nargs='+', help='<Required> Set flag', required=False)

for _, value in parser.parse_args()._get_kwargs():
    if value is not None:
        paths = paths + value

if len(paths) == 0:
    print("Paths empty adding local path")
    paths.append(os.path.dirname(os.path.abspath(sys.argv[0])))

graphs_txt = []
print('Searching in: ', paths)
for i in paths:
    for x in os.walk(i):
        for file in os.listdir(x[0]):
            if fnmatch.fnmatch(file,'*.txt'):
                graphs_txt.append((x[0].replace('\\', '/'), file))

sns.set(style="ticks")
for dir, file in graphs_txt:
    print("\tDrawing graphs of: ", dir + "/" +file )
    data = np.genfromtxt(dir+ "/" + file, delimiter=";")
    
    ds = pd.DataFrame(data={'Generation': data[:, 0], 'Fitness': data[:, 1], 'Type': 'Individual'})
    clean_ds = ds.copy()

    # DEPRECATED
    '''
    sns.jointplot(data[:,0], data[:,1],kind="hex", stat_func=kendalltau, color="#4CB391", ratio=4)
    ptl.savefig(dir + "/" + file + ".hex.png", pad_inches=1.25)
    ptl.clf()

    ds["Generation"] = round(ds["Generation"]/200)
    sns.boxplot(x="Generation", y="Fitness", data=ds,size=18)
    ptl.savefig(dir + "/" + file + ".box.png",  pad_inches=1.25)
    ptl.clf()

    sns.violinplot(x="Generation", y="Fitness",data=ds,palette="muted",size=18)
    ptl.savefig(dir + "/" + file + ".violin.png",  pad_inches=1.25)
    ptl.clf()
    '''

    tsplot_df = clean_ds.copy()
    #tsplot_df["Generation"] = round(tsplot_df["Generation"])
    df = tsplot_df[["Fitness", "Generation"]]
    gens = df.groupby(by="Generation", as_index=False)
    mean = gens.mean()["Fitness"].as_matrix()
    x = gens.mean()["Generation"].as_matrix()
    sd = gens.std()
    sd = sd.fillna(0)["Fitness"].as_matrix()
    cis = (mean - sd, mean + sd)
    ptl.clf()
    ptl.fill_between(x, cis[0], cis[1], alpha=0.2)
    ptl.plot(x, mean)
    ptl.margins(x=0)
    ptl.xlabel("Generace")
    ptl.ylabel("Fitness")
    ptl.tight_layout()
    ptl.savefig(dir + "/" + file + ".tsplot.pdf",dpi=900,format="pdf", pad_inches=2)
    ptl.clf()

    print("\t\tFinished")
