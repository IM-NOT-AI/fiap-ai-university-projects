# PBL - Modulo NLP de Diagnostico Cardiologico
### Fase 2 - Parte 1 (Extracao de Sintomas) + Parte 2 (Classificador de Risco)

> Isaac Maciel - RM98222 - 2TIAOA - Turno Noturno

---

## AVISO IMPORTANTE PARA A BANCA

> Os arquivos desta pasta sao **copias** dos originais localizados em:
>
> **Projeto principal:** `challenge/ai_cardiology/` (raiz do repositorio)
>
> - Notebooks originais: `challenge/ai_cardiology/notebooks/`
> - Dados processados: `challenge/ai_cardiology/data/processed/`
> - Repositorio GitHub: **https://github.com/IM-NOT-AI/fiap-ai-university-projects**
>
> Todos os notebooks aqui contem os **outputs de execucao completos**. Voce pode
> abrir e auditar qualquer `.ipynb` sem precisar re-executar.

---

## Onde Esta Cada Entregavel (Acesso Rapido)

| Entregavel | Arquivo nesta pasta | Criterio FIAP |
|---|---|---|
| D1 - 10 frases de sintomas de pacientes | `data/processed/D1_sintomas_pacientes.txt` | PBL Parte 1 |
| D2 - Mapa sintoma-doenca (929 linhas) | `data/processed/D2_mapa_sintomas_doencas.csv` | PBL Parte 1 |
| D3 - Frases rotuladas alto/baixo risco (**oficial**) | `data/processed/D3_frases_risco_rotuladas_v2_mimic.csv` | PBL Parte 2 |
| Codigo PBL Parte 1 v1 | `notebooks/NB6_symptom_extraction.ipynb` | PBL Parte 1 |
| Codigo PBL Parte 2 v1 (referencia leakage) | `notebooks/NB7_risk_classifier.ipynb` | PBL Parte 2 |
| Codigo EDA corpus MIMIC | `notebooks/nlp_mimic_iv/NB9_eda_nlp_mimic_iv.ipynb` | Auditoria |
| Codigo Parte 1 v2 MIMIC | `notebooks/nlp_mimic_iv/NB10_symptom_extraction.ipynb` | PBL Parte 1 |
| Codigo Parte 2 v2 MIMIC (**oficial**) | `notebooks/nlp_mimic_iv/NB11_risk_classifier.ipynb` | PBL Parte 2 |
| Modelo pkl treinado (9.8 KB) | `data/processed/model/nb11_tfidf_logreg.pkl` | Artefato |
| Graficos EDA/leakage (NB9) | `data/processed/charts_nb9_eda/` (11 PNGs) | Avaliacao |
| Graficos extracao sintomas (NB6) | `data/processed/charts_nb6_extracao/` (17 PNGs) | Avaliacao |
| Iteracao v1 completa (referencia) | `data/processed/v1_pt_br/` | Auditoria |

---

## Estrutura Detalhada desta Pasta

```
pbl/
+-- README.md                              <- este arquivo
|
+-- notebooks/
|   +-- NB6_symptom_extraction.ipynb       <- Parte 1 v1: extracao sintomas PT-BR (72 celulas)
|   +-- NB7_risk_classifier.ipynb          <- Parte 2 v1: classificador PT-BR (F1=1.0 - leakage)
|   +-- nlp_mimic_iv/
|       +-- NB9_eda_nlp_mimic_iv.ipynb     <- EDA MIMIC-IV-ECG, analise Jaccard, diagnostico
|       +-- NB10_symptom_extraction.ipynb  <- Parte 1 v2: D1 real + D2 35 regras ACC/AHA
|       +-- NB11_risk_classifier.ipynb     <- Parte 2 v2: ENTREGAVEL OFICIAL
|
+-- data/
    +-- raw/
    |   +-- .gitkeep                       <- corpus bruto nao incluido (MIMIC restrito PhysioNet)
    |                                         (PDFs PT-BR rastreados via DVC no projeto principal)
    +-- processed/
        +-- D1_sintomas_pacientes.txt          <- 10 frases de pacientes (v1 PT-BR)
        +-- D2_mapa_sintomas_doencas.csv       <- mapa sintoma-doenca 929 linhas 7 colunas
        +-- D3_frases_risco_rotuladas_v2_mimic.csv  <- 100 frases MIMIC (ENTREGAVEL OFICIAL D3)
        +-- corpus_mimic_ecg_rotulado_v2.csv   <- 1.193 frases rotuladas NB9 (base do NB11)
        +-- mimic_eda_stats.json               <- estatisticas e metricas do corpus MIMIC
        +-- model/
        |   +-- nb11_tfidf_logreg.pkl          <- MODELO OFICIAL (pipeline sklearn, 9.8 KB)
        +-- charts_nb9_eda/                    <- 11 PNGs do NB9
        |   +-- sec01_distribuicao_temporal.png
        |   +-- sec02_cobertura_campos.png
        |   +-- sec03_top30_termos.png
        |   +-- sec04_pattern_coverage.png
        |   +-- sec04_rotulagem.png
        |   +-- sec4b_espectro_risco.png
        |   +-- sec4b_expansao_padroes.png
        |   +-- sec05_boxplots_medidas.png
        |   +-- sec06_comprimento_frases.png
        |   +-- sec06_jaccard_comparacao.png   <- GRAFICO-CHAVE: diagnostico do leakage
        |   +-- sec07_balanceamento.png
        +-- charts_nb6_extracao/               <- 17 PNGs do NB6
        |   +-- chart1_corpus_composicao.png ... chart11_diagnostico_sugestao.png
        |   +-- nb10_mimic_ed_profile.png
        |   +-- sec_d2_cobertura.png ... sec5_heatmap_acuidade_disposicao.png
        +-- v1_pt_br/                          <- ITERACAO ANTERIOR (referencia historica)
            +-- D3_frases_risco_rotuladas_v1_ptbr.csv   <- D3 v1 (80 frases PT-BR)
            +-- model/
            |   +-- risk_classifier.pkl        <- modelo v1 (F1=1.0 - leakage)
            |   +-- tfidf_vectorizer.pkl
            |   +-- experiment_log.json
            |   +-- model_card.md
            |   +-- optimal_threshold.json
            +-- charts_nb7/                    <- 12 PNGs do NB7
```

