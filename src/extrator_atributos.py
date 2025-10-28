import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

AMINOACIDOS = "ACDEFGHIKLMNPQRSTVWY"

def gerar_vocabulario_pares_2x2():
    # todos os pares 2x2 com skip (representado por 'X' no meio)
    return [f"{a1}{a2}X{a3}{a4}"
            for a1 in AMINOACIDOS for a2 in AMINOACIDOS
            for a3 in AMINOACIDOS for a4 in AMINOACIDOS]

def extrair_kmer_2x2(sequencia: str, skip: int = 2):
    """
    Extrai todos os padrões 'AA X BB' (2 aa, pula 'skip', + 2 aa).
    Ex.: 'ACDE...' com skip=2 -> AC X DE
    """
    seq = sequencia.upper()
    pares = []
    for i in range(len(seq) - (2 + skip + 1)):
        p1 = seq[i:i+2]
        p2 = seq[i+skip:i+skip+2]
        if len(p1) == 2 and len(p2) == 2:
            pares.append(f"{p1}X{p2}")
    return pares

def montar_matriz_binaria(sequencias, skip=2, limite_sequencias=400):
    voc = gerar_vocabulario_pares_2x2()
    idx = {p: i for i, p in enumerate(voc)}
    n = min(limite_sequencias, len(sequencias))
    M = np.zeros((n, len(voc)), dtype=int)

    for i in range(n):
        presentes = set(extrair_kmer_2x2(sequencias[i], skip=skip))
        for p in presentes:
            if p in idx:
                M[i, idx[p]] = 1

    # retira colunas sem variância (tudo 0)
    variancia = np.var(M, axis=0)
    M = M[:, variancia > 0]
    return M

def normalizar(M):
    return StandardScaler().fit_transform(M)

def reduzir_pca(X, n_componentes=300):
    # garante limites (pca não aceita mais componentes que min(n_amostras-1, n_features))
    n_max = min(X.shape[0]-1, X.shape[1], n_componentes)
    pca = PCA(n_components=max(2, n_max))
    Xp = pca.fit_transform(X)
    return Xp, pca
