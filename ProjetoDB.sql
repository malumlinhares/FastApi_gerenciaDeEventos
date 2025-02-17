--
-- PostgreSQL database dump
--

-- Dumped from database version 17.3 (Debian 17.3-1.pgdg120+1)
-- Dumped by pg_dump version 17.3 (Debian 17.3-1.pgdg120+1)

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
-- Name: tipo_patrocinador; Type: TYPE; Schema: public; Owner: admin
--

CREATE TYPE public.tipo_patrocinador AS ENUM (
    'publico',
    'privado'
);


ALTER TYPE public.tipo_patrocinador OWNER TO admin;

--
-- Name: inserir_log_novo_patrocinador(); Type: FUNCTION; Schema: public; Owner: admin
--

CREATE FUNCTION public.inserir_log_novo_patrocinador() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
            BEGIN
                IF NEW.tipo = 'privado' THEN
                    INSERT INTO logs (mensagem, data_criacao, event_details)
                    VALUES (
                        'Novo patrocinador privado: ' || NEW.nome || ' (ID: ' || NEW.id || ')',  -- mensagem
                        CURRENT_TIMESTAMP,                                                      -- data_criacao
                        'Detalhes do evento não disponíveis'                                     -- event_details
                    );
                END IF;
                RETURN NEW;
            END;
            $$;


ALTER FUNCTION public.inserir_log_novo_patrocinador() OWNER TO admin;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: autenticadores; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.autenticadores (
    id integer NOT NULL,
    chave_autenticacao character varying NOT NULL,
    orgao character varying NOT NULL,
    status character varying,
    data_expiracao date
);


ALTER TABLE public.autenticadores OWNER TO admin;

--
-- Name: autenticadores_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.autenticadores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.autenticadores_id_seq OWNER TO admin;

--
-- Name: autenticadores_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.autenticadores_id_seq OWNED BY public.autenticadores.id;


--
-- Name: certificados; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.certificados (
    id integer NOT NULL,
    evento_id integer NOT NULL,
    participante_id integer NOT NULL,
    autenticador_id integer,
    data_emissao date,
    codigo_verificacao character varying
);


ALTER TABLE public.certificados OWNER TO admin;

--
-- Name: certificados_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.certificados_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.certificados_id_seq OWNER TO admin;

--
-- Name: certificados_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.certificados_id_seq OWNED BY public.certificados.id;


--
-- Name: enderecos; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.enderecos (
    id integer NOT NULL,
    rua character varying NOT NULL,
    cep character varying NOT NULL,
    numero integer NOT NULL,
    complemento character varying,
    ponto_de_referencia character varying
);


ALTER TABLE public.enderecos OWNER TO admin;

--
-- Name: enderecos_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.enderecos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.enderecos_id_seq OWNER TO admin;

--
-- Name: enderecos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.enderecos_id_seq OWNED BY public.enderecos.id;


--
-- Name: eventos; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.eventos (
    id integer NOT NULL,
    nome character varying NOT NULL,
    categoria character varying NOT NULL,
    data date NOT NULL,
    numerohoras integer NOT NULL,
    local_id integer NOT NULL,
    organizador_id integer NOT NULL,
    descricao character varying,
    limite_participantes integer
);


ALTER TABLE public.eventos OWNER TO admin;

--
-- Name: eventos_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.eventos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.eventos_id_seq OWNER TO admin;

--
-- Name: eventos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.eventos_id_seq OWNED BY public.eventos.id;


--
-- Name: inscricao; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.inscricao (
    numero_inscricao integer NOT NULL,
    status character varying DEFAULT 'Pendente'::character varying NOT NULL,
    forma_pagamento character varying NOT NULL,
    valor double precision NOT NULL,
    participante_id integer NOT NULL,
    data_pagamento timestamp without time zone,
    observacao character varying
);


ALTER TABLE public.inscricao OWNER TO admin;