---

## Resultados Finais - NB11 (Entregavel Oficial)

| Metrica | Valor |
|---|---|
| Acuracia de teste | 96.0% |
| F1 macro | 0.970 |
| ROC-AUC | 1.000 |
| CV 5-fold | 0.970 +/- 0.024 |
| Falsos Negativos (alto risco perdido) | **0** |
| Falsos Positivos | 1 ("right bundle branch block") |
| Vocabulario aprendido | 185 termos |
| Tamanho do modelo pkl | 9.8 KB |
| Deploy alvo | Raspberry Pi 5 (inferencia assincrona) |

**Modelo:** Pipeline sklearn — TfidfVectorizer(ngram_range=(1,2), max_features=1000)
+ LogisticRegression(C=1.0, class_weight='balanced'). Serializado em `model/nb11_tfidf_logreg.pkl`.

---

## Por Que Existem Duas Versoes (v1 e v2)

### v1 PT-BR - F1 = 1.000 (Leakage de Dominio)

O NB7 atingiu F1 = 1.000 com o corpus PT-BR da Fase 1. Resultado suspeito — auditoria imediata.

**Causa raiz:** o corpus misturava dois tipos de documentos com estilos radicalmente distintos:
- **Alto risco** → diretrizes SBC/SUS: vocabulario academico-normativo, estrutura formal
- **Baixo risco** → relatos de caso SciELO/BVS: vocabulario narrativo-clinico, variavel por autor

O modelo aprendeu o **estilo do documento**, nao o conteudo diagnostico.
Metrica objetiva: **Jaccard de vocabulario entre classes = 0.021** (saudavel: > 0.15).
Ver grafico: `charts_nb9_eda/sec06_jaccard_comparacao.png`

### v2 MIMIC - F1 = 0.970 (Resultado Real)

Pivote para MIMIC-IV-ECG: 800.035 ECGs com laudos gerados pelo algoritmo GE MUSE.
O mesmo algoritmo gera os laudos para todos os exames — vocabulario identico para
alto e baixo risco. O modelo e forcado a aprender o conteudo clinico.
**Jaccard pos-pivote = 0.224** (range saudavel).

| Indicador | v1 PT-BR | v2 MIMIC | Limite saudavel |
|---|---|---|---|
| F1 reportado | 1.000 | **0.970** | < 0.99 |
| Jaccard vocabulario entre classes | 0.021 | **0.224** | > 0.15 |
| Corpus por classe | diferente | identico (GE MUSE) | identico |
| Falsos Negativos | 0 (trivial) | **0 (real)** | 0 |
| Veredicto | Leakage | **Entregavel oficial** | — |

A iteracao v1 permanece em `data/processed/v1_pt_br/` como registro de maturidade de
engenharia: diagnosticar e corrigir problemas de qualidade de dados e parte do processo.

---

## Como Re-Executar (Opcional)

O ambiente completo esta documentado em `challenge/ai_cardiology/` do repositorio principal.

```bash
# Ativar ambiente CPU (Python 3.12)
.fiap_venv_py312\Scripts\activate

# Executar na ordem:
# 1. NB6 - extracao sintomas v1 (opcional, saidas ja presentes)
# 2. NB9 - EDA MIMIC (requer acesso PhysioNet)
# 3. NB10 - extracao sintomas v2 (requer acesso PhysioNet)
# 4. NB11 - classificador v2 (requer corpus_mimic_ecg_rotulado_v2.csv do NB9)
```

> Os notebooks nesta pasta ja tem outputs completos — nao e necessario re-executar para avaliacao.
