import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import requests
import seaborn as sns
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BALLDONTLIE_API_KEY")
BASE_URL = "https://api.balldontlie.io/v1"
SEASON = 2025

GRAFICOS_DIR = Path("graficos")
GRAFICOS_DIR.mkdir(exist_ok=True)

PLAYER_IDS_COMPARACAO = {
    "Stephen Curry": 115,
    "LeBron James": 237,
}


def verificar_chave():
    if not API_KEY:
        raise RuntimeError(
            "Chave da API não encontrada. "
            "Crie um arquivo .env baseado em .env.example e "
            "adicione BALLDONTLIE_API_KEY."
        )


def requisicao_api(endpoint, params=None):
    verificar_chave()

    headers = {
        "Authorization": API_KEY
    }

    url = f"{BASE_URL}/{endpoint}"

    try:
        resposta = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=30
        )
        resposta.raise_for_status()
        return resposta.json()

    except requests.exceptions.HTTPError as erro:
        if resposta.status_code == 401:
            raise RuntimeError(
                "A chave da API é inválida ou não foi aceita."
            ) from erro

        if resposta.status_code == 429:
            raise RuntimeError(
                "Limite de requisições da API atingido. "
                "Tente novamente mais tarde."
            ) from erro

        raise RuntimeError(
            f"Erro HTTP {resposta.status_code}: {resposta.text}"
        ) from erro

    except requests.exceptions.RequestException as erro:
        raise RuntimeError(
            f"Não foi possível conectar à API: {erro}"
        ) from erro


def buscar_estatisticas_temporada(season=SEASON):
    params = {
        "seasons[]": season,
        "per_page": 100,
    }

    dados = requisicao_api("stats", params)

    registros = dados.get("data", [])

    if not registros:
        raise RuntimeError(
            f"Nenhuma estatística encontrada para a temporada {season}."
        )

    return registros


def estatisticas_para_dataframe(registros):
    linhas = []

    for item in registros:
        jogador = item.get("player") or {}
        time = item.get("team") or {}

        linhas.append({
            "player_id": jogador.get("id"),
            "jogador": (
                f"{jogador.get('first_name', '')} "
                f"{jogador.get('last_name', '')}"
            ).strip(),
            "time": time.get("full_name", "N/A"),
            "jogo_id": (item.get("game") or {}).get("id"),
            "minutos": item.get("min"),
            "pontos": item.get("pts", 0),
            "rebotes": item.get("reb", 0),
            "assistencias": item.get("ast", 0),
            "roubos": item.get("stl", 0),
            "tocos": item.get("blk", 0),
            "turnovers": item.get("turnover", 0),
            "fg_pct": item.get("fg_pct", 0),
            "fg3_pct": item.get("fg3_pct", 0),
            "ft_pct": item.get("ft_pct", 0),
        })

    df = pd.DataFrame(linhas)

    colunas_numericas = [
        "pontos",
        "rebotes",
        "assistencias",
        "roubos",
        "tocos",
        "turnovers",
        "fg_pct",
        "fg3_pct",
        "ft_pct",
    ]

    for coluna in colunas_numericas:
        df[coluna] = pd.to_numeric(
            df[coluna],
            errors="coerce"
        ).fillna(0)

    return df


def calcular_medias(df):
    medias = (
        df.groupby(["player_id", "jogador", "time"], as_index=False)
        .agg(
            jogos=("jogo_id", "nunique"),
            pontos=("pontos", "mean"),
            rebotes=("rebotes", "mean"),
            assistencias=("assistencias", "mean"),
            roubos=("roubos", "mean"),
            tocos=("tocos", "mean"),
            turnovers=("turnovers", "mean"),
        )
    )

    return medias.round(2)


def mostrar_ranking(medias, coluna, titulo, quantidade=10):
    ranking = (
        medias.sort_values(coluna, ascending=False)
        .head(quantidade)
        .reset_index(drop=True)
    )

    ranking.index += 1

    print(f"\n{'=' * 60}")
    print(titulo)
    print(f"{'=' * 60}")

    colunas = ["jogador", "time", "jogos", coluna]

    print(
        ranking[colunas].to_string(
            index=True,
            justify="left"
        )
    )

    return ranking


