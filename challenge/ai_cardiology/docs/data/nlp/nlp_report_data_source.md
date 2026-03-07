<details open>
<summary><strong><font size="5">📗 4º Arquitetura de Dados NLP - Mapeamento de Corpus Clínico e Governança de Fontes CardioIA</font></strong></summary>
<br>

<details open>
<summary><strong><font size="4">Escopo Técnico e Governança de Dados</font></strong></summary>
<br>

<p align="justify">
O desenvolvimento de sistemas de Inteligência Artificial voltados para a cardiologia no cenário brasileiro enfrenta um obstáculo crítico de engenharia: a carência de corpora textuais anotados que reflitam a realidade operativa do Sistema Único de Saúde, SUS, e da prática clínica nacional. O projeto <strong>CardioIA</strong>, em sua Fase 1, viabiliza essa lacuna através da construção de um Corpus Textual robusto, desenhado para o treinamento e fine tuning de modelos de Processamento de Linguagem Natural, NLP.
</p>

<p align="justify">
A estratégia de governança estabelece uma separação rígida entre as camadas de dados:
</p>

<ul>
  <li><strong>Camada Raw Data (<code>data/raw/nlp/</code>):</strong> Reservada exclusivamente para o armazenamento dos arquivos brutos, como os PDFs originais e documentos desestruturados. Estes ativos são imutáveis e servem de entrada para os pipelines de extração.</li>
  <li><strong>Camada de Documentação (<code>docs/assets/data/nlp/</code>):</strong> Local onde reside este relatório, os metadados de contexto e as referências técnicas, sem misturar massa de dados bruta com documentação de projeto.</li>
</ul>

<p align="justify">
A curadoria utilizou a metodologia <strong>Data Centric AI</strong>, priorizando a autoridade e densidade informativa dos dados sobre a complexidade algorítmica. As fontes selecionadas abrangem o Ministério da Saúde, a Sociedade Brasileira de Cardiologia, SBC, SciELO e a Biblioteca Virtual em Saúde, BVS.
</p>

</details>

<br>

<details open>
<summary><strong><font size="4">1º Arquétipo: Diretrizes e Protocolos</font></strong></summary>
<br>

* **Título Original:** Protocolo Clínico e Diretrizes Terapêuticas (PCDT) da Síndrome Coronariana Aguda
* **Contexto:** Módulo Alvo: Classificador de Risco (Triagem) e Árvore de Decisão. Define métricas numéricas rígidas ("tempo porta-ECG") e regras imperativas de conduta no SUS.
* **Ano de Publicação:** 2021 (Atualizado em publicações da CONITEC)
* **Fonte:** Ministério da Saúde - https://www.gov.br/conitec/pt-br/midias/protocolos/protocolo_uso/pcdt_sindromescoronarianasagudas.pdf
* **Justificativa de Engenharia de Dados:** Apresenta alta densidade de métricas operacionais e de tempo-alvo. O texto é escrito no formato imperativo de conduta do SUS, sendo perfeito para calibrar o motor de NLP na extração de gatilhos e triagem de urgência.
* **Snippet de Validação:** "Pacientes com dor torácica ou sintomas sugestivos de infarto devem realizar um eletrocardiograma (ECG) em até 10 minutos a partir do início da triagem... O resultado deve constar na classificação de risco."
* **Nome do Arquivo:** `protocolo_sus_sindrome_coronariana.pdf`

<br>

* **Título Original:** Atualização da Diretriz de Ressuscitação Cardiopulmonar e Cuidados Cardiovasculares de Emergência da Sociedade Brasileira de Cardiologia
* **Contexto:** Base fundamental para suporte avançado de vida, focando em arritmias letais, parada cardiorrespiratória e choques elétricos.
* **Ano de Publicação:** 2019
* **Fonte:** Sociedade Brasileira de Cardiologia (SBC) - http://publicacoes.cardiol.br/portal/abc/portugues/2019/v11303/pdf/11303025.pdf
* **Justificativa de Engenharia de Dados:** Este documento fornece algoritmos determinísticos e fluxogramas rigorosos de Suporte Avançado de Vida em Cardiologia (ACLS). Sua estrutura baseada em ações sequenciais e checagens temporais é ideal para treinar a IA na extração de regras de resposta imediata a eventos críticos.
* **Snippet de Validação:** **Em Breve**
* **Nome do Arquivo:** `diretriz_sbc_ressuscitacao_cardiopulmonar.pdf`

