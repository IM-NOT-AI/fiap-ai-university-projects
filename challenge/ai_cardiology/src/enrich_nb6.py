# -*- coding: utf-8 -*-
"""
enrich_nb6.py  –  Enriquecimento abrangente do NB6 (symptom_extraction.ipynb)
Adds heatmap displays, expands interpretation cells, and prepends DS lifecycle callouts.
"""
import json
import os

NB_PATH = r"C:\Users\isaac\Desktop\FIAP-AI-university-projects\last_year\challenge\ai_cardiology\notebooks\symptom_extraction.ipynb"
# Nota: este script reside em src/ e opera sobre o notebook em notebooks/
# Execute a partir da raiz do projeto ou ajuste NB_PATH conforme necessario.

with open(NB_PATH, encoding="utf-8") as f:
    nb = json.load(f)

cells = nb["cells"]
print(f"Loaded notebook with {len(cells)} cells.")

# ─── helpers ────────────────────────────────────────────────────────────────

def find_cell(unique_str, cell_type=None):
    """Return (index, cell) for the first cell whose joined source contains unique_str."""
    for i, c in enumerate(cells):
        if cell_type and c["cell_type"] != cell_type:
            continue
        src = "".join(c["source"])
        if unique_str in src:
            return i, c
    return None, None

def append_code(cell, code_str):
    """Append code_str to a code cell's source and clear outputs."""
    src = "".join(cell["source"])
    cell["source"] = src + code_str
    cell["outputs"] = []
    cell["execution_count"] = None

def replace_md(cell, new_source):
    """Replace entire markdown cell source."""
    cell["source"] = new_source

def prepend_md(cell, prefix_str):
    """Prepend prefix_str to a markdown cell source."""
    src = "".join(cell["source"])
    cell["source"] = prefix_str + src

# ════════════════════════════════════════════════════════════════════════════
# SECTION A – ADD STYLED DATAFRAME DISPLAYS
# ════════════════════════════════════════════════════════════════════════════

# A1 – df_disease[['arquivo', 'tipo', 'superclasse', 'risco', 'diagnostico']]
A1_CODE = """

# --- Heatmap: DISEASE_MAP estilizado por superclasse e risco ---
print('\\nTabela com heatmap de superclasse e risco:')
_SC_BG  = {'MI':'background-color:#ffd6d6;color:#7b0000','STTC':'background-color:#fff0d6;color:#7b4000',
            'CD':'background-color:#d6e8ff;color:#003c7b','HYP':'background-color:#ead6ff;color:#4b007b',
            'NORM':'background-color:#d6ffe8;color:#006b1e','INCONCLUSIVO':'background-color:#ebebeb;color:#555'}
_RISCO_BG = {'alto':'background-color:#ffecec;color:#900000','baixo':'background-color:#ecffec;color:#006400'}
display(
    df_disease[['arquivo','tipo','superclasse','risco','diagnostico']]
    .style
    .map(lambda v: _SC_BG.get(str(v), ''), subset=['superclasse'])
    .map(lambda v: _RISCO_BG.get(str(v), ''), subset=['risco'])
    .set_caption('Heatmap \u2014 DISEASE_MAP: 26 documentos com superclasse PTB-XL e nivel de risco')
    .set_properties(**{'font-size': '11px', 'border': '1px solid #ddd'})
)
"""

i, c = find_cell("df_disease[['arquivo', 'tipo', 'superclasse', 'risco', 'diagnostico']]", "code")
if c is not None:
    append_code(c, A1_CODE)
    print(f"A1 applied to cell {i}")
else:
    print("WARNING: A1 cell not found!")

# A2 – df_lookup[['arquivo', 'tipo', 'superclasse', 'n_stems', 'stems']]
A2_CODE = """

# --- Heatmap: Lexico de gatilho por superclasse e n_stems ---
print('\\nTabela com heatmap do lexico de gatilho:')
display(
    df_lookup[['arquivo','tipo','superclasse','n_stems','stems']]
    .style
    .background_gradient(subset=['n_stems'], cmap='Blues', vmin=0, vmax=12)
    .map(lambda v: _SC_BG.get(str(v), ''), subset=['superclasse'])
    .set_caption('Heatmap \u2014 edge_trigger_lookup.json: stems TF-IDF discriminativos por documento')
    .set_properties(**{'font-size': '11px'})
    .format({'n_stems': '{:d}'})
)
"""

i, c = find_cell("df_lookup[['arquivo', 'tipo', 'superclasse', 'n_stems', 'stems']]", "code")
if c is not None:
    append_code(c, A2_CODE)
    print(f"A2 applied to cell {i}")
else:
    print("WARNING: A2 cell not found!")

# A3 – df_stats groupby
A3_CODE = """

# --- Heatmap: Estatisticas por tipo de documento ---
print('\\nTabela com heatmap de estatisticas do corpus:')
_stats_grouped = df_stats[['tipo','n_palavras','n_sentencas','n_chars']].groupby('tipo').agg(
    docs=('n_palavras','count'),
    palavras_media=('n_palavras','mean'),
    palavras_max=('n_palavras','max'),
    palavras_min=('n_palavras','min'),
    sentencas_media=('n_sentencas','mean'),
).round(0).astype(int).reset_index()
display(
    _stats_grouped.style
    .background_gradient(subset=['palavras_media','palavras_max','sentencas_media'], cmap='YlOrRd')
    .background_gradient(subset=['docs'], cmap='Blues')
    .set_caption('Heatmap \u2014 Estatisticas do corpus por tipo de documento (maior = mais escuro)')
    .set_properties(**{'font-size': '11px'})
    .bar(subset=['palavras_min'], color='#d4edda', vmin=0)
)
"""

i, c = find_cell("df_stats[['tipo', 'n_palavras', 'n_sentencas', 'n_chars']].groupby", "code")
if c is not None:
    append_code(c, A3_CODE)
    print(f"A3 applied to cell {i}")
else:
    print("WARNING: A3 cell not found!")

# A4 – pd.crosstab(df_disease['tipo'], df_disease['superclasse'])
A4_CODE = """

# --- Heatmap: Crosstab tipo x superclasse ---
print('\\nCrosstab com heatmap tipo x superclasse:')
_ct_styled = pd.crosstab(df_disease['tipo'], df_disease['superclasse'])
display(
    _ct_styled.style
    .background_gradient(cmap='Blues', axis=None)
    .set_caption('Heatmap \u2014 Tipo de Documento x Superclasse PTB-XL (frequencia de documentos)')
    .set_properties(**{'font-size': '11px', 'text-align': 'center'})
    .highlight_max(axis=None, color='#d62728', props='color: white; font-weight: bold')
)
"""

i, c = find_cell("pd.crosstab(df_disease['tipo'], df_disease['superclasse'])", "code")
if c is not None:
    append_code(c, A4_CODE)
    print(f"A4 applied to cell {i}")
else:
    print("WARNING: A4 cell not found!")

# A5 – df_demo = pd.DataFrame(demo_rows)
A5_CODE = """

# --- Heatmap: Demo RSLP estilizado ---
print('\\nDemo RSLP com heatmap:')
display(
    df_demo.style
    .set_caption('Heatmap \u2014 Demonstracao do pipeline RSLP: tokens -> stems -> sintomas detectados')
    .map(lambda v: 'background-color:#e8f5e9' if ',' in str(v) and len(str(v)) > 3 else '', subset=['sintomas_detectados'])
    .set_properties(**{'font-size': '11px', 'white-space': 'pre-wrap'})
    .highlight_null(color='#fff3cd')
)
"""

