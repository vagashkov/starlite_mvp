--
-- PostgreSQL database dump
--

-- Dumped from database version 14.2
-- Dumped by pg_dump version 14.4

-- Started on 2022-11-13 18:15:07 +03

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 3579 (class 1262 OID 21664)
-- Name: staff; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE staff WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'en_US.UTF-8';


ALTER DATABASE staff OWNER TO postgres;

\connect staff

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 209 (class 1259 OID 21665)
-- Name: employees; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.employees (
    id integer NOT NULL,
    name character varying NOT NULL,
    post character varying NOT NULL
);


ALTER TABLE public.employees OWNER TO postgres;

--
-- TOC entry 3573 (class 0 OID 21665)
-- Dependencies: 209
-- Data for Name: employees; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.employees VALUES (1, 'Ivan Marakasoff', 'CEO');
INSERT INTO public.employees VALUES (2, 'Top Lawyer', 'CLO');
INSERT INTO public.employees VALUES (3, 'Kilobit Megabitov', 'CIO');
INSERT INTO public.employees VALUES (4, 'Giveme Moremoney', 'CFO');
INSERT INTO public.employees VALUES (5, 'Chair fon Table', 'CAO');


--
-- TOC entry 3433 (class 2606 OID 21671)
-- Name: employees employees_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_pkey PRIMARY KEY (id);


--
-- TOC entry 3580 (class 0 OID 0)
-- Dependencies: 209
-- Name: TABLE employees; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.employees TO staff;


-- Completed on 2022-11-13 18:15:07 +03

--
-- PostgreSQL database dump complete
--