--
-- Name: inscricao_numero_inscricao_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.inscricao_numero_inscricao_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.inscricao_numero_inscricao_seq OWNER TO admin;

--
-- Name: inscricao_numero_inscricao_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.inscricao_numero_inscricao_seq OWNED BY public.inscricao.numero_inscricao;


--
-- Name: locais; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.locais (
    id integer NOT NULL,
    cidade character varying NOT NULL,
    nome character varying NOT NULL,
    estado character varying,
    descricao character varying
);


ALTER TABLE public.locais OWNER TO admin;

--
-- Name: locais_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.locais_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.locais_id_seq OWNER TO admin;

--
-- Name: locais_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.locais_id_seq OWNED BY public.locais.id;


--
-- Name: logs; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.logs (
    id integer NOT NULL,
    "timestamp" timestamp with time zone DEFAULT now(),
    data_criacao timestamp with time zone DEFAULT now(),
    mensagem text NOT NULL,
    event_details text
);


ALTER TABLE public.logs OWNER TO admin;

--
-- Name: logs_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.logs_id_seq OWNER TO admin;

--
-- Name: logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.logs_id_seq OWNED BY public.logs.id;


--
-- Name: organizadores; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.organizadores (
    id integer NOT NULL,
    nome character varying NOT NULL,
    email character varying NOT NULL,
    cnpj character varying NOT NULL,
    telefone character varying,
    nome_contato character varying
);


ALTER TABLE public.organizadores OWNER TO admin;

--
-- Name: organizadores_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.organizadores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.organizadores_id_seq OWNER TO admin;

--
-- Name: organizadores_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.organizadores_id_seq OWNED BY public.organizadores.id;


--
-- Name: participantes; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.participantes (
    id integer NOT NULL,
    nome character varying NOT NULL,
    email character varying NOT NULL,
    tipo character varying NOT NULL,
    anuidade integer,
    elegivel_upgrade integer NOT NULL,
    endereco_id integer,
    telefone character varying,
    responsavel character varying,
    CONSTRAINT participantes_check CHECK (((((tipo)::text = 'vip'::text) AND (anuidade IS NOT NULL)) OR (((tipo)::text = 'padrao'::text) AND (anuidade = 0)))),
    CONSTRAINT participantes_check1 CHECK (((((tipo)::text = 'padrao'::text) AND (elegivel_upgrade = 1)) OR ((tipo)::text = 'vip'::text))),
    CONSTRAINT participantes_tipo_check CHECK (((tipo)::text = ANY ((ARRAY['vip'::character varying, 'padrao'::character varying])::text[])))
);


ALTER TABLE public.participantes OWNER TO admin;

--
-- Name: participantes_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.participantes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.participantes_id_seq OWNER TO admin;

--
-- Name: participantes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.participantes_id_seq OWNED BY public.participantes.id;


--
-- Name: patrocinadores; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.patrocinadores (
    id integer NOT NULL,
    nome character varying NOT NULL,
    email character varying NOT NULL,
    tipo public.tipo_patrocinador NOT NULL,
    orgao_responsavel character varying,
    responsavel_comercial character varying,
    telefone character varying,
    nome_responsavel character varying
);


ALTER TABLE public.patrocinadores OWNER TO admin;

--
-- Name: patrocinadores_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.patrocinadores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.patrocinadores_id_seq OWNER TO admin;

--
-- Name: patrocinadores_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.patrocinadores_id_seq OWNED BY public.patrocinadores.id;


--
-- Name: patrocinios; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.patrocinios (
    id integer NOT NULL,
    valor double precision NOT NULL,
    descricao character varying NOT NULL,
    evento_id integer NOT NULL,
    patrocinador_id integer NOT NULL,
    status character varying,
    observacao character varying
);


ALTER TABLE public.patrocinios OWNER TO admin;

--
-- Name: patrocinios_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.patrocinios_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.patrocinios_id_seq OWNER TO admin;