i, c = find_cell("df_demo = pd.DataFrame(demo_rows)", "code")
if c is not None:
    append_code(c, A5_CODE)
    print(f"A5 applied to cell {i}")
else:
    print("WARNING: A5 cell not found!")

# A6 – df_all[['arquivo', 'tipo', 'superclasse_ptbxl', 'risco', 'trigger_score', 'n_sintomas', 'sintomas_str', 'frase_sintomatica']].head(15)
A6_CODE = """

# --- Heatmap: df_all amostra com trigger_score e n_sintomas ---
print('\\nAmostra estilizada do pipeline completo:')
display(
    df_all[['arquivo','tipo','superclasse_ptbxl','risco','trigger_score','n_sintomas','sintomas_str']].head(20)
    .style
    .background_gradient(subset=['trigger_score'], cmap='RdYlGn', vmin=0, vmax=4)
    .background_gradient(subset=['n_sintomas'], cmap='Blues', vmin=0, vmax=5)
    .map(lambda v: _SC_BG.get(str(v), ''), subset=['superclasse_ptbxl'])
    .map(lambda v: _RISCO_BG.get(str(v), ''), subset=['risco'])
    .set_caption('Heatmap \u2014 Frases sintomaticas extraidas: trigger_score (vermelho=baixo, verde=alto) e n_sintomas (azul=mais sintomas)')
    .set_properties(**{'font-size': '10px'})
    .format({'trigger_score': '{:d}', 'n_sintomas': '{:d}'})
)
"""

i, c = find_cell("Amostra do DataFrame de frases sintom", "code")
if c is not None:
    append_code(c, A6_CODE)
    print(f"A6 applied to cell {i}")
else:
    print("WARNING: A6 cell not found!")

# A7 – resumo = ( ... resumo.sort_values
A7_CODE = """

# --- Heatmap: Resumo por documento com gradiente ---
print('\\nResumo estilizado com gradiente:')
display(
    resumo[['arquivo','tipo','superclasse_ptbxl','risco','n_frases','score_medio','score_max','n_sintomas_medio']]
    .style
    .background_gradient(subset=['score_medio','score_max'], cmap='RdYlGn', vmin=0, vmax=4)
    .background_gradient(subset=['n_frases'], cmap='Blues', vmin=0, vmax=resumo['n_frases'].max())
    .background_gradient(subset=['n_sintomas_medio'], cmap='Purples', vmin=0, vmax=5)
    .map(lambda v: _SC_BG.get(str(v), ''), subset=['superclasse_ptbxl'])
    .map(lambda v: _RISCO_BG.get(str(v), ''), subset=['risco'])
    .set_caption('Heatmap \u2014 Resumo do pipeline por documento (score_medio: verde=alto discriminativo)')
    .set_properties(**{'font-size': '10px'})
    .format({'score_medio': '{:.2f}', 'score_max': '{:d}', 'n_sintomas_medio': '{:.2f}', 'n_frases': '{:d}'})
    .highlight_max(subset=['score_medio'], color='#28a745', props='color:white;font-weight:bold')
    .highlight_min(subset=['score_medio'], color='#dc3545', props='color:white;font-weight:bold')
)
"""

i, c = find_cell("resumo = (", "code")
if c is not None:
    append_code(c, A7_CODE)
    print(f"A7 applied to cell {i}")
else:
    print("WARNING: A7 cell not found!")

# A8 – df_top = (
A8_CODE = """

# --- Heatmap: Top 15 frases por trigger_score ---
print('\\nTop 15 frases estilizadas:')
display(
    df_top.style
    .background_gradient(subset=['trigger_score'], cmap='RdYlGn', vmin=0, vmax=df_top['trigger_score'].max())
    .background_gradient(subset=['n_sintomas'], cmap='Blues', vmin=0, vmax=5)
    .map(lambda v: _SC_BG.get(str(v), ''), subset=['superclasse_ptbxl'])
    .map(lambda v: _RISCO_BG.get(str(v), ''), subset=['risco'])
    .set_caption('Heatmap \u2014 Top 15 frases por trigger_score: melhor cobertura lexical clinica')
    .set_properties(**{'font-size': '10px'})
    .format({'trigger_score': '{:d}', 'n_sintomas': '{:d}'})
)
"""

i, c = find_cell("df_top = (", "code")
if c is not None:
    append_code(c, A8_CODE)
    print(f"A8 applied to cell {i}")
else:
    print("WARNING: A8 cell not found!")

# A9 – df_mapa_out.head(5)  (the save CSV cell)
A9_CODE = """

# --- Heatmap: amostra do mapa_sintomas_doencas.csv ---
print('\\nAmostra estilizada do CSV gerado:')
display(
    df_mapa_out.head(15).style
    .map(lambda v: _SC_BG.get(str(v), ''), subset=['Superclasse_PTB-XL'])
    .map(lambda v: _RISCO_BG.get(str(v), ''), subset=['Nivel_Risco'])
    .background_gradient(subset=['Trigger_Score'], cmap='RdYlGn', vmin=0, vmax=df_mapa_out['Trigger_Score'].max())
    .highlight_null(color='#fff3cd')
    .set_caption('Heatmap \u2014 mapa_sintomas_doencas.csv: entregavel FIAP com sintomas, doenca e superclasse PTB-XL')
    .set_properties(**{'font-size': '11px'})
    .format({'Trigger_Score': '{:d}'})
)
"""

i, c = find_cell("df_mapa_out.head(5)", "code")
if c is not None:
    append_code(c, A9_CODE)
    print(f"A9 applied to cell {i}")
else:
    print("WARNING: A9 cell not found!")

# A10 – df_selected = df_quality.loc[selected_indices]
A10_CODE = """

# --- Heatmap: frases selecionadas para sintomas_pacientes.txt ---
print('\\nFrames selecionadas estilizadas (heatmap):')
display(
    df_selected[['n_frase','superclasse_ptbxl','risco','trigger_score','n_sintomas','n_words','alpha_ratio','diagnostico']]
    .style
    .background_gradient(subset=['trigger_score'], cmap='RdYlGn', vmin=0, vmax=5)
    .background_gradient(subset=['n_sintomas'], cmap='Blues', vmin=0, vmax=5)
    .background_gradient(subset=['alpha_ratio'], cmap='Greens', vmin=0.6, vmax=1.0)
    .background_gradient(subset=['n_words'], cmap='Purples', vmin=5, vmax=80)
    .map(lambda v: _SC_BG.get(str(v), ''), subset=['superclasse_ptbxl'])
    .map(lambda v: _RISCO_BG.get(str(v), ''), subset=['risco'])
    .set_caption('Heatmap \u2014 10 frases selecionadas: trigger_score (qualidade clinica), alpha_ratio (pureza textual), n_words (comprimento)')
    .set_properties(**{'font-size': '11px'})
    .format({'trigger_score': '{:d}', 'n_sintomas': '{:d}', 'alpha_ratio': '{:.2f}', 'n_words': '{:d}'})
    .highlight_max(subset=['trigger_score'], color='#28a745', props='color:white;font-weight:bold')
)
"""

