# O Prova Matemática da Dimensionalidade no Edge Computing

A decisão de limitar a ingestão de dados a um número restrito de documentos (em contraste com abordagens massivas de *Big Data*) é fundamentada em restrições físicas e matemáticas inerentes à computação de borda. No **Nó 3 (Raspberry Pi 5)**, os recursos de CPU e memória RAM são compartilhados e altamente restritos, operando sob limites térmicos severos.

O modelo de Extração de Características utilizado (TF-IDF) gera uma matriz bidimensional onde as linhas correspondem aos documentos ($D$) e as colunas representam o vocabulário único total ($V$).

### A Complexidade de Busca e o Paradoxo de Zipf

A Lei de Zipf demonstra empiricamente que a expansão do número de documentos em um *corpus* médico resulta em um crescimento não-linear do vocabulário, inflado rapidamente por jargões raros, variações morfológicas e erros de digitalização (OCR).

O tempo de inferência dinâmica ($T_{inf}$), definido como o tempo necessário para o orquestrador varrer a matriz e recuperar a diretriz clínica correta em tempo real, cresce linearmente em função do tamanho do vocabulário:

$$T_{inf} = O(V \times D)$$

Simultaneamente, o impacto na memória RAM ($M_{ram}$), assumindo o uso de tensores de ponto flutuante de 64 bits (8 bytes), é dado por:

$$M_{ram} = D \times V \times 8 \text{ bytes}$$

### A Justificativa do Funil de Curadoria e Poda (Data Pruning)

Se escalássemos a base bruscamente para $D = 1000$ documentos e um vocabulário de $V = 100.000$ palavras únicas, o peso da matriz causaria esgotamento de memória. Mais criticamente, a execução do algoritmo de *Fuzzy Matching* (Distância de Levenshtein) contra um dicionário de $100.000$ raízes semânticas levaria a CPU ARM do Raspberry Pi a 100% de utilização. Este pico de processamento causaria *Thermal Throttling* (estrangulamento térmico), resultando na perda de pacotes vitais (telemetria do ECG) e comprometendo a integridade do monitoramento em tempo real.

Para viabilizar o *Minimum Viable Product* (MVP) em *Edge Computing* com latência na casa dos milissegundos, a matriz foi rigorosamente purificada. Através de um processo de **Data Pruning** (utilizando inferência do modelo Gemini 3.1 iterado sobre os documentos brutos para mapear as páginas clinicamente relevantes), expurgamos a metodologia acadêmica e referências bibliográficas. Isso reduziu o volume bruto dos PDFs em até 89.8%, otimizando o *Feature Space* final a exatas **6.276 dimensões** de alto valor diagnóstico, retendo apenas o núcleo duro da inteligência.

---

## Estruturação de Diretórios e Fluxo Físico (Flattened Data Lake)

Para cobrir todos os eixos de decisão clínica sem violar as restrições matemáticas provadas acima, abdicamos de subpastas profundas e consolidamos o *Data Lake* bruto em uma estrutura plana (*Flattened*) no diretório `data/raw/nlp`. A taxonomia ortogonal agora é governada estritamente por **prefixos de arquivo**, contendo 26 artefatos homologados:

* 📄 **`diretriz_*` / `protocolo_*`**: O eixo da Ação Legal e Triagem (Protocolos SUS e SBC).
* 📄 **`relato_caso_*`**: O eixo da Fenotipagem e Narrativa (Evolução de sintomas em UTI).
* 📄 **`revisao_*`**: O eixo do Contexto e Comorbidades (Tabelas de estratificação de risco e biomarcadores).
* 📄 **`bula_profissional_*`**: O eixo da Intervenção Química (Posologia exata, diluição e interações medicamentosas).

### Da Entropia à Memória Inerte

O repositório abriga a coleção de PDFs brutos extraídos da SciELO, BVS e ANVISA. O pipeline de dados foi arquitetado para realizar a poda espacial por geometria (gerando os artefatos em `data/processed/nlp/pruned_pdfs`), seguida pela extração textual e sanitização morfológica (*Stemming* e *Fuzzy Matching* com limiar de 85% para isolar radicais puros). 

O objetivo final do pipeline não é processar a linguagem humana no momento da emergência médica, mas sim **pré-computar** a base. O texto é destilado offline e exportado como um artefato JSON estático para `data/processed/nlp/cleaned_txt/edge_trigger_lookup.json`. Esta transmutação converte uma busca matematicamente pesada de matrizes esparsas numa requisição direta de dicionário, reduzindo o tempo de inferência estrutural para a constante absoluta de $O(1)$.

### Convergência de Hardware: O Fluxo de Borda

O isolamento do processamento reflete a separação de responsabilidades no hardware para garantir latência zero:

1.  **Wearable (Sensor de Aquisição):** Coleta a voltagem analógica do paciente e transmite o vetor serial via BLE.

2.  **Raspberry Pi (Orquestrador e Conversor):** Recebe o sinal temporal bidimensional e o transforma em uma matriz espacial (Espectrograma).

3.  **Google Coral TPU (Aceleração Espacial):** Recebe o Espectrograma. Operando a 4 TOPS, a NPU executa a classificação convolucional (Ex: "Fibrilação Atrial: 98%") em tempo real. O Coral processa exclusivamente visão computacional quantizada (INT8), não linguagem natural.

4.  **Raspberry Pi (O Gatilho Assíncrono):** Ao interceptar o limite crítico de anomalia classificado pelo Coral, a CPU ARM do Pi ativa o módulo NLP dormente, consulta a *Lookup Table* no disco e projeta a ação clínica de resgate na tela (ex: *Cardioversão / Anticoagulação / Varfarina*), isolando o estresse computacional e viabilizando o socorro médico imediato.