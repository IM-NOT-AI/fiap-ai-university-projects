# Cardio-Edge-AI - Entregaveis Fase 2
### Challenge: Artificial Intelligence - FIAP 2026 - 2TIAOA

> **Isaac Maciel** - RM98222 - 2TIAOA - Turno Noturno

---

## AVISO IMPORTANTE PARA A BANCA

> Esta pasta (`entregaveis_fase2/`) e um **pacote curado de entrega** com copias dos
> arquivos essenciais para avaliacao. O **projeto completo** reside em:
>
> `challenge/ai_cardiology/` — codigo-fonte, notebooks com outputs, dados processados,
> historico de commits, documentacao tecnica e artefatos DVC.
>
> Repositorio GitHub: **https://github.com/IM-NOT-AI/fiap-ai-university-projects**
>
> Os notebooks nesta pasta sao **copias identicas** dos originais em
> `challenge/ai_cardiology/notebooks/`, com todos os outputs de execucao preservados.
> Voce pode abrir qualquer `.ipynb` aqui e ver os resultados sem re-executar.

---

## Como Navegar Este Pacote (Guia Rapido)

| Voce quer avaliar... | Va para... |
|---|---|
| Extracao de sintomas + mapa de conhecimento (PBL Parte 1) | `pbl/notebooks/NB6_symptom_extraction.ipynb` |
| Classificador de risco com TF-IDF (PBL Parte 2, **entregavel oficial**) | `pbl/notebooks/nlp_mimic_iv/NB11_risk_classifier.ipynb` |
| D1 - 10 frases de pacientes | `pbl/data/processed/D1_sintomas_pacientes.txt` |
| D2 - mapa sintoma-doenca (929 linhas) | `pbl/data/processed/D2_mapa_sintomas_doencas.csv` |
| D3 - frases rotuladas (100 frases, v2 MIMIC oficial) | `pbl/data/processed/D3_frases_risco_rotuladas_v2_mimic.csv` |
| Modelo pkl treinado (9,8 KB) | `pbl/data/processed/model/nb11_tfidf_logreg.pkl` |
| Graficos de avaliacao do classificador (NB9 EDA) | `pbl/data/processed/charts_nb9_eda/` |
| Graficos de extracao de sintomas (NB6) | `pbl/data/processed/charts_nb6_extracao/` |
| Graficos e modelo da iteracao v1 PT-BR | `pbl/data/processed/v1_pt_br/` |
| Portal React (codigo-fonte) | `ir_alem_1/src/` |
| Portal React (como executar) | `ir_alem_1/README.md` |
| Notebook MLP ECG | `ir_alem_2/notebooks/mlp_ecg_heartbeat.ipynb` |
| Modelo MLP (.keras e .tflite INT8) | `ir_alem_2/data/processed/models/` |
| Amostras de ECG por classe (15 PNGs) | `ir_alem_2/data/processed/images/ecg_samples/` |
| Graficos de avaliacao MLP | `ir_alem_2/data/processed/charts/` |

---

## Estrutura Completa deste Pacote