i, c = find_cell("df_selected = df_quality.loc[selected_indices]", "code")
if c is not None:
    append_code(c, A10_CODE)
    print(f"A10 applied to cell {i}")
else:
    print("WARNING: A10 cell not found!")

# A11 – df_val = pd.DataFrame(val_results) and display(df_val)
A11_CODE = """

# --- Heatmap: DataFrame de validacao ---
print('\\nValidacao estilizada com heatmap:')
display(
    df_val.style
    .map(lambda v: 'background-color:#d4edda;color:#155724;font-weight:bold' if str(v)=='\u2713' else 'background-color:#f8d7da;color:#721c24;font-weight:bold', subset=['cobertura_ok'])
    .map(lambda v: _SC_BG.get(str(v), ''), subset=['superclasse_esperada'])
    .background_gradient(subset=['trigger_score'], cmap='Blues', vmin=0, vmax=df_val['trigger_score'].max())
    .background_gradient(subset=['n_sintomas'], cmap='Greens', vmin=0, vmax=5)
    .set_caption('Heatmap \u2014 Validacao do pipeline: cobertura (verde=OK), trigger_score (azul=maior cobertura lexical)')
    .set_properties(**{'font-size': '11px'})
    .format({'trigger_score': '{:d}', 'n_sintomas': '{:d}'})
)
"""

i, c = find_cell("df_val = pd.DataFrame(val_results)", "code")
if c is not None:
    append_code(c, A11_CODE)
    print(f"A11 applied to cell {i}")
else:
    print("WARNING: A11 cell not found!")

# ════════════════════════════════════════════════════════════════════════════
# SECTION B – REPLACE INTERPRETATION MARKDOWN CELLS
# ════════════════════════════════════════════════════════════════════════════

# B1
B1_NEW = """---
**INTERPRETA\u00c7\u00c3O \u2014 Composi\u00e7\u00e3o do Corpus (Gr\u00e1fico 1)**

O corpus Fase 1 apresenta **26 documentos PT-BR** distribu\u00eddos em 5 categorias com perfis lingu\u00edsticos distintos:

| Categoria | Docs | Perfil Lingu\u00edstico |
|---|---|---|
| Revis\u00e3o Cient\u00edfica | 8 (~31%) | Epidemiol\u00f3gica, fisiopatol\u00f3gica, biomarcadores |
| Relato de Caso | 8 (~31%) | Narrativa cl\u00ednica, sintomas diretos, linguagem descritiva |
| Bula ANVISA | 5 (~19%) | Prescritiva, t\u00e9cnica, rea\u00e7\u00f5es adversas e indica\u00e7\u00f5es |
| Diretriz SBC | 3 (~12%) | Normativa, orientada a decis\u00e3o terap\u00eautica |
| Protocolo SUS | 2 (~8%) | Direta, emergencial, algoritmos de manejo |

**An\u00e1lise quantitativa:** A paridade num\u00e9rica entre Revis\u00f5es Cient\u00edficas e Relatos de Caso (8 vs 8 documentos) \u00e9 enganosa em termos de volume textual \u2014 revis\u00f5es acad\u00eamicas s\u00e3o tipicamente 5 a 10x mais longas que relatos individuais. Isso significa que, em palavras brutas, o corpus \u00e9 dominado por linguagem cient\u00edfica, n\u00e3o cl\u00ednica narrativa.

**Implica\u00e7\u00e3o para Ci\u00eancia de Dados \u2014 Vi\u00e9s de Corpus:**
> **[RISCO DE VI\u00c9S]** A predomin\u00e2ncia de texto cient\u00edfico sobre texto cl\u00ednico-narrativo pode distorcer o l\u00e9xico TF-IDF gerado no NB5. O `SYMPTOM_KEYWORDS` foi calibrado manualmente justamente como mecanismo de contrabalanceamento: garante que a extra\u00e7\u00e3o priorize linguagem sintom\u00e1tica independentemente do perfil do documento de origem.

**Implica\u00e7\u00e3o para o Pipeline:**
- Documentos normativos (Diretrizes SBC) produzem mais frases brutas por volume, mas com menor especificidade cl\u00ednica por frase
- Relatos de Caso s\u00e3o compactos mas geram frases de alto valor cl\u00ednico
- O `trigger_score` (Se\u00e7\u00e3o 8) \u00e9 o mecanismo que corrige essa assimetria, ranqueando frases pela afinidade lexical com o l\u00e9xico TF-IDF discriminativo do documento de origem

**Para o NB7:** Esta composi\u00e7\u00e3o informa a estrat\u00e9gia de amostragem \u2014 o mapa_sintomas_doencas.csv ter\u00e1 desbalanceamento de classe proporcional ao corpus, exigindo `class_weight='balanced'` no classificador de risco."""

i, c = find_cell("**INTERPRETA\u00c7\u00c3O:** O corpus \u00e9 dominado por Revis\u00f5es Cient\u00edficas", "markdown")
if c is not None:
    replace_md(c, B1_NEW)
    print(f"B1 applied to cell {i}")
else:
    print("WARNING: B1 cell not found!")

# B2
B2_NEW = """---
**INTERPRETA\u00c7\u00c3O \u2014 Contribui\u00e7\u00e3o Lexical por Categoria (Gr\u00e1fico 2)**

O gr\u00e1fico mostra o n\u00famero de stems TF-IDF \u00fanicos contribu\u00eddos por cada categoria ao `edge_trigger_lookup.json`. Este n\u00famero representa a riqueza do vocabul\u00e1rio discriminativo de cada grupo de documentos.

**An\u00e1lise por categoria:**
- **Revis\u00f5es Cient\u00edficas**: Maior contribui\u00e7\u00e3o absoluta por n\u00famero de documentos (8 revis\u00f5es \u00d7 10 stems cada = at\u00e9 80 stems, com sobreposi\u00e7\u00e3o reduzida pela especificidade de cada artigo). Vocabul\u00e1rio diversificado cobrindo ceramidas, miRNAs, GDF-15, \u00edndices hematol\u00f3gicos.
- **Relatos de Caso**: Alta densidade por documento \u2014 cada relato introduz vocabulary muito espec\u00edfico (nomes de doen\u00e7as raras, interven\u00e7\u00f5es cir\u00fargicas, agentes infecciosos). Os stems de "chagas", "chikunguny", "fluorouracil" e "pseudoaneurism" v\u00eam exclusivamente dessa categoria.
- **Diretrizes SBC**: Vocabul\u00e1rio t\u00e9cnico-cl\u00ednico focado (ACODs, RCP, anticoagula\u00e7\u00e3o). Alta especificidade mas menor diversidade que revis\u00f5es.
- **Bulas ANVISA**: Vocabul\u00e1rio farmacol\u00f3gico denso \u2014 nomes de princ\u00edpios ativos (alteplase, clopidogrel, enoxaparina) dominam os stems, com baixa sobreposi\u00e7\u00e3o entre categorias.
- **Protocolos SUS**: Menor contribui\u00e7\u00e3o por ter apenas 2 documentos, mas com vocabulary operacional relevante (ICP, IAMCSST, tromb\u00f3lise).

**Feature Engineering \u2014 Especificidade dos Stems:**
> **[FEATURE ENGINEERING]** A diversidade lexical entre categorias valida o TF-IDF como mecanismo de feature extraction. Stems de alta especificidade por categoria (ex: "fluorouracil" \u2192 STTC, "chagas" \u2192 CD, "enoxaparin" \u2192 MI) atuar\u00e3o como features altamente discriminativas no modelo NB7, funcionando como \u00e2ncoras de classe. Stems compartilhados entre categorias (ex: "insuficienc", "cardiac") ser\u00e3o penalizados pelo IDF, perdendo import\u00e2ncia relativa.

**Implica\u00e7\u00e3o para o Pipeline:**
A baixa sobreposi\u00e7\u00e3o entre stems de categorias distintas confirma que o `edge_trigger_lookup.json` captura "assinaturas textuais" \u00fanicas por documento. O `trigger_score` calculado em cada frase \u00e9, portanto, uma medida genu\u00edna de afinidade cl\u00ednica \u2014 n\u00e3o ru\u00eddo aleat\u00f3rio."""