--
-- Name: patrocinios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.patrocinios_id_seq OWNED BY public.patrocinios.id;


--
-- Name: autenticadores id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.autenticadores ALTER COLUMN id SET DEFAULT nextval('public.autenticadores_id_seq'::regclass);


--
-- Name: certificados id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.certificados ALTER COLUMN id SET DEFAULT nextval('public.certificados_id_seq'::regclass);


--
-- Name: enderecos id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.enderecos ALTER COLUMN id SET DEFAULT nextval('public.enderecos_id_seq'::regclass);


--
-- Name: eventos id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.eventos ALTER COLUMN id SET DEFAULT nextval('public.eventos_id_seq'::regclass);


--
-- Name: inscricao numero_inscricao; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.inscricao ALTER COLUMN numero_inscricao SET DEFAULT nextval('public.inscricao_numero_inscricao_seq'::regclass);


--
-- Name: locais id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.locais ALTER COLUMN id SET DEFAULT nextval('public.locais_id_seq'::regclass);


--
-- Name: logs id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.logs ALTER COLUMN id SET DEFAULT nextval('public.logs_id_seq'::regclass);


--
-- Name: organizadores id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.organizadores ALTER COLUMN id SET DEFAULT nextval('public.organizadores_id_seq'::regclass);


--
-- Name: participantes id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.participantes ALTER COLUMN id SET DEFAULT nextval('public.participantes_id_seq'::regclass);


--
-- Name: patrocinadores id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.patrocinadores ALTER COLUMN id SET DEFAULT nextval('public.patrocinadores_id_seq'::regclass);


--
-- Name: patrocinios id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.patrocinios ALTER COLUMN id SET DEFAULT nextval('public.patrocinios_id_seq'::regclass);


--
-- Data for Name: autenticadores; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.autenticadores (id, chave_autenticacao, orgao, status, data_expiracao) FROM stdin;
1	AUTH001	Instituto Nacional de Certificação	Ativo	2026-12-31
2	AUTH002	Conselho Federal de Educação	Ativo	2025-11-15
3	AUTH003	Ministério da Ciência e Tecnologia	Inativo	2024-09-30
4	AUTH004	Secretaria Estadual de Pesquisa	Ativo	2027-03-20
5	AUTH005	Agência Nacional de Tecnologia	Ativo	2026-06-10
6	AUTH006	Departamento de Segurança Digital	Ativo	2026-09-05
7	AUTH007	Comissão de Certificação Nacional	Inativo	2024-10-15
8	AUTH008	Centro de Autenticação Oficial	Ativo	2027-01-30
9	AUTH009	Agência de Regulação e Certificação	Ativo	2025-12-01
10	AUTH010	Instituto de Normas Técnicas	Ativo	2026-03-10
\.


--
-- Data for Name: certificados; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.certificados (id, evento_id, participante_id, autenticador_id, data_emissao, codigo_verificacao) FROM stdin;
1	1	1	1	2024-07-10	CERT-001
2	2	2	2	2024-07-15	CERT-002
3	3	3	3	2024-08-01	CERT-003
4	4	4	4	2024-08-10	CERT-004
5	5	5	5	2024-08-20	CERT-005
6	6	6	6	2024-08-25	CERT-006
7	7	7	7	2024-09-01	CERT-007
8	8	8	8	2024-09-05	CERT-008
9	9	9	9	2024-09-10	CERT-009
10	10	10	10	2024-09-15	CERT-010
\.


--
-- Data for Name: enderecos; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.enderecos (id, rua, cep, numero, complemento, ponto_de_referencia) FROM stdin;
1	Av. Paulista	01310-100	1000	Sala 101	Próximo ao MASP
2	Rua das Flores	20031-010	500	\N	Ao lado do metrô
3	Alameda Santos	01419-001	1200	Bloco B	Em frente ao shopping
4	Rua Augusta	01304-001	650	\N	Próximo à Av. Paulista
5	Av. Brasil	22041-010	900	\N	Perto da praia
6	Rua XV de Novembro	80020-310	300	\N	Centro Histórico
7	Av. das Nações	70150-000	1500	\N	Próximo ao Palácio do Planalto
8	Rua Chile	40020-000	450	\N	Centro Antigo
9	Av. Sete de Setembro	40110-000	750	\N	Próximo ao Farol da Barra
10	Rua Amazonas	69010-020	550	\N	Perto do Teatro Amazonas
\.


