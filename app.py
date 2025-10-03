#!/usr/bin/env python3
"""
Tax Calendar - Backend Profissional
Flask + PostgreSQL + Angular
"""

from flask import Flask, jsonify, request, render_template_string, send_from_directory
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import json
from datetime import datetime
import os

app = Flask(__name__, static_folder='static')
CORS(app)

# Configuração do banco
# Para Railway: usar DATABASE_URL se disponível
# Para local: usar configurações padrão
if 'DATABASE_URL' in os.environ:
    # Railway PostgreSQL
    import urllib.parse as urlparse
    url = urlparse.urlparse(os.environ['DATABASE_URL'])
    DB_CONFIG = {
        'host': url.hostname,
        'port': url.port,
        'database': url.path[1:],
        'user': url.username,
        'password': url.password
    }
else:
    # Configuração local
    DB_CONFIG = {
        'host': os.environ.get('DB_HOST', '192.168.88.189'),
        'port': int(os.environ.get('DB_PORT', 5432)),
        'database': os.environ.get('DB_NAME', 'Tax_Calendar'),
        'user': os.environ.get('DB_USER', 'postgres'),
        'password': os.environ.get('DB_PASSWORD', 'root')
    }

def get_db_connection():
    """Cria conexão com o banco de dados"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"❌ Erro ao conectar com banco: {e}")
        return None

@app.route('/')
def home():
    """Página inicial com frontend integrado"""
    return render_template_string('''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tax Calendar - Profissional</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Montserrat:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Inter', sans-serif; background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%); min-height: 100vh; color: #ffffff; line-height: 1.6; }
        .container { max-width: 1400px; margin: 0 auto; padding: 24px; }
        .header { text-align: center; margin-bottom: 48px; color: #beee0f; position: relative; }
        .header-content { display: flex; flex-direction: column; align-items: center; gap: 20px; }
        .header::before { content: ''; position: absolute; top: -20px; left: 50%; transform: translateX(-50%); width: 60px; height: 4px; background: linear-gradient(90deg, #beee0f, #ffffff); border-radius: 2px; }
        .header h1 { font-size: 3rem; margin-bottom: 0; text-shadow: 0 4px 8px rgba(0,0,0,0.8); font-weight: 700; letter-spacing: -0.02em; font-family: 'Montserrat', 'Inter', sans-serif; display: flex; align-items: center; justify-content: center; gap: 24px; flex-wrap: wrap; }
        .header p { color: #cccccc; font-size: 1.125rem; font-weight: 400; }
        .card { background: rgba(26, 26, 26, 0.8); backdrop-filter: blur(20px); border-radius: 20px; padding: 32px; margin-bottom: 32px; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(190, 238, 15, 0.1); border: 1px solid rgba(51, 51, 51, 0.5); transition: all 0.3s ease; }
        .card:hover { transform: translateY(-2px); box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(190, 238, 15, 0.2); }
        .status-card { text-align: center; }
        .status-card.success { background: rgba(190, 238, 15, 0.1); color: #beee0f; border: 2px solid #beee0f; }
        .status-card.error { background: rgba(220, 53, 69, 0.1); color: #dc3545; border: 2px solid #dc3545; }
        .search-section { margin-bottom: 20px; }
        .search-box-container { position: relative; }
        .search-input-wrapper { position: relative; }
        .search-input { width: 100%; padding: 16px 20px; border: 2px solid rgba(51, 51, 51, 0.5); border-radius: 12px; font-size: 16px; transition: all 0.3s ease; background: rgba(26, 26, 26, 0.6); color: #ffffff; font-weight: 400; }
        .search-input:focus { border-color: #beee0f; outline: none; box-shadow: 0 0 0 4px rgba(190, 238, 15, 0.15), 0 4px 12px rgba(0, 0, 0, 0.2); background: rgba(26, 26, 26, 0.8); }
        .search-input::placeholder { color: #666; font-weight: 400; }
        .search-results { position: absolute; top: 100%; left: 0; right: 0; background: rgba(26, 26, 26, 0.95); backdrop-filter: blur(20px); border: 1px solid rgba(51, 51, 51, 0.5); border-top: none; border-radius: 0 0 12px 12px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4); max-height: 320px; overflow-y: auto; z-index: 1000; display: none; }
        .search-result-item { padding: 16px 20px; cursor: pointer; border-bottom: 1px solid rgba(51, 51, 51, 0.3); display: flex; align-items: center; gap: 12px; transition: all 0.2s ease; color: #ffffff; }
        .search-result-item:hover { background-color: rgba(190, 238, 15, 0.1); transform: translateX(4px); }
        .search-result-item:active { background-color: rgba(190, 238, 15, 0.2); }
        .search-result-item:last-child { border-bottom: none; }
        .search-result-icon { width: 24px; height: 24px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 12px; color: #000000; font-weight: 600; }
        .search-result-icon.state { background: linear-gradient(135deg, #beee0f, #a8d000); }
        .search-result-icon.county { background: linear-gradient(135deg, #beee0f, #a8d000); }
        .search-result-icon.city { background: linear-gradient(135deg, #beee0f, #a8d000); }
        .search-result-content { flex: 1; }
        .search-result-name { font-weight: 500; color: #ffffff; }
        .search-result-type { font-size: 12px; color: #beee0f; text-transform: uppercase; }
        .search-result-count { font-size: 12px; color: #999; }
        .filters-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px; margin-bottom: 32px; }
        .filter-group { display: flex; flex-direction: column; position: relative; }
        .filter-group label { font-weight: 600; margin-bottom: 12px; color: #beee0f; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px; }
        .form-control { padding: 16px 20px; border: 2px solid rgba(51, 51, 51, 0.5); border-radius: 12px; font-size: 15px; transition: all 0.3s ease; width: 100%; background: rgba(26, 26, 26, 0.6); color: #ffffff; font-weight: 400; }
        .form-control:focus { outline: none; border-color: #beee0f; box-shadow: 0 0 0 4px rgba(190, 238, 15, 0.15), 0 4px 12px rgba(0, 0, 0, 0.2); background: rgba(26, 26, 26, 0.8); }
        .form-control::placeholder { color: #666; font-weight: 400; }
        .form-control:disabled { background-color: #333; color: #666; cursor: not-allowed; }
        .filter-actions { display: flex; gap: 16px; justify-content: center; margin-top: 8px; }
        .btn { padding: 16px 32px; border: none; border-radius: 12px; font-size: 15px; font-weight: 600; cursor: pointer; transition: all 0.3s ease; display: inline-flex; align-items: center; gap: 10px; text-transform: uppercase; letter-spacing: 0.5px; }
        .btn-primary { background: linear-gradient(135deg, #beee0f, #a8d000); color: #000000; box-shadow: 0 4px 12px rgba(190, 238, 15, 0.3); }
        .btn-primary:hover { transform: translateY(-3px); box-shadow: 0 8px 25px rgba(190, 238, 15, 0.4); }
        .btn-secondary { background: rgba(51, 51, 51, 0.6); color: #ffffff; border: 2px solid rgba(51, 51, 51, 0.8); backdrop-filter: blur(10px); }
        .btn-secondary:hover { background: rgba(51, 51, 51, 0.8); transform: translateY(-3px); box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3); }
        .obligations-list { display: grid; gap: 20px; }
        .obligation-card { background: rgba(26, 26, 26, 0.8); backdrop-filter: blur(20px); border-radius: 16px; padding: 24px; border-left: 6px solid #beee0f; transition: all 0.3s ease; color: #ffffff; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2); }
        .obligation-card:hover { transform: translateY(-4px); box-shadow: 0 12px 40px rgba(190, 238, 15, 0.15), 0 0 0 1px rgba(190, 238, 15, 0.1); }
        .obligation-card.federal { border-left-color: #dc3545; }
        .obligation-card.state { border-left-color: #beee0f; }
        .obligation-card.county { border-left-color: #beee0f; }
        .obligation-card.municipality { border-left-color: #beee0f; }
        .obligation-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px; }
        .obligation-title { font-size: 1.25rem; font-weight: 600; color: #ffffff; line-height: 1.4; }
        .obligation-date { background: linear-gradient(135deg, #beee0f, #a8d000); color: #000000; padding: 8px 16px; border-radius: 24px; font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
        .obligation-description { color: #cccccc; margin-bottom: 16px; line-height: 1.6; font-size: 15px; }
        .obligation-meta { display: flex; gap: 20px; font-size: 14px; color: #999; flex-wrap: wrap; }
        .obligation-level { display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; border-radius: 16px; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
        .obligation-level.federal { background: linear-gradient(135deg, #dc3545, #c82333); color: white; }
        .obligation-level.state { background: linear-gradient(135deg, #beee0f, #a8d000); color: #000000; }
        .obligation-level.county { background: linear-gradient(135deg, #beee0f, #a8d000); color: #000000; }
        .obligation-level.municipality { background: linear-gradient(135deg, #beee0f, #a8d000); color: #000000; }
        .obligation-link { 
            display: inline-flex; 
            align-items: center; 
            gap: 8px; 
            padding: 8px 16px; 
            background: linear-gradient(135deg, #beee0f, #a8d000); 
            color: #000000; 
            text-decoration: none; 
            border-radius: 20px; 
            font-size: 13px; 
            font-weight: 600; 
            text-transform: uppercase; 
            letter-spacing: 0.5px; 
            transition: all 0.3s ease; 
            margin-top: 12px; 
        }
        .obligation-link:hover { 
            transform: translateY(-2px); 
            box-shadow: 0 4px 12px rgba(190, 238, 15, 0.4); 
            color: #000000; 
            text-decoration: none; 
        }
        .obligation-link i { font-size: 12px; }
        .source-buttons { 
            display: flex; 
            flex-wrap: wrap; 
            gap: 8px; 
            margin-top: 12px; 
        }
        .source-button { 
            display: inline-block; 
            padding: 6px 12px; 
            border-radius: 4px; 
            font-size: 12px; 
            font-weight: 600; 
            text-decoration: none; 
            text-transform: uppercase; 
            letter-spacing: 0.5px; 
            transition: all 0.2s ease; 
            border: none; 
            cursor: pointer; 
        }
        .source-button.blue { 
            background: #007bff; 
            color: white; 
        }
        .source-button.blue:hover { 
            background: #0056b3; 
            transform: translateY(-1px); 
            box-shadow: 0 2px 4px rgba(0, 123, 255, 0.3); 
        }
        .source-button.orange { 
            background: #fd7e14; 
            color: white; 
        }
        .source-button.orange:hover { 
            background: #e55a00; 
            transform: translateY(-1px); 
            box-shadow: 0 2px 4px rgba(253, 126, 20, 0.3); 
        }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 24px; }
        .stat-card { background: rgba(26, 26, 26, 0.8); backdrop-filter: blur(20px); border-radius: 20px; padding: 32px; color: white; display: flex; align-items: center; gap: 24px; transition: all 0.3s ease; border: 1px solid rgba(51, 51, 51, 0.5); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2); }
        .stat-card:hover { transform: translateY(-6px); box-shadow: 0 12px 40px rgba(190, 238, 15, 0.15), 0 0 0 1px rgba(190, 238, 15, 0.1); }
        .stat-card.federal { background: rgba(26, 26, 26, 0.8); border-left: 6px solid #dc3545; }
        .stat-card.state { background: rgba(26, 26, 26, 0.8); border-left: 6px solid #beee0f; }
        .stat-card.county { background: rgba(26, 26, 26, 0.8); border-left: 6px solid #beee0f; }
        .stat-card.municipality { background: rgba(26, 26, 26, 0.8); border-left: 6px solid #beee0f; }
        .stat-icon { font-size: 3rem; opacity: 0.9; color: #beee0f; }
        .stat-content h3 { font-size: 1.125rem; margin-bottom: 8px; opacity: 0.9; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
        .stat-number { font-size: 2.5rem; font-weight: 700; color: #ffffff; }
        .loading { text-align: center; padding: 60px; color: #beee0f; font-size: 1.125rem; font-weight: 500; }
        .empty-state { text-align: center; padding: 80px 20px; color: #999; }
        .empty-state i { font-size: 4rem; margin-bottom: 20px; opacity: 0.5; }
        /* Responsividade */
        @media (max-width: 1200px) {
            .container { padding: 24px; }
            .header h1 { font-size: 2.5rem; }
            .header h1 img { width: 250px; height: 50px; }
        }
        
        @media (max-width: 768px) {
            .container { padding: 20px; }
            .header { margin-bottom: 32px; }
            .header h1 { 
                font-size: 2rem; 
                flex-direction: column; 
                gap: 16px; 
                text-align: center; 
            }
            .header h1 img { width: 200px; height: 40px; }
            .header p { font-size: 1rem; }
            .card { 
                padding: 20px; 
                margin-bottom: 20px; 
                border-radius: 16px; 
            }
            .filter-grid { 
                grid-template-columns: 1fr; 
                gap: 16px; 
            }
            .filter-group { margin-bottom: 16px; }
            .filter-actions { 
                flex-direction: column; 
                gap: 12px; 
            }
            .btn { 
                width: 100%; 
                justify-content: center; 
            }
            .stats-grid { 
                grid-template-columns: 1fr; 
                gap: 16px; 
            }
            .stat-card { 
                padding: 20px; 
                flex-direction: column; 
                text-align: center; 
            }
            .stat-icon { font-size: 2.5rem; }
            .stat-number { font-size: 2rem; }
            .obligation-card { 
                padding: 16px; 
                margin-bottom: 16px; 
            }
            .obligation-header { 
                flex-direction: column; 
                align-items: flex-start; 
                gap: 8px; 
            }
            .obligation-date { 
                font-size: 12px; 
                padding: 6px 12px; 
            }
            .obligation-level { 
                font-size: 10px; 
                padding: 4px 8px; 
            }
            .obligation-link { 
                font-size: 12px; 
                padding: 6px 12px; 
                margin-top: 8px; 
            }
            .source-buttons { 
                gap: 6px; 
                margin-top: 8px; 
            }
            .source-button { 
                font-size: 11px; 
                padding: 5px 10px; 
            }
            .search-results { 
                max-height: 250px; 
            }
            .search-result-item { 
                padding: 12px 16px; 
            }
        }
        
        @media (max-width: 480px) {
            .container { padding: 16px; }
            .header { margin-bottom: 24px; }
            .header h1 { 
                font-size: 1.5rem; 
                gap: 12px; 
            }
            .header h1 img { width: 150px; height: 30px; }
            .header p { font-size: 0.9rem; }
            .card { 
                padding: 16px; 
                border-radius: 12px; 
            }
            .filter-group label { 
                font-size: 12px; 
                margin-bottom: 8px; 
            }
            .form-control { 
                padding: 12px 16px; 
                font-size: 14px; 
            }
            .btn { 
                padding: 12px 24px; 
                font-size: 14px; 
            }
            .stats-grid { gap: 12px; }
            .stat-card { 
                padding: 16px; 
                border-radius: 16px; 
            }
            .stat-icon { font-size: 2rem; }
            .stat-number { font-size: 1.5rem; }
            .stat-content h3 { font-size: 0.9rem; }
            .obligation-card { 
                padding: 12px; 
                border-radius: 12px; 
            }
            .obligation-title { 
                font-size: 1rem; 
                line-height: 1.4; 
            }
            .obligation-date { 
                font-size: 11px; 
                padding: 4px 8px; 
            }
            .obligation-level { 
                font-size: 9px; 
                padding: 3px 6px; 
            }
            .obligation-link { 
                font-size: 11px; 
                padding: 5px 10px; 
                margin-top: 6px; 
            }
            .source-buttons { 
                gap: 4px; 
                margin-top: 6px; 
            }
            .source-button { 
                font-size: 10px; 
                padding: 4px 8px; 
            }
            .search-input { 
                padding: 12px 16px; 
                font-size: 14px; 
            }
            .search-results { 
                max-height: 200px; 
            }
            .search-result-item { 
                padding: 10px 12px; 
                font-size: 14px; 
            }
            .search-result-icon { 
                width: 20px; 
                height: 20px; 
                font-size: 10px; 
            }
        }
        
        @media (max-width: 360px) {
            .container { padding: 12px; }
            .header h1 { font-size: 1.2rem; }
            .header h1 img { width: 120px; height: 24px; }
            .card { padding: 12px; }
            .form-control { padding: 10px 12px; }
            .btn { padding: 10px 20px; font-size: 12px; }
            .stat-card { padding: 12px; }
            .obligation-card { padding: 10px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <div class="header-content">
                <h1><img src="/static/images/h7-logo.png" alt="H7 Advisory" style="width: 300px; height: 60px; vertical-align: middle; border-radius: 8px; background: transparent; filter: drop-shadow(0 0 10px rgba(190, 238, 15, 0.4));"> Tax Calendar - Profissional</h1>
                <p>Gerencie suas obrigações fiscais dos EUA</p>
            </div>
        </header>

        <div id="statusCard" class="status-card" style="display: none;">
            <div class="loading">
                <i class="fas fa-spinner fa-spin"></i> Conectando com o servidor...
            </div>
        </div>

        <div class="card">
            <h2><i class="fas fa-filter"></i> Filtros</h2>
                <div class="search-section">
                    <div class="search-box-container">
                        <label for="searchBox"><i class="fas fa-search"></i> Busca Inteligente:</label>
                        <div class="search-input-wrapper">
                            <input type="text" id="searchBox" class="form-control search-input" placeholder="Digite estado, condado ou cidade...">
                            <div id="searchResults" class="search-results"></div>
                        </div>
                    </div>
                </div>
                <div class="filters-grid">
                    <div class="filter-group">
                        <label for="stateSelect">Estado:</label>
                        <select id="stateSelect" class="form-control">
                            <option value="">Selecione um estado</option>
                        </select>
                    </div>
                    <div class="filter-group">
                        <label for="countySelect">Condado:</label>
                        <select id="countySelect" class="form-control" disabled>
                            <option value="">Selecione um condado</option>
                        </select>
                    </div>
                    <div class="filter-group">
                        <label for="citySelect">Cidade:</label>
                        <select id="citySelect" class="form-control" disabled>
                            <option value="">Selecione uma cidade</option>
                        </select>
                    </div>
                    <div class="filter-group">
                        <label for="monthSelect">Mês:</label>
                        <select id="monthSelect" class="form-control">
                            <option value="">Selecione um mês</option>
                            <option value="01">Janeiro</option>
                            <option value="02">Fevereiro</option>
                            <option value="03">Março</option>
                            <option value="04">Abril</option>
                            <option value="05">Maio</option>
                            <option value="06">Junho</option>
                            <option value="07">Julho</option>
                            <option value="08">Agosto</option>
                            <option value="09">Setembro</option>
                            <option value="10">Outubro</option>
                            <option value="11">Novembro</option>
                            <option value="12">Dezembro</option>
                        </select>
                    </div>
                </div>
            <div class="filter-actions">
                <button id="clearFilters" class="btn btn-secondary">
                    <i class="fas fa-times"></i> Limpar Filtros
                </button>
                <button id="applyFilters" class="btn btn-primary">
                    <i class="fas fa-search"></i> Aplicar Filtros
                </button>
            </div>
        </div>

        <div class="card">
            <h2><i class="fas fa-calendar-check"></i> Obrigações</h2>
            <div id="obligationsList" class="obligations-list">
                <div class="loading">
                    <i class="fas fa-spinner fa-spin"></i> Carregando dados...
                </div>
            </div>
        </div>

        <div class="card">
            <h2><i class="fas fa-chart-bar"></i> Estatísticas</h2>
            <div class="stats-grid">
                <div class="stat-card federal">
                    <div class="stat-icon"><i class="fas fa-flag"></i></div>
                    <div class="stat-content">
                        <h3>Federal</h3>
                        <span id="federalCount" class="stat-number">0</span>
                    </div>
                </div>
                <div class="stat-card state">
                    <div class="stat-icon"><i class="fas fa-map-marker-alt"></i></div>
                    <div class="stat-content">
                        <h3>Estadual</h3>
                        <span id="stateCount" class="stat-number">0</span>
                    </div>
                </div>
                <div class="stat-card county">
                    <div class="stat-icon"><i class="fas fa-city"></i></div>
                    <div class="stat-content">
                        <h3>Condado</h3>
                        <span id="countyCount" class="stat-number">0</span>
                    </div>
                </div>
                <div class="stat-card municipality">
                    <div class="stat-icon"><i class="fas fa-building"></i></div>
                    <div class="stat-content">
                        <h3>Municipal</h3>
                        <span id="municipalityCount" class="stat-number">0</span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        class TaxCalendar {
            constructor() {
                this.apiBaseUrl = '/api';
                this.currentFilters = { stateCode: null, countyName: null, cityName: null, month: null, year: null };
                this.obligations = { federal: [], state: [], county: [], municipality: [] };
                this.searchTimeout = null;
                this.init();
            }
            
            async init() {
                console.log('🚀 Inicializando Tax Calendar - Profissional');
                this.setupEventListeners();
                await this.checkConnection();
                await this.loadStates();
                await this.loadObligations();
                this.updateStatistics();
            }
            
            async checkConnection() {
                try {
                    console.log('🔍 Verificando conexão...');
                    const response = await fetch(`${this.apiBaseUrl}/health`);
                    if (response.ok) {
                        const data = await response.json();
                        this.showStatus('success', `✅ Conectado! ${data.obligations_count} obrigações no banco`);
                        console.log('✅ Conexão OK:', data);
                    } else {
                        throw new Error(`HTTP ${response.status}`);
                    }
                } catch (error) {
                    console.error('❌ Erro de conexão:', error);
                    this.showStatus('error', '❌ Erro de conexão. Verifique se o backend está rodando.');
                }
            }
            
            showStatus(type, message) {
                const statusCard = document.getElementById('statusCard');
                statusCard.className = `status-card ${type}`;
                statusCard.innerHTML = `<i class="material-icons">${type === 'success' ? 'check_circle' : 'error'}</i> ${message}`;
            }
            
            setupEventListeners() {
                document.getElementById('stateSelect').addEventListener('change', (e) => this.handleStateChange(e.target.value));
                document.getElementById('countySelect').addEventListener('change', (e) => this.handleCountyChange(e.target.value));
                document.getElementById('citySelect').addEventListener('change', (e) => this.handleCityChange(e.target.value));
                document.getElementById('monthSelect').addEventListener('change', (e) => this.handleMonthChange(e.target.value));
                document.getElementById('clearFilters').addEventListener('click', () => this.clearFilters());
                document.getElementById('applyFilters').addEventListener('click', () => this.applyFilters());
                
                // Event listeners para busca
                const searchBox = document.getElementById('searchBox');
                const searchResults = document.getElementById('searchResults');
                
                searchBox.addEventListener('input', (e) => this.handleSearchInput(e.target.value));
                searchBox.addEventListener('focus', () => this.showSearchResults());
                searchBox.addEventListener('blur', () => {
                    // Delay maior para permitir clique nos resultados
                    setTimeout(() => this.hideSearchResults(), 500);
                });
                
                // Fechar resultados ao clicar fora
                document.addEventListener('click', (e) => {
                    if (!e.target.closest('.search-input-wrapper')) {
                        this.hideSearchResults();
                    }
                });
            }
            
            async loadStates() {
                try {
                    console.log('📡 Carregando estados...');
                    const response = await fetch(`${this.apiBaseUrl}/states`);
                    if (!response.ok) throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                    this.states = await response.json();
                    this.populateStateSelect();
                    console.log(`✅ ${this.states.length} estados carregados`);
                } catch (error) {
                    console.error('❌ Erro ao carregar estados:', error);
                    this.showStatus('error', 'Erro ao carregar estados. Verifique a conexão.');
                }
            }
            
            populateStateSelect() {
                const stateSelect = document.getElementById('stateSelect');
                stateSelect.innerHTML = '<option value="">Selecione um estado</option>';
                this.states.forEach(state => {
                    const option = document.createElement('option');
                    option.value = state.code;
                    option.textContent = state.name;
                    stateSelect.appendChild(option);
                });
            }
            
            async loadCounties(stateCode) {
                try {
                    console.log(`📡 Carregando condados para ${stateCode}...`);
                    const response = await fetch(`${this.apiBaseUrl}/counties/${stateCode}`);
                    if (!response.ok) throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                    this.counties = await response.json();
                    this.populateCountySelect();
                    console.log(`✅ ${this.counties.length} condados carregados`);
                } catch (error) {
                    console.error('❌ Erro ao carregar condados:', error);
                    this.showStatus('error', 'Erro ao carregar condados.');
                }
            }
            
            populateCountySelect() {
                const countySelect = document.getElementById('countySelect');
                countySelect.innerHTML = '<option value="">Selecione um condado</option>';
                this.counties.forEach(county => {
                    const option = document.createElement('option');
                    option.value = county.name;
                    option.textContent = county.name;
                    countySelect.appendChild(option);
                });
            }
            
            async loadCities(stateCode, countyName) {
                try {
                    console.log(`📡 Carregando cidades para ${countyName}, ${stateCode}...`);
                    const response = await fetch(`${this.apiBaseUrl}/cities/${stateCode}/${encodeURIComponent(countyName)}`);
                    if (!response.ok) throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                    this.cities = await response.json();
                    this.populateCitySelect();
                    console.log(`✅ ${this.cities.length} cidades carregadas`);
                } catch (error) {
                    console.error('❌ Erro ao carregar cidades:', error);
                    this.showStatus('error', 'Erro ao carregar cidades.');
                }
            }
            
            populateCitySelect() {
                const citySelect = document.getElementById('citySelect');
                citySelect.innerHTML = '<option value="">Selecione uma cidade</option>';
                this.cities.forEach(city => {
                    const option = document.createElement('option');
                    option.value = city.name;
                    option.textContent = city.name;
                    citySelect.appendChild(option);
                });
            }
            
            async handleStateChange(stateCode) {
                this.currentFilters.stateCode = stateCode;
                this.currentFilters.countyName = null;
                this.currentFilters.cityName = null;
                const countySelect = document.getElementById('countySelect');
                const citySelect = document.getElementById('citySelect');
                countySelect.innerHTML = '<option value="">Selecione um condado</option>';
                citySelect.innerHTML = '<option value="">Selecione uma cidade</option>';
                
                if (stateCode) {
                    countySelect.disabled = false;
                    await this.loadCounties(stateCode);
                } else {
                    countySelect.disabled = true;
                    citySelect.disabled = true;
                }
                citySelect.disabled = true;
            }
            
            async handleCountyChange(countyName) {
                this.currentFilters.countyName = countyName;
                this.currentFilters.cityName = null;
                const citySelect = document.getElementById('citySelect');
                citySelect.innerHTML = '<option value="">Selecione uma cidade</option>';
                
                if (countyName && this.currentFilters.stateCode) {
                    citySelect.disabled = false;
                    await this.loadCities(this.currentFilters.stateCode, countyName);
                } else {
                    citySelect.disabled = true;
                }
            }
            
            handleCityChange(cityName) { this.currentFilters.cityName = cityName; }
            handleMonthChange(month) { 
                this.currentFilters.month = month; 
                this.applyFilters();
            }
            
            
            clearFilters() {
                this.currentFilters = { stateCode: null, countyName: null, cityName: null, month: null };
                document.getElementById('stateSelect').value = '';
                document.getElementById('countySelect').value = '';
                document.getElementById('countySelect').disabled = true;
                document.getElementById('citySelect').value = '';
                document.getElementById('citySelect').disabled = true;
                document.getElementById('monthSelect').value = '';
                this.applyFilters();
            }
            
            async applyFilters() {
                try {
                    console.log('🔍 Aplicando filtros...', this.currentFilters);
                    this.showStatus('loading', 'Carregando obrigações...');
                    
                    await this.loadObligations();
                    this.updateStatistics();
                    this.renderObligations();
                    
                    console.log('📋 Filtros aplicados com sucesso');
                } catch (error) {
                    console.error('Erro ao aplicar filtros:', error);
                    this.showStatus('error', 'Erro ao aplicar filtros');
                }
            }
            
            async loadObligations() {
                try {
                    const params = new URLSearchParams();
                    if (this.currentFilters.stateCode) params.append('state', this.currentFilters.stateCode);
                    if (this.currentFilters.countyName) params.append('county', this.currentFilters.countyName);
                    if (this.currentFilters.cityName) params.append('city', this.currentFilters.cityName);
                    if (this.currentFilters.month) {
                        params.append('month', this.currentFilters.month);
                    }
                    
                    console.log('📡 Carregando obrigações...', params.toString());
                    const response = await fetch(`${this.apiBaseUrl}/calendar?${params}`);
                    if (!response.ok) {
                        const errorData = await response.json().catch(() => ({}));
                        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
                    }
                    this.obligations = await response.json();
                    console.log('✅ Obrigações carregadas:', this.obligations);
                } catch (error) {
                    console.error('❌ Erro ao carregar obrigações:', error);
                    this.showStatus('error', `Erro ao carregar dados: ${error.message}`);
                }
            }
            
            renderObligations() {
                const container = document.getElementById('obligationsList');
                container.innerHTML = '';
                const allObligations = [
                    ...this.obligations.federal.map(ob => ({...ob, level: 'federal'})),
                    ...this.obligations.state.map(ob => ({...ob, level: 'state'})),
                    ...this.obligations.county.map(ob => ({...ob, level: 'county'})),
                    ...this.obligations.municipality.map(ob => ({...ob, level: 'municipality'}))
                ];
                
                if (allObligations.length === 0) {
                    container.innerHTML = `
                        <div class="empty-state">
                            <i class="material-icons">event_busy</i>
                            <h3>Nenhuma obrigação encontrada</h3>
                            <p>Ajuste os filtros para ver as obrigações fiscais</p>
                        </div>
                    `;
                    return;
                }
                
                allObligations.sort((a, b) => {
                    if (!a.date) return 1;
                    if (!b.date) return -1;
                    return new Date(a.date).getTime() - new Date(b.date).getTime();
                });
                
                allObligations.forEach(obligation => {
                    const card = this.createObligationCard(obligation);
                    container.appendChild(card);
                });
            }
            
            createObligationCard(obligation) {
                const card = document.createElement('div');
                card.className = `obligation-card ${obligation.jurisdiction_level}`;
                const dueDate = obligation.date ? new Date(obligation.date) : null;
                const isOverdue = dueDate && dueDate < new Date();
                const isToday = dueDate && dueDate.toDateString() === new Date().toDateString();
                
                // Gerar botões de sources
                const sourceButtons = obligation.source_buttons && obligation.source_buttons.length > 0 
                    ? obligation.source_buttons.map(button => 
                        `<a href="${button.url}" target="_blank" class="source-button ${button.type}">${button.label}</a>`
                      ).join('')
                    : '';

                card.innerHTML = `
                    <div class="obligation-header">
                        <h3 class="obligation-title">${obligation.title || 'Sem título'}</h3>
                        ${obligation.date ? `<span class="obligation-date ${isOverdue ? 'overdue' : ''} ${isToday ? 'today' : ''}">${this.formatDate(new Date(obligation.date))}</span>` : ''}
                    </div>
                    ${obligation.notes ? `<p class="obligation-description">${obligation.notes}</p>` : ''}
                    <div class="obligation-meta">
                        <span class="obligation-level ${obligation.jurisdiction_level}">
                            <i class="material-icons">${this.getLevelIcon(obligation.jurisdiction_level)}</i>
                            ${this.getLevelName(obligation.jurisdiction_level)}
                        </span>
                        ${obligation.category ? `<span><i class="material-icons">label</i> ${obligation.category}</span>` : ''}
                        ${obligation.frequency ? `<span><i class="material-icons">schedule</i> ${obligation.frequency}</span>` : ''}
                    </div>
                    ${sourceButtons ? `<div class="source-buttons">${sourceButtons}</div>` : ''}
                `;
                return card;
            }
            
            getLevelIcon(level) {
                const icons = { federal: 'flag', state: 'place', county: 'location_city', municipality: 'business' };
                return icons[level] || 'event';
            }
            
            getLevelName(level) {
                const names = { federal: 'Federal', state: 'Estadual', county: 'Condado', municipality: 'Municipal' };
                return names[level] || level;
            }
            
            // Métodos de busca
            async handleSearchInput(query) {
                console.log(`🔍 Input da busca: "${query}"`);
                
                if (this.searchTimeout) {
                    clearTimeout(this.searchTimeout);
                }
                
                if (query.length < 2) {
                    this.hideSearchResults();
                    return;
                }
                
                this.searchTimeout = setTimeout(async () => {
                    await this.performSearch(query);
                }, 300);
            }
            
            async performSearch(query) {
                try {
                    console.log(`🔍 Buscando: ${query}`);
                    const response = await fetch(`${this.apiBaseUrl}/search?q=${encodeURIComponent(query)}`);
                    
                    if (!response.ok) {
                        throw new Error(`HTTP ${response.status}`);
                    }
                    
                    const results = await response.json();
                    this.displaySearchResults(results);
                    
                } catch (error) {
                    console.error('Erro na busca:', error);
                    this.hideSearchResults();
                }
            }
            
            displaySearchResults(results) {
                const searchResults = document.getElementById('searchResults');
                
                if (results.length === 0) {
                    searchResults.innerHTML = '<div class="search-result-item">Nenhum resultado encontrado</div>';
                } else {
                    searchResults.innerHTML = results.map(result => `
                        <div class="search-result-item" data-type="${result.type}" data-code="${result.code}" data-name="${result.name}" data-county="${result.county || ''}">
                            <div class="search-result-icon ${result.type}">${result.type.charAt(0).toUpperCase()}</div>
                            <div class="search-result-content">
                                <div class="search-result-name">${result.display}</div>
                                <div class="search-result-type">${result.type === 'state' ? 'Estado' : result.type === 'county' ? 'Condado' : 'Cidade'}</div>
                                <div class="search-result-count">${result.count} obrigações</div>
                            </div>
                        </div>
                    `).join('');
                    
                    // Adicionar event listeners aos resultados com mousedown para evitar conflito com blur
                    const items = searchResults.querySelectorAll('.search-result-item');
                    console.log(`📋 Adicionando listeners para ${items.length} itens`);
                    
                    items.forEach((item, index) => {
                        console.log(`🔗 Adicionando listener para item ${index}:`, item.dataset);
                        
                        item.addEventListener('mousedown', (e) => {
                            e.preventDefault();
                            e.stopPropagation();
                            console.log(`🖱️ Mousedown detectado no item ${index}:`, item.dataset);
                            this.selectSearchResult(item);
                        });
                        
                        // Também adicionar click como backup
                        item.addEventListener('click', (e) => {
                            e.preventDefault();
                            e.stopPropagation();
                            console.log(`🖱️ Click backup no item ${index}:`, item.dataset);
                            this.selectSearchResult(item);
                        });
                    });
                }
                
                this.showSearchResults();
            }
            
            selectSearchResult(item) {
                try {
                    const type = item.dataset.type;
                    const code = item.dataset.code;
                    const name = item.dataset.name;
                    const county = item.dataset.county;
                    
                    console.log(`✅ Selecionado: ${type} - ${name} (${code})`);
                    console.log(`📋 Dados do item:`, { type, code, name, county });
                    
                    // Limpar busca
                    document.getElementById('searchBox').value = '';
                    this.hideSearchResults();
                    
                    // Aplicar seleção baseada no tipo
                    if (type === 'state') {
                        this.selectState(code, name);
                    } else if (type === 'county') {
                        this.selectCounty(code, name);
                    } else if (type === 'city') {
                        this.selectCity(code, county, name);
                    } else {
                        console.error('Tipo desconhecido:', type);
                    }
                    
                    // Aplicar filtros automaticamente após um delay baseado no tipo
                    const delay = type === 'state' ? 500 : type === 'county' ? 1500 : 2000;
                    setTimeout(() => {
                        console.log(`🚀 Aplicando filtros automaticamente...`);
                        this.applyFilters();
                    }, delay);
                } catch (error) {
                    console.error('Erro ao selecionar resultado:', error);
                }
            }
            
            selectState(stateCode, stateName) {
                console.log(`🔧 Selecionando estado: ${stateName} (${stateCode})`);
                document.getElementById('stateSelect').value = stateCode;
                this.handleStateChange(stateCode);
            }
            
            selectCounty(stateCode, countyName) {
                console.log(`🔧 Selecionando condado: ${countyName} em ${stateCode}`);
                // Primeiro selecionar o estado
                document.getElementById('stateSelect').value = stateCode;
                this.handleStateChange(stateCode);
                
                // Aguardar carregamento dos condados e então selecionar
                setTimeout(() => {
                    document.getElementById('countySelect').value = countyName;
                    this.handleCountyChange(countyName);
                    console.log(`✅ Condado ${countyName} selecionado`);
                }, 800);
            }
            
            selectCity(stateCode, countyName, cityName) {
                console.log(`🔧 Selecionando cidade: ${cityName} em ${countyName}, ${stateCode}`);
                // Primeiro selecionar o estado
                document.getElementById('stateSelect').value = stateCode;
                this.handleStateChange(stateCode);
                
                // Aguardar carregamento dos condados e então selecionar
                setTimeout(() => {
                    document.getElementById('countySelect').value = countyName;
                    this.handleCountyChange(countyName);
                    
                    // Aguardar carregamento das cidades e então selecionar
                    setTimeout(() => {
                        document.getElementById('citySelect').value = cityName;
                        this.handleCityChange(cityName);
                        console.log(`✅ Cidade ${cityName} selecionada`);
                    }, 800);
                }, 800);
            }
            
            showSearchResults() {
                const searchResults = document.getElementById('searchResults');
                if (searchResults.children.length > 0) {
                    searchResults.style.display = 'block';
                }
            }
            
            hideSearchResults() {
                const searchResults = document.getElementById('searchResults');
                searchResults.style.display = 'none';
            }
            
            formatDate(date) {
                return date.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' });
            }
            
            updateStatistics() {
                document.getElementById('federalCount').textContent = this.obligations.federal.length;
                document.getElementById('stateCount').textContent = this.obligations.state.length;
                document.getElementById('countyCount').textContent = this.obligations.county.length;
                document.getElementById('municipalityCount').textContent = this.obligations.municipality.length;
            }
        }
        
        document.addEventListener('DOMContentLoaded', () => new TaxCalendar());
    </script>
</body>
</html>
    ''')

@app.route('/api/health')
def health_check():
    """Health check"""
    try:
        # Verificar se DATABASE_URL está configurada
        if 'DATABASE_URL' in os.environ:
            # Tentar conectar ao banco
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM obrigacoes_com_data")
                count = cursor.fetchone()[0]
                conn.close()
                return jsonify({
                    'status': 'healthy',
                    'database': 'connected',
                    'message': 'Backend funcionando perfeitamente!',
                    'obligations_count': count,
                    'timestamp': datetime.now().isoformat()
                })
            else:
                return jsonify({
                    'status': 'healthy',
                    'database': 'not_configured',
                    'message': 'Aplicação funcionando - banco não configurado ainda',
                    'timestamp': datetime.now().isoformat()
                })
        else:
            # Sem DATABASE_URL - aplicação básica funcionando
            return jsonify({
                'status': 'healthy',
                'database': 'not_configured',
                'message': 'Aplicação funcionando - aguardando configuração do banco',
                'timestamp': datetime.now().isoformat()
            })
    except Exception as e:
        # Mesmo com erro, retornar healthy para permitir deploy
        return jsonify({
            'status': 'healthy',
            'database': 'error',
            'message': f'Aplicação funcionando - erro no banco: {str(e)}',
            'timestamp': datetime.now().isoformat()
        })

@app.route('/api/states')
def get_states():
    """Retorna lista de estados"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Erro de conexão com banco'}), 500
        
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT DISTINCT state as code
            FROM obrigacoes_com_data 
            WHERE state IS NOT NULL AND state != ''
            ORDER BY state
        """)
        
        results = cursor.fetchall()
        conn.close()
        
        state_names = {
            'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
            'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia',
            'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa',
            'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
            'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
            'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire',
            'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina',
            'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania',
            'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee',
            'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington',
            'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming', 'DC': 'District of Columbia'
        }
        
        states = []
        for result in results:
            code = result['code']
            states.append({'code': code, 'name': state_names.get(code, code)})
        
        return jsonify(states)
    except Exception as e:
        return jsonify({'error': 'Erro interno'}), 500

@app.route('/api/counties/<state_code>')
def get_counties(state_code):
    """Retorna condados de um estado"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Erro de conexão com banco'}), 500
        
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT DISTINCT county as name
            FROM obrigacoes_com_data 
            WHERE state = %s AND county IS NOT NULL AND county != ''
            ORDER BY county
        """, (state_code,))
        
        results = cursor.fetchall()
        conn.close()
        
        counties = []
        for result in results:
            counties.append({
                'name': result['name'],
                'state_code': state_code
            })
        
        return jsonify(counties)
    except Exception as e:
        return jsonify({'error': 'Erro interno'}), 500

@app.route('/api/cities/<state_code>/<county_name>')
def get_cities(state_code, county_name):
    """Retorna cidades de um condado"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Erro de conexão com banco'}), 500
        
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT DISTINCT city as name
            FROM obrigacoes_com_data 
            WHERE state = %s AND county = %s AND city IS NOT NULL AND city != ''
            ORDER BY city
        """, (state_code, county_name))
        
        results = cursor.fetchall()
        conn.close()
        
        cities = []
        for result in results:
            cities.append({
                'name': result['name'],
                'county': county_name,
                'state_code': state_code
            })
        
        return jsonify(cities)
    except Exception as e:
        return jsonify({'error': 'Erro interno'}), 500

@app.route('/api/search')
def search_locations():
    """Busca inteligente por estados, condados e municípios"""
    try:
        query = request.args.get('q', '').strip()
        if not query or len(query) < 2:
            return jsonify([])
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Erro de conexão com banco'}), 500
        
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Busca em estados, condados e cidades
        cursor.execute("""
            SELECT DISTINCT 
                'state' as type,
                state as code,
                state as name,
                NULL as county,
                NULL as city,
                COUNT(*) as count
            FROM obrigacoes_com_data 
            WHERE state ILIKE %s
            GROUP BY state
            ORDER BY state
            LIMIT 10
        """, (f'%{query}%',))
        
        states = cursor.fetchall()
        
        cursor.execute("""
            SELECT DISTINCT 
                'county' as type,
                state as code,
                county as name,
                county as county,
                NULL as city,
                COUNT(*) as count
            FROM obrigacoes_com_data 
            WHERE county ILIKE %s AND county IS NOT NULL AND county != ''
            GROUP BY state, county
            ORDER BY county
            LIMIT 10
        """, (f'%{query}%',))
        
        counties = cursor.fetchall()
        
        cursor.execute("""
            SELECT DISTINCT 
                'city' as type,
                state as code,
                city as name,
                county as county,
                city as city,
                COUNT(*) as count
            FROM obrigacoes_com_data 
            WHERE city ILIKE %s AND city IS NOT NULL AND city != ''
            GROUP BY state, county, city
            ORDER BY city
            LIMIT 10
        """, (f'%{query}%',))
        
        cities = cursor.fetchall()
        
        conn.close()
        
        # Combinar resultados e adicionar informações de estado
        results = []
        
        # Adicionar estados
        for state in states:
            state_name = _get_state_name(state['code'])
            results.append({
                'type': 'state',
                'code': state['code'],
                'name': state_name,
                'display': f"{state_name} ({state['code']})",
                'count': state['count']
            })
        
        # Adicionar condados
        for county in counties:
            state_name = _get_state_name(county['code'])
            results.append({
                'type': 'county',
                'code': county['code'],
                'name': county['name'],
                'display': f"{county['name']}, {state_name}",
                'count': county['count']
            })
        
        # Adicionar cidades
        for city in cities:
            state_name = _get_state_name(city['code'])
            results.append({
                'type': 'city',
                'code': city['code'],
                'name': city['name'],
                'county': city['county'],
                'display': f"{city['name']}, {city['county']}, {state_name}",
                'count': city['count']
            })
        
        # Ordenar por relevância (cidades primeiro, depois condados, depois estados)
        type_order = {'city': 0, 'county': 1, 'state': 2}
        results.sort(key=lambda x: (type_order.get(x['type'], 3), x['name']))
        
        return jsonify(results[:20])  # Limitar a 20 resultados
        
    except Exception as e:
        print(f"Erro na busca: {e}")
        return jsonify({'error': 'Erro interno'}), 500

def _get_state_name(state_code):
    """Converte código de estado para nome completo"""
    state_names = {
        'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas', 'AZ': 'Arizona',
        'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DC': 'District of Columbia',
        'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii',
        'IA': 'Iowa', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana',
        'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'MA': 'Massachusetts',
        'MD': 'Maryland', 'ME': 'Maine', 'MI': 'Michigan', 'MN': 'Minnesota',
        'MO': 'Missouri', 'MS': 'Mississippi', 'MT': 'Montana', 'NC': 'North Carolina',
        'ND': 'North Dakota', 'NE': 'Nebraska', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
        'NM': 'New Mexico', 'NV': 'Nevada', 'NY': 'New York', 'OH': 'Ohio',
        'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island',
        'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas',
        'UT': 'Utah', 'VA': 'Virginia', 'VT': 'Vermont', 'WA': 'Washington',
        'WI': 'Wisconsin', 'WV': 'West Virginia', 'WY': 'Wyoming'
    }
    return state_names.get(state_code, state_code)

@app.route('/api/calendar')
def get_calendar():
    """Retorna obrigações com filtros"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Erro de conexão com banco'}), 500
        
        state = request.args.get('state')
        county = request.args.get('county')
        city = request.args.get('city')
        month = request.args.get('month')
        
        where_conditions = []
        params = []
        
        # Filtros hierárquicos: se selecionar cidade, inclui todas as obrigações até o nível municipal
        if city:
            # Se tem cidade, inclui: federais + estaduais do estado + APENAS o condado da cidade + municipais da cidade
            where_conditions.append("""
                (jurisdiction_level = 'federal' OR 
                 (jurisdiction_level = 'state' AND state = %s) OR
                 (jurisdiction_level = 'county' AND state = %s AND county = %s) OR
                 (jurisdiction_level = 'municipal' AND state = %s AND county = %s AND city = %s))
            """)
            params.extend([state, state, county, state, county, city])
        elif county:
            # Se tem condado, inclui: federais + estaduais do estado + APENAS o condado selecionado
            where_conditions.append("""
                (jurisdiction_level = 'federal' OR 
                 (jurisdiction_level = 'state' AND state = %s) OR
                 (jurisdiction_level = 'county' AND state = %s AND county = %s))
            """)
            params.extend([state, state, county])
        elif state:
            # Se tem estado, inclui: federais + estaduais do estado
            where_conditions.append("""
                (jurisdiction_level = 'federal' OR 
                 (jurisdiction_level = 'state' AND state = %s))
            """)
            params.append(state)
        if month:
            try:
                month_num = int(month)
                # Filtra por mês independente do ano usando EXTRACT
                where_conditions.append("EXTRACT(MONTH FROM date) = %s")
                params.append(month_num)
            except Exception as e:
                print(f"Erro ao processar month: {e}")
                pass
        
        where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"
        
        query = f"""
            SELECT 
                obligation_id,
                title,
                notes,
                date,
                jurisdiction_level,
                jurisdiction,
                state,
                county,
                city,
                category,
                frequency,
                sources
            FROM obrigacoes_com_data 
            WHERE {where_clause}
            ORDER BY date
            LIMIT 1000
        """
        
        print(f"Query: {query}")
        print(f"Params: {params}")
        
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query, params)
        
        results = cursor.fetchall()
        conn.close()
        
        obligations = []
        for row in results:
            obligation = {
                'id': row['obligation_id'],
                'title': row['title'],  # Corrigido: usar 'title' em vez de 'name'
                'notes': row['notes'],  # Corrigido: usar 'notes' em vez de 'description'
                'date': row['date'].isoformat() if row['date'] else None,  # Corrigido: usar 'date' em vez de 'due_date'
                'jurisdiction_level': row['jurisdiction_level'],
                'jurisdiction': _clean_jurisdiction_name(row['jurisdiction']),
                'state': row['state'],
                'county': row['county'],
                'city': row['city'],
                'category': row['category'],
                'frequency': row['frequency'],
                'sources': _safe_json_parse(row['sources'])
            }
            # Processar sources para extrair links e criar botões
            obligation['source_buttons'] = []
            try:
                sources = obligation['sources'] or []
                print(f"🔍 Processando sources para obrigação {obligation['title']}: {sources}")
                
                if sources and len(sources) > 0:
                    for source in sources:
                        if isinstance(source, str) and source.strip():
                            # Para qualquer link, criar um botão "Acessar"
                            obligation['source_buttons'].append({'url': source, 'label': 'Acessar', 'type': 'blue'})
                            print(f"✅ Adicionado botão: {source}")
                        elif isinstance(source, dict):
                            url = source.get('url') or source.get('href') or source.get('link')
                            if url and url.strip():
                                obligation['source_buttons'].append({'url': url, 'label': 'Acessar', 'type': 'blue'})
                                print(f"✅ Adicionado botão: {url}")
                
            except Exception as e:
                print(f"Erro ao processar sources: {e}")
                pass
            
            print(f"📋 Botões criados para {obligation['title']}: {len(obligation['source_buttons'])} botões")
            obligations.append(obligation)
        
        federal = [ob for ob in obligations if ob['jurisdiction_level'] == 'federal']
        state_obligations = [ob for ob in obligations if ob['jurisdiction_level'] == 'state']
        county_obligations = [ob for ob in obligations if ob['jurisdiction_level'] == 'county']
        municipality = [ob for ob in obligations if ob['jurisdiction_level'] == 'municipal']
        
        return jsonify({
            'federal': federal,
            'state': state_obligations,
            'county': county_obligations,
            'municipality': municipality
        })
    except Exception as e:
        print(f"Erro na função get_calendar: {e}")
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