i, c = find_cell("**INTERPRETA\u00c7\u00c3O:** Revis\u00f5es Cient\u00edficas dominam a contribui\u00e7\u00e3o lexical", "markdown")
if c is not None:
    replace_md(c, B2_NEW)
    print(f"B2 applied to cell {i}")
else:
    print("WARNING: B2 cell not found!")

# B3
B3_NEW = """---
**INTERPRETA\u00c7\u00c3O \u2014 Estat\u00edsticas M\u00e9tricas do Corpus (Gr\u00e1fico 3)**

**Boxplot (palavras por tipo):**
- **Revis\u00f5es Cient\u00edficas** apresentam a maior mediana de palavras e a maior vari\u00e2ncia \u2014 confirma que coletamos artigos de tamanhos muito distintos: revis\u00f5es curtas (~800 palavras, ex: GDF-15) e revis\u00f5es extensas (~4000+ palavras, ex: fibrilação atrial). Esta heterogeneidade \u00e9 esperada em literatura acad\u00eamica.
- **Relatos de Caso** s\u00e3o o grupo mais homog\u00eaneo: artigos cl\u00ednicos t\u00eam estrutura padronizada (hist\u00f3rico, exame, diagn\u00f3stico, discuss\u00e3o) resultando em tamanhos similares (tipicamente 600-1500 palavras ap\u00f3s pruning).
- **Bulas ANVISA** s\u00e3o extensas por natureza regulat\u00f3ria (posologia, advert\u00eancias, farmacocin\u00e9tica), mas padronizadas em estrutura.
- **Diretrizes SBC** e **Protocolos SUS** variam por escopo cl\u00ednico \u2014 a diretriz de RCP \u00e9 mais extensa que a de fibrilação atrial.

**Scatter (palavras vs. senten\u00e7as):**
A correla\u00e7\u00e3o positiva forte entre palavras e senten\u00e7as confirma que o comprimento m\u00e9dio de senten\u00e7a \u00e9 consistente across o corpus (estimativa: ~15-20 palavras/senten\u00e7a). Isso \u00e9 esperado em linguagem m\u00e9dica formal PT-BR. N\u00e3o h\u00e1 outliers com senten\u00e7as anormalmente longas ou curtas, validando que o NB4 (pruning) limpou adequadamente par\u00e1grafos cont\u00ednuos sem pontua\u00e7\u00e3o.

**Limpeza de Dados \u2014 Calibra\u00e7\u00e3o de Filtros:**
> **[LIMPEZA DE DADOS]** O filtro `min_palavras=8` na extra\u00e7\u00e3o de frases (Se\u00e7\u00e3o 8) foi definido baseado nesta an\u00e1lise: comprimentos m\u00e9dios de ~15-20 palavras/senten\u00e7a implicam que frases com <8 palavras s\u00e3o provavelmente fragmentos (refer\u00eancias bibliogr\u00e1ficas, cabe\u00e7alhos, t\u00edtulos de se\u00e7\u00e3o) e n\u00e3o senten\u00e7as cl\u00ednicas completas. O filtro de 70 palavras no limite superior (Se\u00e7\u00e3o 10.2) exclui par\u00e1grafos longos que passaram pelo segmentador como "senten\u00e7as \u00fanicas".

**Implica\u00e7\u00e3o para o Pipeline:**
O total de palavras no corpus (~50.000-100.000 palavras estimadas) \u00e9 adequado para TF-IDF com dimensionalidade 6.276 (gerada no NB5). A rela\u00e7\u00e3o dimensionalidade/corpus \u00e9 saud\u00e1vel, evitando underfitting por esparsidade extrema."""

i, c = find_cell("**INTERPRETA\u00c7\u00c3O:** O boxplot mostra alta vari\u00e2ncia nas Revis\u00f5es Cient\u00edficas", "markdown")
if c is not None:
    replace_md(c, B3_NEW)
    print(f"B3 applied to cell {i}")
else:
    print("WARNING: B3 cell not found!")

# B4
B4_NEW = """---
**INTERPRETA\u00c7\u00c3O \u2014 Distribui\u00e7\u00e3o de Superclasses e Risco (Gr\u00e1fico 4)**

**Pizza de superclasses:**
A distribui\u00e7\u00e3o por superclasse PTB-XL reflete o perfil deliberado do corpus constru\u00eddo para cobrir as principais cardiopatias:
- **CD (Dist\u00farbios de Condu\u00e7\u00e3o, ~42%)**: Maior grupo por concentrar m\u00faltiplos tipos de documento \u2014 relatos de miocardite, fibrilação atrial (revis\u00e3o + diretriz), cardiomiopatia de Chagas, IC descompensada. A amplitude cl\u00ednica de CD \u00e9 a maior das superclasses.
- **MI (Infarto do Mioc\u00e1rdio, ~19%)**: Representado por relatos de IAMCSST, bulas de alteplase/clopidogrel/enoxaparina e protocolo SUS de s\u00edndrome coron\u00e1ria. Vocabul\u00e1rio muito espec\u00edfico e coeso.
- **NORM (Normal, ~19%)**: Documentos de revis\u00e3o de biomarcadores (ceramidas, GDF-15, miRNAs) mapeados como NORM por descreverem popula\u00e7\u00f5es de refer\u00eancia sem cardiopatia aguda.
- **STTC (Altera\u00e7\u00f5es ST-T, ~12%)**: Angina inst\u00e1vel, fibrilação ventricular por cardiotoxicidade, Takotsubo \u2014 grupo heterog\u00eaneo mas clinicamente relevante.
- **HYP (Hipertrofia, ~8%)**: Apenas 2 documentos (IC descompensada SUS + estrog\u00eanio/obesidade), o grupo mais sub-representado.

**An\u00e1lise de Risco:**
- **Alto risco (84%)**: Todos os documentos normativos e relatos de caso s\u00e3o de alto risco \u2014 condi\u00e7\u00f5es agudas que requerem interven\u00e7\u00e3o imediata.
- **Baixo risco (16%)**: Exclusivo de revis\u00f5es de biomarcadores NORM (ceramidas, GDF-15, miRNAs), que descrevem marcadores diagn\u00f3sticos sem apresenta\u00e7\u00e3o de crise.

**Prepara\u00e7\u00e3o para Modelagem \u2014 Desbalanceamento de Classes:**
> **[PREPARA\u00c7\u00c3O PARA MODELAGEM]** O corpus apresenta desbalanceamento moderado a severo: CD (~42%) vs HYP (~8%), raz\u00e3o 5:1. Para o NB7, isso exige: (1) `class_weight='balanced'` na Regress\u00e3o Log\u00edstica; (2) avalia\u00e7\u00e3o por F1-score macro (n\u00e3o acur\u00e1cia global, que seria inflacionada por CD); (3) poss\u00edvel oversampling de HYP e STTC se a performance de valida\u00e7\u00e3o for insatisfat\u00f3ria. As quotas no `sintomas_pacientes.txt` (MI=3, STTC=4, CD=3) foram definidas para contrariar intencionalmente essa predomin\u00e2ncia."""

