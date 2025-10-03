#!/usr/bin/env python3
"""
Script para migrar dados do banco local para Railway PostgreSQL
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import os
import json

# Configuração do banco local
LOCAL_DB = {
    'host': '192.168.88.189',
    'port': 5432,
    'database': 'Tax_Calendar',
    'user': 'postgres',
    'password': 'root'
}

def get_local_connection():
    """Conexão com banco local"""
    return psycopg2.connect(**LOCAL_DB)

def get_railway_connection():
    """Conexão com Railway PostgreSQL"""
    if 'DATABASE_URL' not in os.environ:
        raise Exception("DATABASE_URL não encontrada. Configure no Railway.")
    
    return psycopg2.connect(os.environ['DATABASE_URL'])

def migrate_data():
    """Migra dados do banco local para Railway"""
    print("🚀 Iniciando migração de dados...")
    
    # Conectar aos bancos
    local_conn = get_local_connection()
    railway_conn = get_railway_connection()
    
    try:
        local_cursor = local_conn.cursor(cursor_factory=RealDictCursor)
        railway_cursor = railway_conn.cursor()
        
        # 1. Migrar obrigacoes_com_data
        print("📋 Migrando obrigacoes_com_data...")
        local_cursor.execute("SELECT * FROM obrigacoes_com_data")
        obligations = local_cursor.fetchall()
        
        # Limpar tabela no Railway
        railway_cursor.execute("DROP TABLE IF EXISTS obrigacoes_com_data CASCADE")
        
        # Criar tabela no Railway
        railway_cursor.execute("""
            CREATE TABLE obrigacoes_com_data (
                obligation_id SERIAL PRIMARY KEY,
                title VARCHAR(500),
                notes TEXT,
                date DATE,
                jurisdiction_level VARCHAR(50),
                jurisdiction VARCHAR(200),
                state VARCHAR(10),
                county VARCHAR(100),
                city VARCHAR(100),
                category VARCHAR(100),
                frequency VARCHAR(50),
                sources JSONB
            )
        """)
        
        # Inserir dados
        for obligation in obligations:
            railway_cursor.execute("""
                INSERT INTO obrigacoes_com_data 
                (title, notes, date, jurisdiction_level, jurisdiction, state, county, city, category, frequency, sources)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                obligation['title'],
                obligation['notes'],
                obligation['date'],
                obligation['jurisdiction_level'],
                obligation['jurisdiction'],
                obligation['state'],
                obligation['county'],
                obligation['city'],
                obligation['category'],
                obligation['frequency'],
                json.dumps(obligation['sources']) if obligation['sources'] else None
            ))
        
        # 2. Migrar obrigacoes_sem_data
        print("📋 Migrando obrigacoes_sem_data...")
        local_cursor.execute("SELECT * FROM obrigacoes_sem_data")
        obligations_no_date = local_cursor.fetchall()
        
        # Limpar tabela no Railway
        railway_cursor.execute("DROP TABLE IF EXISTS obrigacoes_sem_data CASCADE")
        
        # Criar tabela no Railway
        railway_cursor.execute("""
            CREATE TABLE obrigacoes_sem_data (
                id SERIAL PRIMARY KEY,
                title VARCHAR(500),
                notes TEXT
            )
        """)
        
        # Inserir dados
        for obligation in obligations_no_date:
            railway_cursor.execute("""
                INSERT INTO obrigacoes_sem_data (title, notes)
                VALUES (%s, %s)
            """, (obligation['title'], obligation['notes']))
        
        # Commit das alterações
        railway_conn.commit()
        
        print(f"✅ Migração concluída!")
        print(f"📊 {len(obligations)} obrigações com data migradas")
        print(f"📊 {len(obligations_no_date)} obrigações sem data migradas")
        
    except Exception as e:
        print(f"❌ Erro na migração: {e}")
        railway_conn.rollback()
        raise
    finally:
        local_conn.close()
        railway_conn.close()

if __name__ == '__main__':
    migrate_data()
