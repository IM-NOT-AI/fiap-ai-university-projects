<details open>
<summary><strong><font size="5">📕 1º PTB-XL: O Padrão-Ouro da Eletrocardiografia - Origem e Validação Clínica</font></strong></summary>
<br>

<p align="justify">
O dataset PTB-XL não é apenas um repositório de dados; é um artefato histórico, metrológico e o principal <em>benchmark</em> global aberto para a cardiologia computacional baseada em <em>Deep Learning</em>. A sua versão mais recente (1.0.3, Novembro de 2022) resolve de forma definitiva a crise de reprodutibilidade em algoritmos preditivos cardiovasculares.
</p>

<p align="justify">
<strong>De Onde São e Como Foram Conseguidos:</strong><br>
A origem dos dados remonta à Alemanha, especificamente à Physikalisch-Technische Bundesanstalt (PTB), o Instituto Nacional de Metrologia alemão. Em vez de utilizar um único centro de excelência (o que geraria viés geográfico), o PTB-XL agregou informações de dezenas de ambientes clínicos. A base atual consolida <strong>21.799 registros clínicos de ECG de 12 derivações</strong> (com 10 segundos de duração), provenientes de <strong>18.869 pacientes</strong>. A demografia é altamente equilibrada e representativa: 52% do sexo masculino e 48% do feminino, com idades variando de 0 a 95 anos (mediana de 62). A aquisição física foi realizada utilizando equipamentos da Schiller AG. Os sinais brutos, originalmente em formato proprietário, foram convertidos para o padrão aberto WFDB (<em>Waveform Database</em>), disponibilizados em duas resoluções: altíssima fidelidade a 500Hz e uma versão leve de 100Hz (com precisão de 16-bit e resolução de 1μV/LSB). 
<br><br>
<em>Governança e LGPD/HIPAA:</em> Todo o dataset foi severamente anonimizado. As datas de gravação originais sofreram um <em>offset</em> (deslocamento) aleatório por paciente e indivíduos com mais de 89 anos tiveram suas idades cravadas artificialmente em "300 anos" para inviabilizar a reidentificação, em estrita conformidade com protocolos éticos.
</p>

<p align="justify">
<strong>Quando Foram Coletados:</strong><br>
A janela temporal da coleta primária abrange um período de quase sete anos, entre <strong>outubro de 1989 e junho de 1996</strong>. Esta era "pré-compressão agressiva" permitiu a captura de dados digitais limpos que permaneceram arquivados e restritos. O projeto passou por longas curadorias até ser convertido para uso da comunidade de Machine Learning a partir de 2020, atingindo sua maturidade na versão 1.0.3 (2022), onde duplicatas residuais foram expurgadas para garantir métricas de validação imaculadas.
</p>

<p align="justify">
<strong>A "Origem da Verdade" (Ground Truth) e Engenharia de Rótulos:</strong><br>
A utilidade incontestável do PTB-XL para o aprendizado de máquina repousa no rigor de suas anotações. A extração dos laudos passou por dupla validação humana por cardiologistas especialistas. Foram mapeadas 71 declarações diferentes seguindo o rigoroso padrão <strong>SCP-ECG</strong> (<em>Standard Communication Protocol for Computer-assisted Electrocardiography</em>). Para facilitar o treinamento em múltiplos níveis de complexidade, as patologias foram estruturadas em 5 Superclasses Diagnósticas principais (alguns registros possuem múltiplos rótulos):
</p>

<ul>
  <li><strong>NORM (9.514 registros):</strong> ECG Normal (Controle saudável).</li>
  <li><strong>MI (5.469 registros):</strong> Infarto do Miocárdio.</li>
  <li><strong>STTC (5.235 registros):</strong> Alterações do Segmento ST e Onda T (Isquemia aguda).</li>
  <li><strong>CD (4.898 registros):</strong> Distúrbios de Condução (Bloqueios de ramo).</li>
  <li><strong>HYP (2.649 registros):</strong> Hipertrofia (Sobrecarga de câmaras).</li>
</ul>

<p align="justify">
Além do diagnóstico, o dataset embute uma riqueza absurda de <strong>Metadados de Sinal</strong>, cruciais para treinar <em>Gatekeepers</em>. Eles incluem anotações sobre ruído estático (<em>static_noise</em>), ruído de explosão (<em>burst_noise</em>), flutuações de linha de base (<em>baseline_drift</em>), batimentos extras sistólicos e a presença de marcapassos ativos.
</p>

<p align="justify">
<strong>Para Que Foram Criados e Estratégia de MLOps:</strong><br>
Originalmente concebido para estudar parâmetros de gravação digital, o PTB-XL é hoje a espinha dorsal para testes de visão computacional e sinais sequenciais na medicina. Para resolver o problema do viés de treinamento (onde pesquisadores validam modelos nos dados errados), o PTB-XL já fornece uma arquitetura de particionamento (<em>Data Splitting</em>) cravada cientificamente: <strong>10-fold cross-validation</strong> estratificado pelo paciente.
<br><br>
A recomendação mandatória (que será seguida no CardioIA) é:
<ul>
  <li><strong>Folds 1 a 8:</strong> Conjunto de Treinamento.</li>
  <li><strong>Fold 9:</strong> Conjunto de Validação.</li>
  <li><strong>Fold 10:</strong> Conjunto de Teste Cego (Composto exclusivamente por registros que passaram por altíssimo crivo de auditoria humana).</li>
</ul>
</p>

<p align="justify">
<strong>Referência e Citação Acadêmica:</strong><br>
Wagner, P., Strodthoff, N., Bousseljot, R., Samek, W., & Schaeffter, T. (2022). <em>PTB-XL, a large publicly available electrocardiography dataset (version 1.0.3)</em>. PhysioNet. <a href="https://doi.org/10.13026/kfzx-aw45">https://doi.org/10.13026/kfzx-aw45</a>
</p>

</details>