--
-- Data for Name: eventos; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.eventos (id, nome, categoria, data, numerohoras, local_id, organizador_id, descricao, limite_participantes) FROM stdin;
1	Tech Conference	Tecnologia	2025-03-15	8	1	1	Conferência de tecnologia.	500
2	Saúde e Bem-estar	Saúde	2025-04-10	6	2	2	Evento sobre saúde e bem-estar.	300
3	Empreendedorismo 2025	Negócios	2025-05-20	10	3	3	Conferência sobre startups.	400
4	Música ao Vivo	Entretenimento	2025-06-25	5	4	4	Show e apresentações ao vivo.	700
5	Feira do Livro	Educação	2025-07-15	6	5	5	Feira com autores e editoras.	600
6	Hackathon Nacional	Tecnologia	2025-08-10	24	6	6	Competição de programação.	200
7	Congresso Jurídico	Direito	2025-09-05	8	7	7	Discussões sobre legislação.	250
8	Festival de Cinema	Cultura	2025-10-20	12	8	8	Mostra de filmes nacionais.	500
9	Fórum de Sustentabilidade	Meio Ambiente	2025-11-10	7	9	9	Palestras sobre sustentabilidade.	350
10	Congresso de Engenharia	Engenharia	2025-12-05	9	10	10	Discussões sobre inovação na engenharia.	450
\.


--
-- Data for Name: inscricao; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.inscricao (numero_inscricao, status, forma_pagamento, valor, participante_id, data_pagamento, observacao) FROM stdin;
1	Pendente	Cartão de Crédito	150	1	2025-02-01 10:00:00	Pagamento via cartão de crédito
2	Pendente	Boleto Bancário	200	2	\N	Aguardando pagamento
3	Confirmado	Transferência Bancária	120	3	2025-02-02 12:30:00	Pagamento confirmado
4	Pendente	Dinheiro	180	4	\N	Aguardando pagamento
5	Confirmado	Cartão de Crédito	250	5	2025-02-03 14:00:00	Pagamento confirmado
6	Pendente	Boleto Bancário	220	6	\N	Aguardando pagamento
7	Confirmado	Transferência Bancária	170	7	2025-02-04 15:30:00	Pagamento confirmado
8	Pendente	Cartão de Crédito	210	8	\N	Aguardando pagamento
9	Confirmado	Dinheiro	190	9	2025-02-05 16:00:00	Pagamento confirmado
10	Pendente	Boleto Bancário	160	10	\N	Aguardando pagamento
\.


--
-- Data for Name: locais; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.locais (id, cidade, nome, estado, descricao) FROM stdin;
1	São Paulo	Centro de Eventos SP	SP	Espaço amplo para conferências.
2	Rio de Janeiro	Auditório RJ	RJ	Auditório moderno e equipado.
3	Belo Horizonte	Expo Minas	MG	Centro de exposições em BH.
4	Fortaleza	Centro Cultural Fortaleza	CE	Local para eventos culturais.
5	Recife	Arena Recife	PE	Grande arena multiuso.
6	Porto Alegre	Teatro Porto Alegre	RS	Espaço cultural e eventos.
7	Curitiba	Pavilhão Curitiba	PR	Centro de convenções.
8	Brasília	Palácio de Convenções	DF	Espaço para grandes eventos.
9	Salvador	Centro de Eventos SSA	BA	Centro de convenções em Salvador.
10	Manaus	Auditório Amazonas	AM	Auditório de alta tecnologia.
\.


