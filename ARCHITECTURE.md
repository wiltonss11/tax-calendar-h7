# 🏗️ Arquitetura do Sistema - Tax Calendar

## 📊 Visão Geral

O Tax Calendar é uma aplicação web full-stack para gerenciar obrigações fiscais dos Estados Unidos, com suporte a múltiplos níveis hierárquicos (Federal, Estadual, Condado e Municipal).

## 🎯 Objetivos do Sistema

- **Centralização**: Todas as obrigações fiscais em um local
- **Hierarquia**: Filtros em cascata por localização geográfica
- **Flexibilidade**: Suporte a diferentes níveis de obrigações
- **Análise**: Ferramentas para análise de dados e redundância
- **Usabilidade**: Interface intuitiva e responsiva

## 🏛️ Arquitetura em Camadas

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (JavaScript)                    │
├─────────────────────────────────────────────────────────────┤
│  • Interface de Usuário                                     │
│  • Filtros em Cascata                                       │
│  • Visualização Lista/Calendário                            │
│  • Estatísticas em Tempo Real                              │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND (Python Flask)                   │
├─────────────────────────────────────────────────────────────┤
│  • API REST                                                 │
│  • Lógica de Negócio                                        │
│  • Validação de Dados                                       │
│  • Análise com Pandas                                       │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                 BANCO DE DADOS (PostgreSQL)                  │
├─────────────────────────────────────────────────────────────┤
│  • Dados Estruturados                                       │
│  • Relacionamentos Hierárquicos                            │
│  • Integridade Referencial                                  │
│  • Performance Otimizada                                    │
└─────────────────────────────────────────────────────────────┘
```

## 🗄️ Modelo de Dados

### Hierarquia Geográfica
```
Federal (IRS)
├── State (Estados)
│   ├── County (Condados)
│   │   └── Municipality (Municípios)
```

### Tabelas Principais

#### 1. Localização
- **states**: Estados dos EUA
- **counties**: Condados por estado
- **municipalities**: Municípios por condado

#### 2. Obrigações
- **federal_obligations**: Obrigações federais (IRS)
- **state_obligations**: Obrigações estaduais
- **county_obligations**: Obrigações de condados
- **municipality_obligations**: Obrigações municipais

### Relacionamentos
```sql
states (1) ──→ (N) counties
counties (1) ──→ (N) municipalities
states (1) ──→ (N) state_obligations
counties (1) ──→ (N) county_obligations
municipalities (1) ──→ (N) municipality_obligations
```

## 🔄 Fluxo de Dados

### 1. Carregamento Inicial
```
Frontend → API /states → Backend → PostgreSQL
```

### 2. Filtros em Cascata
```
Estado Selecionado → API /counties/{state_id} → Carrega Condados
Condado Selecionado → API /municipalities/{county_id} → Carrega Municípios
```

### 3. Visualização de Obrigações
```
Filtros Aplicados → API /calendar → Backend → PostgreSQL → Frontend
```

## 🛠️ Tecnologias

### Frontend
- **HTML5**: Estrutura semântica
- **CSS3**: Estilos modernos com Flexbox/Grid
- **JavaScript ES6+**: Lógica da aplicação
- **Font Awesome**: Ícones

### Backend
- **Python 3.8+**: Linguagem principal
- **Flask**: Framework web
- **SQLAlchemy**: ORM
- **Pandas**: Análise de dados
- **psycopg2**: Driver PostgreSQL

### Banco de Dados
- **PostgreSQL 12+**: Banco relacional
- **Índices**: Otimização de consultas
- **Constraints**: Integridade referencial

## 📡 API Endpoints

### Localização
```
GET /api/states                    # Lista estados
GET /api/counties/{state_id}       # Condados por estado
GET /api/municipalities/{county_id} # Municípios por condado
```

### Obrigações
```
GET /api/federal-obligations       # Obrigações federais
GET /api/state-obligations/{state_id}     # Obrigações estaduais
GET /api/county-obligations/{county_id}   # Obrigações de condado
GET /api/municipality-obligations/{municipality_id} # Obrigações municipais
GET /api/calendar                   # Todas as obrigações (com filtros)
```

## 🔍 Análise de Dados

### Ferramentas
- **Pandas**: Manipulação e análise
- **SQLAlchemy**: Consultas otimizadas
- **Excel Export**: Relatórios detalhados

### Métricas
- Contagem por nível
- Detecção de duplicatas
- Distribuição geográfica
- Análise temporal

## 🚀 Deployment

### Desenvolvimento
```bash
python setup.py    # Configuração inicial
python run.py      # Execução
```

### Produção
- **Backend**: Gunicorn + Nginx
- **Frontend**: Servidor web estático
- **Banco**: PostgreSQL clusterizado
- **Cache**: Redis (futuro)

## 🔒 Segurança

### Medidas Implementadas
- Validação de entrada
- Sanitização de dados
- CORS configurado
- Prepared statements

### Futuras Implementações
- Autenticação JWT
- Rate limiting
- HTTPS obrigatório
- Logs de auditoria

## 📈 Performance

### Otimizações Atuais
- Índices no banco
- Consultas otimizadas
- Cache de dados frequentes
- Lazy loading

### Monitoramento
- Logs de performance
- Métricas de uso
- Alertas de erro

## 🔄 Escalabilidade

### Horizontal
- Load balancer
- Múltiplas instâncias
- Database sharding

### Vertical
- Otimização de queries
- Cache Redis
- CDN para assets

## 🧪 Testes

### Estratégia
- Testes unitários (backend)
- Testes de integração (API)
- Testes E2E (frontend)

### Ferramentas
- pytest (Python)
- Jest (JavaScript)
- Selenium (E2E)

## 📊 Monitoramento

### Métricas
- Tempo de resposta
- Taxa de erro
- Uso de recursos
- Queries lentas

### Alertas
- Falhas de sistema
- Performance degradada
- Erros de banco
- Uso excessivo de recursos

## 🔮 Roadmap

### Fase 1 ✅
- Estrutura base
- Filtros em cascata
- Interface responsiva
- Análise de dados

### Fase 2 🔄
- Importação de planilhas
- Notificações
- Relatórios
- Dashboard admin

### Fase 3 📋
- Autenticação
- Multi-tenant
- API pública
- Mobile app

### Fase 4 🚀
- Machine Learning
- Integração externa
- Analytics avançado
- Microserviços

---

**💡 Nota**: Esta arquitetura foi projetada para ser modular, escalável e fácil de manter, permitindo evolução gradual conforme as necessidades do negócio.
