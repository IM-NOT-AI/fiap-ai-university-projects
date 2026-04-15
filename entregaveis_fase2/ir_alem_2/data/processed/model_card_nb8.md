# Model Card - NB8 MLP ECG Heartbeat Classifier

## Descricao

Rede MLP para classificacao de arritmias cardiacas em batimentos ECG segmentados.
Treinada no dataset MIT-BIH Arrhythmia (Kaggle: shayanfazeli/heartbeat).

## Tarefa

Classificacao multiclasse (5 classes) a partir de 187 pontos de sinal ECG.

## Dataset

- Fonte: MIT-BIH Arrhythmia Database, re-processado por Shayan Fazeli
- Treino: 87,554 amostras | Teste: 21,892 amostras
- Features: 187 pontos de sinal ECG a 360 Hz (~0.52s por batimento)
- Normalizacao: min-max global [0,1] na criacao + Z-score por amostra

## Classes

| ID | Nome                | Treino | Teste |
|----|---------------------|--------|-------|
|  0 | Normal (N)          | 72.471 | 18.118 |
|  1 | Supraventricular (S)|  2.223 |    556 |
|  2 | Ventricular (V)     |  5.788 |  1.448 |
|  3 | Fusion (F)          |    641 |    162 |
|  4 | Desconhecido (Q)    |  6.431 |  1.608 |

## Arquitetura

MLP: Input(187) -> Dense(256,BN,DR0.30) -> Dense(128,BN,DR0.25) -> Dense(64,BN,DR0.20) -> Dense(5,softmax)
Parametros totais: ~91,397

## Metricas no Conjunto de Teste

- Acuracia: 0.9464
- F1 Macro: 0.7994
- F1 Weighted: 0.9525

~~~
                      precision    recall  f1-score   support

          Normal (N)     0.9939    0.9466    0.9696     18118
Supraventricular (S)     0.4542    0.8381    0.5891       556
     Ventricular (V)     0.8594    0.9454    0.9004      1448
          Fusion (F)     0.4111    0.9136    0.5670       162
    Desconhecido (Q)     0.9565    0.9857    0.9709      1608

            accuracy                         0.9464     21892
           macro avg     0.7350    0.9259    0.7994     21892
        weighted avg     0.9642    0.9464    0.9525     21892

~~~

## Latencia

- TFLite INT8: 102.5 KB
- Latencia CPU (local): 0.039 ms/batimento
- Alvo Coral TPU: <1ms

## Limitacoes

- Treinado em 1 derivacao (MLII do MIT-BIH) - pode nao generalizar para outras derivacoes
- Dataset dos anos 90 com equipamento especifico - variabilidade real pode ser maior
- NAO deve ser usado como diagnostico clinico definitivo - apenas triagem automatizada

## Uso Pretendido

Triagem de arritmias em wearable cardiaco (Wearable XIAO nRF52840 + ADS1293),
rodando no Coral TPU acoplado ao Raspberry Pi 5 (Hub do projeto Cardio-Edge-AI).
