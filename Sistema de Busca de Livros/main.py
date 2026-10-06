import os
import pandas as pd
import matplotlib.pyplot as plt
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('buscaLivrosAPIKEY')

url = "https://www.googleapis.com/books/v1/volumes"

busca = input("Digite o título ou o autor: ")

params = {
    "q": busca,
    "maxResults": 10,
    "key": api_key
}

response = requests.get(url, params=params)

if response.status_code == 200:
  data = response.json()
else:
  print("Erro ao consultar a API.")
  exit()

livros = []

for item in data.get("items", []):
  info = item["volumeInfo"]

  livros.append({
      "Título" : info.get("title", "Sem título"),
      "Autor": ", ".join(info.get("authors", ["Desconhecido"])),
      "Ano" : info.get("publishedDate", "Desconhecido"),
      "Gêneros" : ", ".join(info.get("categories", ["Sem gênero"]))
  })

df = pd.DataFrame(livros)
df["Ano"] = pd.to_numeric(
  df["Ano"].astype(str).str[:4],
  errors="coerce"
)

mais_antigos = (
  df.dropna(subset=["Ano"])
    .sort_values("Ano")
    .head(10)
    .reset_index(drop=True)
)
print(mais_antigos)

quantidade_por_ano = df["Ano"].value_counts().sort_index()
quantidade_por_ano.plot(kind="bar")

plt.title("Quantidade de livros por ano")
plt.xlabel("Ano")
plt.ylabel("Quantidade de livros")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()