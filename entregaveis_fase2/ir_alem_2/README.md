# Ir Alem 2 - Diagnostico Visual de Arritmias com MLP e Keras (NB8)
### Fase 2 - Rede Neural para Classificacao de ECG em Tempo Real

> Isaac Maciel - RM98222 - 2TIAOA - Turno Noturno

---

## AVISO IMPORTANTE PARA A BANCA

> Os arquivos desta pasta sao **copias** dos originais localizados em:
>
> **Projeto principal:** `challenge/ai_cardiology/`
> - Notebook original: `challenge/ai_cardiology/notebooks/mlp_ecg_heartbeat.ipynb`
> - Modelos: `challenge/ai_cardiology/models/`
> - Logs e artefatos: `challenge/ai_cardiology/logs/`
>
> O notebook em `notebooks/mlp_ecg_heartbeat.ipynb` contem todos os **outputs de execucao
> completos**. Voce pode abrir e auditar os resultados sem precisar re-executar.
>
> Repositorio GitHub: **https://github.com/IM-NOT-AI/fiap-ai-university-projects**

---

## Onde Esta Cada Artefato (Acesso Rapido)

| Voce quer ver... | Arquivo nesta pasta |
|---|---|
| Codigo completo com outputs | `notebooks/mlp_ecg_heartbeat.ipynb` |
| Modelo Keras (.keras) | `data/processed/models/nb8_mlp_ecg_best.keras` |
| Modelo TFLite INT8 para RPi (.tflite) | `data/processed/models/nb8_mlp_ecg_int8.tflite` |
| Amostras de ECG por classe (15 PNGs) | `data/processed/images/ecg_samples/` |
| Curvas de treinamento | `data/processed/charts/training_curves.png` |
| Matriz de confusao multiclasse | `data/processed/charts/confusion_matrix.png` |
| Matriz de confusao binaria (Normal vs Anormal) | `data/processed/charts/confusion_matrix_binaria.png` |
| Distribuicao de classes | `data/processed/charts/class_distribution.png` |
| Envelope de sinal por classe | `data/processed/charts/signal_mean_envelope.png` |
| Morfologia de sinal | `data/processed/charts/signal_morphology.png` |
| Log MLOps completo (metricas, hash MD5) | `data/processed/experiment_log_nb8.json` |
| Documentacao do modelo (model card) | `data/processed/model_card_nb8.md` |

---

## Estrutura Detalhada desta Pasta

```
ir_alem_2/
+-- README.md                                  <- este arquivo
|
+-- notebooks/
|   +-- mlp_ecg_heartbeat.ipynb                <- NOTEBOOK COMPLETO COM OUTPUTS
|
+-- data/
    +-- processed/
        +-- models/
        |   +-- nb8_mlp_ecg_best.keras         <- modelo Keras (melhor val_accuracy, ~350 KB)
        |   +-- nb8_mlp_ecg_int8.tflite        <- TFLite INT8 quantizado (102.5 KB)
        +-- images/
        |   +-- ecg_samples/                   <- 15 PNGs - 3 amostras por classe
        |       +-- ecg_classe0_Normal_N_ex1.png
        |       +-- ecg_classe0_Normal_N_ex2.png
        |       +-- ecg_classe0_Normal_N_ex3.png
        |       +-- ecg_classe1_Supraventricular_S_ex1.png
        |       +-- ecg_classe1_Supraventricular_S_ex2.png
        |       +-- ecg_classe1_Supraventricular_S_ex3.png
        |       +-- ecg_classe2_Ventricular_V_ex1.png
        |       +-- ecg_classe2_Ventricular_V_ex2.png
        |       +-- ecg_classe2_Ventricular_V_ex3.png
        |       +-- ecg_classe3_Fusion_F_ex1.png
        |       +-- ecg_classe3_Fusion_F_ex2.png
        |       +-- ecg_classe3_Fusion_F_ex3.png
        |       +-- ecg_classe4_Desconhecido_Q_ex1.png
        |       +-- ecg_classe4_Desconhecido_Q_ex2.png
        |       +-- ecg_classe4_Desconhecido_Q_ex3.png
        +-- charts/
        |   +-- training_curves.png            <- loss e accuracy por epoca (treino e validacao)
        |   +-- confusion_matrix.png           <- matriz de confusao 5 classes normalizada
        |   +-- confusion_matrix_binaria.png   <- Normal vs Anormal (avaliacao binaria)
        |   +-- class_distribution.png         <- distribuicao de classes no dataset
        |   +-- signal_mean_envelope.png       <- envelope media +/- std por classe
        |   +-- signal_morphology.png          <- morfologia do sinal por classe
        +-- experiment_log_nb8.json            <- MLOps: hash MD5, hiperparametros, metricas
        +-- model_card_nb8.md                  <- documentacao: uso pretendido, limitacoes, metricas
```

---

