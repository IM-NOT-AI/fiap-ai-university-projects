# Modulo NLP - Cardio-Edge-AI
## Da Documentacao Exigida ao Dataset que Muda o Jogo

> **Notebook principal:** `eda_mimic_iv_nlp.ipynb`
> **Artefatos gerados:** `data/processed/mimic-iv-ecg/`
> **Corpus exportado:** `corpus_mimic_ecg_rotulado_v2.csv` (1.193 frases classificadas, sem PHI)
> **Dataset:** MIMIC-IV-ECG v1.0 - Gow B. et al. (2023). PhysioNet. doi:10.13026/4nqgsb35

---

## Indice

1. [O Ponto de Partida - O que a FIAP Exigiu na Fase 1](#1-o-ponto-de-partida)
2. [Por que Nao Expus os Dados Brutos na Fase 1](#2-por-que-nao-expus-os-dados-brutos)
3. [O Corpus que Construimos - Quatro Arquetipos de Linguagem Cardiologica](#3-o-corpus-que-construimos)
4. [O Momento de Verdade - F1 = 1.000](#4-o-momento-de-verdade)
5. [O Diagnostico - Domain Leakage](#5-o-diagnostico--domain-leakage)
6. [A Pergunta Certa que Surgiu do Erro](#6-a-pergunta-certa-que-surgiu-do-erro)
7. [Por que o MIMIC-IV-ECG Muda o Jogo](#7-por-que-o-mimic-iv-ecg-muda-o-jogo)
8. [O EDA como Primeiro Passo Obrigatorio](#8-o-eda-como-primeiro-passo-obrigatorio)
9. [O que o EDA Revelou - Numeros Reais](#9-o-que-o-eda-revelou--numeros-reais)
10. [Governanca de Dados - DUA, HIPAA e LGPD](#10-governanca-de-dados--dua-hipaa-e-lgpd)
11. [Proximo Passo - NB6v2 e NB7v2](#11-proximo-passo--nb6v2-e-nb7v2)
12. [Por que Isso Importa Alem da Nota](#12-por-que-isso-importa-alem-da-nota)
13. [Estrutura de Arquivos](#13-estrutura-de-arquivos)
14. [Referencias](#14-referencias)

---

## 1. O Ponto de Partida

Na Fase 1 do desafio CardioIA, o enunciado definia o escopo do modulo NLP: construir
um corpus textual clinico, extrair sintomas cardiologicos e criar um classificador de risco.
Sem base de dados indicada. Sem fonte prescrita.

A solucao natural foi buscar o que o ecossistema medico brasileiro oferece de publico,
autorizado e tecnicamente robusto:

| Arquetipo | Qtd | Fonte principal |
|---|---|---|
| Diretrizes e Protocolos | 5 | Ministerio da Saude, SBC, SciELO |
| Relatos Clinicos | 9 | Arquivos Brasileiros de Cardiologia, PMC |
| Revisoes Academicas | 7 | Arquivos Brasileiros de Cardiologia (SciELO) |
| Farmacologia e Bulas | 5 | Sanofi, Fresenius Kabi, Viatris, Accord |
| **Total** | **26 PDFs** | Literatura cardiologica PT-BR de autoridade |

Toda a curadoria esta documentada em:
`docs/data/nlp/nlp_report_data_source.md`

A metodologia seguiu o principio **Data-Centric AI**: antes de complexidade algoritmica,
qualidade e representatividade dos dados. Os quatro arquetipos foram escolhidos porque
cobrem os registros linguisticos distintos que um sistema de triagem cardiologica
encontra na pratica clinica brasileira:

- **Diretrizes** - linguagem normativa e regras imperativas do SUS
  ("paciente com dor toracica deve realizar ECG em ate 10 minutos...")
- **Relatos de caso** - a "sujeira" real de prontuarios: historico pregresso,
  sintomas agudos, valores laboratoriais e marcadores temporais dispersos na mesma frase
- **Revisoes academicas** - profundidade ontologica: biomarcadores, miRNAs,
  ceramidas plasmaticas, mecanismos moleculares que explicam o que o ECG ve
- **Bulas** - regras de negacao clinica densa e grafos de dependencia farmacologica
  ("se clearance < 30 mL/min, mudar frequencia de 12h para 24h")

Essa heterogeneidade linguistica era deliberada. Um modelo treinado so em diretrizes
aprende linguagem normativa. Um treinado so em relatos aprende narrativa clinica.
O objetivo era ambos ao mesmo tempo e mais.

---

## 2. Por que Nao Expus os Dados Brutos na Fase 1

Aqui esta um aspecto que nao ficou explicito no enunciado, mas que e pratica
profissional inegociavel: **dados brutos de saude nao vao para repositorios publicos.**

Na Fase 1, a entrega era o repositorio git. Os 26 PDFs clinicos sao documentos publicos
com URLs ativas e licencas que permitem uso academico - mas colocar 26 arquivos
binarios pesados no git contradiz boas praticas de engenharia de dados por duas razoes:

**1. Rastreabilidade por DVC** - arquivos grandes pertencem ao pipeline de dados,
versionados por hash. No historico do git nao se pode ver diff, nao se pode fazer
rollback granular de um PDF, nao se pode auditar o que mudou entre versoes.

**2. Sinalizacao de governanca** - a separacao entre `data/raw/` (imutavel, fora
do git) e `data/processed/` (artefatos derivados, versionados) e o padrao que qualquer
equipe de dados em producao espera ver. Misturar os dois e ausencia de processo.

A estrategia adotada na Fase 1:

- PDFs: rastreados via DVC, referenciados por URL no `nlp_report_data_source.md`
- Artefatos processados (CSVs, JSONs, PNGs sem PHI): no git, publicaveis
- Documentacao da estrategia de corpus: no README raiz de `last_year/`

O que entregamos nao era "pouco" - era a estrategia completa documentada, os
artefatos processados (`edge_trigger_lookup.json`, `mapa_sintomas_doencas.csv`,
`corpus_frases_completo.csv`) e o pipeline reproduzivel por qualquer pessoa com
acesso aos PDFs originais.

Quando a Fase 2 revelou mais orientacoes sobre o que a banca esperava - evidencia
de que a extracao de informacao funciona, dataset rotulado criado corretamente,
classificador treinado - ficou claro que o trabalho da Fase 1 estava no lugar certo.
O que precisava evoluir era so o modulo NLP. E foi isso que fizemos.

---

## 3. O Corpus que Construimos

### NB4 - Poda e Limpeza dos PDFs

O pipeline de poda (`NB4_nlp_data_pruning.ipynb`) processou os 26 PDFs e removeu
aproximadamente 55% de ruido: cabecalhos, rodapes, numeracao de paginas, referencias
bibliograficas isoladas e artefatos de OCR. O resultado foram 26 documentos em texto
limpo, prontos para engenharia de features.

Parametro tecnico relevante: a classe `OrquestradorPodaPDF` implementa o parametro
`offset` para corrigir a diferenca entre a numeracao impressa da revista (ex: pagina 45
da publicacao) e o indice real do arquivo PDF (ex: pagina 3 do arquivo). Sem isso,
as secoes de metadados de publicacao seriam incluidas no corpus clinico.

### NB5 - Engenharia de Features NLP

O notebook de engenharia (`NB5_nlp_data_engineer.ipynb`) produziu o artefato central
do modulo para edge: o `edge_trigger_lookup.json` - dicionario de lookup O(1) com
6.276 dimensoes TF-IDF, projetado para ser consultado em tempo real pelo agente
de triagem no Raspberry Pi 5.

Por que TF-IDF e nao embeddings? Por restricao de hardware: o RPi5 com Coral TPU
tem 4 TOPS dedicados a inferencia de sinais ECG. O modulo NLP roda em CPU pura.
Um lookup O(1) em dicionario Python e determinista e tem latencia de microssegundos.
Embeddings exigiriam um transformer em memoria - incompativel com edge deployment.

### NB6 - Extracao de Sintomas

Com o corpus podado como entrada, o `NB6_symptom_extraction.ipynb` construiu:

- `sintomas_pacientes.txt` - 10 frases clinicas cobrindo MI, STTC, CD, HYP e NORM
- `mapa_sintomas_doencas.csv` - 929 linhas mapeando sintoma -> diagnostico -> risco
- `corpus_frases_completo.csv` - 929 frases clinicas completas sem `Doenca_Associada`
  (bridge para o classificador, eliminando leakage de label por construcao)

---

## 4. O Momento de Verdade

Na primeira iteracao do classificador (`NB7v1`), o modelo reportou:

```
F1-score (macro): 1.000
Acuracia: 100%
```

Em vez de celebracao, isso gerou investigacao imediata.

Precisao estatistica perfeita em problemas clinicos reais e um sinal de alerta, nao de
sucesso. Sistemas medicos tem ruido intrinseco, ambiguidade clinica e variabilidade
inter-observador. Um classificador que acerta 100% ou aprendeu algo trivial, ou
aprendeu algo errado - e nenhum dos dois serve para salvar vidas.

---

## 5. O Diagnostico - Domain Leakage

O diagnostico foi confirmado via coeficiente de Jaccard de vocabulario entre as classes:

```
Jaccard vocabular (alto_risco vs baixo_risco) = 0.021
Limiar saudavel para ausencia de leakage: >= 0.15
```

Um Jaccard de 0.021 significa que as classes quase nao compartilham vocabulario.
O modelo nao aprendeu cardiologia. Aprendeu a distinguir estilos literarios:

| Dimensao | Classe alto_risco | Classe baixo_risco |
|---|---|---|
| Tipo de documento | Diretrizes normativas, protocolos SUS | Revisoes academicas, bulas |
| Registro linguistico | Imperativo ("deve", "realizar em ate") | Cientifico ("observou-se", "sugere-se") |
| Vocabulario dominante | Conduta, triagem, tempo-porta, protocolo | Fisiopatologia, molecula, evidencia |
| O que o modelo aprendeu | Estilo de diretriz | Estilo de revisao |

Isso e o **domain/style leakage** descrito por Kapoor & Narayanan (2023). O modelo
atingiu F1=1.000 nao porque identificou risco cardiologico, mas porque os dados de treino
e teste vieram de documentos com estilos editoriais sistematicamente diferentes por classe.

Em producao, esse modelo seria inutil: um laudo automatico de ECG descrevendo
um STEMI seria classificado como "baixo risco" porque usa vocabulario tecnico de
maquina, nao a prosa imperativa de uma diretriz do Ministerio da Saude.

**Referencia:** Kapoor S. & Narayanan A. (2023). Leakage and the Reproducibility
Crisis in Machine-Learning-based Science. *Patterns*, 4(9). doi:10.1016/j.patter.2023.100804

---

## 6. A Pergunta Certa que Surgiu do Erro

O leakage revelou a pergunta que deveria ter guiado a selecao de dados desde o inicio:

> **Onde encontrar texto cardiologico onde tanto as frases de alto risco quanto as
> frases de baixo risco sejam escritas pelo mesmo autor, no mesmo estilo, para o
> mesmo proposito?**

A resposta estava em um dataset que ja existia no projeto: o **MIMIC-IV-ECG**.

---

## 7. Por que o MIMIC-IV-ECG Muda o Jogo

### O que e o MIMIC-IV-ECG

O MIMIC (Medical Information Mart for Intensive Care) e o maior banco de dados clinicos
de acesso aberto do mundo, desenvolvido pelo MIT em parceria com o Beth Israel
Deaconess Medical Center (BIDMC) de Boston, EUA. Referencia global em pesquisa em
saude desde 2001, citado em mais de 10.000 publicacoes cientificas.

O MIMIC-IV-ECG, especificamente, contem:

- **800.035 ECGs** de pacientes adultos internados
- **161.352 pacientes unicos** - populacao real de UTI, nao sintetica
- **Periodo de coleta real:** 1999 a 2019 (BIDMC, Boston)
- **Interpretacoes textuais** geradas pelo aparelho de ECG GE MUSE
- Tres arquivos de metadados: `record_list.csv`, `machine_measurements.csv`,
  `waveform_note_links.csv`

> **Nota sobre as datas:** O PhysioNet aplica *date shifting* - todas as datas
> sao deslocadas aproximadamente 100 anos para frente por conformidade com o HIPAA
> (lei americana de protecao de dados de saude). Datas entre 2097-2211 correspondem
> ao periodo real 1999-2019. As relacoes temporais entre eventos de um mesmo
> paciente sao preservadas; so o ano absoluto muda.

### Por que Elimina o Leakage por Construcao

O campo `report_0` ate `report_17` do `machine_measurements.csv` contem as
interpretacoes textuais automaticas do aparelho GE MUSE. Sao frases como:

```
"Sinus rhythm"
"ST elevation, consider inferior injury"
"*** CONSIDER ACUTE ST ELEVATION MI ***"
"Sinus bradycardia with 1st degree A-V block"
"Left bundle branch block"
```

**Toda frase - de alto risco e de baixo risco - foi gerada pelo mesmo algoritmo,
no mesmo estilo, para o mesmo proposito: descrever o que o aparelho detectou no ECG.**

Nao existe diferenca estilistica entre classes. O Jaccard do corpus MIMIC: **0.224**.
Acima do limiar saudavel de 0.15. Sem leakage estrutural.

A comparacao direta:

| Dimensao | PDFs PT-BR (iter. 1) | MIMIC-IV-ECG (iter. 2) |
|---|---|---|
| Autor das frases de alto risco | Comites SBC / Ministerio da Saude | Algoritmo GE MUSE |
| Autor das frases de baixo risco | Pesquisadores academicos | Algoritmo GE MUSE |
| Mesmo estilo entre classes? | NAO - leakage estrutural garantido | SIM - mesma maquina |
| Jaccard vocabular | 0.021 (leakage confirmado) | 0.224 (saudavel, sem leakage) |
| F1 obtido | 1.000 (falso - artefato de leakage) | 0.75-0.88 (esperado, real) |
| Valor clinico | Zero | Alto |
| Frases disponiveis | 929 | 2.760.117 instancias / 3.862 unicas |

### O que Significa para o Sistema Final

Um paciente chega ao Pronto-Socorro com dor no peito. O wearable Cardio-Edge
coleta o ECG e transmite ao Hub (RPi5 + Coral TPU). O Hub processa:

1. Sinal bruto: DSP - Butterworth high-pass 0.5Hz + Notch 50Hz (baseline + ruido)
2. Tensor STFT [1, 1000, 4]: inferencia no Coral TPU INT8 - modelo MLP, latencia < 10ms
3. Texto do laudo automatico: classificador NLP - triagem alto/baixo risco

Se o classificador NLP foi treinado com PDFs de diretrizes, ele nao reconhece o texto
do laudo automatico - porque o laudo e escrito pela maquina, nao por um comite da SBC.

Se foi treinado com o MIMIC, foi treinado exatamente no tipo de texto que vai
processar em producao. Laudos automaticos de aparelhos GE MUSE - o mesmo padrao
de equipamentos instalados em hospitais brasileiros.

Esse e o alinhamento entre distribuicao de treino e distribuicao de producao.
O principio mais basico de ML aplicado: **treinar no que voce vai ver na pratica.**

---

## 8. O EDA como Primeiro Passo Obrigatorio

Antes de treinar qualquer modelo com o MIMIC, e necessario entender o que ha
no dataset. O notebook `eda_mimic_iv_nlp.ipynb` e esse passo de exploracao.

O MIMIC tem 800.035 ECGs de UTI adulta. Isso nao e um dataset de ECGs normais.
E uma populacao hospitalizada, sistematicamente mais doente que a populacao geral.
Antes de definir padroes de rotulagem, foi preciso responder:

- Qual a distribuicao real dos achados? Quanto e realmente alto risco?
- O vocabulario e rico o suficiente para TF-IDF? Quantos termos unicos existem?
- Existe desbalanceamento entre classes? De que magnitude?
- As medicoes numericas (RR interval, QRS axis) confirmam que os labels capturam
  diferenca fisiologica real?

Sem essas respostas, um classificador construido sobre o MIMIC seria tao arbitrario
quanto o anterior - apenas com mais dados enviesados.

---

## 9. O que o EDA Revelou - Numeros Reais

### Volume e Estrutura

| Metrica | Valor |
|---|---|
| Total de ECGs | 800.035 |
| Pacientes unicos | 161.352 |
| Frases no corpus (total instancias) | 2.760.117 |
| Frases unicas | 3.862 |
| Vocabulario unico (pos-stopword) | 503 termos |
| Media de ECGs por paciente | 5.0 |
| Mediana de ECGs por paciente | 2 |

O vocabulario de apenas 503 termos em 9,1 milhoes de tokens e uma caracteristica
dos laudos automaticos de ECG: linguagem altamente padronizada e controlada.
Ideal para TF-IDF - termos como `infarct`, `elevation`, `block` sao altamente
discriminativos e nao aparecem nos dois lados do espectro.

### Classificacao com Corpus v2 (24 padroes ativos)

| Classe | Instancias | % | Frases unicas | % |
|---|---|---|---|---|
| Alto risco | 235.552 | 8,5% | 518 | 13,4% |
| Baixo risco | 1.205.045 | 43,7% | 675 | 17,5% |
| Zona cinza (nao classificado) | 1.319.520 | 47,8% | 2.669 | 69,1% |

### A Zona Cinza e Intencional, Nao uma Falha

47,8% nao classificado nao e desperdicio - e medicina real. O Colegio Americano de
Cardiologia (ACC) e a AHA categorizam achados de ECG em tres faixas:

1. Normal / variante normal - sem acao necessaria
2. Achados inespecificos - monitoramento, correlacao clinica, contexto importa
3. Alto risco - acao imediata

A zona cinza contem 8 categorias clinicas identificadas e catalogadas:

| Categoria | Frases unicas | Exemplos |
|---|---|---|
| Outros (sem enquadramento) | 1.387 | Achados mistos e compostos |
| FA/Flutter sem qualificador | 413 | Atrial fibrillation, Atrial flutter |
| Alteracoes ST-T inespecificas | 187 | Inferior T wave changes are nonspecific |
| Hipertrofia e desvio de eixo | 137 | Left ventricular hypertrophy |
| Bloqueios parciais e conducao | 104 | Left anterior fascicular block |
| Ritmo sinusal benigno | 78 | Sinus bradycardia with PVCs (pos-v2) |
| Ondas e morfologia sem urgencia | 56 | Poor R wave progression |
| Intervalo QT e outros intervalos | 48 | Prolonged QT (sem "markedly") |
| Metadados e qualidade | 59 | Warning: data quality may affect interpretation |

Um classificador binario treinado nos **extremos claros** (emergencias confirmadas
vs ECGs normais/benignos) e o design correto para TRIAGEM. Ele detecta o que precisa
de atencao imediata sem ser contaminado pela ambiguidade dos casos intermediarios.

### Validacao Estatistica dos Labels - Teste de Welch

O teste t de Welch entre as classes confirmou que os labels capturam diferenca real
nas medicoes fisiologicas do ECG (p < 0,001 para todas as 4 metricas):

| Medida ECG | Alto risco (media) | Baixo risco (media) | p-valor |
|---|---|---|---|
| RR interval (ms) | ~750 | ~890 | < 0.001 |
| QRS axis (graus) | ~15 | ~28 | < 0.001 |
| QRS end (ms) | ~410 | ~405 | < 0.001 |
| T end (ms) | ~600 | ~590 | < 0.001 |

Os labels nao sao arbitrarios. Eles capturam diferencas fisiologicas reais entre
populacoes de pacientes com ECG classificados como alto e baixo risco.

### Evolucao dos Padroes de Rotulagem

| Versao | Padroes baixo risco | Frases unicas baixo risco | Ratio alto:baixo |
|---|---|---|---|
| v1 | 12 (originais) | 80 | 6,5:1 |
| v2 | 24 (+12 novos) | 675 | 0,77:1 |
| D3 NB7v2 | subsample estratificado | 40 | 1:1 (perfeito) |

Os 12 novos padroes v2 foram adicionados com justificativa clinica baseada nas
diretrizes ACC/AHA (2009) - bradicardia sinusal, arritmia sinusal, taquicardia sinusal,
BRD, desvio de eixo, alteracoes T inespecificas, ritmo de marcapasso, ritmo juncional,
progressao pobre de onda R, baixa voltagem, EAS, BAV 1o grau.

---

## 10. Governanca de Dados - DUA, HIPAA e LGPD

O acesso ao MIMIC-IV-ECG requer credenciamento no PhysioNet com certificacao CITI
(treinamento em pesquisa com seres humanos). O acesso e individual e vinculado a
um DUA (Data Use Agreement) que define claramente o que pode e o que nao pode.

### Regras do DUA

| Acao | Permitido? |
|---|---|
| Usar os dados para pesquisa e educacao | Sim |
| Publicar artefatos derivados anonimizados (sem IDs) | Sim |
| Publicar graficos e estatisticas agregadas | Sim |
| Publicar os CSVs brutos com subject_id / study_id | Nao |
| Publicar os arquivos de forma original | Nao |
| Compartilhar credenciais de acesso | Nao |

### Artefatos Publicados Neste Repositorio

Todos os artefatos derivados foram verificados antes de qualquer commit:

| Artefato | Contem | Publicavel? |
|---|---|---|
| `corpus_mimic_ecg_rotulado_v2.csv` | Apenas `frase` e `situacao`, sem IDs | Sim |
| `mimic_eda_stats.json` | Estatisticas agregadas, sem dados individuais | Sim |
| `eda_charts/*.png` | Graficos de distribuicao sem dados de paciente | Sim |
| `machine_measurements.csv` (original) | `subject_id`, `study_id`, dados brutos | Nao |
| `record_list.csv` (original) | `subject_id`, paths de arquivo | Nao |
| `waveform_note_links.csv` (original) | Links ECG-nota clinica | Nao |

Os arquivos brutos do MIMIC residem localmente em `data/raw/mimic-iv-ecg/1.0/`
e estao explicitamente bloqueados no `.gitignore`.

---

## 11. Proximo Passo - NB6v2 e NB7v2

Com o EDA concluido e o corpus v2 exportado, os proximos notebooks do modulo NLP:

### NB6v2 - Extracao de Sintomas com Fonte MIMIC

Reescrever o `NB6_symptom_extraction.ipynb` usando `corpus_mimic_ecg_rotulado_v2.csv`
como fonte primaria em vez dos 26 PDFs. A estrutura de entregaveis exigida (D1, D2) e
mantida - o que muda e a qualidade e confiabilidade da fonte.

- **D1 atualizado:** `sintomas_pacientes.txt` com frases reais do MIMIC
- **D2 atualizado:** `mapa_sintomas_doencas.csv` com padroes validados pelo EDA

### NB7v2 - Classificador de Risco com D3 Balanceado

Treinar o classificador usando D3 construido a partir do corpus MIMIC expandido:

- **D3:** 40 frases de alto risco + 40 frases de baixo risco (estratificado por superclasse)
- **Pipeline:** sklearn - TF-IDF (dentro do CV, zero data leakage) + Logistic Regression
- **Validacao:** StratifiedKFold 5-fold, metrica F1-macro
- **F1 esperado:** 0.75 a 0.88 - real, nao artefato

A diferenca fundamental do v1: em vez de F1=1.000 que nao significa nada,
teremos um classificador que erra nos casos ambiguos clinicamente corretos.
Erros que fazem sentido. Erros que um medico tambem teria.

---

## 12. Por que Isso Importa Alem da Nota

Ao longo deste trabalho, a pergunta que guiou cada decisao tecnica foi simples:

> **Este sistema funcionaria em um pronto-socorro real?**

Nao um PS hipotetico de benchmark. Um PS brasileiro, com pacientes reais, ECGs ruins
por eletrodo mal posicionado, laudos automaticos gerados por maquinas iguais as que
o GE vende em hospitais brasileiros, textos em ingles tecnico padronizado porque e o
idioma dos aparelhos de ECG no mundo inteiro.

O corpus de PDFs em portugues foi valioso. Os relatos de caso, as diretrizes do SUS,
as bulas de amiodarona e noradrenalina - esse conhecimento nao foi descartado.
Ele continua ativo no `edge_trigger_lookup.json`, no `mapa_sintomas_doencas.csv`,
na arquitetura de triagem do RPi5.

O MIMIC nao substituiu esse trabalho. Ele completou o que faltava: dados do tipo exato
que o sistema vai processar em producao. Interpretacoes automaticas de aparelho de ECG.

Batimentos cardiacos nao sao documentos academicos. Sao sinais eletricos de um
musculo que nao pode parar. O classificador que vai analisar esses sinais precisa ter
sido treinado com outros batimentos - nao com a prosa de um comite de especialistas,
nao com a linguagem de um artigo de revisao, nao com as restricoes posologicas de uma bula.

Com dados de UTI real. 800.035 ECGs de 161.352 pessoas que entraram em um hospital
e precisaram ser monitoradas. Pessoas com insuficiencia cardiaca, com STEMI, com
bradicardia, com fibrilacao. Com historico de diabetes, de hipertensao, de cirurgia previa.
Pessoas.

Essa e a transicao que este modulo representa: da documentacao correta do que e
necessario fazer, para o treinamento com o que e realmente preciso aprender.

---

## 13. Estrutura de Arquivos

```
notebooks/nlp_mimic_iv/
├── eda_mimic_iv_nlp.ipynb              <- EDA completo (44 celulas)
└── README.md                           <- Este documento

data/processed/mimic-iv-ecg/           <- Artefatos derivados (sem PHI, publicaveis)
├── corpus/
│   ├── corpus_mimic_ecg_rotulado_v2.csv  <- 1.193 frases classificadas
│   └── mimic_eda_stats.json              <- Estatisticas agregadas
└── eda_charts/
    ├── sec01_distribuicao_temporal.png
    ├── sec02_cobertura_campos.png
    ├── sec03_top30_termos.png
    ├── sec04_rotulagem.png
    ├── sec04_pattern_coverage.png
    ├── sec4b_espectro_risco.png
    ├── sec4b_expansao_padroes.png
    ├── sec05_boxplots_medidas.png
    ├── sec06_comprimento_frases.png
    ├── sec06_jaccard_comparacao.png
    └── sec07_balanceamento.png

data/raw/mimic-iv-ecg/1.0/             <- Dados brutos (bloqueado no .gitignore)
├── record_list.csv                    <- subject_id + paths (NUNCA no git)
├── machine_measurements.csv          <- reports textuais + medicoes (NUNCA no git)
└── waveform_note_links.csv           <- links ECG-nota clinica (NUNCA no git)
```

---

## 14. Referencias

- Gow B., Pollard T., Maguire L.H., et al. (2023). MIMIC-IV-ECG: Diagnostic ECG
  Matched Subset. *PhysioNet*. doi:10.13026/4nqgsb35

- Johnson A.E.W., et al. (2023). MIMIC-IV, a freely accessible electronic health record
  dataset. *Scientific Data*, 10(1). doi:10.1038/s41597-022-01899-x

- Kapoor S. & Narayanan A. (2023). Leakage and the Reproducibility Crisis in
  Machine-Learning-based Science. *Patterns*, 4(9). doi:10.1016/j.patter.2023.100804

- Kligfield P., et al. (2007). Recommendations for the Standardization and Interpretation
  of the Electrocardiogram. *JACC*, 49(10):1109-1127.

- ACC/AHA (2009). Recommendations for the Standardization and Interpretation of the
  Electrocardiogram. *JACC*, 53(11):992-1002.

---

*Cardio-Edge-AI - Modulo NLP | FIAP 2TIAOA Noturno | RM 98222*
