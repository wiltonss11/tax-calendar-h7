# 📋 Instruções de Uso - Tax Calendar

## 🚀 Início Rápido

### 1. Configuração Inicial
```bash
# Clone o repositório (se aplicável)
# Navegue até o diretório do projeto
cd Tax_CalendarX

# Execute a configuração automática
python setup.py
```

### 2. Configuração Manual (se necessário)

#### Instalar PostgreSQL
- **Windows**: Baixe do site oficial do PostgreSQL
- **macOS**: `brew install postgresql`
- **Linux**: `sudo apt-get install postgresql postgresql-contrib`

#### Configurar Banco de Dados
```bash
# Criar banco de dados
createdb tax_calendar

# Ou via psql
psql -U postgres
CREATE DATABASE tax_calendar;
\q
```

#### Configurar Variáveis de Ambiente
```bash
# Copie o arquivo de exemplo
cp backend/env_example.txt backend/.env

# Edite o arquivo .env com suas credenciais
# DATABASE_URL=postgresql://seu_usuario:sua_senha@localhost/tax_calendar
```

### 3. Executar a Aplicação

#### Opção 1: Script Automático
```bash
python run.py
```

#### Opção 2: Manual
```bash
# Terminal 1 - Backend
cd backend
python app.py

# Terminal 2 - Frontend (opcional)
# Abra frontend/index.html no navegador
```

## 📊 Importação de Dados

### Formato da Planilha
A planilha deve conter as seguintes colunas:

| Coluna | Descrição | Obrigatório | Exemplo |
|--------|-----------|-------------|---------|
| `level` | Nível da obrigação | Sim | federal, state, county, municipality |
| `name` | Nome da obrigação | Sim | Form 1040 - Individual Income Tax |
| `description` | Descrição | Não | Declaração de imposto de renda |
| `due_date` | Data de vencimento | Sim | 2024-04-15 |
| `form_number` | Número do formulário | Não | 1040 |
| `category` | Categoria | Não | Income Tax |
| `state` | Estado (para level state/county/municipality) | Condicional | California |
| `county` | Condado (para level county/municipality) | Condicional | Los Angeles County |
| `municipality` | Município (para level municipality) | Condicional | Los Angeles |

### Importar Dados
```bash
# Usando o script de importação
python backend/import_data.py sample_data/tax_obligations_sample.csv

# Ou converta sua planilha Excel para CSV primeiro
```

## 🔧 Desenvolvimento

### Estrutura do Projeto
```
Tax_CalendarX/
├── backend/                 # Servidor Python Flask
│   ├── app.py              # Aplicação principal
│   ├── config.py           # Configurações
│   ├── database_setup.py   # Setup do banco
│   ├── data_analysis.py    # Análise com Pandas
│   ├── import_data.py      # Importação de dados
│   └── requirements.txt    # Dependências
├── frontend/               # Interface JavaScript
│   ├── index.html          # Página principal
│   ├── styles.css          # Estilos
│   └── app.js              # Lógica JavaScript
├── sample_data/            # Dados de exemplo
└── README.md               # Documentação
```

### Comandos Úteis

#### Análise de Dados
```bash
cd backend
python data_analysis.py
```

#### Reset do Banco de Dados
```bash
cd backend
python database_setup.py
```

#### Verificar Dependências
```bash
cd backend
pip list
```

## 🐛 Solução de Problemas

### Erro: "ModuleNotFoundError"
```bash
# Ative o ambiente virtual
cd backend
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### Erro: "Connection refused" (PostgreSQL)
1. Verifique se o PostgreSQL está rodando
2. Confirme as credenciais no arquivo `.env`
3. Teste a conexão:
```bash
psql -U seu_usuario -d tax_calendar
```

### Erro: "Port 5000 already in use"
```bash
# Encontre o processo usando a porta
netstat -ano | findstr :5000  # Windows
lsof -i :5000                 # Linux/Mac

# Mate o processo ou mude a porta no app.py
```

### Frontend não carrega dados
1. Verifique se o backend está rodando na porta 5000
2. Abra o console do navegador (F12) para ver erros
3. Verifique se a URL da API está correta em `frontend/app.js`

## 📈 Funcionalidades

### ✅ Implementadas
- Filtros em cascata (Federal → Estado → Condado → Município)
- Visualização em lista e calendário
- Estatísticas em tempo real
- Interface responsiva
- API REST completa
- Análise de redundância com Pandas
- Importação de planilhas

### 🔄 Em Desenvolvimento
- Notificações por email
- Exportação de relatórios
- Sistema de usuários
- Dashboard administrativo

## 📞 Suporte

### Logs de Debug
```bash
# Ative o modo debug no .env
FLASK_DEBUG=True

# Verifique os logs no console
```

### Backup do Banco
```bash
# Backup
pg_dump tax_calendar > backup.sql

# Restore
psql tax_calendar < backup.sql
```

### Limpeza Completa
```bash
# Remove ambiente virtual
rm -rf backend/venv

# Remove banco de dados
dropdb tax_calendar

# Reconfigure tudo
python setup.py
```

## 🎯 Próximos Passos

1. **Importe seus dados**: Use o script `import_data.py` com sua planilha
2. **Personalize**: Ajuste cores, textos e funcionalidades conforme necessário
3. **Deploy**: Configure para produção quando estiver pronto
4. **Monitore**: Use as ferramentas de análise para manter os dados organizados

---

**💡 Dica**: Mantenha sempre um backup dos seus dados antes de fazer alterações importantes!
