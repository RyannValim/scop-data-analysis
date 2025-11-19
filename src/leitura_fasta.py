from typing import List, Tuple

def extrair_classe_do_cabecalho(cabecalho: str) -> str:
    partes = cabecalho.split()
    if len(partes) > 1:
        return partes[1]
    return "UNKNOWN"

def carregar_sequencias_fasta(caminho_arquivo: str) -> List[Tuple[str, str]]:
    lista_cabecalho_sequencia: List[Tuple[str, str]] = []

    cabecalho_atual: str | None = None
    linhas_sequencia: list[str] = []

    with open(caminho_arquivo, "r") as arquivo:
        for linha in arquivo:
            linha = linha.strip()

            if not linha:
                continue

            if linha.startswith(">"):
                if cabecalho_atual is not None and linhas_sequencia:
                    sequencia_completa = "".join(linhas_sequencia)
                    classe = extrair_classe_do_cabecalho(cabecalho_atual)
                    lista_cabecalho_sequencia.append((classe, sequencia_completa))

                cabecalho_atual = linha
                linhas_sequencia = []
            else:
                linhas_sequencia.append(linha)

        if cabecalho_atual is not None and linhas_sequencia:
            sequencia_completa = "".join(linhas_sequencia)
            classe = extrair_classe_do_cabecalho(cabecalho_atual)
            lista_cabecalho_sequencia.append((classe, sequencia_completa))

    return lista_cabecalho_sequencia