i, c = find_cell("**INTERPRETA\u00c7\u00c3O:** CD domina com ~42% do corpus", "markdown")
if c is not None:
    replace_md(c, B4_NEW)
    print(f"B4 applied to cell {i}")
else:
    print("WARNING: B4 cell not found!")

# B5
B5_NEW = """---
**INTERPRETA\u00c7\u00c3O \u2014 Frequ\u00eancia dos SYMPTOM_KEYWORDS (Gr\u00e1fico 5)**

**Distribui\u00e7\u00e3o em 3 tiers de frequ\u00eancia:**

**Tier Alto (vermelho, >50% do m\u00e1ximo):**
- **"dor"** (612 ocorr\u00eancias): Domina amplamente por ser termo poliss\u00eamico em contexto card\u00edaco (dor precordial, dor tor\u00e1cica, dor retroesternal) e aparecer em todas as categorias de documento.
- **"sintoma"** (~162): Frequente em linguagem epidemiol\u00f3gica e cl\u00ednica como meta-refer\u00eancia a queixas.
- **"insuficiencia"** (~124): Core do vocabul\u00e1rio card\u00edaco \u2014 insufici\u00eancia card\u00edaca, insufici\u00eancia respirat\u00f3ria, insufici\u00eancia coron\u00e1riana.

**Tier M\u00e9dio (laranja, 20-50%):**
- **"choque"**, **"taquicardia"**: Frequentes em contextos de emerg\u00eancia cardiол\u00f3gica, presentes em RCP, IC descompensada, IAMCSST.
- **"refere"**: Qualificador contextual t\u00edpico de relatos de caso ("paciente refere dispneia").
- **"angina"**: Concentrada nos documentos STTC e MI.

**Tier Baixo (azul, <20%):**
- **"hemoptise"**, **"sibilos"**, **"ortopneia"**: Alta especificidade cl\u00ednica \u2014 quando presentes, indicam frases de alta relev\u00e2ncia, mas s\u00e3o raros no corpus porque IC avan\u00e7ada e edema pulmonar s\u00e3o subrepresentados.
- **"dessaturacao"**, **"crepitantes"**: Termos f\u00edsico-semi\u00f3ticos espec\u00edficos de exame f\u00edsico, aparecem principalmente em relatos de caso.

**Feature Engineering \u2014 Tiers como Pesos de Relev\u00e2ncia:**
> **[FEATURE ENGINEERING]** O tier de frequ\u00eancia tem implica\u00e7\u00e3o direta para a qualidade da extra\u00e7\u00e3o: keywords de **tier alto** (dor, sintoma, insuficiencia) t\u00eam alto recall mas baixa precis\u00e3o \u2014 filtram muitas frases mas incluem ru\u00eddo. Keywords de **tier baixo** (hemoptise, ortopneia, sibilos) t\u00eam baixo recall mas alta precis\u00e3o \u2014 cada detec\u00e7\u00e3o indica frase clinicamente rica. O `trigger_score` funciona como mecanismo de reranking que compensa essa assimetria, priorizando frases onde M\u00daltiplos keywords de alta especificidade s\u00e3o combinados com stems discriminativos do l\u00e9xico TF-IDF.

**Observa\u00e7\u00e3o metodol\u00f3gica:** A alta frequ\u00eancia de qualificadores contextuais ("apresentou", "evoluiu com", "admitida com") justifica sua inclus\u00e3o no `SYMPTOM_KEYWORDS` \u2014 esses termos identificam o contexto narrativo de um caso cl\u00ednico, mesmo que n\u00e3o sejam sintomas per se. Eles garantem que o pipeline capture frases de relato cl\u00ednico real, n\u00e3o apenas frases que mencionam doen\u00e7as em contexto abstrato."""

i, c = find_cell('"insuficiencia" e "dor" lideram com alta frequ', "markdown")
if c is not None:
    replace_md(c, B5_NEW)
    print(f"B5 applied to cell {i}")
else:
    print("WARNING: B5 cell not found!")

# B6
B6_NEW = """---
**INTERPRETA\u00c7\u00c3O \u2014 Frases Sintom\u00e1ticas por Documento (Gr\u00e1fico 6)**

**Total: 929 frases sintom\u00e1ticas extra\u00eddas de 26 documentos.**

**An\u00e1lise por documento:**
- **Diretrizes SBC lideram** em volume bruto (183 frases na diretriz de RCP, 148 na de angina inst\u00e1vel) \u2014 documentos normativos extensos com muitos protocolos que descrevem condi\u00e7\u00f5es e sintomas de forma repetida ao longo do texto.
- **Protocolo SUS de S\u00edndrome Coron\u00e1ria** (90 frases): Algoritmos de manejo com crit\u00e9rios de sintomas bem definidos.
- **Relatos de Caso individuais** produzem de 8 a 24 frases \u2014 menor volume absoluto, mas densidade cl\u00ednica superior por frase.
- **`revisao_fibrilacao_atrial_filtrado.txt` produziu 0 frases**: \u00danico documento com stems_lookup=0, indicando que o NB5 n\u00e3o gerou stems para esse documento (provavelmente porque o texto era muito similar a outros documentos de fibrilação atrial, diluindo seu TF-IDF). Este \u00e9 um ponto de aten\u00e7\u00e3o \u2014 o documento existe no DISEASE_MAP mas n\u00e3o contribui para o pipeline de extra\u00e7\u00e3o.

**Distribui\u00e7\u00e3o por superclasse:**
- **CD (443/929 = 47.7%)**: Reflexo direto do dom\u00ednio de documentos CD no corpus (11/26 docs).
- **MI (185/929 = 19.9%)** e **STTC (170/929 = 18.3%)**: Propor\u00e7\u00e3o menor por menos documentos, mas vocabul\u00e1rio mais espec\u00edfico.
- **NORM (79)** e **HYP (52)**: Naturalmente baixos \u2014 revis\u00f5es de biomarcadores usam linguagem epidemiol\u00f3gica, n\u00e3o sintom\u00e1tica.

**Implica\u00e7\u00e3o para Ci\u00eancia de Dados \u2014 Documentos Dominantes:**
> **[RISCO DE DOMIN\u00c2NCIA]** Documentos como a diretriz de RCP (183 frases) e a de angina (148 frases) dominam quantitativamente o mapa_sintomas_doencas.csv. Se o NB7 for treinado sem controle desse vi\u00e9s, o classificador aprender\u00e1 o estilo lingu\u00edstico dessas diretrizes, n\u00e3o a linguagem cl\u00ednica geral de CD/STTC. Estrat\u00e9gias de mitiga\u00e7\u00e3o: subsampling por documento no NB7, ou adicionar peso inverso ao n\u00famero de frases por documento.

**Observa\u00e7\u00e3o sobre Relatos de Caso:**
Os 8 relatos somam apenas ~102 frases no total, uma m\u00e9dia de ~13 frases/relato. Apesar do menor volume, essas frases s\u00e3o candidatas priorit\u00e1rias para o `sintomas_pacientes.txt` por sua alta especificidade cl\u00ednica e trigger_score elevado."""