--
-- Data for Name: logs; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.logs (id, "timestamp", data_criacao, mensagem, event_details) FROM stdin;
1	2025-02-17 12:10:04.263087+00	2025-02-17 12:10:04.263087+00	Novo patrocinador privado: Empresa P (ID: 12)	Detalhes do evento não disponíveis
2	2025-02-17 12:10:42.704295+00	2025-02-17 12:10:42.704295+00	Novo patrocinador privado: string (ID: 13)	Detalhes do evento não disponíveis
\.


--
-- Data for Name: organizadores; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.organizadores (id, nome, email, cnpj, telefone, nome_contato) FROM stdin;
1	Eventos SP	eventossp@email.com	12345678000101	11999999999	Carlos Silva
2	Eventos RJ	eventosrj@email.com	12345678000102	21999999999	Ana Souza
3	Eventos MG	eventosmg@email.com	12345678000103	31999999999	Marcos Lima
4	Eventos CE	eventosce@email.com	12345678000104	85999999999	Rita Costa
5	Eventos PE	eventospe@email.com	12345678000105	81999999999	Pedro Rocha
6	Eventos RS	eventosrs@email.com	12345678000106	51999999999	João Mendes
7	Eventos PR	eventospr@email.com	12345678000107	41999999999	Clara Azevedo
8	Eventos DF	eventosdf@email.com	12345678000108	61999999999	Lucas Nunes
9	Eventos BA	eventosba@email.com	12345678000109	71999999999	Sofia Fernandes
10	Eventos AM	eventosam@email.com	12345678000110	92999999999	Bruno Oliveira
\.


--
-- Data for Name: participantes; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.participantes (id, nome, email, tipo, anuidade, elegivel_upgrade, endereco_id, telefone, responsavel) FROM stdin;
1	Alice Silva	alice@email.com	vip	1200	0	1	11999990001	Carlos Souza
2	Bruno Costa	bruno@email.com	padrao	0	1	2	11999990002	Fernanda Lima
3	Carla Mendes	carla@email.com	vip	1500	0	3	11999990003	Ricardo Alves
4	Daniel Ferreira	daniel@email.com	padrao	0	1	4	11999990004	Mariana Duarte
5	Eduardo Santos	eduardo@email.com	vip	2000	0	5	11999990005	Juliana Rocha
6	Fernanda Lima	fernanda@email.com	padrao	0	1	6	11999990006	Roberto Nunes
7	Gabriel Oliveira	gabriel@email.com	vip	1750	0	7	11999990007	Amanda Martins
8	Helena Souza	helena@email.com	padrao	0	1	8	11999990008	Thiago Pereira
9	Igor Mendes	igor@email.com	vip	1300	0	9	11999990009	Vanessa Lopes
10	Juliana Rocha	juliana@email.com	padrao	0	1	10	11999990010	Felipe Cardoso
\.


--
-- Data for Name: patrocinadores; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.patrocinadores (id, nome, email, tipo, orgao_responsavel, responsavel_comercial, telefone, nome_responsavel) FROM stdin;
1	Empresa A	patrocinioA@email.com	privado	\N	João Silva	11988887777	Maria Oliveira
2	Empresa B	patrocinioB@email.com	publico	Ministério da Cultura	\N	21988887777	Ana Souza
3	Empresa C	patrocinioC@email.com	privado	\N	Fernanda Lima	31988887777	Ricardo Gomes
4	Empresa D	patrocinioD@email.com	publico	Prefeitura RJ	\N	85988887777	Cláudia Torres
5	Empresa E	patrocinioE@email.com	privado	\N	Sônia Medeiros	81988887777	Roberto Nunes
6	Empresa F	patrocinioF@email.com	privado	\N	Henrique Castro	51988887777	Letícia Carvalho
7	Empresa G	patrocinioG@email.com	publico	Secretaria de Ciência e Tecnologia	\N	41988887777	Sérgio Almeida
8	Empresa H	patrocinioH@email.com	privado	\N	Gabriela Lopes	61988887777	Paula Mendes
9	Empresa I	patrocinioI@email.com	publico	Ministério do Turismo	\N	71988887777	Eduardo Lima
10	Empresa J	patrocinioJ@email.com	privado	\N	Tatiane Moreira	92988887777	Júlio César
11	teste_gatilho	teste@gatilho	privado	\N	gatilho	string	string
12	Empresa P	patrocinioP@email.com	privado	\N	João P Silva	11999997777	Maria de Oliveira
13	string	string	privado	\N	string	string	string
\.


