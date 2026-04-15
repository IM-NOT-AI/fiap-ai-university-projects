# symptom_extraction/

**Autor:** Isaac Maciel, RM 98222, 2TIAOA, FIAP AI 2026
**Disciplina:** Artificial Intelligence, Challenge 2026, Turno Noturno
**Fase:** 2, modulo NLP, parte 1 de 2
**Notebook de origem:** NB6 - symptom_extraction.ipynb
**Script de enriquecimento:** src/enrich_nb6.py
**Data de geracao:** 11/03/2026

---

## 1. O que e este diretorio

Este diretorio contem os artefatos produzidos pelo NB6 do projeto Cardio-Edge-AI. Sao os outputs do terceiro estagio do pipeline NLP da Fase 2: a extracao de frases sintomaticas clinicas a partir dos 26 documentos PT-BR coletados na Fase 1.

**Analogia:** imagine que a Fase 1 construiu uma biblioteca medica com 26 livros. O NB6 e o bibliotecario treinado que leu todos os livros, sublinhou as frases onde pacientes descrevem queixas, e organizou essas frases em duas listas de entrega: um catalogo completo (o CSV) e uma selecao curada das 10 melhores (o TXT).

---

## 2. Contexto: o Desafio FIAP 2026 e o Cardio-Edge-AI

O projeto Cardio-Edge-AI propoe uma plataforma de cardiologia inteligente com tres nos fisicos:

- **Wearable** (XIAO nRF52840 + ADS1293): capta ECG de 24 bits via BLE 5.0 a 100 Hz, autonomia de 15h com bateria LiPo 750 mAh.
- **Hub** (Raspberry Pi 5 + Google Coral Edge TPU 4 TOPS): processa sinais em borda, executa modelos INT8 sobre espectrogramas STFT 224x224, classifica arritmias sem enviar dados brutos para a nuvem.
- **Lab** (ASUS ROG Strix / Google Colab): retreino de modelos, analise exploratoria, geracao de artefatos NLP.

A Fase 2 (11/03/2026 a 14/04/2026) constroi o modulo NLP do sistema. A motivacao e clara: o ECG captura o estado eletrico do coracao, mas o paciente comunica sua experiencia em linguagem natural - "sinto dor no peito", "fico sem ar quando subo escada". O sistema precisa entender essas queixas para correlaciona-las com os padroes eletrocardiograficos detectados pelo wearable. O NB6 e a peca que constroi essa ponte entre linguagem clinica e classificacao cardiologica.

---

## 3. Posicao no pipeline: do NB1 ao NB6

```
NB1 ptbxl_eda           - 21.799 ECGs, 6 superclasses PTB-XL
NB2 holter_iot          - 8,64 M instancias IoT simuladas, 24h
NB3 signal_vision_eda   - espectrogramas STFT 224x224, tensores .npy
NB4 nlp_data_pruning    - 26 PDFs PT-BR podados, reducao ~55% ruido
NB5 nlp_data_engineer   - TF-IDF 6.276 dim, edge_trigger_lookup.json
         |
         v
NB6 symptom_extraction  <-- ESTE NOTEBOOK
         |
         +-- mapa_sintomas_doencas.csv  (929 linhas, corpus de treino NB7)
         +-- sintomas_pacientes.txt     (10 frases quality-filtered)
         |
         v
NB7 risk_classifier     - TF-IDF + Regressao Logistica, alto/baixo risco
```

O NB6 consome dois artefatos do NB5: o diretorio `parsed_txt/` com os 26 textos filtrados, e o arquivo `cleaned/edge_trigger_lookup.json` com os stems TF-IDF discriminativos de cada documento. Sem esses dois insumos, o NB6 nao executa.

---

## 4. Conteudo deste diretorio

```
symptom_extraction/
  mapa_sintomas_doencas.csv   - entregavel D1 da Fase 2 (929 linhas x 7 colunas)
  sintomas_pacientes.txt      - entregavel D2 da Fase 2 (10 frases clinicas)
  charts/                     - 10 graficos PNG do notebook
    chart1_corpus_composicao.png
    chart2_lexical_contribution.png
    chart3_doc_stats.png
    chart4_superclass_distribution.png
    chart5_keyword_frequency.png
    chart6_frases_por_doc.png
    chart7_trigger_score_by_sc.png
    chart8_top_words_by_sc.png
    chart9_mapa_stats.png
    chart10_trigger_score_10_frases.png
  README.md                   - este arquivo
```

---

## 5. Os outputs em detalhe

### 5.1 mapa_sintomas_doencas.csv