<br>

* **Título Original:** Diretriz Brasileira de Fibrilação Atrial
* **Contexto:** Diretriz focada no manejo de Fibrilação Atrial, cruzando escores de risco com terapias de anticoagulação e reversão de ritmo.
* **Ano de Publicação:** 2024 / 2025
* **Fonte:** Sociedade Brasileira de Cardiologia (SBC) - https://sobrac.org/wp-content/uploads/2025/09/2025-0618_Diretriz-de-Fibrilacao-Atrial_port.x66747-1.pdf
* **Justificativa de Engenharia de Dados:** O texto é construído sobre o cruzamento de escores clínicos de risco (como o CHA2DS2-VASc) com regras estritas de anticoagulação e controle de frequência. Isso ensinará o modelo a vincular achados eletrocardiográficos diretamente com as respectivas "Classes de Recomendação" e "Níveis de Evidência".
* **Snippet de Validação:** **Em Breve**
* **Nome do Arquivo:** `diretriz_sbc_fibrilacao_atrial.pdf`

<br>

* **Título Original:** Diretrizes Brasileiras para Diagnóstico e Tratamento da Insuficiência Cardíaca com Fração de Ejeção Reduzida
* **Contexto:** Tratamento e diagnóstico da ICFER, com hierarquia de severidade baseada em sintomas físicos e resposta farmacológica.
* **Ano de Publicação:** 2018
* **Fonte:** Ministério da Saúde / CONITEC - https://www.gov.br/conitec/pt-br/midias/protocolos/20201211_relatorio_diretrizes_brasileiras_icfer_final_409_2018_publicao2020.pdf
* **Justificativa de Engenharia de Dados:** Contém a hierarquização estruturada das classes funcionais de gravidade clínica (ex: NYHA) mapeadas diretamente para restrições e dosagens farmacológicas precisas. É o arquétipo ideal para o sistema aprender a extrair parâmetros restritivos ("Se X, não faça Y") antes de sugerir intervenções.
* **Snippet de Validação:** **Em Breve**
* **Nome do Arquivo:** `diretriz_sus_insuficiencia_cardiaca.pdf`

<br>

* **Título Original:** Diretrizes da SBC sobre Angina Instável e IAM sem Supradesnível do Segmento ST
* **Contexto:** Módulo Alvo: Motor de Recomendação Terapêutica e Farmacologia de antiagregação e estratificação de risco isquêmico.
* **Ano de Publicação:** 2021
* **Fonte:** SciELO / SBC - https://www.scielo.br/j/abc/a/QvqxLFycJhLvNGFzPhsbZPF/?lang=pt
* **Justificativa de Engenharia de Dados:** É o texto mais denso em termos de farmacologia condicional (doses ajustadas por idade/peso). Ele ensina ao modelo não apenas qual remédio usar, mas quando não usar (contraindicações) e qual o nível de certeza científica daquela decisão (Nível de Evidência A, B ou C).
* **Snippet de Validação:** "Clopidogrel: Dose de ataque de 300 mg... (se idade > 75 anos, dose de apenas 75 mg)... Recomenda-se a utilização de escores validados, como o GRACE ou TIMI."
* **Nome do Arquivo:** `diretriz_sbc_angina_instavel.pdf`

</details>

<br>

<details open>
<summary><strong><font size="4">2º Arquétipo: Relatos Clínicos</font></strong></summary>
<br>

