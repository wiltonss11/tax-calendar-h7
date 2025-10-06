--
-- PostgreSQL database dump
--

-- Dumped from database version 16.9
-- Dumped by pg_dump version 17.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: obrigacoes_sem_data; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.obrigacoes_sem_data (id, obligation_id, title, jurisdiction_level, jurisdiction, state, county, city, category, frequency, notes, sources, created_at, updated_at) VALUES (2, 'irs-form-ss-4', 'IRS Form SS-4 - Solicitação de EIN', 'federal', 'IRS', NULL, NULL, NULL, 'Geral', 'Anual', 'Sem data fixa. Deve ser feito antes de apresentar declarações ou abrir contas bancárias comerciais.', '{https://www.irs.gov/businesses/small-businesses-self-employed/employer-id-numbers}', '2025-09-30 14:38:56.21852', '2025-09-30 14:38:56.21852');
INSERT INTO public.obrigacoes_sem_data (id, obligation_id, title, jurisdiction_level, jurisdiction, state, county, city, category, frequency, notes, sources, created_at, updated_at) VALUES (3, 'state-business-registration', 'Registro de Negócio Estadual', 'state', 'varia por estado', NULL, NULL, NULL, 'Geral', 'Anual', 'Ao constituir/registrar a empresa no estado; necessário antes de obter licenças e recolher impostos.', '{https://www.usa.gov/register-your-business}', '2025-09-30 14:38:56.21852', '2025-09-30 14:38:56.21852');
INSERT INTO public.obrigacoes_sem_data (id, obligation_id, title, jurisdiction_level, jurisdiction, state, county, city, category, frequency, notes, sources, created_at, updated_at) VALUES (4, 'sales-tax-permit', 'Inscrição para Permissão de Sales Tax', 'state', 'varia por estado (CDTFA/NY DTF/TX CPA, etc.)', NULL, NULL, NULL, 'Geral', 'Anual', 'Antes de começar a vender bens/serviços tributáveis; requisito para cobrança de Sales/Use Tax.', '{https://www.cdtfa.ca.gov/,https://comptroller.texas.gov/,https://www.tax.ny.gov/}', '2025-09-30 14:38:56.21852', '2025-09-30 14:38:56.21852');
INSERT INTO public.obrigacoes_sem_data (id, obligation_id, title, jurisdiction_level, jurisdiction, state, county, city, category, frequency, notes, sources, created_at, updated_at) VALUES (5, 'local-business-license', 'Licença Comercial Municipal/Condado', 'municipal', 'varia por cidade/condado', NULL, NULL, NULL, 'Geral', 'Anual', 'Requerida antes do início das operações no município/condado; renovações podem ter calendários próprios.', '{}', '2025-09-30 14:38:56.21852', '2025-09-30 14:38:56.21852');


--
-- Name: obrigacoes_sem_data_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.obrigacoes_sem_data_id_seq', 5, true);


--
-- PostgreSQL database dump complete
--