--
-- Data for Name: patrocinios; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.patrocinios (id, valor, descricao, evento_id, patrocinador_id, status, observacao) FROM stdin;
1	5000	Patrocínio principal para evento de tecnologia	1	2	Ativo	Acordo firmado com a empresa X.
2	3000	Patrocínio de alimentação durante o evento	2	3	Ativo	Inclui fornecimento de lanches.
3	1500	Patrocínio para brindes e sorteios	1	4	Inativo	Aguardando contrato.
4	8000	Patrocínio para evento cultural	3	5	Ativo	Envolvimento com a promoção de arte local.
5	2000	Patrocínio para evento esportivo	4	6	Ativo	Focando no apoio à saúde e bem-estar.
6	4500	Patrocínio de transporte para participantes	2	7	Ativo	Transporte de ida e volta para o evento.
7	6000	Patrocínio de mídia e publicidade	5	8	Ativo	Campanha de mídia online e offline.
8	1200	Patrocínio para decoração e ambientação	6	9	Inativo	Aguardando ajustes no projeto.
9	2500	Patrocínio de equipamentos e infraestrutura	7	10	Ativo	Cobre o aluguel de equipamentos de som e luz.
10	10000	Patrocínio de palestras e workshops	8	1	Ativo	Patrocínio completo das atividades do evento.
\.


--
-- Name: autenticadores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.autenticadores_id_seq', 10, true);


--
-- Name: certificados_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.certificados_id_seq', 10, true);


--
-- Name: enderecos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.enderecos_id_seq', 10, true);


--
-- Name: eventos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.eventos_id_seq', 10, true);


--
-- Name: inscricao_numero_inscricao_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.inscricao_numero_inscricao_seq', 10, true);


--
-- Name: locais_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.locais_id_seq', 10, true);


--
-- Name: logs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.logs_id_seq', 2, true);


--
-- Name: organizadores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.organizadores_id_seq', 10, true);


--
-- Name: participantes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.participantes_id_seq', 10, true);


--
-- Name: patrocinadores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.patrocinadores_id_seq', 13, true);


--
-- Name: patrocinios_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.patrocinios_id_seq', 10, true);


--
-- Name: autenticadores autenticadores_chave_autenticacao_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.autenticadores
    ADD CONSTRAINT autenticadores_chave_autenticacao_key UNIQUE (chave_autenticacao);


--
-- Name: autenticadores autenticadores_orgao_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.autenticadores
    ADD CONSTRAINT autenticadores_orgao_key UNIQUE (orgao);


--
-- Name: autenticadores autenticadores_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.autenticadores
    ADD CONSTRAINT autenticadores_pkey PRIMARY KEY (id);


--
-- Name: certificados certificados_codigo_verificacao_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.certificados
    ADD CONSTRAINT certificados_codigo_verificacao_key UNIQUE (codigo_verificacao);


--
-- Name: certificados certificados_evento_id_participante_id_autenticador_id_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.certificados
    ADD CONSTRAINT certificados_evento_id_participante_id_autenticador_id_key UNIQUE (evento_id, participante_id, autenticador_id);


--
-- Name: certificados certificados_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.certificados
    ADD CONSTRAINT certificados_pkey PRIMARY KEY (id);