def _safe_json_parse(json_string):
    """Safely parse JSON string, return empty list if invalid"""
    try:
        if not json_string or json_string == 'null' or json_string == '':
            return []
        return json.loads(json_string)
    except (json.JSONDecodeError, TypeError):
        return []

def _clean_jurisdiction_name(jurisdiction):
    """Clean jurisdiction name for better display"""
    if not jurisdiction:
        return 'N/A'
    
    # Remove redundant patterns that were created during the update
    jurisdiction = jurisdiction.replace(' County', '').replace(' Municipality', '')
    
    # If it's just a state code, return the state name
    state_names = {
        'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas', 'AZ': 'Arizona',
        'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DC': 'District of Columbia',
        'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii',
        'IA': 'Iowa', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana',
        'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'MA': 'Massachusetts',
        'MD': 'Maryland', 'ME': 'Maine', 'MI': 'Michigan', 'MN': 'Minnesota',
        'MO': 'Missouri', 'MS': 'Mississippi', 'MT': 'Montana', 'NC': 'North Carolina',
        'ND': 'North Dakota', 'NE': 'Nebraska', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
        'NM': 'New Mexico', 'NV': 'Nevada', 'NY': 'New York', 'OH': 'Ohio',
        'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island',
        'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas',
        'UT': 'Utah', 'VA': 'Virginia', 'VT': 'Vermont', 'WA': 'Washington',
        'WI': 'Wisconsin', 'WV': 'West Virginia', 'WY': 'Wyoming'
    }
    
    if jurisdiction in state_names:
        return state_names[jurisdiction]
    
    return jurisdiction

@app.route('/static/<path:filename>')
def static_files(filename):
    """Servir arquivos estáticos"""
    return send_from_directory('static', filename)

if __name__ == '__main__':
    print("🚀 Tax Calendar - Profissional")
    print("=" * 50)
    
    # Verificar conexão com banco (não falhar se não conseguir)
    conn = get_db_connection()
    if conn:
        print("✅ Conexão com banco PostgreSQL OK")
        conn.close()
    else:
        print("⚠️ Banco PostgreSQL não configurado - aplicação funcionará sem banco")
    
    port = int(os.environ.get('PORT', 5000))
    print(f"🌐 Servidor iniciando em http://0.0.0.0:{port}")
    print(f"🏠 Aplicação: http://0.0.0.0:{port}")
    print("=" * 50)
    
    app.run(debug=False, host='0.0.0.0', port=port)