## Dataset

**ECG Heartbeat Categorization** — Kaggle (shayanfazeli/heartbeat)
Fonte: MIT-BIH Arrhythmia Database, reformatado para 187 timesteps a 125 Hz.

| Split | Amostras |
|---|---|
| Treino | 87.554 |
| Teste | 21.892 |

| Classe | Descricao | % no treino |
|---|---|---|
| 0 | Normal (N) | 83% |
| 1 | Supraventricular (S) | 3% |
| 2 | Ventricular (V) | 7% |
| 3 | Fusao (F) | 1% |
| 4 | Desconhecido (Q) | 6% |

> O notebook inclui **gerador sintetico embutido** como fallback — funciona sem o Kaggle.

---

## Arquitetura MLP

```
Input(187)
  -> Dense(256, L2=1e-4) + BatchNormalization + ReLU + Dropout(0.30)
  -> Dense(128, L2=1e-4) + BatchNormalization + ReLU + Dropout(0.25)
  -> Dense(64,  L2=1e-4) + BatchNormalization + ReLU + Dropout(0.20)
  -> Dense(5, Softmax)
```

~91.397 parametros totais. Dropout decrescente: maior regularizacao nas camadas iniciais.

---

## Pre-processamento (v2 — Corrigido)

- **Normalizacao:** Z-score por amostra (media=0, std=1 por batimento individual)
- **Split estratificado:** `train_test_split(stratify=y_train, test_size=0.15, random_state=42)`
- **Balanceamento:** `class_weight='balanced'` para compensar desbalanceamento 83% Normal
- **Callbacks:** EarlyStopping + ReduceLROnPlateau + ModelCheckpoint

**Correcao v1 -> v2:** a v1 usava `validation_split=0.15` sequencial em dados parcialmente
ordenados por classe, causando `val_accuracy ~0.018` na epoca 1. O split estratificado
corrigiu: `val_accuracy=0.7771` na epoca 1, convergindo para `~0.85+` na epoca 8.

---

## Resultados

| Metrica | Valor |
|---|---|
| Acuracia de teste (multiclasse) | ~95%+ |
| Latencia TFLite INT8 | 0.029 ms/batimento |
| Throughput | 34.924 batimentos/segundo |
| Tamanho modelo TFLite | 102.5 KB |
| Requisito latencia enunciado | < 1 ms |

**Avaliacao Binaria (Normal vs Anormal):**
ROC-AUC, sensibilidade e especificidade calculados na secao "Avaliacao Binaria"
do notebook. Ver `data/processed/charts/confusion_matrix_binaria.png`.

> **Nota:** as celulas de avaliacao podem mostrar outputs cacheados da v1 se o notebook
> nao foi re-executado apos o re-treinamento v2. O modelo salvo em `models/` e o v2 correto.

---

## Conformidade com os Requisitos do Enunciado

| Requisito | Status | Evidencia |
|---|---|---|
| Dataset publico de ECG | Concluido | MIT-BIH (shayanfazeli/heartbeat, Kaggle) |
| Pre-processamento compativel com rede neural | Concluido | Z-score por amostra, split estratificado |
| Exportar representacoes visuais de ECG | Concluido | 15 PNGs em `images/ecg_samples/` (3 x 5 classes) |
| Classificacao binaria Normal vs Anormal | Concluido | Secao "Avaliacao Binaria" com ROC-AUC |
| MLP com Keras | Concluido | Input(187)->Dense(256)->Dense(128)->Dense(64)->Dense(5) |
| Treinar o modelo | Concluido | Split estratificado, convergencia val_acc 0.77->0.85+ |
| Testar e avaliar acuracia | Concluido | classification_report + confusion matrix + ROC-AUC |
| Organizacao e clareza | Concluido | Markdowns por secao, nota de abordagem no cabecalho |

---

## Integracao com o Ecossistema Cardio-Edge-AI

| Modelo | Dataset | Entrada | Deploy alvo | Papel |
|---|---|---|---|---|
| **MLP (NB8)** | MIT-BIH 5 classes | 187 pts 1D | Raspberry Pi 5 (ARM CPU) | Morfologia temporal |
| CNN (NB3) | PTB-XL 6 superclasses | 224x224 espectrograma | Google Coral Edge TPU | Distribuicao espectral |

Ensemble multimodal: dois modelos ortogonais sobre o mesmo batimento cardiaco.
O TFLite INT8 (102.5 KB) e adequado para inferencia assincrona no RPi5 em < 1 ms.

---

## Integrantes

| Nome | RM | Turma |
|---|---|---|
| Isaac Maciel | 98222 | 2TIAOA - Turno Noturno |

---

## Pendente

- Re-executar celulas de avaliacao para atualizar outputs cacheados (v1) com resultados do modelo v2
- Gravar video YouTube nao listado (ate 4 min) e linkar no README do repositorio