--
-- Name: enderecos enderecos_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.enderecos
    ADD CONSTRAINT enderecos_pkey PRIMARY KEY (id);


--
-- Name: eventos eventos_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.eventos
    ADD CONSTRAINT eventos_pkey PRIMARY KEY (id);


--
-- Name: inscricao inscricao_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.inscricao
    ADD CONSTRAINT inscricao_pkey PRIMARY KEY (numero_inscricao);


--
-- Name: locais locais_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.locais
    ADD CONSTRAINT locais_pkey PRIMARY KEY (id);


--
-- Name: logs logs_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.logs
    ADD CONSTRAINT logs_pkey PRIMARY KEY (id);


--
-- Name: organizadores organizadores_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.organizadores
    ADD CONSTRAINT organizadores_pkey PRIMARY KEY (id);


--
-- Name: participantes participantes_email_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.participantes
    ADD CONSTRAINT participantes_email_key UNIQUE (email);


--
-- Name: participantes participantes_endereco_id_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.participantes
    ADD CONSTRAINT participantes_endereco_id_key UNIQUE (endereco_id);


--
-- Name: participantes participantes_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.participantes
    ADD CONSTRAINT participantes_pkey PRIMARY KEY (id);


--
-- Name: patrocinadores patrocinadores_email_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.patrocinadores
    ADD CONSTRAINT patrocinadores_email_key UNIQUE (email);


--
-- Name: patrocinadores patrocinadores_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.patrocinadores
    ADD CONSTRAINT patrocinadores_pkey PRIMARY KEY (id);


--
-- Name: patrocinios patrocinios_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.patrocinios
    ADD CONSTRAINT patrocinios_pkey PRIMARY KEY (id);


--
-- Name: patrocinadores trg_notificacao_patrocinador_privado; Type: TRIGGER; Schema: public; Owner: admin
--

CREATE TRIGGER trg_notificacao_patrocinador_privado AFTER INSERT ON public.patrocinadores FOR EACH ROW EXECUTE FUNCTION public.inserir_log_novo_patrocinador();


--
-- Name: certificados certificados_autenticador_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.certificados
    ADD CONSTRAINT certificados_autenticador_id_fkey FOREIGN KEY (autenticador_id) REFERENCES public.autenticadores(id);


--
-- Name: certificados certificados_evento_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.certificados
    ADD CONSTRAINT certificados_evento_id_fkey FOREIGN KEY (evento_id) REFERENCES public.eventos(id);


--
-- Name: certificados certificados_participante_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.certificados
    ADD CONSTRAINT certificados_participante_id_fkey FOREIGN KEY (participante_id) REFERENCES public.participantes(id);


--
-- Name: eventos eventos_local_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.eventos
    ADD CONSTRAINT eventos_local_id_fkey FOREIGN KEY (local_id) REFERENCES public.locais(id);


--
-- Name: eventos eventos_organizador_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.eventos
    ADD CONSTRAINT eventos_organizador_id_fkey FOREIGN KEY (organizador_id) REFERENCES public.organizadores(id);


--
-- Name: inscricao inscricao_participante_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.inscricao
    ADD CONSTRAINT inscricao_participante_id_fkey FOREIGN KEY (participante_id) REFERENCES public.participantes(id);


--
-- Name: participantes participantes_endereco_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.participantes
    ADD CONSTRAINT participantes_endereco_id_fkey FOREIGN KEY (endereco_id) REFERENCES public.enderecos(id) ON DELETE CASCADE;


--
-- Name: patrocinios patrocinios_evento_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.patrocinios
    ADD CONSTRAINT patrocinios_evento_id_fkey FOREIGN KEY (evento_id) REFERENCES public.eventos(id) ON DELETE CASCADE;


--
-- Name: patrocinios patrocinios_patrocinador_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.patrocinios
    ADD CONSTRAINT patrocinios_patrocinador_id_fkey FOREIGN KEY (patrocinador_id) REFERENCES public.patrocinadores(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

