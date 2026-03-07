# Diretrizes Éticas e Governança de Dados: O Relatório Belmont

**_Documento de Referência para Conformidade Ética no Projeto CardioIA_**

Este documento resume os princípios fundamentais estabelecidos pelo **Relatório Belmont** (1979), criado pela *National Commission for the Protection of Human Subjects of Biomedical and Behavioral Research*. Ele serve como guia mandatório para todas as etapas de coleta, processamento e modelagem de dados neste projeto acadêmico.

---

## Introdução e Contexto

O Relatório Belmont foi criado para identificar princípios éticos básicos que devem nortear a pesquisa envolvendo seres humanos. Diferente de códigos anteriores que eram apenas regras, este relatório fornece uma base analítica para resolver problemas éticos complexos que surgem durante a pesquisa.

> **Nota de Governança:** No contexto do CardioIA, tratamos dados de pacientes (simulados ou reais anonimizados). A adesão a estes princípios garante que nossa IA não apenas funcione tecnicamente, mas respeite a dignidade humana.

---

## Fronteiras entre Prática e Pesquisa

Para fins de conformidade no desenvolvimento de nosso software médico, é crucial distinguir:

* **`Prática` (Terapia):** Refere-se a intervenções desenhadas unicamente para melhorar o bem-estar de um paciente individual, com expectativa razoável de sucesso. O objetivo é diagnóstico ou tratamento.
* **`Pesquisa` (Experimentação):** Designa uma atividade desenhada para testar uma hipótese, permitir conclusões e contribuir para o **conhecimento generalizável**. Normalmente descrita em um protocolo formal.

**Aplicação no Projeto:**
O desenvolvimento dos modelos de Machine Learning do CardioIA classifica-se como **`Pesquisa`**, pois visa gerar conhecimento generalizável sobre padrões cardíacos, e não tratar imediatamente o paciente cujos dados estão sendo usados para treino.

---

## Princípios Éticos Básicos

O relatório identifica três princípios gerais prescritivos relevantes para a pesquisa com seres humanos:

### Respeito às Pessoas (**_Respect for Persons_**)
Este princípio incorpora duas convicções éticas fundamentais:
1.  Os indivíduos devem ser tratados como **agentes autônomos**.
2.  Pessoas com autonomia diminuída têm direito à proteção.

* **Violação de Ética:** Repudiar os julgamentos considerados de uma pessoa, negar a liberdade de agir ou reter informações necessárias para uma decisão.

### Beneficência (**_Beneficence_**)
Neste contexto, beneficência é uma obrigação forte, não apenas caridade. Duas regras gerais formulam este princípio:
* **1.** Não causar danos (**_do no harm_**).
* **2.** Maximizar possíveis benefícios e minimizar possíveis danos.

> "Aprender o que irá de fato beneficiar pode exigir expor pessoas a riscos. O problema é decidir quando é justificável buscar certos benefícios apesar dos riscos envolvidos".

### Justiça (**_Justice_**)
Refere-se à imparcialidade na distribuição ("o que é merecido"). Uma injustiça ocorre quando um benefício a que uma pessoa tem direito é negado sem boa razão ou quando um fardo é imposto indevidamente.

**Critérios de Distribuição Justa:**
* A cada pessoa uma parte igual.
* A cada pessoa de acordo com a necessidade individual.
* A cada pessoa de acordo com o esforço individual.
* A cada pessoa de acordo com a contribuição social.
* A cada pessoa de acordo com o mérito.

---

## Aplicações Práticas no Ciclo de Vida dos Dados

A aplicação dos princípios gerais à conduta de pesquisa leva à consideração dos seguintes requisitos:

### Consentimento Informado (`Informed Consent`)
O respeito pelas pessoas exige que os sujeitos tenham a oportunidade de escolher o que acontecerá com eles. O processo contém três elementos:

1.  **Informação:** Deve-se revelar o procedimento, propósitos, riscos, benefícios antecipados e alternativas. Deve haver um padrão de "voluntário razoável" — a extensão e natureza da informação devem ser tais que as pessoas saibam que o procedimento não é necessário para seu cuidado.
2.  **Compreensão:** A maneira como a informação é apresentada é crucial. Apresentar de forma desorganizada ou rápida pode afetar adversamente a capacidade de escolha.
3.  **Voluntariedade:** O consentimento só é válido se dado livremente, sem coerção (ameaça de dano) ou influência indevida (oferta de recompensa excessiva ou inapropriada).

### Avaliação de Riscos e Benefícios (`Assessment of Risks and Benefits`)
Requer uma análise sistemática e não arbitrária.
* **Riscos:** Possibilidade de dano psicológico, físico, legal, social e econômico.
* **Justificativa:** Riscos aos sujeitos devem ser superados pela soma dos benefícios antecipados ao sujeito e à sociedade (conhecimento).
* **Redução:** Riscos devem ser reduzidos ao necessário para atingir o objetivo da pesquisa.

### Seleção de Sujeitos (`Selection of Subjects`)
Decorre do princípio da **Justiça**.
* **Justiça Individual:** Pesquisadores devem exibir imparcialidade; não devem oferecer pesquisa benéfica apenas a "favoritos" ou selecionar apenas pessoas "indesejáveis" para pesquisas arriscadas.
* **Justiça Social:** Distinção entre classes de sujeitos. Classes menos sobrecarregadas devem ser chamadas primeiro a aceitar riscos, exceto se a pesquisa for diretamente relacionada à condição da classe envolvida.
    * *Atenção:* Evitar o uso sistemático de minorias raciais, economicamente desfavorecidos ou institucionalizados apenas devido à sua disponibilidade fácil ou manipulabilidade.

---

## Integração com o CardioIA

Para o projeto **CardioIA**, aplicaremos o Relatório Belmont da seguinte forma:

1.  **Anonimização Rigorosa:** Em conformidade com o *Respeito às Pessoas*, todos os dados baixados (MIMIC-IV, PPG-DaLiA) devem ser verificados quanto à remoção de PII (Personal Identifiable Information).
2.  **Análise de Viés (Bias):** Em conformidade com a *Justiça*, analisaremos se nossos datasets de treino contêm representação equilibrada de gênero e raça, evitando que o modelo performe mal em grupos minoritários.
3.  **Segurança de Dados:** Em conformidade com a *Beneficência*, garantiremos que os dados estejam armazenados em ambientes seguros (`/data/processed`), minimizando o risco de vazamento (dano legal/social) aos titulares dos dados.

---
*Documento elaborado com base no texto oficial do The Belmont Report (April 18, 1979), Department of Health, Education, and Welfare.*