```
entregaveis_fase2/
|
+-- README.md                              <- este arquivo (guia geral)
|
+-- pbl/                                   <- PBL: Parte 1 + Parte 2 do enunciado NLP
|   +-- README.md                          <- guia detalhado, metricas, leakage
|   +-- notebooks/
|   |   +-- NB6_symptom_extraction.ipynb   <- extracao sintomas v1 (PT-BR corpus)
|   |   +-- NB7_risk_classifier.ipynb      <- classificador v1 (F1=1.0, leakage - referencia)
|   |   +-- nlp_mimic_iv/
|   |       +-- NB9_eda_nlp_mimic_iv.ipynb     <- EDA MIMIC, diagnostico do leakage
|   |       +-- NB10_symptom_extraction.ipynb  <- D1 real MIMIC-IV-ED + D2 ACC/AHA
|   |       +-- NB11_risk_classifier.ipynb     <- ENTREGAVEL OFICIAL (acc=0.96, FN=0)
|   +-- data/
|       +-- raw/
|       |   +-- .gitkeep                   <- corpus bruto restrito (MIMIC PhysioNet + DVC)
|       +-- processed/
|           +-- D1_sintomas_pacientes.txt          <- D1 entregavel
|           +-- D2_mapa_sintomas_doencas.csv       <- D2 entregavel (929 linhas)
|           +-- D3_frases_risco_rotuladas_v2_mimic.csv  <- D3 entregavel oficial
|           +-- corpus_mimic_ecg_rotulado_v2.csv   <- 1.193 frases NB9
|           +-- mimic_eda_stats.json               <- estatisticas do corpus
|           +-- model/
|           |   +-- nb11_tfidf_logreg.pkl          <- MODELO OFICIAL (9.8 KB)
|           +-- charts_nb9_eda/                    <- 11 PNGs (inclui Jaccard plot)
|           +-- charts_nb6_extracao/               <- 17 PNGs extracao sintomas
|           +-- v1_pt_br/                          <- iteracao anterior (referencia)
|               +-- D3_frases_risco_rotuladas_v1_ptbr.csv
|               +-- model/                         <- pkl NB7, experiment_log, threshold
|               +-- charts_nb7/                    <- 12 PNGs NB7
|
+-- ir_alem_1/                             <- Ir Alem 1: Portal React + Vite
|   +-- README.md                          <- instrucoes npm install/run dev, credenciais
|   +-- index.html
|   +-- package.json
|   +-- vite.config.js
|   +-- src/                               <- CODIGO-FONTE COMPLETO
|       +-- contexts/AuthContext.jsx       <- JWT simulado
|       +-- hooks/useAuth.js
|       +-- services/authService.js        <- mock JWT
|       +-- services/mockData.js           <- 15 pacientes PTB-XL
|       +-- components/                    <- Layout, Navbar, PrivateRoute, Modal, Toast
|       +-- pages/                         <- Login, Dashboard, Patients, Appointments
|
+-- ir_alem_2/                             <- Ir Alem 2: MLP ECG com Keras (NB8)
    +-- README.md                          <- arquitetura, metricas, conformidade enunciado
    +-- notebooks/
    |   +-- mlp_ecg_heartbeat.ipynb        <- NOTEBOOK COMPLETO COM OUTPUTS
    +-- data/
        +-- processed/
            +-- models/
            |   +-- nb8_mlp_ecg_best.keras     <- modelo Keras (melhor val_accuracy)
            |   +-- nb8_mlp_ecg_int8.tflite    <- TFLite INT8 (102.5 KB, < 1ms)
            +-- images/
            |   +-- ecg_samples/               <- 15 PNGs (3 por classe x 5 classes)
            +-- charts/                        <- 6 PNGs (training_curves, confusion_matrix...)
            +-- experiment_log_nb8.json        <- MLOps, hash MD5, metricas
            +-- model_card_nb8.md              <- documentacao do modelo
```

---

## Jornada Tecnica da Fase 2

### Iteracao 1: Corpus PT-BR (NB6 + NB7)

Ponto de partida: reutilizacao do corpus de 26 textos clinicos PT-BR da Fase 1
(diretrizes SBC, protocolos SUS, bulas ANVISA, relatos de caso SciELO/BVS).

- NB6 extraiu sintomas e produziu D1/D2 com 929 linhas de mapa de conhecimento.
- NB7 treinou TF-IDF + Logistic Regression e obteve **F1 = 1.000**.

O F1 perfeito acionou alerta de qualidade: **leakage de dominio**.
Os textos de diretrizes (SBC/SUS) tinham estilo academico distinto dos relatos clinicos.
Jaccard de vocabulario entre classes = **0.021** (threshold saudavel: > 0.15).

### Iteracao 2: Corpus MIMIC-IV-ECG (NB9 + NB10 + NB11) - ENTREGAVEL OFICIAL

Pivote para o MIMIC-IV-ECG (800.035 ECGs, PhysioNet/MIT). Os laudos sao gerados
pelo algoritmo automatizado GE MUSE — vocabulario identico para alto e baixo risco.
Jaccard pos-pivote = **0.224** (range saudavel, modelo aprende conteudo clinico real).

- NB9: EDA do corpus, selecao de 1.193 frases, diagnostico formal do leakage.
- NB10: D1 com 10 chiefcomplaints reais do MIMIC-IV-ED, D2 com 35 regras ACC/AHA.
- NB11: D3 com 100 frases, TF-IDF + LogReg, **acc=0.96, ROC-AUC=1.0, FN=0, 9.8 KB**.

### Comparativo Final

| Versao | Corpus | F1 | FN | Jaccard | Veredicto |
|---|---|---|---|---|---|
| v1 PT-BR (NB7) | 26 PDFs SBC/SUS/ANVISA | 1.000 | 0 | 0.021 | Leakage de dominio |
| **v2 MIMIC (NB11)** | 1.193 laudos GE MUSE | **0.970** | **0** | **0.224** | **Entregavel oficial** |

---

## Submissao via Portal do Aluno FIAP

1. Compactar esta pasta como `entregaveis_fase2.zip`
2. Acessar o Portal do Aluno - Challenge AI Cardiology - Fase 2
3. Realizar upload do `.zip`
4. Incluir no campo de observacoes o link do GitHub

> Notebooks com outputs completos e historico de commits no repositorio GitHub.
> Dados brutos do MIMIC-IV nao estao incluidos (acesso restrito PhysioNet/CITI Program).