* **Título Original:** Evolução Tardia da Cardiomiopatia de Takotsubo Após TAVI
* **Contexto:** Módulo Alvo: Extração de Linha do Tempo (Temporalidade) e Processamento de Prontuário narrativo de paciente idoso com comorbidades.
* **Ano de Publicação:** **Em Breve**
* **Fonte:** SciELO - https://www.scielo.br/j/abcic/a/TrhrRv46grNPPmZwGvs5cnh/?lang=pt
* **Justificativa de Engenharia de Dados:** Diferente dos protocolos limpos, este texto simula a "sujeira" e a riqueza de um prontuário real. Ele mistura histórico pregresso, sintomas agudos e dados físicos numéricos, forçando seu modelo a conectar pontos temporais dispersos.
* **Snippet de Validação:** "Uma mulher de 77 anos foi internada com sintomas de falta de ar e chiado... A anamnese detalhada da paciente incluía hipertensão e TAVI realizado devido à estenose aórtica há quatro meses."
* **Nome do Arquivo:** `relato_caso_takotsubo.pdf`

<br>

* **Título Original:** Coronavírus e o Coração | Um Relato de Caso sobre a Evolução da COVID-19 Associado à Evolução Cardiológica
* **Contexto:** Rastreamento longitudinal cruzando o declínio sistêmico viral com a evolução de dano e inflamação cardiológica severa.
* **Ano de Publicação:** 2020
* **Fonte:** Arquivos Brasileiros de Cardiologia (SciELO) - https://www.scielo.br/j/abc/a/FhdvV9qsmPbL4KFfMqwtNBv/?format=pdf&lang=pt
* **Justificativa de Engenharia de Dados:** Apresenta marcadores temporais explícitos cruzando o declínio sistêmico com a evolução cardiológica (ex: "Em 16 de março de 2020..."). Excelente para treinar modelos de Extração de Relação Temporal e rastreamento longitudinal de comorbidades.
* **Snippet de Validação:** **Em Breve**
* **Nome do Arquivo:** `relato_caso_miocardite_covid19.pdf`

<br>

* **Título Original:** Miocardite após Coinfecção Recente por Vírus da Dengue e Chikungunya: Relato de Caso
* **Contexto:** Associação de infecções virais endêmicas (arboviroses) com miocardite aguda, integrando métricas laboratoriais fluidas na narrativa.
* **Ano de Publicação:** 2019
* **Fonte:** Arquivos Brasileiros de Cardiologia (SciELO) - https://www.scielo.br/j/abc/a/pxGbNgtjcq5m7JhgSMbMC7m/?format=pdf&lang=pt
* **Justificativa de Engenharia de Dados:** Este texto injeta tabelas laboratoriais com variação de unidades de medida (mg/dL, mmol/L, x10^9/L) no meio da prosa livre, forçando o parser do NER a associar o valor numérico à entidade clínica e temporal correta (Dia 1, Dia 2, Dia 4).
* **Snippet de Validação:** **Em Breve**
* **Nome do Arquivo:** `relato_caso_miocardite_coinfeccao_arboviroses.pdf`

<br>

* **Título Original:** Insuficiência Cardíaca e Arbovirose
* **Contexto:** Descrição de falência sistêmica associada a choque hemodinâmico induzido por patógenos tropicais.
* **Ano de Publicação:** 2020
* **Fonte:** Arquivos Brasileiros de Cardiologia (SciELO) - https://www.scielo.br/j/abc/a/6ktNcHzvtqMt5JjGc93KGmb/?format=pdf&lang=pt
* **Justificativa de Engenharia de Dados:** Traz o desafio da descrição de perfis hemodinâmicos misturados com progressão de falência de órgãos. O texto utiliza jargões clínicos de enfermaria (ex: "perfil hemodinâmico B9", "clearance de creatinina de 19 ml/min") ideais para a construção de dicionários fenotípicos.
* **Snippet de Validação:** **Em Breve**
* **Nome do Arquivo:** `relato_caso_ic_descompensada_arbovirose.pdf`

<br>