i, c = find_cell("Documentos de CD (azul) dominam o topo da lista", "markdown")
if c is not None:
    replace_md(c, B6_NEW)
    print(f"B6 applied to cell {i}")
else:
    print("WARNING: B6 cell not found!")

# B7
B7_NEW = """---
**INTERPRETA\u00c7\u00c3O \u2014 Trigger Score por Superclasse PTB-XL (Gr\u00e1fico 7)**

O `trigger_score` \u00e9 a m\u00e9trica central de qualidade cl\u00ednica do pipeline \u2014 mede a interse\u00e7\u00e3o entre os stems RSLP de uma frase e os stems TF-IDF discriminativos do documento de origem.

**An\u00e1lise por superclasse:**
- **MI (mediana ~1.5, scores at\u00e9 4+)**: Maior trigger_score por ter o vocabul\u00e1rio mais espec\u00edfico e coeso \u2014 relatos de IAMCSST usam termos como "tromb\u00f3lise", "stent", "oclus\u00e3o coron\u00e1riana", "ST elevado" que mapeiam diretamente aos stems TF-IDF das bulas de alteplase/clopidogrel e do protocolo de s\u00edndrome coron\u00e1ria. Alta precis\u00e3o l\u00e9xica.
- **STTC (mediana ~1.0, alta vari\u00e2ncia)**: Grupo heterog\u00eaneo \u2014 fibrilação ventricular por cardiotoxicidade tem stems muito espec\u00edficos (fluorouracil, CDI), mas Takotsubo e angina inst\u00e1vel compartilham vocabulary com CD, diluindo o score.
- **CD (mediana ~0.5, alta vari\u00e2ncia)**: Dispers\u00e3o elevada reflete a heterogeneidade dos 11 documentos CD \u2014 miocardite por COVID-19 tem vocabulary muito diferente de cardiomiopatia de Chagas. Documentos com stems no lookup t\u00eam scores altos; revis\u00f5es de fibrilação atrial (que n\u00e3o t\u00eam lookup) t\u00eam score 0.
- **HYP (mediana ~0.5)**: Apenas 2 documentos, vocabul\u00e1rio de IC descompensada e estrog\u00eanio/obesidade \u2014 especificidade moderada.
- **NORM (mediana ~0, muito concentrado em 0)**: Confirma\u00e7\u00e3o do esperado \u2014 revis\u00f5es de biomarcadores usam vocabulary gen\u00e9rico n\u00e3o capturado pelo l\u00e9xico TF-IDF de documentos cl\u00ednicos. Scores pr\u00f3ximos de 0 indicam que essas frases n\u00e3o t\u00eam afinidade com nenhum documento cl\u00ednico espec\u00edfico.

**Threshold de Qualidade:**
> **[FEATURE ENGINEERING]** O trigger_score funciona como **feature de qualidade** para filtrar frases candidatas. A an\u00e1lise do boxplot sugere: frases com score \u2265 2 s\u00e3o clinicamente discriminativas (topo 25% de MI); frases com score = 0 ainda s\u00e3o v\u00e1lidas se contiverem keywords de sintoma relevantes (STTC com Takotsubo). O threshold adotado na Se\u00e7\u00e3o 10.2 prioriza scores altos mas n\u00e3o exclui score=0 para completar quotas, garantindo cobertura de todas as superclasses.

**Valida\u00e7\u00e3o do L\u00e9xico TF-IDF:**
A separa\u00e7\u00e3o estat\u00edstica entre NORM (score \u2248 0) e MI (score > 1) confirma que o `edge_trigger_lookup.json` do NB5 tem poder discriminativo real: frases de documentos cl\u00ednicos agudos s\u00e3o genuinamente mais informativas para o sistema de apoio ao diagn\u00f3stico do que frases de revis\u00f5es de biomarcadores."""

i, c = find_cell("MI apresenta os maiores trigger_scores", "markdown")
if c is not None:
    replace_md(c, B7_NEW)
    print(f"B7 applied to cell {i}")
else:
    print("WARNING: B7 cell not found!")

# B8
B8_NEW = """---
**INTERPRETA\u00c7\u00c3O \u2014 Top 15 Palavras por Superclasse PTB-XL (Gr\u00e1fico 8)**

**MI \u2014 Vocabul\u00e1rio do Infarto:**
O grupo MI apresenta vocabul\u00e1rio altamente espec\u00edfico e coeso: termos como "infarto", "miocardio", "coronaria", "trombolitica", "stent", "arterial" dominam. A presen\u00e7a de termos de procedimento (ICP, tromb\u00f3lise) junto com termos anat\u00f4micos (parede livre, pseudoaneurisma) e farmacol\u00f3gicos (enoxaparina, clopidogrel) reflete a natureza dos documentos: bulas de anticoagulantes + protocolo de s\u00edndrome coron\u00e1ria + relato de IAMCSST. O vocabul\u00e1rio \u00e9 o mais homog\u00eaneo das tr\u00eas superclasses \u2014 facilitar\u00e1 a classifica\u00e7\u00e3o no NB7.

**STTC \u2014 Vocabul\u00e1rio Heterog\u00eaneo de Altera\u00e7\u00f5es ST-T:**
STTC agrupa condi\u00e7\u00f5es diferentes \u2014 fibrilação ventricular por cardiotoxicidade, Takotsubo e angina inst\u00e1vel. O vocabul\u00e1rio reflete essa heterogeneidade: "arritmia", "fluorouracil", "ventricular", "eletrocardiografico", "biomarcadores". A coexist\u00eancia de termos de arritmia (fibrilação) com termos de cardiomiopatia (Takotsubo) e termos de isquemia (angina, ST) desafia o classificador \u2014 STTC \u00e9 a classe com maior risco de confus\u00e3o com MI e CD.

**CD \u2014 Vocabul\u00e1rio Mais Amplo e Diverso:**
CD apresenta o vocabul\u00e1rio mais heterog\u00eaneo, refletindo os 11 documentos de naturezas muito distintas: "insuficiencia", "cardiaca", "fibrilacao", "miocardite", "chagas", "ventricular", "ritmo". A sobreposi\u00e7\u00e3o sem\u00e2ntica com MI (insufici\u00eancia card\u00edaca p\u00f3s-infarto) e HYP (IC por hipertrofia) \u00e9 o maior desafio de classifica\u00e7\u00e3o do corpus.

**Feature Engineering \u2014 TF-IDF como Separador de Classes:**
> **[FEATURE ENGINEERING]** O vocabul\u00e1rio observado confirma que o TF-IDF ter\u00e1 features discriminativas para MI vs NORM e MI vs CD, mas enfrentar\u00e1 desafio maior em CD vs STTC. Para o NB7, considerar: (1) n-gramas bigrams para capturar "dor precordial", "fibrilação ventricular", "choque cardiog\u00eanico" como features compostas; (2) feature engineering adicional com indicadores de presen\u00e7a de termos espec\u00edficos de cada superclasse; (3) regulariza\u00e7\u00e3o L2 adequada para lidar com a alta dimensionalidade do TF-IDF.

**Valida\u00e7\u00e3o da Qualidade do Pipeline:**
O alinhamento entre o vocabul\u00e1rio extra\u00eddo pelas frases sintom\u00e1ticas e o conhecimento cl\u00ednico esperado de cada superclasse confirma que o pipeline NB4\u2192NB5\u2192NB6 funcionou corretamente. N\u00e3o h\u00e1 contamina\u00e7\u00e3o cruzada evidente (ex: termos de MI dominantes em NORM), o que valida a cadeia de processamento."""