**O que e:** tabela estruturada com 929 linhas, cada uma representando uma frase sintomatica extraida do corpus. E o corpus de treinamento principal para o NB7.

**Colunas:**

| Coluna | Tipo | Descricao |
|--------|------|-----------|
| Sintoma_1 | str | primeiro SYMPTOM_KEYWORD encontrado na frase |
| Sintoma_2 | str | segundo keyword (vazio se nao existir) |
| Sintoma_3 | str | terceiro keyword (vazio se nao existir) |
| Doenca_Associada | str | diagnostico do documento de origem |
| Superclasse_PTB-XL | str | label PTB-XL: MI, STTC, CD, HYP, NORM |
| Nivel_Risco | str | alto (MI/STTC/CD/HYP) ou baixo (NORM) |
| Trigger_Score | int | numero de stems TF-IDF da frase que aparecem no lookup do documento |

**Distribuicao por superclasse:**

```
CD    443 frases (47.7%)
MI    185 frases (19.9%)
STTC  170 frases (18.3%)
NORM   79 frases ( 8.5%)
HYP    52 frases ( 5.6%)
```

**Por que o CSV e estruturado assim:** o NB7 consumira este arquivo como dataset de treinamento. As colunas Sintoma_1/2/3 serao concatenadas e vetorizadas via TF-IDF. O Trigger_Score pode ser usado como feature numerica adicional. O Nivel_Risco e a label binaria de classificacao.

**Analogia:** e como uma ficha de triagem hospitalar pre-preenchida. Cada linha e um paciente ficticio cujas queixas foram extraidas da literatura clinica. O NB7 aprendera, a partir dessas fichas, a reconhecer queixas de alto risco (infarto, arritmia maligna) versus baixo risco (biomarcadores em populacao saudavel).

**Aviso de qualidade:** celulas vazias em Sintoma_2 e Sintoma_3 sao intencionais, nao erros. Frases com apenas 1 keyword detectado nao tem segundo ou terceiro sintoma. No NB7, tratar como NaN via `.fillna('')` antes de concatenar.

### 5.2 sintomas_pacientes.txt

**O que e:** selecao das 10 melhores frases clinicas do corpus, distribuidas por superclasse PTB-XL com quotas balanceadas (MI=3, STTC=4, CD=3). Serve como corpus de validacao clinica do sistema de apoio ao diagnostico.

**Criterios de selecao em camadas:**

Camada 1 - filtro de qualidade textual:
- Excluir frases com DOI, URLs, ISSN, ISBN, referencias a figuras e tabelas
- Razao de caracteres alfabeticos maior ou igual a 70% (alpha_ratio >= 0.70)
- Comprimento entre 8 e 70 palavras

Camada 2 - ranqueamento por trigger_score:
- Dentro de cada superclasse, ordenar por trigger_score decrescente
- Priorizar frases de documentos distintos (diversidade de fonte)

Camada 3 - quotas fixas:
- MI = 3 frases (sub-representado no corpus, prioridade maxima)
- STTC = 4 frases (representacao adequada ao risco alto)
- CD = 3 frases (limitado para compensar a dominancia no corpus)

**Metricas de validacao (Secao 11 do notebook):**
- Total de frases: 10
- Cobertura (>= 1 sintoma detectado): 100%
- Media de sintomas por frase: 1.00
- Trigger score medio: 6.90
- Trigger score maximo: 9

**Analogia:** e como a lista dos 10 casos clinicos mais representativos que um professor de medicina escolheria para um exame. Nao sao os mais faceis nem os mais dificeis, sao os mais instrutivosd - um de infarto com trombolise, um de arritmia maligna por cardiotoxicidade, um de choque cardiogenico. Cada frase cobre um cenario real de uso do sistema Cardio-Edge-AI.

### 5.3 charts/ (10 graficos PNG)

Cada grafico foi salvo em 110 DPI para uso em relatorios e apresentacoes FIAP.

| Arquivo | Tipo de grafico | O que mostra |
|---------|-----------------|--------------|
| chart1_corpus_composicao.png | barras horizontais | distribuicao dos 26 docs por categoria |
| chart2_lexical_contribution.png | barras horizontais | stems TF-IDF unicos por categoria |
| chart3_doc_stats.png | boxplot + scatter | palavras e sentencas por tipo de documento |
| chart4_superclass_distribution.png | pizza + stacked bar | superclasses PTB-XL e proporcao de risco |
| chart5_keyword_frequency.png | barras horizontais coloridas | frequencia dos 48 SYMPTOM_KEYWORDS com tiers |
| chart6_frases_por_doc.png | barras horizontais | frases extraidas por documento (26 docs) |
| chart7_trigger_score_by_sc.png | boxplot + stripplot | distribuicao do trigger_score por superclasse |
| chart8_top_words_by_sc.png | barras multiplas | top 15 palavras nas frases de MI, STTC e CD |
| chart9_mapa_stats.png | barras duplas | sintomas mais comuns e linhas por superclasse no CSV |
| chart10_trigger_score_10_frases.png | barras verticais coloridas | trigger_score das 10 frases do TXT |

