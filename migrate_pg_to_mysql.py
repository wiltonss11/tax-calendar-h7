#!/usr/bin/env python3
"""
Migra dados do PostgreSQL (origem) para MySQL (destino - Railway) em chunks.

Origem (PostgreSQL):
  - host: 192.168.88.189
  - port: 5432
  - database: Tax_Calendar
  - user: postgres
  - password: root

Destino (MySQL Railway):
  - URL recebida pelo usuário (mysql://...)
  - Convertida para mysql+pymysql://... para SQLAlchemy

Tabelas:
  - obrigacoes_com_data
  - obrigacoes_sem_data
"""

import os
import sys
from urllib.parse import urlparse

import pandas as pd
from sqlalchemy import create_engine, text


POSTGRES_URL = os.environ.get(
    "POSTGRES_URL",
    "postgresql+psycopg2://postgres:root@192.168.88.189:5432/Tax_Calendar",
)

MYSQL_URL_RAW = os.environ.get(
    "MYSQL_URL",
    "mysql://root:kODqKBZBEYeYuYXYzwgVmvzqjGgHaxoE@shinkansen.proxy.rlwy.net:29062/railway",
)

def to_sqlalchemy_mysql_url(url: str) -> str:
    # Converte mysql://user:pass@host:port/db para mysql+pymysql://user:pass@host:port/db?charset=utf8mb4
    parsed = urlparse(url)
    if parsed.scheme.startswith("mysql+"):
        # já tem driver
        return url if "charset=" in url else (url + ("&" if "?" in url else "?") + "charset=utf8mb4")
    # monta com pymysql
    base = f"mysql+pymysql://{parsed.username}:{parsed.password}@{parsed.hostname}:{parsed.port}{parsed.path}"
    if parsed.query:
        return f"{base}?{parsed.query}&charset=utf8mb4"
    return f"{base}?charset=utf8mb4"


def ensure_tables_mysql(mysql_engine):
    # Cria as tabelas com tipos adequados quando não existirem
    with mysql_engine.begin() as conn:
        conn.execute(text(
            """
            CREATE TABLE IF NOT EXISTS obrigacoes_com_data (
                obligation_id INT AUTO_INCREMENT PRIMARY KEY,
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
                sources JSON
            )
            """
        ))
        conn.execute(text(
            """
            CREATE TABLE IF NOT EXISTS obrigacoes_sem_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(500),
                notes TEXT
            )
            """
        ))


def truncate_mysql(mysql_engine):
    with mysql_engine.begin() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        conn.execute(text("TRUNCATE TABLE obrigacoes_com_data"))
        conn.execute(text("TRUNCATE TABLE obrigacoes_sem_data"))
        conn.execute(text("SET FOREIGN_KEY_CHECKS=1"))


def migrate_table(pg_engine, mysql_engine, table_name: str, chunksize: int = 5000):
    print(f"➡️ Migrando tabela: {table_name}")
    total = 0
    for chunk in pd.read_sql(f"SELECT * FROM {table_name}", pg_engine, chunksize=chunksize):
        # Normaliza JSON em 'sources' se vier como string
        if "sources" in chunk.columns:
            # Garante compatibilidade de JSON: strings vazias ou None -> NULL
            chunk["sources"] = chunk["sources"].apply(lambda v: None if v in ("", None) else v)
        chunk.to_sql(table_name, mysql_engine, if_exists="append", index=False)
        total += len(chunk)
        print(f"   - {total} linhas migradas...")
    print(f"✅ Concluído: {table_name} ({total} linhas)")


def main():
    try:
        mysql_url = to_sqlalchemy_mysql_url(MYSQL_URL_RAW)
        print(f"MySQL: {mysql_url}")
        print(f"Postgres: {POSTGRES_URL}")

        pg_engine = create_engine(POSTGRES_URL)
        mysql_engine = create_engine(mysql_url)

        ensure_tables_mysql(mysql_engine)
        truncate_mysql(mysql_engine)

        migrate_table(pg_engine, mysql_engine, "obrigacoes_com_data", chunksize=2000)
        migrate_table(pg_engine, mysql_engine, "obrigacoes_sem_data", chunksize=2000)

        print("\n🎉 Migração finalizada com sucesso!")
    except Exception as e:
        print(f"❌ Erro na migração: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