i, c = find_cell("O vocabul\u00e1rio por superclasse \u00e9 clinicamente coerente", "markdown")
if c is not None:
    replace_md(c, B8_NEW)
    print(f"B8 applied to cell {i}")
else:
    print("WARNING: B8 cell not found!")

# B9
B9_NEW = """---
**INTERPRETA\u00c7\u00c3O \u2014 Estat\u00edsticas do mapa_sintomas_doencas.csv (Gr\u00e1fico 9)**

**Shape do mapa: 929 linhas \u00d7 7 colunas** (entreg\u00e1vel principal do NB6).

**Top sintomas no mapa:**
- **"insuficiencia"** e **"dor"** dominam por serem keywords de alta frequ\u00eancia que aparecem em todas as categorias de documento cardiол\u00f3gico \u2014 s\u00e3o sintomas cardinais da cardiologia cl\u00ednica PT-BR.
- **"apresentou"** e **"quadro de"** s\u00e3o qualificadores contextuais \u2014 confirmam que o pipeline captura frases de relato cl\u00ednico, n\u00e3o apenas men\u00e7\u00f5es isoladas de termos m\u00e9dicos.
- **"choque"**, **"taquicardia"**, **"angina"**: Sintomas de emerg\u00eancia cardiол\u00f3gica com alta especificidade, bem representados.
- **"hipotensao"**, **"dispneia"**: Sintomas inespec\u00edficos mas clinicamente relevantes em cardiologia.
- Sintomas raros ("hemoptise", "ortopneia", "sibilos") t\u00eam frequ\u00eancia baixa mas alta precis\u00e3o diagn\u00f3stica quando presentes.

**Distribui\u00e7\u00e3o por superclasse:**
CD (~60% das linhas) > MI (~20%) > STTC (~18%) > NORM (~9%) > HYP (~6%). Este desbalanceamento \u00e9 estrutural \u2014 deriva da composi\u00e7\u00e3o do corpus, n\u00e3o de um bug no pipeline.

**Limpeza de Dados \u2014 Qualidade do CSV:**
> **[LIMPEZA DE DADOS]** O CSV gerado cont\u00e9m c\u00e9lulas vazias em Sintoma_2 e Sintoma_3 quando a frase tem apenas 1 ou 2 keywords detectados. Isso \u00e9 intencional \u2014 for\u00e7ar 3 sintomas por frase quando n\u00e3o existem geraria dados artificiais. No NB7, estas c\u00e9lulas vazias devem ser tratadas como `NaN` e n\u00e3o como string vazia, exigindo `.fillna('')` antes de concatenar para feature extraction. O `Trigger_Score=0` em algumas linhas (frases de NORM) indica frases v\u00e1lidas em termos de keywords mas sem afinidade TF-IDF espec\u00edfica.

**Prepara\u00e7\u00e3o para Modelagem (NB7):**
> **[PREPARA\u00c7\u00c3O PARA MODELAGEM]** O `mapa_sintomas_doencas.csv` servir\u00e1 como corpus de treinamento para o classificador NB7 de alto/baixo risco. Label mapping: MI, STTC, CD, HYP \u2192 alto risco; NORM, INCONCLUSIVO \u2192 baixo risco. O `Trigger_Score` poder\u00e1 ser usado como feature adicional al\u00e9m do TF-IDF das frases, enriquecendo a representa\u00e7\u00e3o vetorial. Estrat\u00e9gia de valida\u00e7\u00e3o: holdout 80/20 estratificado por superclasse, com avalia\u00e7\u00e3o por F1-score macro e AUC-ROC."""

i, c = find_cell('"insuficiencia" e "dor" s\u00e3o os sintomas mais representados', "markdown")
if c is not None:
    replace_md(c, B9_NEW)
    print(f"B9 applied to cell {i}")
else:
    print("WARNING: B9 cell not found!")

# B10
B10_NEW = """---
**INTERPRETA\u00c7\u00c3O \u2014 Trigger Score das 10 Frases Selecionadas (Gr\u00e1fico 10)**

**As 10 frases selecionadas para o `sintomas_pacientes.txt`** representam o output cl\u00ednico mais qualificado do pipeline NB6.

**An\u00e1lise por superclasse:**

**MI (3 frases, F1-F3):**
- Frases do protocolo SUS de s\u00edndrome coron\u00e1ria, bula de alteplase e bula de enoxaparina \u2014 documentos com stems muito espec\u00edficos de infarto.
- Trigger scores mais altos: o vocabulary de MI (ICP, IAMCSST, tromb\u00f3lise, subcut\u00e2neo) tem alta sobreposi\u00e7\u00e3o com o l\u00e9xico TF-IDF dessas bulas e protocolo.
- Frases clinicamente representativas: descrevem ativa\u00e7\u00e3o do sistema de sa\u00fade para infarto agudo \u2014 exatamente o cen\u00e1rio de uso do Cardio-Edge-AI.

**STTC (4 frases, F4-F7):**
- 2 frases da diretriz de angina inst\u00e1vel (trigger_score alto por clopidogrel/SCASSST overlap), 1 da fibrilação ventricular/cardiotoxicidade, 1 de Takotsubo.
- A frase de Takotsubo pode ter trigger_score pr\u00f3ximo de 0 \u2014 o relato usa linguagem descritiva gen\u00e9rica ("apresenta-se com altera\u00e7\u00f5es eletrocardiogr\u00e1ficas") que n\u00e3o captura os stems espec\u00edficos do lookup.
- **Decis\u00e3o de pipeline**: A sele\u00e7\u00e3o por quota garante que STTC seja representada mesmo com scores baixos \u2014 clinicamente correto, pois STTC tem alta mortalidade e sub-diagn\u00f3stico frequente.

**CD (3 frases, F8-F10):**
- Chagas (assist\u00eancia ventricular), desfibrilação (RCP), noradrenalina (choque cardiog\u00eanico).
- A frase 9 ("Quadro 5.5 \u2013 Orienta\u00e7\u00e3o para desfibrilação...") \u00e9 borderline \u2014 cont\u00e9m estrutura tabular residual. Trigger_score alto por overlap com stems de RCP (rcp, compresso, choque).

**Valida\u00e7\u00e3o do Filtro de Qualidade:**
> **[LIMPEZA DE DADOS]** O filtro `passes_quality()` (alpha_ratio \u2265 0.70, 8 \u2264 n_words \u2264 70, sem URLs/DOI/ISSN) foi efetivo: 195 frases descartadas de 929 (21.0%), taxa de aprova\u00e7\u00e3o 79.0%. O filtro corretamente elimina refer\u00eancias bibliogr\u00e1ficas, cabe\u00e7alhos de se\u00e7\u00e3o, e fragmentos num\u00e9ricos que passaram pelo segmentador de frases.

**Implica\u00e7\u00e3o Sist\u00eamica \u2014 Cardio-Edge-AI:**
As 10 frases selecionadas cobrem os principais cen\u00e1rios de triagem do sistema: infarto agudo (MI), altera\u00e7\u00f5es de ST e arritmias malignas (STTC), e dist\u00farbios de condu\u00e7\u00e3o/IC aguda (CD). A cobertura 100% de sintomas detectados com m\u00e9dia de 1.0 keyword/frase indica que frases cl\u00ednicas reais t\u00eam pelo menos 1 indicador de queixa \u2014 validando a abordagem baseada em keywords como camada prim\u00e1ria de triagem no pipeline NLP edge."""