---

## 6. Como o NB6 foi construido: o pipeline secao a secao

### Secao 0 - Objetivo e Mapa de Raciocinio

Apresenta o fluxo completo em ASCII art, do NB1 ao NB7. Estabelece os dois entregaveis FIAP da Fase 2.

### Secao 1 - Ambiente e Importacoes

Configura o ambiente Python 3.10.0 com as bibliotecas necessarias: pandas 2.3.3, seaborn 0.13.2, matplotlib 3.10.8, nltk 3.9.2, numpy 1.26.4. Define as paletas de cores SC_COLORS (uma cor por superclasse PTB-XL) e CAT_COLORS (uma cor por categoria de documento). Inicializa o RSLPStemmer do NLTK.

**Por que o RSLP e nao outro stemmer:** o RSLP (Removedor de Sufixos da Lingua Portuguesa) e especifico para PT-BR. Stemmers genericos como o Porter Stemmer foram desenvolvidos para ingles e produzem raizes incorretas em portugues. Por exemplo, "insuficiencia" com RSLP vira "insuficienc"; com Porter vira algo sem sentido para o portugues.

### Secao 2 - Inventario do Corpus

Define os caminhos de entrada e saida, carrega a lista dos 26 arquivos `*_filtrado.txt`, e instancia o DISEASE_MAP.

**O que e o DISEASE_MAP:** e um dicionario Python que funciona como tabela de metadados dos 26 documentos. Cada chave e o nome do arquivo; cada valor e um dicionario com quatro campos: `tipo` (categoria do documento), `diagnostico` (descricao clinica livre), `superclasse` (label PTB-XL correspondente) e `risco` (alto ou baixo).

**Analogia:** o DISEASE_MAP e o catalogo da biblioteca. Sem ele, o pipeline saberia que leu um texto, mas nao saberia que esse texto e sobre infarto, nem que pertence a superclasse MI, nem que e alto risco. E a ponte entre o arquivo de texto bruto e o conhecimento clinico estruturado.

**Estilizacao heatmap:** o DataFrame derivado do DISEASE_MAP e exibido com `.style.map()` do pandas Styler, colorindo cada celula da coluna `superclasse` com a cor correspondente da paleta SC_COLORS (vermelho para MI, laranja para STTC, azul para CD, roxo para HYP, verde para NORM). A coluna `risco` e colorida em vermelho-claro para alto e verde-claro para baixo.

### Secao 3 - Lexico de Gatilho Clinico

Carrega o `edge_trigger_lookup.json` gerado pelo NB5. Para cada documento, o lookup contem os 10 stems RSLP mais discriminativos pelo criterio TF-IDF - ou seja, os termos com alta frequencia no documento e baixa frequencia no restante do corpus.

**Analogia:** o lookup e a "impressao digital textual" de cada documento. Assim como uma impressao digital identifica uma pessoa de forma unica, os 10 stems do lookup identificam o vocabulario que torna aquele documento distinto dos outros 25. "fluorouracil" e a impressao digital do relato de cardiotoxicidade por 5-FU; "chagas" e a impressao digital do relato de cardiomiopatia chagasica.

**Observacao importante:** `revisao_fibrilacao_atrial_filtrado.txt` tem `n_stems=0` no lookup. O NB5 nao gerou stems para esse documento porque seu conteudo era tao similar ao de outros documentos de fibrilacao atrial (diretriz SBC + revisao com cancer) que o TF-IDF nao encontrou termos suficientemente discriminativos. Isso explica por que esse documento produziu 0 frases no pipeline.

### Secao 4 - Analise Estatistica do Corpus

Calcula metricas basicas de cada documento: numero de palavras, sentencas e caracteres. Agrupa por tipo de documento para comparar o perfil metrico de cada categoria.

**Resultados:**
- Total de palavras no corpus: 118.361
- Total de sentencas: 4.189
- Comprimento medio de sentenca: ~28 palavras (tipico de linguagem medica formal PT-BR)
- Diretrizes SBC: maior mediana de palavras (~15.700 por documento)
- Relatos de Caso: mais homogeneos (~600 a 1.640 palavras por documento)