* **Título Original:** Cardiotoxicidade induzida pelo 5-Fluorouracil manifestada como Fibrilação Ventricular (Baseado no relato de 65 anos com carcinoma)
* **Contexto:** Mapeamento de iatrogenia (efeito adverso severo oncológico) resultando em arritmia cardíaca fatal em UTI.
* **Ano de Publicação:** 2023
* **Fonte:** PubMed Central (PMC) - https://pmc.ncbi.nlm.nih.gov/articles/PMC10735207/
* **Justificativa de Engenharia de Dados:** Altíssima densidade de escopos de negação médica ("não revelou qualquer estenose", "não mostrou anormalidade de perfusão"). Crucial para treinar a IA a não alucinar diagnósticos que o médico expressamente descartou na narrativa.
* **Snippet de Validação:** **Em Breve**
* **Nome do Arquivo:** `relato_caso_fibrilacao_ventricular_cardiotoxicidade.pdf`

<br>

* **Título Original:** Disfunção cardíaca associada à quimioterapia: um relato de caso
* **Contexto:** Correlação entre toxicidade progressiva quimioterápica e a redução gradual da capacidade mecânica de ejeção do ventrículo.
* **Ano de Publicação:** 2024
* **Fonte:** Revista de Medicina - USP (SciELO) - https://revistas.usp.br/revistadc/pt_BR/article/download/226320/209354/726639
* **Justificativa de Engenharia de Dados:** Ótimo para a modelagem de extração de frações de ejeção ecocardiográficas ao longo de um acompanhamento. Ele correlaciona valores numéricos de imagem (sistólica de 26%) com sinais físicos clássicos como taquicardia.
* **Snippet de Validação:** **Em Breve**
* **Nome do Arquivo:** `relato_caso_disfuncao_cardiaca_quimioterapia.pdf`

<br>

* **Título Original:** Infarto agudo do miocárdio com supradesnivelamento do segmento ST complicado por ruptura da parede livre
* **Contexto:** Relato de complicação mecânica isquêmica fatal, ensinando ao modelo a linha do tempo entre o evento oclusivo e o rasgo tecidual.
* **Ano de Publicação:** 2020
* **Fonte:** Arquivos Brasileiros de Cardiologia (PMC) - https://pmc.ncbi.nlm.nih.gov/articles/PMC8386952/
* **Justificativa de Engenharia de Dados:** Apresenta o clássico desafio NLP dos "marcadores temporais retroativos" ("Quatro dias antes, a paciente reportou..."). O modelo precisará entender o conceito de T-zero (momento da admissão) e projetar os sintomas num passado referencial.
* **Snippet de Validação:** **Em Breve**
* **Nome do Arquivo:** `relato_caso_iamcsst_ruptura_parede_livre.pdf`

<br>

* **Título Original:** Assistência Circulatória Mecânica Esquerda como Ponte para Candidatura na Miocardiopatia Chagásica
* **Contexto:** Doença miocárdica de etiologia parasitária endêmica requerendo suporte mecânico vital de bombeamento contínuo.
* **Ano de Publicação:** 2018
* **Fonte:** Arquivos Brasileiros de Cardiologia (SciELO) - https://www.scielo.br/j/abc/a/GGgt4WmRW7S35td5c4qXPZD/?format=pdf&lang=pt
* **Justificativa de Engenharia de Dados:** Riquíssimo em dados numéricos contínuos em formato de texto descritivo avançado (ex: "pressão sistólica do ventrículo direito de 30 mmHg"). Obriga a rede neural a isolar parâmetros específicos de cateterismo do resto da narrativa subjetiva.
* **Snippet de Validação:** **Em Breve**
* **Nome do Arquivo:** `relato_caso_assistencia_circulatoria_chagas.pdf`

<br>

* **Título Original:** Diretriz Brasileira de Fibrilação Atrial - Revisão Complementar
* **Contexto:** Artigo de revisão aprofundado consolidando a base teórica e fisiopatológica da Fibrilação Atrial e seus gatilhos elétricos.
* **Ano de Publicação:** **Em Breve**
* **Fonte:** **Em Breve**
* **Justificativa de Engenharia de Dados:** Incorpora densidade vetorial às ramificações de fisiopatologia elétrica atrial, garantindo que o algoritmo reconheça nuances no remodelamento do nó sinoatrial antes de recomendar condutas.
* **Snippet de Validação:** **Em Breve**
* **Nome do Arquivo:** `revisao_fibrilacao_atrial.pdf`

