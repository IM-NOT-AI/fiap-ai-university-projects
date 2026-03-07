<details open>
<summary><strong><font size="5">📘 5º PPG-DaLiA: O Desafio do Mundo Real - Fotopletismografia e Artefatos de Movimento</font></strong></summary>
<br>

<p align="justify">
Enquanto bancos de dados clínicos (como o PTB-XL) fornecem a base para o diagnóstico em ambiente hospitalar controlado, o ecossistema de <em>Edge Computing</em> e dispositivos <em>Wearables</em> exige um treinamento focado em variabilidade ambulatorial. O <strong>PPG-DaLiA</strong> (<em>Photoplethysmography Dataset for motion compensation and heart rate estimation in Daily Life Activities</em>) é o artefato de dados projetado estritamente para resolver o maior problema da engenharia de sinais biomédicos portáteis: a extração de frequência cardíaca fidedigna sob extrema contaminação por artefatos de movimento.
</p>

<p align="justify">
<strong>De Onde São e Como Foram Conseguidos (Topologia de Hardware Duplo):</strong><br>
Doado ao <em>UCI Machine Learning Repository</em> em 2019, o dataset apresenta um volume massivo de <strong>8.3 milhões de instâncias multivariadas e temporais</strong>. A coleta foi realizada com 15 sujeitos saudáveis submetidos a um protocolo de "Atividades de Vida Diária" (<em>Daily Life Activities</em> - DaLiA), como sentar, ler, caminhar, subir escadas, jogar pebolim, pedalar e dirigir. 
<br><br>
A excelência deste dataset reside na sua <strong>Arquitetura de Aquisição Multimodal Síncrona</strong>. Para capturar as limitações do hardware comercial e a fisiologia real, cada paciente foi equipado com dois dispositivos simultâneos, gerando tensores paralelos:
</p>

<ul>
  <li><strong>Dispositivo de Pulso (Empatica E4):</strong> Simula o relógio inteligente do paciente. Ele extrai os sinais vitais brutos através do Volume de Pulso Sanguíneo via Fotopletismografia (<strong>BVP/PPG amostrado a 64 Hz</strong>), Atividade Eletrodérmica para medir sudorese/estresse (EDA a 4 Hz), Temperatura Corporal (4 Hz) e, crucialmente, a Aceleração Espacial em 3 eixos (Acelerômetro 3D a 32 Hz) para registrar o balanço do braço.</li>
  <li><strong>Dispositivo de Tórax (RespiBAN):</strong> Atua como a âncora de segurança clínica. Ele registra o Eletrocardiograma padrão-ouro (<strong>ECG amostrado em altíssima resolução a 700 Hz</strong>), a taxa de respiração (700 Hz) e a aceleração do tronco (700 Hz).</li>
</ul>

<p align="justify">
<strong>A "Origem da Verdade" (Ground Truth) e Sincronização de Sinais:</strong><br>
A fotopletismografia (PPG) baseia-se na emissão de luz na pele para medir a variação do fluxo sanguíneo nos capilares. O problema arquitetural é que o movimento do braço (balançar, digitar) altera a refração da luz, destruindo o sinal cardíaco. <br>
A genialidade do PPG-DaLiA para <em>Machine Learning</em> é que <strong>o ECG do tórax fornece a Verdade Absoluta (Ground Truth) irrefutável para a Frequência Cardíaca</strong>. O modelo de Inteligência Artificial é forçado a olhar para a onda ruidosa do pulso (PPG) junto com os tremores do braço (Acelerômetro 3D) e aprender matematicamente a "subtrair" o ruído espacial para tentar adivinhar a Frequência Cardíaca verdadeira que está sendo registrada secretamente pelo ECG no peito do paciente. É um problema clássico e denso de regressão e fusão de sensores.
</p>

<p align="justify">
<strong>Quando Foram Coletados e Governança:</strong><br>
Publicado e doado em 29 de julho de 2019 sob a licença de acesso aberto <em>Creative Commons Attribution 4.0 International (CC BY 4.0)</em>. Ao contrário de bases de dados restritas que necessitam de acordos de uso de dados (DUA) complexos, o PPG-DaLiA foi explicitamente curado para democratizar a pesquisa em <em>Computer Science</em> e Processamento de Sinais, não contendo dados de prontuários ou valores faltantes (<em>Missing Values: No</em>), o que facilita a ingestão em pipelines de dados automatizados de 2.7 GB (em sua forma zipada original).
</p>

<p align="justify">
<strong>Para Que Foram Criados e Estratégia de MLOps:</strong><br>
A inserção deste dataset no projeto <strong>CardioIA</strong> visa calibrar o Nó de Aquisição (Wearable) antes que o sinal chegue ao Raspberry Pi. Suas principais aplicações de treinamento incluem:
</p>

<ul>
  <li><strong>Compensação de Artefato de Movimento (Motion Artefact - MA):</strong> Uso de Filtros Adaptativos ou Redes Neurais Convolucionais 1D (CNN-1D) para isolar as frequências causadas pela inércia física (medidas pelo acelerômetro) e removê-las do espectro do sinal óptico (PPG).</li>
  <li><strong>Estimação Regressiva Contínua:</strong> Ao contrário da classificação estática (Infarto vs. Normal), aqui a IA executa uma tarefa de <em>Regressão Contínua</em> temporal, predizendo a variável alvo real e dinâmica (Batimentos Por Minuto - BPM) a cada fração de segundo.</li>
  <li><strong>Delineamento de Fusão Sensorial (Sensor Fusion):</strong> Ensina o algoritmo a não confiar cegamente no sensor óptico se o sensor de Atividade Eletrodérmica (EDA) e o Acelerômetro indicarem que o paciente está em intenso movimento físico, atuando como um <em>Gatekeeper</em> dinâmico de confiança da informação na borda (Edge).</li>
</ul>

<p align="justify">
<strong>Referência e Citação Acadêmica Oficial:</strong><br>
Reiss, A., Indlekofer, I., & Schmidt, P. (2019). <em>PPG-DaLiA [Dataset]</em>. UCI Machine Learning Repository. <a href="https://doi.org/10.24432/C53890">https://doi.org/10.24432/C53890</a>
</p>

</details>