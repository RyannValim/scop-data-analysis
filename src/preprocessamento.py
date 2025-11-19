from typing import Tuple
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder

def pre_processar_dados(
    df: pd.DataFrame,
    nome_coluna_classe: str = "classe"
) -> Tuple[object, object, LabelEncoder, StandardScaler]:
    X = df.drop(columns=[nome_coluna_classe])
    y = df[nome_coluna_classe]

    normalizador = StandardScaler(with_mean=False)
    X_normalizado = normalizador.fit_transform(X)

    codificador_rotulos = LabelEncoder()
    y_codificado = codificador_rotulos.fit_transform(y)

    return X_normalizado, y_codificado, codificador_rotulos, normalizador