<br>

* **Título Original:** Dissecção aórtica de tipo B de Stanford: relato de caso e revisão de literatura
* **Contexto:** Urgência vascular maior atuando como o principal diagnóstico diferencial no paciente que chega à emergência com suspeita de infarto.
* **Ano de Publicação:** 2024
* **Fonte:** Brazilian Journal of Health (BrJoHealth) - https://brjohealth.com/index.php/ojs/article/download/160/150/286
* **Justificativa de Engenharia de Dados:** Ensina o modelo a mapear entidades anatômicas espaciais aliadas a sistemas de classificação por imagem (Classificação de Stanford B). Fundamental para o cruzamento de NLP com achados visuais sugerindo dor torácica catastrófica que não é Infarto.
* **Snippet de Validação:** **Em Breve**
* **Nome do Arquivo:** `relato_caso_disseccao_aortica_stanford.pdf`

</details>

<br>

<details open>
<summary><strong><font size="4">3º Arquétipo: Revisões Acadêmicas</font></strong></summary>
<br>

* **Título Original:** Síndrome Cardiorrenal Aguda: Qual Critério Diagnóstico Utilizar e sua Importância para o Prognóstico?
* **Contexto:** Fisiopatologia cruzada abordando a interseção patológica onde a falência da bomba cardíaca induz congestão e isquemia do filtro renal.
* **Ano de Publicação:** 2020
* **Fonte:** Arquivos Brasileiros de Cardiologia (SciELO) - https://www.scielo.br/j/abc/a/ppZHhz5H9yytzsfRnzY6Gmv/?format=pdf&lang=pt
* **Justificativa de Engenharia de Dados:** Apresenta definições determinísticas e critérios sintáticos sobre falência orgânica bidirecional, essencial para treinar a IA a mapear correlações estruturadas (triplas) entre sobrecarga hemodinâmica, níveis de creatinina sérica e remodelamento ventricular no Knowledge Graph, utilizando classificações como RIFLE e AKIN.
* **Snippet de Validação:** **Em Breve**
* **Nome do Arquivo:** `revisao_sindrome_cardiorrenal_criterios_prognostico.pdf`

<br>

* **Título Original:** Rastreamento, Diagnóstico e Manejo da Fibrilação Atrial em Pacientes com Câncer: Evidências Atuais e Perspectivas Futuras
* **Contexto:** Interação do estado sistêmico pró-trombótico oncológico com o desenvolvimento arritmogênico, fundando as bases da Cardio-Oncologia no sistema.
* **Ano de Publicação:** 2022
* **Fonte:** Arquivos Brasileiros de Cardiologia (SciELO) - https://www.scielo.br/j/abc/a/xJK5pNQGfPxQwT7JYq3QhKn/?format=pdf&lang=pt
* **Justificativa de Engenharia de Dados:** Enriquece a dimensionalidade do vocabulário com jargões oncológicos cruzados com arritmogênese, ensinando ao modelo de Word Embeddings a associar agentes antineoplásicos (antraciclinas, agentes alquilantes) a danos endoteliais, e processar paradoxos de risco (risco de sangramento vs. necessidade de anticoagulação).
* **Snippet de Validação:** **Em Breve**
* **Nome do Arquivo:** `revisao_fibrilacao_atrial_pacientes_cancer.pdf`

<br>