**Por que isso importa para o pipeline:** o filtro `min_palavras=8` na extracao de frases foi calibrado com base nessa analise. Frases com menos de 8 palavras em um corpus com sentencas medias de 28 palavras sao quase certamente fragmentos - referencias bibliograficas, cabecalhos, numeros de pagina - e nao sentencas clinicas completas.

### Secao 5 - Mapeamento Clinico Completo

Exibe tabelas de distribuicao e um crosstab tipo x superclasse. Confirma que o corpus esta distribuido conforme o design: CD domina (12/26 documentos), NORM e representado apenas por revisoes cientificas, MI concentra-se em bulas e protocolo SUS.

**O crosstab como ferramenta de auditoria:** o cruzamento tipo vs superclasse revela que nao ha documento de Relato de Caso mapeado para NORM, o que e clinicamente correto - relatos descrevem casos agudos, nao populacoes de referencia. Tambem confirma que HYP aparece somente em Protocolo SUS e Revisao Cientifica, nao em Relatos de Caso, o que e uma limitacao do corpus coletado.

### Secao 6 - Palavras-Gatilho de Sintoma

Define o `SYMPTOM_KEYWORDS`: lista com 48 termos que sinalizam presenca de queixa clinica em linguagem medica PT-BR. A lista esta organizada em dois grupos:

- **Keywords diretos** (28 termos): descrevem o sintoma em si - "dor", "dispneia", "taquicardia", "edema", "sincope", "hemoptise", entre outros.
- **Keywords contextuais** (20 termos): descrevem o contexto narrativo em que o sintoma aparece - "apresentou", "evoluiu com", "admitida com", "refere", "queixa de", entre outros.

**Por que keywords contextuais importam:** uma frase como "o paciente refere piora aos esforcos" seria descartada se o pipeline buscasse apenas sintomas diretos, pois "piora" e "esforcos" nao estao na lista. Mas "refere" captura que e uma narrativa de queixa clinica. Os qualificadores contextuais garantem que frases de relato clinico real sejam capturadas mesmo quando o sintoma e descrito de forma indireta.

**Frequencia dos keywords no corpus:**
- "dor": 612 ocorrencias (tier alto - alta frequencia, baixa precisao)
- "sintoma": 162 ocorrencias (tier alto)
- "insuficiencia": 124 ocorrencias (tier alto)
- "taquicardia": 83 ocorrencias (tier medio)
- "hemoptise", "ortopneia", "sibilos": menos de 20 ocorrencias (tier baixo - baixa frequencia, alta precisao)

**Analogia dos tiers:** keywords de tier alto sao como o "detetive generalista" - acham muita coisa mas incluem falsos positivos. Keywords de tier baixo sao como o "especialista forense" - raramente acionados, mas quando acionados, indicam algo muito especifico. O trigger_score e o sistema que combina os dois, dando mais credito a frases onde termos raros e especificos aparecem juntos.

### Secao 7 - Stemming RSLP e Alinhamento com o Lexico de Gatilho

Define as quatro funcoes centrais do pipeline:

```python
def normalizar(texto):
    # Remove acentos e converte para minusculas
    # "Taquicardia" vira "taquicardia"
    # "insuficiencia" vira "insuficiencia" (sem cedilha, sem acento)

def tokenizar_e_stemizar(texto):
    # Extrai tokens alfabeticos e aplica RSLP
    # ["taquicardia", "ventricular"] vira ["taquicardi", "ventricul"]

def contem_sintoma(frase):
    # Retorna True se qualquer SYMPTOM_KEYWORD esta na frase normalizada
    # Filtro rapido O(k) onde k = tamanho do SYMPTOM_KEYWORDS

def calcular_trigger_score(frase, doc_stems):
    # Conta quantos stems do lookup aparecem nos stems da frase
    # Interseccao de conjuntos: O(min(|stems_frase|, |doc_stems|))
```

**Por que normalizar antes de buscar keywords:** a frase "Paciente com Insuficiencia Cardiaca" nao conteria "insuficiencia" sem normalizacao, porque a letra maiuscula e o acento tornariam a comparacao falha. `unicodedata.normalize('NFKD')` + `.encode('ascii', 'ignore')` e a tecnica padrao para remover diacriticos em PT-BR de forma deterministica.

**Demonstracao RSLP:**

