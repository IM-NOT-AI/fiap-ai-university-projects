# Cardio-Edge-AI - Entregáveis Fase 1
### Challenge: Artificial Intelligence - FIAP 2026 - 2TIAOA

> **Isaac Maciel** - RM98222 - 2TIAOA - Turno Noturno

---

## Critérios de Avaliação

> Observação do professor de IA: esta pasta foi estruturada para que a banca localize os entregáveis principais com agilidade. Organizada em três subpastas correspondentes às três partes do enunciado: **numérico**, **nlp** e **imagens**.

<p align="center">
  <img src="assets/enunciado_pt4.png" alt="Critérios de Avaliação - Challenge AI Cardiology - Rubrica de Notas" width="720"/>
</p>

---

## Certificação Ética - CITI Program

<p align="center">
  <img src="assets/citi_badge.png" alt="CITI Program Badge - Isaac Maciel" width="400"/>
</p>

8 módulos concluídos: Belmort Report, IRB, HIPAA, populações vulneráveis, conflito de interesses, pesquisa genética, registros médicos e protocolos de conformidade.

---

## Repositório Completo (GitHub)

**https://github.com/IM-NOT-AI/fiap-ai-university-projects**

Histórico completo de commits, decisões arquiteturais, arquivos DVC e toda a documentação técnica e ética do projeto. Commits marcados com `[ENTREGAVEL FASE 1]` identificam cada entregável da sprint com precisão.

---

## Artefatos de Grande Volume (Google Drive)

<p align="center">
  <strong>🔗 <a href="https://drive.google.com/drive/folders/1VKOVi9aioCM5aYMujowbaGDUdODWfTKs?usp=drive_link">Google Drive - Data Lake - Cardio-Edge-AI - Fase 1</a></strong>
</p>

Disponível no Drive por exceder o limite de 256 MB da plataforma:

| Arquivo | Tamanho | Descrição |
|---|---|---|
| `holter_iot_data_simulation.csv` | 468 MB | Dataset sintético Holter 24h - 5.000 pacientes, 35 features ECG/IMU/SpO2 |
| `X_img_train.npy` | 1.018 MB | Tensor de imagens de treino - 15.051 espectrogramas 224x224 |
| `X_img_val.npy` | 131 MB | Tensor de imagens de validação |
| `X_img_test.npy` | 128 MB | Tensor de imagens de teste |

---

## Nota sobre Versionamento de Imagens no Git

> **Aviso de boas práticas:** As amostras de imagens ECG em `imagens/` estão versionadas diretamente no Git a pedido do enunciado (entrega via repositório GitHub). Em um projeto real de produção, **imagens e binários de grande volume nunca devem ser commitados no Git** - o correto é rastrear via DVC, Git LFS ou armazenar em serviços de objeto (S3, GCS). O conjunto completo (100 espectrogramas + 100 grids de 12 derivações) está no Google Drive e versionado via DVC no repositório principal.

---

## Submissão via Portal do Aluno FIAP

Este pacote foi preparado para entrega pela **plataforma do estudante FIAP** (portal.fiap.com.br). O fluxo de entrega é o seguinte:

1. Compactar esta pasta como `entregaveis_fase1.zip`
2. Acessar o Portal do Aluno - área do Challenge AI Cardiology - Fase 1
3. Realizar o upload do `.zip` no campo de entrega da sprint
4. Incluir no campo de observações o link do GitHub e do Google Drive acima

> Os artefatos que excedem o limite de upload estão integralmente disponíveis no Google Drive e versionados via DVC no repositório GitHub.

---

## Estrutura deste Pacote