* **Título Original:** Ceramidas Plasmáticas na Estratificação de Risco das Doenças Cardiovasculares
* **Contexto:** Avanço da fisiopatologia clássica da placa de colesterol para as bases de sinalização molecular celular de esfingolipídios.
* **Ano de Publicação:** 2022
* **Fonte:** Arquivos Brasileiros de Cardiologia (SciELO) - https://www.scielo.br/j/abc/a/QpbKrSjbN6H3c6xs7hGYKjs/?format=pdf&lang=pt
* **Justificativa de Engenharia de Dados:** Apresenta altíssima densidade ontológica sobre vias de glicoesfingolipídios e sinalização inflamatória, crucial para o algoritmo aprender a hierarquia molecular que desencadeia resistência insulínica, apoptose celular e instabilidade de placa aterosclerótica.
* **Snippet de Validação:** **Em Breve**
* **Nome do Arquivo:** `revisao_ceramidas_plasmaticas_risco_cardiovascular.pdf`

<br>

* **Título Original:** GDF-15 como Biomarcador em Doenças Cardiovasculares
* **Contexto:** Avaliação preditiva baseada em cascatas inflamatórias, estresse oxidativo e sinalização celular reativa no remodelamento cardíaco.
* **Ano de Publicação:** 2021
* **Fonte:** Arquivos Brasileiros de Cardiologia (SciELO) - https://www.scielo.br/j/abc/a/yvpBJjjKg89LRZG94bdjQdM/?format=pdf&lang=pt
* **Justificativa de Engenharia de Dados:** Insere nomenclatura sistêmica profunda sobre superfamílias de citocinas inflamatórias e apoptose mediada, permitindo ao modelo dimensional conectar estímulos imunológicos à insuficiência cardíaca crônica. O GDF-15 atua como um nó super-conector no Grafo de Conhecimento.
* **Snippet de Validação:** **Em Breve**
* **Nome do Arquivo:** `revisao_gdf15_biomarcador_doencas_cardiovasculares.pdf`

<br>

* **Título Original:** Relações entre a Redução de Estrogênio, Obesidade e Insuficiência Cardíaca com Fração de Ejeção Preservada
* **Contexto:** O impacto do tecido adiposo como órgão endócrino inflamatório associado à transição menopausal na rigidez diastólica (ICFEP).
* **Ano de Publicação:** 2021
* **Fonte:** Arquivos Brasileiros de Cardiologia (SciELO) - https://www.scielo.br/j/abc/a/yMTqSCkTxhnkK3nZ43wCWKK/?format=pdf&lang=pt
* **Justificativa de Engenharia de Dados:** Maximiza a extração sintática de siglas interrelacionadas sobre adipocinas disfuncionais (TNF-α, IL-6) e perda de proteção hormonal, fornecendo o arcabouço lógico causal para o sistema correlacionar inflamação metabólica à hipertrofia concêntrica no espaço vetorial.
* **Snippet de Validação:** **Em Breve**
* **Nome do Arquivo:** `revisao_estrogenio_obesidade_insuficiencia_cardiaca.pdf`

<br>

* **Título Original:** Papel dos miRNAs na Fisiopatologia das Doenças Cardiovasculares
* **Contexto:** Estudo transcricional profundo da regulação genética não-codificante na angiogênese reativa e estabilidade vascular isquêmica.
* **Ano de Publicação:** 2018
* **Fonte:** Arquivos Brasileiros de Cardiologia (SciELO) - https://www.scielo.br/j/abc/a/xm7z5nQgmMjDjwhzMZNCLdt/?format=pdf&lang=pt
* **Justificativa de Engenharia de Dados:** Traz vocabulário focado em regulação da expressão fenotípica (ex: "miR-210", "miR-27a/b"), refinando os clusters subjacentes do modelo com entidades exatas de epigenética. A aproximação vetorial destes mediadores indica alta correlação mecanicista com a ruptura da placa de ateroma.
* **Snippet de Validação:** **Em Breve**
* **Nome do Arquivo:** `revisao_mirnas_fisiopatologia_cardiovascular.pdf`

<br>