| Frase | Tokens | Stems RSLP | Sintomas Detectados |
|-------|--------|------------|---------------------|
| paciente admitida com dor precordial | paci, admit, com, dor, precord | paci, admit, com, dor, precord | dor, precordial, admitida com |
| apresentou taquicardia ventricular | apresent, taquicardi, ventricul | apresent, taquicardi, ventricul | taquicardia, apresentou |
| evoluiu com choque cardiogenico | evolu, choqu, cardiogen | evolu, choqu, cardiogen | choque, evoluiu com |

**Analogia do RSLP:** e como o "dicionario de raizes" de um idioma. Se voce busca por "corr", encontra "corre", "correndo", "corrida", "corredor". Da mesma forma, o stem "taquicardi" cobre "taquicardia", "taquicardico", "taquicardias". Isso e essencial porque o TF-IDF do NB5 foi construido sobre stems, e a frase do paciente usa a forma inflexionada - sem o stemmer, a correspondencia falharia.

### Secao 8 - Pipeline Completo: Extracao em Todos os 26 Documentos

Executa o pipeline sobre todos os 26 documentos. Para cada documento:
1. Le o texto do arquivo `_filtrado.txt`
2. Segmenta em frases usando `re.split(r'(?<=[.!?;])\s+', texto)`
3. Filtra frases com >= 8 palavras que contenham ao menos um SYMPTOM_KEYWORD
4. Para cada frase filtrada, calcula o trigger_score usando os stems do lookup
5. Registra tudo em um dicionario que vira linha do DataFrame `df_all`

**Resultados por documento:**

```
diretriz_sbc_ressuscitacao_cardiopulmonar  frases=183  stems_lookup=10
diretriz_sbc_angina_instavel               frases=148  stems_lookup=10
protocolo_sus_sindrome_coronariana         frases= 90  stems_lookup=10
diretriz_sbc_fibrilacao_atrial             frases= 86  stems_lookup=10
bula_profissional_clopidogrel              frases= 41  stems_lookup=10
revisao_gdf15_biomarcador                  frases= 42  stems_lookup=10
diretriz_sus_insuficiencia_cardiaca        frases= 40  stems_lookup=10
bula_profissional_amiodarona               frases= 32  stems_lookup=10
bula_profissional_noradrenalina            frases= 30  stems_lookup=10
revisao_sindrome_cardiorrenal              frases= 26  stems_lookup=10
bula_profissional_alteplase                frases= 26  stems_lookup=10
relato_caso_miocardite_covid19             frases= 24  stems_lookup=10
bula_profissional_enoxaparina              frases= 20  stems_lookup=10
revisao_mirnas_fisiopatologia              frases= 18  stems_lookup=10
relato_caso_ic_descompensada_arbovirose    frases= 18  stems_lookup=10
revisao_fibrilacao_atrial_pacientes_cancer frases= 14  stems_lookup=10
revisao_ceramidas_plasmaticas              frases= 13  stems_lookup=10
relato_caso_takotsubo                      frases= 12  stems_lookup=10
revisao_estrogenio_obesidade               frases= 12  stems_lookup=10
relato_caso_disfuncao_cardiaca_quimioter   frases= 11  stems_lookup=10
relato_caso_assistencia_circulatoria_chagas frases= 11  stems_lookup=10
relato_caso_fibrilacao_ventricular_cardi   frases= 10  stems_lookup=10
relato_caso_iamcsst_ruptura_parede         frases=  8  stems_lookup=10
relato_caso_miocardite_coinfeccao          frases=  8  stems_lookup=10
revisao_indices_hematologicos              frases=  6  stems_lookup=10
revisao_fibrilacao_atrial                  frases=  0  stems_lookup= 0  <- anomalia
```

**Total: 929 frases sintomaticas extraidas**

**A anomalia do frases=0:** o documento `revisao_fibrilacao_atrial_filtrado.txt` produziu zero frases porque seu `stems_lookup` e vazio - o NB5 nao conseguiu calcular stems TF-IDF discriminativos para ele. Isso ocorre quando um documento nao tem vocabulario suficientemente unico em relacao aos demais. E um ponto de atencao para reprocessamento no NB5 em versoes futuras.

**Estilizacao heatmap do df_all:** o DataFrame de 929 frases e exibido com gradiente de cor RdYlGn (vermelho-amarelo-verde) na coluna `trigger_score` e gradiente azul em `n_sintomas`. Isso permite identificar visualmente as frases de maior qualidade clinica sem precisar ordenar manualmente.

### Secao 9 - Analise Exploratoria dos Resultados

Constroi uma tabela resumo agrupada por documento com: numero de frases, score medio, score maximo e media de sintomas por frase.

