# Populações Vulneráveis e Proteções Adicionais

**_Protocolos de Inclusão Ética e Mitigação de Vulnerabilidade no CardioIA_**

Este documento técnico define a estratégia do CardioIA para o tratamento de dados provenientes de indivíduos ou grupos que requerem considerações adicionais. Embora o projeto utilize dados secundários (MIMIC-IV), a natureza clínica dos registros (pacientes em UTI, idosos, comorbidades graves) exige um reconhecimento formal da vulnerabilidade médica e situacional para garantir a conformidade com os princípios de Justiça e Respeito pelas Pessoas.

---

## Definição e Escopo de Vulnerabilidade

A vulnerabilidade em pesquisa não é um rótulo estático, mas uma condição dinâmica. Adotamos a definição da *National Bioethics Advisory Commission* (NBAC), que classifica como vulneráveis aqueles que têm dificuldade em fornecer consentimento voluntário e informado devido a:
1.  Limitações na capacidade de tomada de decisão;
2.  Circunstâncias situacionais; ou
3.  Risco aumentado de exploração.

### Justificativa de Inclusão
A exclusão sistemática de populações vulneráveis (como idosos ou pacientes críticos) resultaria em um viés algorítmico prejudicial, falhando em desenvolver tratamentos para aqueles que mais precisam. O CardioIA inclui esses grupos não por conveniência, mas por necessidade científica de representatividade clínica.

---

## Taxonomia de Riscos e Abusos

Historicamente, a pesquisa ética busca prevenir quatro tipos de abusos. No contexto de Data Science retrospectivo, focamos na prevenção da **Exploração** e **Manipulação**.

* **Controle Físico e Coerção:** Inaplicáveis para dados secundários anonimizados.
* **Influência Indevida:** Risco de oferecer incentivos inadequados (não aplicável em dados retrospectivos).
* **Manipulação:** O design deliberado de condições para levar a uma decisão que não seria tomada de outra forma.
* **Exploração:** Tratar sujeitos injustamente para beneficiar o estudo.
    * *Mitigação no CardioIA:* Garantimos que o uso dos dados visa o benefício geral da saúde cardiovascular, honrando a contribuição passiva dos pacientes, sem usá-los meramente como "meios" para um fim acadêmico.

---

## Fontes de Vulnerabilidade no Dataset CardioIA

Analisando o perfil dos dados do MIMIC-IV e potenciais dados complementares, identificamos as seguintes categorias de vulnerabilidade conforme o framework da NBAC:

### Vulnerabilidade Médica (`Medical Vulnerability`)
* **Definição:** Sujeitos com condições de saúde graves para as quais não existem tratamentos padrão satisfatórios.
* **Contexto do Projeto:** A grande maioria dos dados provém de UTIs. Esses pacientes podem ter superestimado benefícios ou não compreendido riscos durante a coleta original devido à gravidade de sua condição.

### Vulnerabilidade Cognitiva Situacional (`Situational Cognitive Vulnerability`)
* **Definição:** Sujeitos que não carecem de capacidade intrínseca, mas estão em situações (como emergência médica aguda) que impedem o exercício efetivo dessa capacidade.
* **Contexto do Projeto:** Dados de emergência cardíaca refletem momentos de extrema tensão onde o consentimento informado pleno é desafiador.

### Vulnerabilidade Social e Econômica
* **Definição:** Desvantagem na distribuição de bens sociais ou pertencimento a grupos socialmente desvalorizados.
* **Contexto do Projeto:** O CardioIA deve monitorar se os algoritmos não perpetuam preconceitos contra minorias raciais ou grupos economicamente desfavorecidos presentes na base de dados, prevenindo a "Vulnerabilidade Social" algorítmica.

---

## Proteções Regulatórias Específicas (Subpartes)

Embora trabalhemos com isenção de IRB para dados secundários, reconhecemos as proteções federais (45 CFR 46) aplicáveis aos dados originais:

* **Subparte B (Mulheres Grávidas/Fetos):** Se analisarmos dados obstétricos cardíacos, reconhecemos a necessidade de garantir que o risco seja mínimo e voltado para a saúde da mãe/feto.
* **Subparte C (Prisioneiros):** Dados de prisioneiros exigem que a pesquisa seja relevante para a condição de encarceramento ou saúde da população prisional.
* **Subparte D (Crianças):** A pesquisa pediátrica é justificada apenas se não puder ser realizada com adultos ou se oferecer benefício direto à criança.

---

## Estratégia de Justiça e Equidade

A vulnerabilidade impacta diretamente o princípio da **Justiça**.

### Seleção Equitativa
Evitamos a seleção de "conveniência". Não usamos dados de populações vulneráveis apenas porque são "fáceis de acessar" (como em casos históricos de abuso), mas porque a patologia cardíaca exige sua inclusão.

### Análise de Viés (Bias)
Reconhecemos que hierarquias sociais e desigualdades de saúde estão "embutidas" nos dados médicos.
* **Ação:** O CardioIA implementará métricas de avaliação de modelo segmentadas por subgrupos demográficos para garantir que a performance preditiva não seja degradada em populações vulneráveis (evitando a exploração digital).

---

## Conclusão

A classificação de "vulnerável" não é um impedimento para a pesquisa, mas um chamado para uma responsabilidade ética elevada. No CardioIA, a utilização de dados de pacientes críticos e grupos marginalizados é conduzida sob estrita governança de dados, assegurando que a tecnologia desenvolvida sirva para reduzir, e não exacerbar, as disparidades de saúde que tornam essas populações vulneráveis em primeiro lugar.

---
*Documentação técnica baseada no módulo "Populations in Research Requiring Additional Considerations and/or Protections" do CITI Program (Jeremy N. Block, PhD, MPP & Bruce Gordon, MD).*