* **Título Original:** Índices Hematológicos Inflamatórios, Doenças Cardiovasculares e Mortalidade: Uma Revisão Narrativa
* **Contexto:** Uso de exames de rastreio de baixo custo (hemograma) organizados em índices de razão para atestar inflamação sistêmica de baixo grau.
* **Ano de Publicação:** 2024
* **Fonte:** Arquivos Brasileiros de Cardiologia (SciELO) - https://www.scielo.br/j/abc/a/KyjkFNCJn68BRTphGtv9BfQ/?format=pdf&lang=pt
* **Justificativa de Engenharia de Dados:** Fornece conexões sintáticas explícitas entre razões de contagem celular de rotina (Relação Neutrófilo-Linfócito, Relação Plaquetas-Linfócitos) e a necrose miocárdica crônica, ensinando à IA como mapear variações laboratoriais primárias diretamente a instabilidades hemodinâmicas letais.
* **Snippet de Validação:** **Em Breve**
* **Nome do Arquivo:** `revisao_indices_hematologicos_inflamatorios_mortalidade.pdf`

</details>

<br>

<details open>
<summary><strong><font size="4">4º Arquétipo: Farmacologia e Bulas</font></strong></summary>
<br>

* **Título Original:** ACTILYSE® (alteplase) Pó liofilizado injetável - Bula Profissional
* **Contexto:** Regramento imperativo para a infusão do agente trombolítico de reperfusão imediata em cenários de isquemia de órgão-alvo.
* **Ano de Publicação:** 2013 / I13-00
* **Fonte:** Saúde Direta - https://www.saudedireta.com.br/catinc/drugs/bulas/actilyse.pdf
* **Justificativa de Engenharia de Dados:** Apresenta alta complexidade de restrições temporais e de teto de peso (10% em bolus, 90% em 60 min, dose máxima baseada no limite de 65 kg), exigindo do modelo a modelagem de grafos de dependência sequencial e limites condicionais numéricos absolutos.
* **Snippet de Validação:** **Em Breve**
* **Nome do Arquivo:** `bula_profissional_alteplase.pdf`

<br>

* **Título Original:** CUTENOX® (enoxaparina sódica) Solução Injetável - Bula do Profissional de Saúde
* **Contexto:** Tratamento de base para anticoagulação plena no paciente acamado em unidade de terapia intensiva coronariana.
* **Ano de Publicação:** 2021 (Versão Bula Padrão Viatris)
* **Fonte:** Viatris - https://www.viatris.com.br/-/media/project/common/viatriscombr/pdf/leaflets_legacy_myl_brazil/cutenox_bula_do_profissional_de_saude.pdf
* **Justificativa de Engenharia de Dados:** Fornece uma matriz posológica bidimensional baseada em peso corporal instantâneo e falência renal (clearance < 30 mL/min), forçando o modelo NLP a extrair regras de transição categórica que alteram dinamicamente a frequência posológica de 12h para 24h.
* **Snippet de Validação:** **Em Breve**
* **Nome do Arquivo:** `bula_profissional_enoxaparina.pdf`

<br>

* **Título Original:** Bissulfato de Clopidogrel 75 mg Comprimido Revestido - Bula para Profissional da Saúde
* **Contexto:** Base teórica da dupla antiagregação plaquetária obrigatória no paciente com síndrome coronariana aguda submetido a *stent*.
* **Ano de Publicação:** 2019 / VPS_01.2019
* **Fonte:** Accord Farmacêutica - https://accordfarma.com.br/bulas/clopidogrel_bula_profissional.pdf
* **Justificativa de Engenharia de Dados:** Introduz variáveis fenotípicas genéticas (metabolizadores lentos da enzima hepática CYP2C19) e densas interações de inibição mútua, instruindo a rede neural a construir lógicas de negação causal e modulação de eficácia terapêutica em grafos de farmacogenômica.
* **Snippet de Validação:** **Em Breve**
* **Nome do Arquivo:** `bula_profissional_clopidogrel.pdf`

<br>

