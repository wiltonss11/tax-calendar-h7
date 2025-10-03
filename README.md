# Tax Calendar - Profissional

Sistema de calendário fiscal para obrigações tributárias dos Estados Unidos, incluindo níveis federal, estadual, municipal e municipal.

## 🚀 Funcionalidades

- **Filtros Hierárquicos**: Federal → Estado → Condado → Município
- **Busca Inteligente**: Encontre estados, condados e municípios rapidamente
- **Filtros por Período**: Visualize obrigações por mês
- **Links de Fontes**: Acesso direto a instruções, formulários e recursos
- **Design Responsivo**: Funciona em desktop, tablet e mobile
- **Tema H7 Advisory**: Interface profissional com cores corporativas

## 🛠️ Tecnologias

- **Backend**: Python + Flask
- **Frontend**: HTML5 + CSS3 + JavaScript
- **Database**: PostgreSQL
- **Styling**: CSS Grid, Flexbox, Glassmorphism

## 📋 Pré-requisitos

- Python 3.8+
- PostgreSQL
- pip (gerenciador de pacotes Python)

## 🔧 Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/wiltonss11/wiltonss11.git
cd wiltonss11
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Configure o banco de dados**
- Crie um banco PostgreSQL
- Configure as credenciais em `app.py`
- Importe os dados das obrigações

4. **Execute a aplicação**
```bash
python app.py
```

5. **Acesse no navegador**
```
http://127.0.0.1:5000
```

## 📊 Estrutura do Banco

### Tabela `obrigacoes_com_data`
- `obligation_id`: ID único
- `title`: Título da obrigação
- `date`: Data de vencimento
- `jurisdiction_level`: Nível (federal, state, county, municipal)
- `jurisdiction`: Jurisdição responsável
- `state`: Estado (código)
- `county`: Condado
- `city`: Cidade
- `category`: Categoria
- `frequency`: Frequência
- `notes`: Observações
- `sources`: Fontes (JSON array)

## 🎨 Personalização

### Cores do Tema H7 Advisory
- **Verde Principal**: `#beee0f`
- **Preto**: `#000000`
- **Gradientes**: Combinações profissionais

### Responsividade
- **Desktop**: Layout completo
- **Tablet**: Ajustes de grid
- **Mobile**: Layout otimizado

## 🔍 API Endpoints

- `GET /api/health` - Status da aplicação
- `GET /api/states` - Lista de estados
- `GET /api/counties/<state>` - Condados por estado
- `GET /api/cities/<state>/<county>` - Cidades por condado
- `GET /api/calendar` - Obrigações com filtros
- `GET /api/search` - Busca inteligente

## 📱 Responsividade

### Breakpoints
- **Desktop**: > 1200px
- **Tablet**: 768px - 1200px
- **Mobile**: < 768px
- **Mobile Small**: < 480px

### Ajustes por Dispositivo
- **Logo**: Redimensionamento automático
- **Cards**: Layout adaptativo
- **Filtros**: Interface otimizada
- **Botões**: Tamanhos apropriados

## 🚀 Deploy

### Opção 1: GitHub Pages (Frontend)
1. Build do frontend
2. Push para branch `gh-pages`
3. Configurar GitHub Pages

### Opção 2: Heroku (Full Stack)
1. Criar `Procfile`
2. Configurar variáveis de ambiente
3. Deploy via Git

### Opção 3: VPS/Cloud
1. Configurar servidor
2. Instalar dependências
3. Configurar nginx/apache
4. Configurar SSL

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Equipe

- **Desenvolvimento**: H7 Advisory
- **Design**: Interface profissional
- **Backend**: Python/Flask
- **Frontend**: HTML/CSS/JavaScript

## 📞 Suporte

Para suporte técnico ou dúvidas:
- **Email**: suporte@h7advisory.com
- **GitHub Issues**: [Criar issue](https://github.com/wiltonss11/wiltonss11/issues)

---

**Tax Calendar - Profissional** | Desenvolvido com ❤️ pela H7 Advisory

## Hi there 👋

<!--
**wiltonss11/wiltonss11** is a ✨ _special_ ✨ repository because its `README.md` (this file) appears on your GitHub profile.

Here are some ideas to get you started:

- 🔭 I'm currently working on Tax Calendar Professional
- 🌱 I'm currently learning Python, Flask, PostgreSQL
- 👯 I'm looking to collaborate on web development projects
- 🤔 I'm looking for help with deployment and optimization
- 💬 Ask me about tax compliance and web development
- 📫 How to reach me: [GitHub](https://github.com/wiltonss11)
- 😄 Pronouns: he/him
- ⚡ Fun fact: I love building professional web applications!
-->
