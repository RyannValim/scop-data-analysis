from typing import Tuple

import numpy as np
from sklearn.decomposition import PCA


def aplicar_pca(
    X: np.ndarray,
    n_componentes: int = 100,
    seed: int = 42
) -> Tuple[np.ndarray, PCA]:
    n_componentes_efetivos = min(n_componentes, X.shape[1])

    modelo_pca = PCA(
        n_components=n_componentes_efetivos,
        random_state=seed
    )

    X_pca = modelo_pca.fit_transform(X)

    return X_pca, modelo_pca