* **Título Original:** EPIKABI® (hemitartarato de norepinefrina) Solução Injetável - Bula Profissional da Saúde
* **Contexto:** Droga vasoativa central para a reversão do choque vasoplégico e cardiogênico na UTI, baseada em monitoramento contínuo.
* **Ano de Publicação:** 2024 / ME-20002198V03
* **Fonte:** Fresenius Kabi - https://www.fresenius-kabi.com/content/dam/fresenius-kabi/br/documents/bulas/medicamentos/Epikabi%20(hemitartarato%20de%20norepinefrina)%20-%20Bula%20Profissional%20da%20Sa%C3%BAde.pdf.coredownload.inline.pdf
* **Justificativa de Engenharia de Dados:** Contém alta variabilidade de unidades dimensionais em estado de infusão contínua (mcg/min versus mcg/kg/min versus mL/min), impondo ao algoritmo inferencial a necessidade de correlacionar conversões ativas de taxa volumétrica estática com titulação retroalimentada hemodinâmica.
* **Snippet de Validação:** **Em Breve**
* **Nome do Arquivo:** `bula_profissional_noradrenalina.pdf`

<br>

* **Título Original:** ANCORON® (cloridrato de amiodarona) - Bula para o Profissional de Saúde
* **Contexto:** Diretrizes restritivas do antiarrítmico de amplo espectro utilizado em algoritmos de parada cardiorrespiratória (ACLS) e Fibrilação Atrial.
* **Ano de Publicação:** 2023
* **Fonte:** Sanofi / Consulta Remédios - https://uploads.consultaremedios.com.br/drug_leaflet/pro/Bula-Ancoron-Profissional-Consulta-Remedios.pdf
* **Justificativa de Engenharia de Dados:** Requer a extração rigorosa de sequenciamento temporal com fase de impregnação tissular prolongada contraposta à fase de manutenção, além de forte lógica de interações restritivas que induzem Torsade de Pointes, mapeando contraindicações elétricas absolutas.
* **Snippet de Validação:** **Em Breve**
* **Nome do Arquivo:** `bula_profissional_amiodarona.pdf`

</details>

<br>

<details open>
<summary><strong><font size="4">Pipeline de Processamento e Engenharia de Sinais Textuais</font></strong></summary>
<br>

<p align="justify">
A amalgamação destes quatro arquétipos fornece a heterogeneidade necessária para validar a arquitetura do CardioIA. A ingestão dos dados passará pelas seguintes etapas técnicas no laboratório ROG Strix:
</p>

<table>
  <tr>
    <th>Processo</th>
    <th>Objetivo Técnico</th>
    <th>Ambiente de Execução</th>
  </tr>
  <tr>
    <td>Limpeza de OCR</td>
    <td>Remoção de ruído de cabeçalhos e normalização UTF 8.</td>
    <td>Laptop ASUS Local</td>
  </tr>
  <tr>
    <td>Tokenização BPE</td>
    <td>Fragmentação de termos médicos complexos em subwords.</td>
    <td>Laptop ASUS Local</td>
  </tr>
  <tr>
    <td>Detecção de Negação</td>
    <td>Implementação do algoritmo NegEx para evitar falsos positivos.</td>
    <td>Laptop ASUS Local</td>
  </tr>
  <tr>
    <td>Fine Tuning NER</td>
    <td>Treinamento de pesos para entidades clínicas brasileiras.</td>
    <td>Google Colab GPU T4</td>
  </tr>
</table>

<br>

<p align="justify">
<strong>Considerações de Governança e LGPD:</strong><br>
Embora os dados brutos permaneçam na pasta <code>raw</code>, o treinamento utilizará técnicas de Named Entity Scrubbing para garantir que nenhuma entidade residual permita a reidentificação de pacientes em relatos de caso. Os dados processados e estruturados em formato JSON serão versionados via DVC, enquanto os arquivos PDFs pesados serão referenciados via links externos para manter o repositório ágil e focado em engenharia.
</p>

<p align="justify">
Em conclusão, o corpus selecionado oferece o rigor normativo dos protocolos, a profundidade das diretrizes e a variância narrativa dos relatos, cobrindo integralmente o espectro da linguagem cardiológica nacional para as próximas fases do CardioIA.
</p>

</details>

</details>