def buscar_media_jogador(medias, player_id):
    jogador = medias[medias["player_id"] == player_id]

    if jogador.empty:
        return None

    return jogador.iloc[0]


def desafio_1(medias):
    nomes = list(PLAYER_IDS_COMPARACAO.keys())

    dados = []

    for nome in nomes:
        player_id = PLAYER_IDS_COMPARACAO[nome]
        jogador = buscar_media_jogador(medias, player_id)

        if jogador is not None:
            dados.append({
                "jogador": nome,
                "Pontos": jogador["pontos"],
                "Rebotes": jogador["rebotes"],
                "Assistências": jogador["assistencias"],
            })

    if len(dados) < 2:
        print(
            "\nNão foi possível encontrar os dois jogadores "
            "para a comparação."
        )
        return

    comparacao = pd.DataFrame(dados)

    comparacao_grafico = comparacao.melt(
        id_vars="jogador",
        var_name="estatistica",
        value_name="media"
    )

    plt.figure(figsize=(10, 6))

    sns.barplot(
        data=comparacao_grafico,
        x="estatistica",
        y="media",
        hue="jogador"
    )

    plt.title(
        f"Comparação de médias - {nomes[0]} x {nomes[1]}"
    )
    plt.xlabel("Estatística")
    plt.ylabel("Média por jogo")
    plt.tight_layout()

    caminho = GRAFICOS_DIR / "comparacao_jogadores.png"
    plt.savefig(caminho, dpi=150)
    plt.close()

    print("\nDESAFIO 1")
    print(comparacao.to_string(index=False))
    print(f"\nGráfico salvo em: {caminho}")


def desafio_2(medias):
    ranking = (
        medias.sort_values("pontos", ascending=False)
        .head(10)
        .copy()
    )

    ranking = ranking.sort_values("pontos", ascending=True)

    plt.figure(figsize=(10, 7))

    sns.barplot(
        data=ranking,
        x="pontos",
        y="jogador",
        orient="h"
    )

    plt.title(
        f"Top 10 jogadores - Média de pontos por jogo ({SEASON})"
    )
    plt.xlabel("Média de pontos")
    plt.ylabel("Jogador")
    plt.tight_layout()

    caminho = GRAFICOS_DIR / "top_10_pontos.png"
    plt.savefig(caminho, dpi=150)
    plt.close()

    print("\nDESAFIO 2")
    print(
        ranking[
            ["jogador", "time", "jogos", "pontos"]
        ]
        .sort_values("pontos", ascending=False)
        .to_string(index=False)
    )

    print(f"\nGráfico salvo em: {caminho}")


def main():
    print("=" * 60)
    print("ESTATÍSTICAS DE JOGOS ESPORTIVOS - NBA")
    print("API: BALLDONTLIE")
    print("=" * 60)

    print(f"\nColetando estatísticas da temporada {SEASON}...")

    registros = buscar_estatisticas_temporada()

    print(f"Registros recebidos da API: {len(registros)}")

    df = estatisticas_para_dataframe(registros)

    print(f"Jogadores encontrados nos registros: {df['jogador'].nunique()}")

    medias = calcular_medias(df)

    print(f"Jogadores após agrupamento: {len(medias)}")

    mostrar_ranking(
        medias,
        "pontos",
        "RANKING - MÉDIA DE PONTOS POR JOGO"
    )

    mostrar_ranking(
        medias,
        "rebotes",
        "RANKING - MÉDIA DE REBOTES POR JOGO"
    )

    mostrar_ranking(
        medias,
        "assistencias",
        "RANKING - MÉDIA DE ASSISTÊNCIAS POR JOGO"
    )

    desafio_1(medias)

    desafio_2(medias)

    print("\n" + "=" * 60)
    print("ANÁLISE CONCLUÍDA!")
    print(f"Confira os gráficos na pasta: {GRAFICOS_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
