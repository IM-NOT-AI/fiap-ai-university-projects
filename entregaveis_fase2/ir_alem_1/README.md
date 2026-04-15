# Ir Alem 1 - Portal CardioIA com React e Vite
### Fase 2 - Interface do Sistema de Diagnostico Cardiologico

> Isaac Maciel - RM98222 - 2TIAOA - Turno Noturno

---

## AVISO IMPORTANTE PARA A BANCA

> O codigo-fonte nesta pasta e uma **copia** do original localizado em:
>
> **Projeto principal:** `challenge/ai_cardiology/frontend/cardioia-portal/`
>
> O `src/` aqui presente e identico ao original. O `node_modules/` nao foi copiado
> para manter o pacote leve - execute `npm install` antes de rodar (instrucoes abaixo).
>
> Repositorio GitHub: **https://github.com/IM-NOT-AI/fiap-ai-university-projects**

---

## Como Executar

```bash
# A partir desta pasta (entregaveis_fase2/ir_alem_1/)
npm install
npm run dev

# Acesse no navegador:
# http://localhost:5173
```

**Credenciais de demonstracao:**

| Usuario | Senha | Perfil |
|---|---|---|
| `cardiologista` | `cardio@123` | Medico |
| `admin` | `admin@123` | Administrador |

Nao ha backend real - toda autenticacao e persistencia sao simuladas no `localStorage`.

---

## Estrutura do Codigo-Fonte

```
ir_alem_1/
+-- README.md              <- este arquivo
+-- index.html             <- entry point HTML (Vite)
+-- package.json           <- dependencias: React 18, react-router-dom 6, Vite 6
+-- vite.config.js         <- configuracao Vite
+-- src/
    +-- main.jsx           <- ponto de entrada React, BrowserRouter
    +-- App.jsx            <- rotas, PrivateRoute, Layout
    +-- App.module.css     <- estilos globais da aplicacao
    +-- index.css          <- reset CSS
    |
    +-- contexts/
    |   +-- AuthContext.jsx        <- JWT simulado, login/logout, isAuthenticated
    |
    +-- hooks/
    |   +-- useAuth.js             <- useContext(AuthContext) com guard de nulo
    |
    +-- services/
    |   +-- authService.js         <- mock JWT (prefixo mock-jwt- + hash), localStorage
    |   +-- mockData.js            <- 15 pacientes PTB-XL, 20 consultas, stats dashboard
    |
    +-- components/
    |   +-- Layout/                <- Navbar + Outlet (estrutura da pagina logada)
    |   +-- Navbar/                <- dark navy, NavLink ativo, avatar, botao logout
    |   +-- PrivateRoute/          <- guarda Outlet react-router v6, redireciona /login
    |   +-- PatientModal/          <- modal detalhes do paciente + interpretacao IA
    |   +-- Toast/                 <- notificacao slide-in, auto-dismiss 3 segundos
    |
    +-- pages/
        +-- Login/                 <- formulario login, estado de erro, hint credenciais
        +-- Dashboard/             <- 4 cards stats, top-5 risco, grafico CSS puro
        +-- Patients/              <- busca, ordenacao, paginacao (8/pagina), badges, modal
        +-- Appointments/          <- formulario useReducer, validacao, Toast, tabela
```

---

## Requisitos do Enunciado Cumpridos

| Requisito | Implementacao | Arquivo |
|---|---|---|
| Autenticacao simulada via Context API (JWT fake no localStorage) | AuthContext + authService.js | `src/contexts/AuthContext.jsx` |
| Listagem de pacientes com base simulada | PatientsPage + mockData.js | `src/pages/Patients/` |
| Formulario de agendamento com useState e useReducer | AppointmentsPage | `src/pages/Appointments/` |
| Dashboard com contagem de pacientes e consultas | DashboardPage | `src/pages/Dashboard/` |
| Protecao de rotas com AuthContext | PrivateRoute + Outlet v6 | `src/components/PrivateRoute/` |
| Estilizacao com CSS Modules | Todos os 25 arquivos .jsx | `**/*.module.css` |
| Uso correto de Hooks (useState, useEffect, useContext) | Em todas as pages | - |
| Componentizacao e organizacao do projeto | contexts/hooks/services/components/pages | - |

---

## Dados do Portal Derivados do Projeto Real

O `mockData.js` nao usa dados ficticioss genericos - reflete o pipeline CardioIA:

- 15 pacientes com as 6 superclasses PTB-XL reais (NORM, MI, STTC, CD, HYP, INCONCLUSIVO)
- Logica de risco identica ao NB11: MI/STTC/CD/HYP = alto risco, NORM = baixo risco
- Precisao exibida no dashboard (96.2%) = acuracia real do NB11
- Badges coloridos por superclasse: MI vermelho, STTC laranja, CD amarelo, HYP roxo, NORM verde

---

## Stack Tecnica

| Tecnologia | Versao | Papel |
|---|---|---|
| React | 18.3 | UI declarativa com hooks |
| react-router-dom | 6.28 | Roteamento com Outlet e PrivateRoute idiomatico |
| Vite | 6 | Bundler e servidor de desenvolvimento |
| CSS Modules | nativo | Estilizacao com escopo por componente |

Sem dependencias externas de UI (sem Material UI, Chakra, Bootstrap ou Tailwind).

---

## Design System

| Token CSS | Valor | Uso |
|---|---|---|
| `--primary` | `#0d1b2a` | Navy escuro - Navbar, cabecalhos |
| `--accent` | `#e63946` | Vermelho cardiaco - alertas, botoes primarios |
| `--success` | `#2a9d8f` | Teal - badges NORM, metricas positivas |
| fundo | `#f8f9fa` | Background geral |
| cards | `#ffffff` + sombra | Superficies elevadas |

---

## Integrantes

| Nome | RM | Turma |
|---|---|---|
| Isaac Maciel | 98222 | 2TIAOA - Turno Noturno |

---

## Pendente

- Gravar video YouTube nao listado (ate 4 min) demonstrando o portal em execucao
- Linkar video no README do repositorio GitHub