**Achado relevante:** as revisoes cientificas de NORM e HYP apresentam scores medios surpreendentemente altos (3.83, 3.77, 3.50). Isso ocorre porque essas revisoes contem termos medicos especificos que coincidem com os stems dos seus respectivos lookups - "ceramidas", "ldl", "icfep", "estrogeni". Os stems sao discriminativos para o documento, mas as frases que os contem nao sao narrativas clinicas de pacientes - sao discussoes epidemiologicas. Isso demonstra que trigger_score alto e necessario mas nao suficiente para identificar frases de valor clinico; o filtro de SYMPTOM_KEYWORDS trabalha em conjunto.

### Secao 10.1 - Entregavel FIAP: mapa_sintomas_doencas.csv

Itera sobre cada frase do df_all, extrai os tres primeiros SYMPTOM_KEYWORDS encontrados, e monta o DataFrame final com as 7 colunas exigidas pelo projeto. Salva como UTF-8 com BOM (encoding='utf-8-sig') para compatibilidade com Excel e LibreOffice.

**Por que UTF-8 com BOM:** o BOM (Byte Order Mark) e um marcador de tres bytes no inicio do arquivo que indica ao Excel que o conteudo e UTF-8. Sem ele, o Excel pode interpretar acentos como caracteres incorretos em sistemas Windows com locale pt-BR.

### Secao 10.2 - Entregavel FIAP: sintomas_pacientes.txt

Aplica o filtro de qualidade `passes_quality()` sobre o df_all, gerando df_quality com 734 frases aprovadas (79.0% de taxa de aprovacao, 195 descartadas).

Em seguida, aplica o algoritmo de selecao por quotas:
1. Para cada superclasse em QUOTAS (MI=3, STTC=4, CD=3)
2. Ordena o pool de frases daquela superclasse por trigger_score decrescente
3. Na primeira passagem, seleciona frases de documentos distintos (diversidade de fonte)
4. Se a quota nao foi atingida, relaxa a restricao de documento distinto na segunda passagem
5. Rastreia indices (nao objetos Series) para evitar comparacoes ambiguas do pandas

**Por que rastrear indices e nao objetos Series:** uma Series do pandas e um array de valores com indice. Quando se tenta `if serie_a not in lista_de_series`, o Python tenta avaliar `serie_a == cada_elemento`, o que para Series retorna outra Series de booleanos, e nao um unico booleano. O pandas lanca `ValueError: The truth value of a Series is ambiguous`. A solucao e usar `if idx not in selected_indices`, comparando inteiros - operacao bem definida e sem ambiguidade.

### Secao 11 - Validacao do Sistema de Apoio ao Diagnostico

Le o `sintomas_pacientes.txt` de volta do disco, faz o parse das frases e metadados, e aplica o pipeline de extracao sobre cada frase. Calcula metricas de cobertura:

```
Total de frases validadas : 10
Cobertura (>= 1 sintoma)  : 100%
Media de sintomas/frase   : 1.00
Trigger score medio       : 6.90
Trigger score maximo      : 9
Cobertura MI              : 100% (3/3 frases)
Cobertura STTC            : 100% (4/4 frases)
Cobertura CD              : 100% (3/3 frases)
```

**O que esses numeros significam para o Cardio-Edge-AI:** cobertura 100% confirma que o sistema consegue detectar pelo menos um marcador de queixa em toda frase clinica real. Na pratica do wearable, quando o paciente digitar ou falar sua queixa no aplicativo companion, o pipeline NLP conseguira identificar o contexto clinico e acionar o nivel de alerta correto no Hub (Raspberry Pi).

---

## 7. Como o enrich_nb6.py funciona e como interage com o .ipynb

### 7.1 O que e um arquivo .ipynb

Um arquivo `.ipynb` e, em essencia, um arquivo JSON. Ao abrir o `symptom_extraction.ipynb` em qualquer editor de texto, voce vera uma estrutura como:

```json
{
  "nbformat": 4,
  "nbformat_minor": 5,
  "metadata": { ... },
  "cells": [
    {
      "cell_type": "markdown",
      "source": "## 1. Ambiente e Importacoes",
      "metadata": {}
    },
    {
      "cell_type": "code",
      "source": "import pandas as pd\nimport seaborn as sns",
      "outputs": [
        {
          "output_type": "stream",
          "text": "Ambiente configurado com sucesso.\n"
        }
      ],
      "execution_count": 1
    }
  ]
}
```

Cada celula e um objeto JSON com tres campos principais:
- `cell_type`: "markdown" (texto formatado) ou "code" (codigo Python executavel)
- `source`: o conteudo da celula - pode ser uma string ou lista de strings
- `outputs`: lista dos resultados da ultima execucao - prints, DataFrames renderizados, graficos como base64