i, c = find_cell("As frases selecionadas t\u00eam trigger_scores acima ou pr\u00f3ximos da m\u00e9dia", "markdown")
if c is not None:
    replace_md(c, B10_NEW)
    print(f"B10 applied to cell {i}")
else:
    print("WARNING: B10 cell not found!")

# ════════════════════════════════════════════════════════════════════════════
# SECTION C – ADD DATA SCIENCE LIFECYCLE CALLOUTS
# ════════════════════════════════════════════════════════════════════════════

# C1 – ## 4. Análise Estatística do Corpus
C1_PREFIX = """> **[LIMPEZA DE DADOS | CONTROLE DE QUALIDADE]** Esta seção caracteriza o corpus para calibrar os filtros de qualidade do pipeline. Entender o comprimento médio das frases do corpus é pré-requisito para definir `min_palavras` e `max_palavras` de forma empiricamente fundada, não arbitrária.

"""

i, c = find_cell("## 4. An\u00e1lise Estat\u00edstica do Corpus", "markdown")
if c is not None:
    prepend_md(c, C1_PREFIX)
    print(f"C1 applied to cell {i}")
else:
    print("WARNING: C1 cell not found!")

# C2 – ## 6. Palavras-Gatilho de Sintoma
C2_PREFIX = """> **[FEATURE ENGINEERING \u2014 VOCABUL\u00c1RIO CL\u00cdNICO]** O `SYMPTOM_KEYWORDS` \u00e9 a camada de feature extraction baseada em dom\u00ednio (domain-driven features) \u2014 lista curada por especialistas cl\u00ednicos como proxy de presen\u00e7a de queixa. Esta abordagem complementa o TF-IDF estat\u00edstico: enquanto o TF-IDF \u00e9 agn\u00f3stico ao dom\u00ednio, o SYMPTOM_KEYWORDS injeta conhecimento cl\u00ednico expl\u00edcito no pipeline.

"""

i, c = find_cell("## 6. Palavras-Gatilho de Sintoma", "markdown")
if c is not None:
    prepend_md(c, C2_PREFIX)
    print(f"C2 applied to cell {i}")
else:
    print("WARNING: C2 cell not found!")

# C3 – ## 7. Stemming RSLP
C3_PREFIX = """> **[FEATURE ENGINEERING \u2014 NORMALIZA\u00c7\u00c3O MORFOL\u00d3GICA]** O RSLP Stemming \u00e9 a etapa de normaliza\u00e7\u00e3o de features textuais: reduz a dimensionalidade do espa\u00e7o de tokens ao mapear formas flexionadas para uma ra\u00edz comum (ex: "taquic\u00e1rdico", "taquicardia", "taquicardias" \u2192 "taquicardi"). Isso maximiza o recall na correspond\u00eancia com o l\u00e9xico TF-IDF, que tamb\u00e9m foi constru\u00eddo sobre stems, n\u00e3o tokens brutos.

"""

i, c = find_cell("## 7. Stemming RSLP", "markdown")
if c is not None:
    prepend_md(c, C3_PREFIX)
    print(f"C3 applied to cell {i}")
else:
    print("WARNING: C3 cell not found!")

# C4 – ## 8. Pipeline Completo
C4_PREFIX = """> **[PIPELINE DE EXTRA\u00c7\u00c3O | FEATURE ENGINEERING]** Esta se\u00e7\u00e3o executa o pipeline completo de extra\u00e7\u00e3o de features textuais cl\u00ednicas: segmenta\u00e7\u00e3o de texto \u2192 filtro por SYMPTOM_KEYWORDS \u2192 c\u00e1lculo de trigger_score via RSLP + TF-IDF matching \u2192 associa\u00e7\u00e3o de metadados cl\u00ednicos. O output (`df_all`) \u00e9 o dataset bruto sobre o qual todos os entreg\u00e1veis FIAP s\u00e3o constru\u00eddos.

"""

i, c = find_cell("## 8. Pipeline Completo", "markdown")
if c is not None:
    prepend_md(c, C4_PREFIX)
    print(f"C4 applied to cell {i}")
else:
    print("WARNING: C4 cell not found!")

# C5 – ## 10.1. Entregável FIAP — mapa_sintomas_doencas.csv
C5_PREFIX = """> **[PREPARA\u00c7\u00c3O PARA MODELAGEM]** O `mapa_sintomas_doencas.csv` \u00e9 o corpus de treinamento estruturado para o NB7. Cada linha representa uma inst\u00e2ncia de treinamento: features textuais (Sintoma_1/2/3, frase impl\u00edcita), metadados cl\u00ednicos (diagn\u00f3stico) e label de classifica\u00e7\u00e3o bin\u00e1ria impl\u00edcita (alto/baixo risco via Nivel_Risco). O Trigger_Score \u00e9 uma feature adicional num\u00e9rica que pode ser usada como input direto no NB7.

"""

i, c = find_cell("## 10.1. Entreg\u00e1vel FIAP", "markdown")
if c is not None:
    prepend_md(c, C5_PREFIX)
    print(f"C5 applied to cell {i}")
else:
    print("WARNING: C5 cell not found!")

# C6 – ## 10.2. Entregável FIAP — sintomas_pacientes.txt
C6_PREFIX = """> **[LIMPEZA DE DADOS | SELE\u00c7\u00c3O COM CRIT\u00c9RIO CL\u00cdNICO]** A sele\u00e7\u00e3o das 10 frases aplica uma camada adicional de limpeza sobre o corpus j\u00e1 filtrado: remove ru\u00eddo bibliogr\u00e1fico (DOIs, URLs, ISSN), garante comprimento adequado para an\u00e1lise cl\u00ednica (8-70 palavras), e mant\u00e9m pureza textual (alpha_ratio \u2265 70%). As quotas por superclasse garantem que o entreg\u00e1vel seja clinicamente representativo, n\u00e3o apenas o resultado de amostragem aleat\u00f3ria.

"""

i, c = find_cell("## 10.2. Entreg\u00e1vel FIAP", "markdown")
if c is not None:
    prepend_md(c, C6_PREFIX)
    print(f"C6 applied to cell {i}")
else:
    print("WARNING: C6 cell not found!")

# ════════════════════════════════════════════════════════════════════════════
# SAVE
# ════════════════════════════════════════════════════════════════════════════

with open(NB_PATH, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f"\nSaved notebook with {len(nb['cells'])} cells.")

# Verify
with open(NB_PATH, encoding="utf-8") as f:
    nb_verify = json.load(f)
print(f"Verification: loaded {len(nb_verify['cells'])} cells successfully.")
print("SUCCESS")
