from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def composicao_aminoacidos(sequencias):
    todos = "".join(sequencias).upper()
    cont = Counter(todos)
    plt.figure(figsize=(8,4))
    sns.barplot(x=list(cont.keys()), y=list(cont.values()))
    plt.title("Frequência de aminoácidos")
    plt.xlabel("Aminoácido"); plt.ylabel("Frequência")
    plt.tight_layout(); plt.show()

def comparar_listas_ids(cab1, cab2):
    import re
    id1 = {re.search(r"[a-zA-Z0-9_]+", h).group() for h in cab1}
    id2 = {re.search(r"[a-zA-Z0-9_]+", h).group() for h in cab2}
    inter = id1 & id2
    print(f"IDs arquivo 1: {len(id1)} | arquivo 2: {len(id2)} | em comum: {len(inter)}")
    if inter:
        print("Exemplos:", list(inter)[:5])

def rodar_kmeans(Xp, k=5, random_state=42):
    km = KMeans(n_clusters=k, random_state=random_state, n_init=20)
    y = km.fit_predict(Xp)
    return y, km

def avaliar_silhueta(Xp, y):
    return silhouette_score(Xp, y)

def grafico_pca_clusters(Xp, y, titulo="Clusters K-Means (PCA)"):
    plt.figure(figsize=(7,6))
    plt.scatter(Xp[:,0], Xp[:,1], c=y, alpha=0.7, cmap="tab20")
    plt.title(titulo); plt.xlabel("PC1"); plt.ylabel("PC2")
    plt.tight_layout(); plt.show()

def dashboard_exploratorio(sequencias, classes):
    tamanhos = [len(s) for s in sequencias]
    aa = "".join(sequencias).upper()
    cont_aa = Counter(aa)
    cont_cls = Counter(classes)

    plt.figure(figsize=(16,9))

    plt.subplot(2,2,1)
    sns.histplot(tamanhos, bins=20, kde=True)
    plt.title("Distribuição dos comprimentos")

    plt.subplot(2,2,2)
    top = dict(cont_cls.most_common(10))
    sns.barplot(x=list(top.keys()), y=list(top.values()))
    plt.title("Top 10 classes SCOP"); plt.xticks(rotation=45)

    plt.subplot(2,2,3)
    sns.barplot(x=list(cont_aa.keys()), y=list(cont_aa.values()))
    plt.title("Composição de aminoácidos")

    plt.subplot(2,2,4)
    amino = 'ACDEFGHIKLMNPQRSTVWY'
    V = np.array([[s.count(a) for a in amino] for s in sequencias])
    from sklearn.decomposition import PCA
    coords = PCA(n_components=2).fit_transform(V)
    plt.scatter(coords[:,0], coords[:,1], alpha=0.6)
    plt.title("PCA da composição por sequência")

    plt.tight_layout(); plt.show()