**Analogia:** o .ipynb e como uma receita culinaria fotografada. A `source` e a lista de ingredientes e modo de preparo. Os `outputs` sao as fotos do prato em cada etapa. Voce pode alterar a receita (editar a source) sem refazer o prato (sem re-executar) - mas as fotos ficam desatualizadas ate a proxima execucao.

### 7.2 O que e um arquivo .py

Um arquivo `.py` e codigo Python puro, sem estrutura de celulas. Quando executado com `python script.py`, o interpretador le e executa o arquivo de cima a baixo, linha por linha. Nao ha conceito de celulas, nao ha armazenamento de outputs no arquivo - tudo vai para o terminal (stdout/stderr) e desaparece quando o processo termina.

**Diferenca fundamental:**

| Aspecto | .ipynb | .py |
|---------|--------|-----|
| Formato em disco | JSON estruturado | texto plano |
| Execucao | celula a celula, interativa | sequencial, do inicio ao fim |
| Outputs | armazenados no JSON junto ao codigo | nao armazenados |
| Visualizacoes | renderizadas inline | abertas em janela separada ou salvas |
| Estado | kernel mantem variaveis entre celulas | cada execucao comeca do zero |
| Uso tipico | exploracao, analise, apresentacao | producao, automacao, scripts |

### 7.3 Como o enrich_nb6.py modifica o .ipynb

O `enrich_nb6.py` nao executa o notebook. Ele realiza uma operacao de edicao cirurgica no arquivo JSON. O fluxo e:

```
1. json.load()  -->  carrega o .ipynb como dicionario Python
2. find_cell()  -->  localiza celulas por substring unica no source
3. append_code() / replace_md() / prepend_md()  -->  modifica o source da celula
4. cell['outputs'] = []  -->  limpa outputs desatualizados das celulas de codigo modificadas
5. json.dump()  -->  salva o dicionario de volta como .ipynb
```

**O que muda no arquivo apos o enrich_nb6.py:**
- As celulas de codigo alvo tem novo codigo Python adicionado ao final do `source`
- As celulas de markdown de interpretacao tem seu `source` completamente substituido
- Alguns headers de secao tem callouts de ciclo de vida DS adicionados ao inicio
- Celulas de codigo modificadas tem `outputs` zerados e `execution_count` nulo

**O que NAO muda:**
- Celulas nao tocadas pelo script ficam identicas, inclusive seus outputs
- A estrutura JSON geral do notebook
- O numero de celulas (66 celulas antes e depois)
- Os metadados do kernel (Python 3.10.0)

**Analogia:** e como uma revisao de texto em um caderno fotografado. Voce nao refaz os experimentos (nao re-executa o notebook), apenas atualiza as anotacoes nas margens (edita os markdowns) e adiciona novos passos de demonstracao nas instrucoes (appenda codigo). As fotos dos resultados anteriores ficam no caderno ate que alguem re-execute as celulas modificadas no Jupyter.

### 7.4 Python em .ipynb versus Python em .py: o que muda na pratica

**Em um .py:**
```python
import pandas as pd
df = pd.DataFrame({'a': [1,2,3]})
print(df)         # imprime no terminal
df.style          # nao faz nada - o Styler e criado mas nao ha onde renderizar
```

**Em um .ipynb:**
```python
import pandas as pd
df = pd.DataFrame({'a': [1,2,3]})
df                # o kernel detecta que o ultimo valor e um DataFrame e o renderiza como HTML
df.style.background_gradient(cmap='Blues')  # renderiza o DataFrame com gradiente de cor
```

**Por que `display()` e necessario em alguns contextos:** dentro de loops ou funcoes, o Jupyter nao renderiza automaticamente o valor da ultima expressao. Por isso o pipeline usa `display(df.style...)` explicitamente - garante que o DataFrame estilizado apareca na saida da celula mesmo quando nao e a ultima linha do codigo.

**As celulas de codigo do .ipynb executam em um kernel compartilhado.** Isso significa que uma variavel definida na celula 5 esta disponivel na celula 20, desde que as celulas tenham sido executadas na ordem correta. E um estado global acumulativo - diferente de um .py onde tudo e local ao escopo de execucao.

### 7.5 ipykernel no VSCode

Ao abrir um `.ipynb` no VSCode, o editor precisa de um "kernel" para executar o codigo - um processo Python separado que recebe o codigo de cada celula, executa, e retorna os resultados.

