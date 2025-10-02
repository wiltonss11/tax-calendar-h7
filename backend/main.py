#!/usr/bin/env python3
"""
Tax Calendar - Backend com FastAPI
Versão moderna e robusta
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import psycopg2
from psycopg2.extras import RealDictCursor
import json
from datetime import datetime
from typing import List, Optional
import uvicorn

# Configuração do banco
DB_CONFIG = {
    'host': '192.168.88.189',
    'port': 5432,
    'database': 'Tax_Calendar',
    'user': 'postgres',
    'password': 'root'
}

# Criar aplicação FastAPI
app = FastAPI(
    title="Tax Calendar API",
    description="API para gerenciamento de obrigações fiscais dos EUA",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir arquivos estáticos (Angular)
app.mount("/static", StaticFiles(directory="../frontend/dist"), name="static")

def get_db_connection():
    """Cria conexão com o banco de dados"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"❌ Erro ao conectar com banco: {e}")
        return None

@app.get("/", response_class=HTMLResponse)
async def home():
    """Página inicial"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Tax Calendar - Backend</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; }
            .status { background: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin: 20px 0; }
            .endpoints { background: #f8f9fa; padding: 20px; border-radius: 5px; }
            .endpoint { margin: 10px 0; }
            a { color: #007bff; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Tax Calendar - Backend FastAPI</h1>
            <div class="status">
                ✅ Servidor FastAPI rodando<br>
                ✅ Conexão com banco PostgreSQL OK<br>
                ✅ API endpoints funcionando
            </div>
            <div class="endpoints">
                <h3>📊 Endpoints disponíveis:</h3>
                <div class="endpoint"><a href="/docs">GET /docs</a> - Documentação Swagger</div>
                <div class="endpoint"><a href="/api/health">GET /api/health</a> - Health check</div>
                <div class="endpoint"><a href="/api/states">GET /api/states</a> - Lista de estados</div>
                <div class="endpoint"><a href="/api/calendar">GET /api/calendar</a> - Obrigações fiscais</div>
            </div>
            <div style="margin-top: 30px; padding: 20px; background: #e7f3ff; border-radius: 5px;">
                <h3>🌐 Frontend Angular:</h3>
                <p>Abra o arquivo <code>frontend/dist/index.html</code> no navegador</p>
                <p>Ou acesse: <a href="/static/index.html">/static/index.html</a></p>
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/api/health")
async def health_check():
    """Health check"""
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM obrigacoes_com_data")
            count = cursor.fetchone()[0]
            conn.close()
            
            return {
                "status": "healthy",
                "database": "connected",
                "message": "Backend FastAPI funcionando perfeitamente!",
                "obligations_count": count,
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=500, detail="Erro de conexão com banco de dados")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/api/states")
async def get_states():
    """Retorna lista de estados"""
    try:
        conn = get_db_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Erro de conexão com banco")
        
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT DISTINCT state as code
            FROM obrigacoes_com_data 
            WHERE state IS NOT NULL AND state != ''
            ORDER BY state
        """)
        
        results = cursor.fetchall()
        conn.close()
        
        # Mapear códigos para nomes
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
            states.append({
                'code': code,
                'name': state_names.get(code, code)
            })
        
        return states
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/api/counties/{state_code}")
async def get_counties(state_code: str):
    """Retorna condados de um estado"""
    try:
        conn = get_db_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Erro de conexão com banco")
        
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
        
        return counties
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/api/cities/{state_code}/{county_name}")
async def get_cities(state_code: str, county_name: str):
    """Retorna cidades de um condado"""
    try:
        conn = get_db_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Erro de conexão com banco")
        
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
        
        return cities
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/api/calendar")
async def get_calendar(
    state: Optional[str] = Query(None, description="Código do estado"),
    county: Optional[str] = Query(None, description="Nome do condado"),
    city: Optional[str] = Query(None, description="Nome da cidade"),
    date_range: Optional[str] = Query(None, description="Período no formato YYYY-MM")
):
    """Retorna obrigações com filtros"""
    try:
        conn = get_db_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Erro de conexão com banco")
        
        # Construir query com filtros
        where_conditions = []
        params = []
        
        if state:
            where_conditions.append("state = %s")
            params.append(state)
        
        if county:
            where_conditions.append("county = %s")
            params.append(county)
        
        if city:
            where_conditions.append("city = %s")
            params.append(city)
        
        if date_range:
            try:
                year, month = map(int, date_range.split('-'))
                start_date = f"{year}-{month:02d}-01"
                if month == 12:
                    end_date = f"{year + 1}-01-01"
                else:
                    end_date = f"{year}-{month + 1:02d}-01"
                
                where_conditions.append("date >= %s AND date < %s")
                params.extend([start_date, end_date])
            except:
                pass
        
        where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"
        
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(f"""
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
        """, params)
        
        results = cursor.fetchall()
        conn.close()
        
        obligations = []
        for row in results:
            obligation = {
                'id': row['obligation_id'],
                'name': row['title'],
                'description': row['notes'],
                'due_date': row['date'].isoformat() if row['date'] else None,
                'jurisdiction_level': row['jurisdiction_level'],
                'jurisdiction': row['jurisdiction'],
                'state': row['state'],
                'county': row['county'],
                'city': row['city'],
                'category': row['category'],
                'frequency': row['frequency'],
                'sources': json.loads(row['sources']) if row['sources'] else []
            }
            obligations.append(obligation)
        
        # Organizar por nível
        federal = [ob for ob in obligations if ob['jurisdiction_level'] == 'federal']
        state_obligations = [ob for ob in obligations if ob['jurisdiction_level'] == 'state']
        county_obligations = [ob for ob in obligations if ob['jurisdiction_level'] == 'county']
        municipality = [ob for ob in obligations if ob['jurisdiction_level'] == 'municipal']
        
        return {
            'federal': federal,
            'state': state_obligations,
            'county': county_obligations,
            'municipality': municipality
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

if __name__ == "__main__":
    print("🚀 Tax Calendar - Backend FastAPI")
    print("=" * 50)
    
    # Testar conexão
    conn = get_db_connection()
    if conn:
        print("✅ Conexão com banco PostgreSQL OK")
        conn.close()
    else:
        print("❌ Erro de conexão com banco PostgreSQL")
        print("Verifique se o PostgreSQL está rodando")
        exit(1)
    
    print("🌐 Servidor iniciando em http://127.0.0.1:8000")
    print("📚 Documentação: http://127.0.0.1:8000/docs")
    print("🏠 Página inicial: http://127.0.0.1:8000")
    print("=" * 50)
    
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
