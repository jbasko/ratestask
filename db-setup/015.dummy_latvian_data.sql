--
-- Additional data to explore some edge cases
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: ports; Type: TABLE DATA; Schema: tasks; Owner: -
--

COPY ports (code, name, parent_slug) FROM stdin;
LVVEN	Ventspils	baltic_main
LVLPX	Liepaja	baltic_main
\.

--
-- Data for Name: prices; Type: TABLE DATA; Schema: tasks; Owner: -
--

COPY prices (orig_code, dest_code, day, price) FROM stdin;
LVVEN	LVLPX	2016-01-01	300
LVVEN	LVRIX	2016-01-01	350
LVLPX	LVRIX	2016-01-01	600
LVVEN	FIHEL	2016-01-01	800
LVVEN	FIRAU	2016-01-01	850
LVVEN	FIKTK	2016-01-01	875
LVLPX	FIHEL	2016-01-01	820
LVLPX	FIRAU	2016-01-01	810
LVLPX	FIKTK	2016-01-01	880
\.