**O que e o ipykernel:** e o pacote que implementa o protocolo Jupyter Kernel para Python. Quando voce instala `pip install ipykernel`, o Python fica "registrado" como um kernel disponivel no VSCode. Sem ele, o VSCode abre o arquivo .ipynb mas nao consegue executar nenhuma celula.

**Como funciona internamente:**
```
VSCode (frontend) <-- protocolo ZMQ --> ipykernel (processo Python separado)
     |                                      |
     | "execute esta celula"                | executa o codigo
     |                                      | guarda variaveis no namespace
     | <-- retorna outputs (texto, HTML, PNG)
     |
     | renderiza outputs inline
```

**Como configurar no VSCode:**
1. Instalar a extensao "Jupyter" da Microsoft no VSCode
2. Instalar `ipykernel` no ambiente Python: `pip install ipykernel`
3. Registrar o ambiente: `python -m ipykernel install --user --name .fiap_venv_py310 --display-name "Python 3.10 (FIAP)"`
4. Abrir o .ipynb, clicar em "Select Kernel" no canto superior direito, escolher "Python 3.10 (FIAP)"

**Para este projeto, o ambiente correto e:** `.fiap_venv_py310` (Python 3.10.0 com tensorflow-gpu 2.10.0, numpy 1.26.4 obrigatorio pelo C API bfloat16). Usar o ambiente CPU (py312) para execucao do NB6 e seguro, ja que o NB6 nao usa tensorflow.

**Diferenca entre executar o .ipynb no VSCode versus no Google Colab:**
- No Colab, o kernel roda em uma VM na nuvem - nao tem acesso ao sistema de arquivos local. Os paths relativos como `../data/processed/nlp/` nao funcionam; e necessario montar o Google Drive.
- No VSCode local, o kernel roda na maquina do desenvolvedor - tem acesso direto ao sistema de arquivos. Os paths relativos funcionam a partir do diretorio do notebook.

---

## 8. Ciclo de vida de dados: o que cada secao representa

| Secao | Etapa DS | Descricao |
|-------|----------|-----------|
| Secao 2 - Inventario | Coleta e catalogacao | mapear os dados disponiveis e seus metadados |
| Secao 3 - Lookup | Carregamento de artefatos | consumir features pre-computadas (NB5) |
| Secao 4 - Estatisticas | Analise exploratoria | entender a distribuicao e qualidade do corpus |
| Secao 5 - Mapeamento | Rotulagem / Label assignment | associar documentos a classes PTB-XL |
| Secao 6 - Keywords | Feature engineering (dominio) | injetar conhecimento clinico no pipeline |
| Secao 7 - Stemming | Pre-processamento / Normalizacao | reduzir dimensionalidade morfologica |
| Secao 8 - Pipeline | Feature extraction | gerar o dataset bruto de features textuais |
| Secao 9 - Analise | Validacao qualitativa | auditoria da qualidade das features extraidas |
| Secao 10.1 - CSV | Preparacao para modelagem | estruturar o corpus de treinamento do NB7 |
| Secao 10.2 - TXT | Limpeza de dados e selecao | filtrar e amostrar com criterio clinico |
| Secao 11 - Validacao | Avaliacao / Metricas | medir cobertura e qualidade do entregavel |

---

## 9. Metricas e resultados consolidados

| Metrica | Valor |
|---------|-------|
| Documentos processados | 26 de 26 |
| Frases brutas extraidas | 929 |
| Frases apos filtro de qualidade | 734 (79.0%) |
| Frases descartadas | 195 (21.0%) |
| Linhas no mapa_sintomas_doencas.csv | 929 |
| Frases no sintomas_pacientes.txt | 10 |
| Cobertura de sintomas (TXT) | 100% |
| Trigger score medio (TXT) | 6.90 |
| Trigger score maximo (TXT) | 9 |
| Media de sintomas por frase (TXT) | 1.00 |
| Graficos gerados | 10 PNG |

---

## 10. Proximo passo: NB7

O NB7 (`risk_classifier.ipynb`) consumira o `mapa_sintomas_doencas.csv` deste diretorio como corpus de treinamento. Atividades previstas:

- Vetoorizacao TF-IDF das colunas Sintoma_1/2/3 concatenadas
- Treinamento de Regressao Logistica com `class_weight='balanced'`
- Label encoding: alto risco (MI, STTC, CD, HYP) vs baixo risco (NORM, INCONCLUSIVO)
- Holdout 80/20 estratificado por superclasse
- Avaliacao por F1-score macro e AUC-ROC
- Entregavel D3: `frases_risco_rotuladas.csv` com >= 40 frases rotuladas
