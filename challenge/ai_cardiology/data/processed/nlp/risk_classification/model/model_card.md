# Model Card - CardioIA Risk Classifier (NB7)

**Gerado automaticamente em:** 2026-04-13T16:47:20.754112
**Autor:** Isaac Maciel - RM 98222 - 2TIAOA - Turno Noturno - FIAP AI 2026

---

## Uso Pretendido

Classificação binaria de frases clinicas em **alto risco** (MI, STTC, CD, HYP) ou **baixo risco** (NORM) com base em texto livre de sintomas. Componente do modulo NLP do sistema Cardio-Edge-AI, executado no hub Raspberry Pi 5 + Google Coral TPU.

**Uso adequado:** Triagem inicial de queixas clinicas em contexto hospitalar PT-BR.
**Uso inadequado:** Diagnostico definitivo, substituicao de avaliacao medica, populacoes nao-cardiologicas.

---

## Dados de Treinamento

| Campo | Valor |
|---|---|
| Fonte | corpus_frases_completo.csv (NB6, 929 frases de 26 documentos PT-BR) |
| Amostras D3 | {len(df_d3_load)} frases (40 alto risco / 40 baixo risco) |
| Hash MD5 (D3) | {data_hash_d3} |
| Linguas | Portugues Brasileiro (PT-BR) |
| Dominio | Cardiologia clinica (hospitalar e academica) |

---

## Arquitetura do Modelo

- **Vetorizacao:** TF-IDF (max_features={best_gs_params.get('tfidf__max_features', 500)}, ngram_range={best_gs_params.get('tfidf__ngram_range', '(1,2)')}, sublinear_tf=True)
- **Classificador:** {best_nome} (C={best_gs_params.get('clf__C', 1.0)}, class_weight=balanced)
- **Pipeline:** sklearn.pipeline.Pipeline (TF-IDF fit apenas no treino - sem data leakage)

---

## Metricas de Desempenho

| Metrica | Valor | IC 95% Bootstrap |
|---|---|---|
| Acuracia (teste) | {test_results[best_nome]['accuracy']:.4f} | [{np.percentile(boot_acc, 2.5):.4f}, {np.percentile(boot_acc, 97.5):.4f}] |
| F1 Macro (teste) | {test_results[best_nome]['f1_macro']:.4f} | [{np.percentile(boot_f1, 2.5):.4f}, {np.percentile(boot_f1, 97.5):.4f}] |
| F1 Alto Risco | {test_results[best_nome]['f1_alto']:.4f} | [{np.percentile(boot_f1_alto, 2.5):.4f}, {np.percentile(boot_f1_alto, 97.5):.4f}] |
| CV F1 Macro | {cv_results_all[best_nome]['test_f1_macro'].mean():.4f} +/- {cv_results_all[best_nome]['test_f1_macro'].std():.4f} | - |
| AUC-ROC | {roc_auc_score((y_test=='alto risco').astype(int), y_prob_alto_fin):.4f} | [{np.percentile(boot_auc, 2.5):.4f}, {np.percentile(boot_auc, 97.5):.4f}] |
| AP Score | {ap_score:.4f} | - |
| Limiar Otimo (clinico) | {optimal_thresh:.2f} | - |

---

## Limitacoes e Vieses

1. **Corpus pequeno:** 80 amostras de treinamento. Metricas de teste tem alta variancia (IC Bootstrap largo).
2. **Vies de representacao:** Baixo risco representado exclusivamente por revisoes academicas, nao por linguagem clinica narrativa de pacientes normais.
3. **Populacao alvo estreita:** Treinado em texto medico PT-BR de cardiologia - nao generaliza para outras especialidades ou idiomas.
4. **Limiar de decisao:** Limiar default 0.5 pode gerar FN clinicamente perigosos. Usar limiar otimo {optimal_thresh:.2f} em producao.
5. **Sem contexto temporal:** Modelo nao diferencia sintomas agudos de cronicos.

---

## Governanca

- class_weight=balanced: SIM
- Pipeline sem data leakage: SIM  
- Validacao cruzada estratificada: SIM (StratifiedKFold k={CV_FOLDS})
- Analise de Falsos Negativos: SIM (FN critico documentado)
- Risco de vies identificado: MEDIO (ver Secao 17)

---

*Cardio-Edge-AI - FIAP AI 2026 - Fase 2 - Modulo NLP*