```
entregaveis_fase1/
|
+-- README.md                                    <- este arquivo
|
+-- assets/                                      <- visuais de referência
|   +-- enunciado_pt4.png                        <- rubrica de avaliação (10 pts)
|   +-- citi_badge.png                           <- badge CITI Program, ética em pesquisa
|
+-- numerico/                                    <- Parte 1 - Dados Numéricos (IoT)
|   +-- ptbxl_engineered_features.csv            <- 6.665 Gêmeos Digitais (features PTB-XL)
|   +-- ptbxl_gateway_fallback.csv               <- 15.051 registros fallback
|   +-- NB1_ptbxl_eda.ipynb                      <- EDA PTB-XL, análise exploratória
|   +-- NB2_holter_iot_simulation.ipynb          <- Simulação IoT Holter 24h
|
+-- nlp/                                         <- Parte 2 - Dados Textuais (NLP)
|   +-- edge_trigger_lookup.json                 <- léxico de gatilho clínico
|   +-- NB4_nlp_data_pruning.ipynb               <- Poda do corpus clínico PT-BR
|   +-- NB5_nlp_data_engineer.ipynb              <- ETL semântico, lookup de gatilho
|   +-- corpus/                                  <- 26 textos clínicos PT-BR (.txt)
|       +-- bula_profissional_*.txt
|       +-- diretriz_sbc_*.txt
|       +-- diretriz_sus_*.txt
|       +-- protocolo_sus_*.txt
|       +-- relato_caso_*.txt
|       +-- revisao_*.txt
|
+-- imagens/                                     <- Parte 3 - Dados Visuais (Visão Computacional)
|   +-- NB3_ptbxl_signal_vision_eda.ipynb        <- Pipeline DSP e espectrogramas
|   +-- espectrogramas/                          <- 5 amostras de espectrogramas Mel (ECG)
|   |   +-- espectrograma_paciente_000[0-4].png
|   +-- ecg_12_derivacoes/                       <- 5 amostras de grids 12 derivações
|       +-- grid_12_leads_paciente_000[0-4].png
|
+-- docs/                                        <- documentação técnica por notebook
    +-- ptbxl_report_data_source.md              <- decisão e justificativa PTB-XL
    +-- ptbxl_eda.md                             <- relatório EDA (NB1)
    +-- holter_iot_data_simulation.md            <- relatório simulação Holter (NB2)
    +-- ptbxl_signal_vision_eda.md               <- relatório visão computacional (NB3)
    +-- nlp_data_pruning.md                      <- relatório poda do corpus (NB4)
    +-- nlp_data_engineer.md                     <- relatório engenharia semântica (NB5)
```

---

## Entregáveis por Requisito da Sprint

### Requisito 1 - Pesquisa e Seleção de Dataset
- **Decisão:** PTB-XL v1.0.3 (CC BY 4.0) - 21.799 ECGs, 71 diagnósticos SCP-ECG
- **Descarte documentado:** PPG-DaLiA (incompatibilidade), MIMIC-IV-ECG (credenciamento em andamento)
- **Documentação:** `docs/ptbxl_report_data_source.md`

### Requisito 2 - Ética em Pesquisa (CITI Program)
- **Certificação:** 8 módulos - badge disponível em `assets/citi_badge.png`
- **Documentação completa:** repositório GitHub em `docs/citi/`

### Requisito 3 - Análise Exploratória (NB1)
- **Notebook:** `numerico/NB1_ptbxl_eda.ipynb`
- **Artefatos:** `numerico/ptbxl_engineered_features.csv` (6.665 Gêmeos Digitais), `numerico/ptbxl_gateway_fallback.csv`
- **Documentação:** `docs/ptbxl_eda.md`

### Requisito 4 - Simulação IoT / Edge Computing (NB2)
- **Notebook:** `numerico/NB2_holter_iot_simulation.ipynb`
- **Dataset:** `holter_iot_data_simulation.csv` (468 MB - Google Drive)
- 5.000 pacientes sintéticos, 24h, 35 features, calibração arquitetural wearable
- **Documentação:** `docs/holter_iot_data_simulation.md`

### Requisito 5 - Visão Computacional / DSP (NB3)
- **Notebook:** `imagens/NB3_ptbxl_signal_vision_eda.ipynb`
- **Amostras versionadas no Git:** `imagens/espectrogramas/` e `imagens/ecg_12_derivacoes/` (5 amostras cada)
- **Pipeline:** filtros Butterworth, espectrogramas Mel, grids 12 derivações, tensores multimodais
- Tensores completos (`X_img_*.npy`, 1.3 GB) no Google Drive
- **Documentação:** `docs/ptbxl_signal_vision_eda.md`

### Requisito 6 - Corpus NLP Clínico - Poda (NB4)
- **Notebook:** `nlp/NB4_nlp_data_pruning.ipynb`
- **Corpus:** `nlp/corpus/` - 26 textos PT-BR: diretrizes SBC/SUS, bulas, relatos de caso, revisões sistemáticas

### Requisito 7 - Engenharia Semântica NLP (NB5)
- **Notebook:** `nlp/NB5_nlp_data_engineer.ipynb`
- **Artefato:** `nlp/edge_trigger_lookup.json` - léxico de gatilho clínico
- **Documentação:** `docs/nlp_data_engineer.md`

---

## Ambiente de Execução

| Componente | Versão |
|---|---|
| Python (CPU) | 3.12.x |
| Python (GPU) | 3.10.14 |
| TensorFlow GPU | 2.10.0 |
| NumPy | 1.26.4 |
| Dataset principal | PTB-XL v1.0.3 (CC BY 4.0) |

**Venv:** `.fiap_venv_py312` (CPU), `.fiap_venv_py310` (GPU/TF)

---

*Cardio-Edge-AI - FIAP AI 2026 - Challenge Artificial Intelligence - Fase 1*
