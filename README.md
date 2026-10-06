🚀 APIs Externas com Python - Projetos Avançados

Bem-vindo à nova coleção de desafios do repositório APIs-Externas!

Nesta fase do projeto, elevamos o nível de complexidade integrando Processamento de Linguagem Natural (NLP), catálogos literários e estatísticas esportivas em tempo real. Continuamos explorando o consumo de APIs RESTful, agora com foco em análise de dados avançada e geração de mídia (áudio).

💻 Desafios Realizados

4️⃣ Conversor de Texto em Voz com Emoções 🎙️

Um sistema inteligente que analisa o sentimento de um texto e o converte em áudio, gerando insights visuais sobre a polaridade das frases.

API Utilizada: AssemblyAI / HuggingFace API

Objetivo: Analisar sentimentos de textos (positivo, negativo, neutro) e converter os resultados em áudio, além de plotar um gráfico de polaridade.

Bibliotecas: requests, textblob, pyttsx3, matplotlib

Conceitos Aplicados: APIs com autenticação via Token, Análise de Sentimentos, Text-to-Speech (TTS).

Desafios Extras Concluídos:

✅ Salvamento automático dos arquivos de áudio categorizados como textos positivos ou negativos.

✅ Automação para "leitura" sequencial de diferentes textos baseada nos sentimentos detectados.

5️⃣ Sistema de Busca de Livros 📚

Um buscador literário robusto que consome o acervo do Google e estrutura os dados de forma analítica.

API Utilizada: Google Books API

Objetivo: Buscar livros por título ou autor e gerar gráficos de tendências sobre os gêneros e anos de publicação.

Bibliotecas: requests, pandas, matplotlib

Conceitos Aplicados: Requisições com parâmetros de URL (Query Strings) e estruturação de tabelas de dados.

Desafios Extras Concluídos:

✅ Filtro de ordenação para isolar e exibir os 10 livros mais antigos do resultado da busca.

✅ Visualização de dados mostrando a quantidade de livros, distribuição de gêneros e anos em um gráfico consolidado.

6️⃣ Estatísticas de Jogos Esportivos 🏀

Uma ferramenta de análise esportiva para fãs e analistas, focada na extração e comparação de métricas de atletas.

API Utilizada: API Sports (Free Tier) / balldontlie (NBA)

Objetivo: Coletar estatísticas detalhadas de times e jogadores, estruturando tudo em rankings, médias e gráficos comparativos.

Bibliotecas: requests, pandas, seaborn, matplotlib

Conceitos Aplicados: Tratamento e paginação de listas complexas em JSON, criação e manipulação de rankings.

Desafios Extras Concluídos:

✅ Comparação direta de estatísticas de dois jogadores diferentes exibida em um gráfico lado a lado.

✅ Motor de cálculo para gerar médias da temporada e rankings dinâmicos de performance.

🛠️ Como executar o projeto na sua máquina

Siga os passos abaixo para testar os scripts localmente com total segurança:

Clone o repositório:

git clone https://github.com/souzzaParabolica/APIs-Externas.git
cd APIs-Externas


Crie um ambiente virtual (Recomendado):

python -m venv venv
source venv/bin/activate  # No Linux/Mac
venv\Scripts\activate     # No Windows


Instale as dependências:

pip install requests textblob pyttsx3 pandas matplotlib seaborn python-dotenv


Configuração de Segurança (Chaves de API):

Este projeto utiliza a biblioteca python-dotenv para proteger as chaves das APIs.

Crie um arquivo chamado .env na raiz do projeto (ou dentro da pasta de cada desafio).

Renomeie ou copie o conteúdo do arquivo .env.example para o seu novo arquivo .env e insira as suas chaves reais:

ASSEMBLYAI_KEY=sua_chave_aqui
HUGGINGFACE_KEY=sua_chave_aqui
SPORTS_API_KEY=sua_chave_aqui


Atenção: O arquivo .env já está no .gitignore para garantir que suas credenciais não sejam enviadas para o GitHub.

👨‍💻 Autor

Desenvolvido por souzzaParabolica.
