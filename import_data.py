#!/usr/bin/env python3
"""
Script para importar dados do CSV para o MySQL do Railway
"""
import csv
import json
import pymysql
from datetime import datetime

# Configuração do MySQL Railway
MYSQL_CONFIG = {
    'host': 'shinkansen.proxy.rlwy.net',
    'port': 29062,
    'user': 'root',
    'password': 'kODqKBZBEYeYuYXYzwgVmvzqjGgHaxoE',
    'database': 'railway',
    'charset': 'utf8mb4'
}

def clean_value(value):
    """Limpa valores para inserção no banco"""
    if value is None or value == '':
        return None
    return str(value).strip()

def parse_date(date_str):
    """Converte string de data para formato MySQL"""
    if not date_str or date_str == '':
        return None
    try:
        # Tenta diferentes formatos de data
        for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y']:
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        return None
    except:
        return None

def parse_sources(sources_str):
    """Converte string JSON para objeto Python"""
    if not sources_str or sources_str == '':
        return None
    try:
        return json.loads(sources_str)
    except:
        return None

def import_obrigacoes_com_data():
    """Importa dados da tabela obrigacoes_com_data"""
    print("🔄 Iniciando importação de obrigacoes_com_data...")
    
    # Conectar ao MySQL
    conn = pymysql.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()
    
    try:
        # Limpar tabela existente
        cursor.execute("TRUNCATE TABLE obrigacoes_com_data")
        print("✅ Tabela limpa")
        
        # Ler CSV e inserir dados
        with open('obrigacoes_com_data.csv', 'r', encoding='latin-1') as file:
            reader = csv.DictReader(file)
            
            batch_size = 1000
            batch = []
            total_imported = 0
            
            for row in reader:
                # Preparar dados
                data = (
                    clean_value(row.get('title')),
                    clean_value(row.get('notes')),
                    parse_date(row.get('date')),
                    clean_value(row.get('jurisdiction_level')),
                    clean_value(row.get('jurisdiction')),
                    clean_value(row.get('state')),
                    clean_value(row.get('county')),
                    clean_value(row.get('city')),
                    clean_value(row.get('category')),
                    clean_value(row.get('frequency')),
                    json.dumps(parse_sources(row.get('sources'))) if row.get('sources') else None
                )
                
                batch.append(data)
                
                # Inserir em lotes
                if len(batch) >= batch_size:
                    insert_batch(cursor, batch)
                    total_imported += len(batch)
                    print(f"📊 Importadas {total_imported} linhas...")
                    batch = []
            
            # Inserir lote restante
            if batch:
                insert_batch(cursor, batch)
                total_imported += len(batch)
            
            conn.commit()
            print(f"✅ Importação concluída: {total_imported} linhas")
            
    except Exception as e:
        print(f"❌ Erro na importação: {e}")
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()

def insert_batch(cursor, batch):
    """Insere um lote de dados"""
    sql = """
    INSERT INTO obrigacoes_com_data 
    (title, notes, date, jurisdiction_level, jurisdiction, state, county, city, category, frequency, sources)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(sql, batch)

def import_obrigacoes_sem_data():
    """Importa dados da tabela obrigacoes_sem_data"""
    print("🔄 Iniciando importação de obrigacoes_sem_data...")
    
    # Conectar ao MySQL
    conn = pymysql.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()
    
    try:
        # Limpar tabela existente
        cursor.execute("TRUNCATE TABLE obrigacoes_sem_data")
        print("✅ Tabela limpa")
        
        # Ler CSV e inserir dados
        with open('obrigacoes_sem_data.csv', 'r', encoding='latin-1') as file:
            reader = csv.DictReader(file)
            
            batch_size = 1000
            batch = []
            total_imported = 0
            
            for row in reader:
                # Preparar dados
                data = (
                    clean_value(row.get('title')),
                    clean_value(row.get('notes'))
                )
                
                batch.append(data)
                
                # Inserir em lotes
                if len(batch) >= batch_size:
                    insert_batch_sem_data(cursor, batch)
                    total_imported += len(batch)
                    print(f"📊 Importadas {total_imported} linhas...")
                    batch = []
            
            # Inserir lote restante
            if batch:
                insert_batch_sem_data(cursor, batch)
                total_imported += len(batch)
            
            conn.commit()
            print(f"✅ Importação concluída: {total_imported} linhas")
            
    except Exception as e:
        print(f"❌ Erro na importação: {e}")
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()

def insert_batch_sem_data(cursor, batch):
    """Insere um lote de dados para obrigacoes_sem_data"""
    sql = """
    INSERT INTO obrigacoes_sem_data (title, notes)
    VALUES (%s, %s)
    """
    cursor.executemany(sql, batch)

def verify_import():
    """Verifica se os dados foram importados corretamente"""
    print("🔍 Verificando importação...")
    
    conn = pymysql.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()
    
    try:
        # Contar registros
        cursor.execute("SELECT COUNT(*) FROM obrigacoes_com_data")
        count_com_data = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM obrigacoes_sem_data")
        count_sem_data = cursor.fetchone()[0]
        
        print(f"📊 obrigacoes_com_data: {count_com_data} registros")
        print(f"📊 obrigacoes_sem_data: {count_sem_data} registros")
        
        if count_com_data > 0:
            print("✅ Importação bem-sucedida!")
        else:
            print("❌ Nenhum dado foi importado")
            
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    print("🚀 Iniciando migração de dados para Railway MySQL...")
    print("=" * 50)
    
    try:
        # Importar dados
        import_obrigacoes_com_data()
        print()
        import_obrigacoes_sem_data()
        print()
        verify_import()
        
        print("=" * 50)
        print("🎉 Migração concluída com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro na migração: {e}")
        print("Verifique se os arquivos CSV existem e se a conexão com o MySQL está funcionando.")
