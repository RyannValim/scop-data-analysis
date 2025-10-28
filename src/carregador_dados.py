import re
from collections import Counter

def carregar_fasta(caminho_fasta: str):
    """
    Lê um arquivo FASTA (header começando com '>') e devolve:
    - cabecalhos: list[str]
    - sequencias: list[str]
    - classes: list[str] (ex.: 'a.1.1.1' ou 'desconhecida')
    """
    sequencias, cabecalhos, classes = [], [], []
    try:
        with open(caminho_fasta, "r") as arq:
            cab_atual, seq_atual = "", ""
            for linha in arq:
                linha = linha.strip()
                if linha.startswith(">"):
                    if cab_atual and seq_atual:
                        cabecalhos.append(cab_atual)
                        sequencias.append(seq_atual)
                        m = re.search(r"a\.\d+\.\d+\.\d+", cab_atual)
                        classes.append(m.group() if m else "desconhecida")
                    cab_atual, seq_atual = linha, ""
                elif linha:
                    seq_atual += linha
            if cab_atual and seq_atual:
                cabecalhos.append(cab_atual)
                sequencias.append(seq_atual)
                m = re.search(r"a\.\d+\.\d+\.\d+", cab_atual)
                classes.append(m.group() if m else "desconhecida")

        print(f"✅ {len(sequencias)} sequências carregadas de {caminho_fasta}")
        return cabecalhos, sequencias, classes
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {caminho_fasta}")
        return [], [], []

def estatisticas_basicas(sequencias, classes):
    tamanhos = [len(s) for s in sequencias]
    print("\n=== ESTATÍSTICAS BÁSICAS ===")
    print(f"Total de sequências: {len(sequencias)}")
    print(f"Mín/Máx/Média: {min(tamanhos)} / {max(tamanhos)} / {sum(tamanhos)/len(tamanhos):.1f}")
    cont = Counter(classes)
    print("Top classes:")
    for c, q in cont.most_common(10):
        print(f"  {c}: {q}")
