from typing import List
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, f1_score
from sklearn.model_selection import ParameterGrid
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA

def otimizar_clusterizacao_kmeans(
    X_normalizado,
    y_verdadeiro,
    n_componentes_pca: int = 100,
    tamanho_amostra: int = 5000,
    lista_n_clusters: List[int] = None,
    seed: int = 42
) -> pd.DataFrame:
    if lista_n_clusters is None:
        lista_n_clusters = [3, 5, 8]

    num_amostras_total = X_normalizado.shape[0]

    if num_amostras_total > tamanho_amostra:
        rng = np.random.default_rng(seed)
        indices_amostra = rng.choice(
            num_amostras_total, size=tamanho_amostra, replace=False
        )
        X_amostra = X_normalizado[indices_amostra]
        y_amostra = y_verdadeiro[indices_amostra]
        print(
            f"⚠️ Usando amostra aleatória de "
            f"{tamanho_amostra}/{num_amostras_total} instâncias para otimização."
        )
    else:
        indices_amostra = np.arange(num_amostras_total)
        X_amostra = X_normalizado
        y_amostra = y_verdadeiro
        print(
            f"✔ Usando todas as {num_amostras_total} instâncias "
            "para otimização de parâmetros."
        )

    n_componentes_efetivos = min(n_componentes_pca, X_amostra.shape[1])
    pca = PCA(n_components=n_componentes_efetivos, random_state=seed)
    X_amostra_pca = pca.fit_transform(X_amostra)

    grade_parametros = {
        "n_clusters": lista_n_clusters,
        "random_state": [seed]
    }

    resultados = []

    print("\n===== Iniciando busca de parâmetros para KMeans =====")
    for parametros in ParameterGrid(grade_parametros):
        print(f"\nTestando parâmetros: {parametros}")

        kmeans = KMeans(**parametros)
        rotulos_clusters = kmeans.fit_predict(X_amostra_pca)

        if len(set(rotulos_clusters)) < 2:
            print("  - Ignorado (apenas 1 cluster encontrado).")
            continue

        valor_silhouette = silhouette_score(X_amostra_pca, rotulos_clusters)

        codificador_clusters = LabelEncoder()
        rotulos_clusters_codificados = codificador_clusters.fit_transform(
            rotulos_clusters
        )

        valor_f1 = f1_score(
            y_amostra,
            rotulos_clusters_codificados,
            average="weighted"
        )

        score_combinado = 0.6 * valor_silhouette + 0.4 * valor_f1

        resultados.append({
            "Algoritmo": "KMeans",
            "Parâmetros": parametros,
            "Silhouette": valor_silhouette,
            "F1_Externo": valor_f1,
            "Score_Combinado": score_combinado
        })

        print(f"  - Silhouette:   {valor_silhouette:.4f}")
        print(f"  - F1 Externo:   {valor_f1:.4f}")
        print(f"  - Score Total:  {score_combinado:.4f}")

    if not resultados:
        print("\n⚠️ Nenhum resultado válido foi obtido na otimização.")
        return pd.DataFrame()

    df_resultados = pd.DataFrame(resultados)
    df_resultados = df_resultados.sort_values(
        "Score_Combinado", ascending=False
    ).reset_index(drop=True)

    print("\n===== Resultados Ordenados =====")
    print(df_resultados)

    return df_resultados