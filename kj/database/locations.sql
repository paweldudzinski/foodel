--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

--
-- Data for Name: locations; Type: TABLE DATA; Schema: public; Owner: p13730_foodel
--

COPY locations (id, name, woj_id, lg_id) FROM stdin;
32	Zachodniopomorskie	\N	pl
2	Dolnośląskie	\N	pl
4	Kujawsko-pomorskie	\N	pl
6	Lubelskie	\N	pl
8	Lubuskie	\N	pl
10	Łódzkie	\N	pl
12	Małopolskie	\N	pl
14	Mazowieckie	\N	pl
16	Opolskie	\N	pl
18	Podkarpackie	\N	pl
20	Podlaskie	\N	pl
22	Pomorskie	\N	pl
24	Śląskie	\N	pl
26	Świętokrzyskie	\N	pl
28	Warmińsko-mazurskie	\N	pl
30	Wielkopolskie	\N	pl
32100	Karlino	32	pl
32101	Tychowo	32	pl
32102	Choszczno	32	pl
32103	Drawno	32	pl
32104	Pełczyce	32	pl
32105	Recz	32	pl
32106	Czaplinek	32	pl
32107	Drawsko Pomorskie	32	pl
32108	Kalisz Pomorski	32	pl
32109	Złocieniec	32	pl
32110	Goleniów	32	pl
32111	Maszewo	32	pl
32112	Nowogard	32	pl
32113	Gryfice	32	pl
32114	Płoty	32	pl
32115	Trzebiatów	32	pl
32116	Cedynia	32	pl
32117	Chojna	32	pl
32118	Gryfino	32	pl
32119	Mieszkowice	32	pl
32120	Moryń	32	pl
32121	Trzcińsko-Zdrój	32	pl
32122	Dziwnów	32	pl
32123	Golczewo	32	pl
32124	Kamień Pomorski	32	pl
32125	Międzyzdroje	32	pl
32126	Wolin	32	pl
32127	Gościno	32	pl
32128	Bobolice	32	pl
32129	Polanów	32	pl
32130	Sianów	32	pl
32131	Barlinek	32	pl
32132	Dębno	32	pl
32133	Myślibórz	32	pl
32134	Nowe Warpno	32	pl
32135	Police	32	pl
32136	Lipiany	32	pl
32137	Pyrzyce	32	pl
32138	Chociwel	32	pl
32139	Dobrzany	32	pl
32140	Ińsko	32	pl
32141	Suchań	32	pl
32142	Barwice	32	pl
32143	Biały Bór	32	pl
32144	Borne Sulinowo	32	pl
32145	Połczyn-Zdrój	32	pl
32146	Człopa	32	pl
32147	Mirosławiec	32	pl
32148	Tuczno	32	pl
32149	Dobra	32	pl
32150	Łobez	32	pl
32151	Resko	32	pl
32152	Węgorzyno	32	pl
32153	Koszalin	32	pl
32154	Szczecin	32	pl
32155	Świnoujście	32	pl
2100	Nowogrodziec	2	pl
2101	Niemcza	2	pl
2102	Góra	2	pl
2103	Wąsosz	2	pl
2104	Bolków	2	pl
2105	Lubawka	2	pl
2106	Bystrzyca Kłodzka	2	pl
2107	Lądek-Zdrój	2	pl
2108	Międzylesie	2	pl
2109	Radków	2	pl
2110	Stronie Śląskie	2	pl
2111	Szczytna	2	pl
2112	Prochowice	2	pl
2113	Leśna	2	pl
2114	Olszyna	2	pl
2115	Ścinawa	2	pl
2116	Gryfów Śląski	2	pl
2117	Lubomierz	2	pl
2118	Lwówek Śląski	2	pl
2119	Mirsk	2	pl
2120	Wleń	2	pl
2121	Milicz	2	pl
2122	Bierutów	2	pl
2123	Międzybórz	2	pl
2124	Syców	2	pl
2125	Twardogóra	2	pl
2126	Jelcz-Laskowice	2	pl
2127	Chocianów	2	pl
2128	Polkowice	2	pl
2129	Przemków	2	pl
2130	Strzelin	2	pl
2131	Wiązów	2	pl
2132	Środa Śląska	2	pl
2133	Jaworzyna Śląska	2	pl
2134	Strzegom	2	pl
2135	Żarów	2	pl
2136	Oborniki Śląskie	2	pl
2137	Prusice	2	pl
2138	Trzebnica	2	pl
2139	Żmigród	2	pl
2140	Głuszyca	2	pl
2141	Mieroszów	2	pl
2142	Brzeg Dolny	2	pl
2143	Wołów	2	pl
2144	Kąty Wrocławskie	2	pl
2145	Sobótka	2	pl
2146	Siechnice	2	pl
2147	Bardo	2	pl
2148	Ząbkowice Śląskie	2	pl
2149	Ziębice	2	pl
2150	Złoty Stok	2	pl
2151	Bogatynia	2	pl
2152	Pieńsk	2	pl
2153	Węgliniec	2	pl
2154	Świerzawa	2	pl
2155	Jelenia Góra	2	pl
2156	Legnica	2	pl
2157	Wrocław	2	pl
2158	Wałbrzych	2	pl
4100	Górzno	4	pl
4101	Jabłonowo Pomorskie	4	pl
4102	Koronowo	4	pl
4103	Solec Kujawski	4	pl
4104	Kowalewo Pomorskie	4	pl
4105	Łasin	4	pl
4106	Radzyń Chełmiński	4	pl
4107	Gniewkowo	4	pl
4108	Janikowo	4	pl
4109	Kruszwica	4	pl
4110	Pakość	4	pl
4111	Dobrzyń nad Wisłą	4	pl
4112	Skępe	4	pl
4113	Mogilno	4	pl
4114	Strzelno	4	pl
4115	Kcynia	4	pl
4116	Mrocza	4	pl
4117	Nakło nad Notecią	4	pl
4118	Szubin	4	pl
4119	Piotrków Kujawski	4	pl
4120	Kamień Krajeński	4	pl
4121	Sępólno Krajeńskie	4	pl
4122	Więcbork	4	pl
4123	Nowe	4	pl
4124	Świecie	4	pl
4125	Tuchola	4	pl
4126	Brześć Kujawski	4	pl
4127	Chodecz	4	pl
4128	Izbica Kujawska	4	pl
4129	Lubień Kujawski	4	pl
4130	Lubraniec	4	pl
4131	Barcin	4	pl
4132	Janowiec Wielkopolski	4	pl
4133	Łabiszyn	4	pl
4134	Żnin	4	pl
4135	Bydgoszcz	4	pl
4136	Grudziądz	4	pl
4137	Toruń	4	pl
4138	Włocławek	4	pl
6100	Frampol	6	pl
6101	Józefów	6	pl
6102	Tarnogród	6	pl
6103	Janów Lubelski	6	pl
6104	Annopol	6	pl
6105	Kock	6	pl
6106	Ostrów Lubelski	6	pl
6107	Bełżyce	6	pl
6108	Bychawa	6	pl
6109	Łęczna	6	pl
6110	Opole Lubelskie	6	pl
6111	Poniatowa	6	pl
6112	Parczew	6	pl
6113	Kazimierz Dolny	6	pl
6114	Nałęczów	6	pl
6115	Ryki	6	pl
6116	Piaski	6	pl
6117	Łaszczów	6	pl
6118	Tyszowce	6	pl
6119	Krasnobród	6	pl
6120	Szczebrzeszyn	6	pl
6121	Zwierzyniec	6	pl
6122	Biała Podlaska	6	pl
6123	Chełm	6	pl
6124	Lublin	6	pl
6125	Zamość	6	pl
8100	Witnica	8	pl
8101	Krosno Odrzańskie	8	pl
8102	Międzyrzecz	8	pl
8103	Skwierzyna	8	pl
8104	Trzciel	8	pl
8105	Bytom Odrzański	8	pl
8106	Kożuchów	8	pl
8107	Nowe Miasteczko	8	pl
8108	Cybinka	8	pl
8109	Ośno Lubuskie	8	pl
8110	Rzepin	8	pl
8111	Słubice	8	pl
8112	Dobiegniew	8	pl
8113	Drezdenko	8	pl
8114	Strzelce Krajeńskie	8	pl
8115	Lubniewice	8	pl
8116	Sulęcin	8	pl
8117	Torzym	8	pl
8118	Świebodzin	8	pl
8119	Zbąszynek	8	pl
8120	Babimost	8	pl
8121	Czerwieńsk	8	pl
8122	Kargowa	8	pl
8123	Nowogród Bobrzański	8	pl
8124	Sulechów	8	pl
8125	Iłowa	8	pl
8126	Małomice	8	pl
8127	Szprotawa	8	pl
8128	Jasień	8	pl
8129	Lubsko	8	pl
8130	Sława	8	pl
8131	Szlichtyngowa	8	pl
8132	Wschowa	8	pl
8133	Gorzów Wielkopolski	8	pl
8134	Zielona Góra	8	pl
10100	Zelów	10	pl
10101	Krośniewice	10	pl
10102	Żychlin	10	pl
10103	Łask	10	pl
10104	Koluszki	10	pl
10105	Rzgów	10	pl
10106	Tuszyn	10	pl
10107	Drzewica	10	pl
10108	Opoczno	10	pl
10109	Działoszyn	10	pl
10110	Pajęczno	10	pl
10111	Sulejów	10	pl
10112	Wolbórz	10	pl
10113	Poddębice	10	pl
10114	Uniejów	10	pl
10115	Kamieńsk	10	pl
10116	Przedbórz	10	pl
10117	Biała Rawska	10	pl
10118	Błaszki	10	pl
10119	Warta	10	pl
10120	Złoczew	10	pl
10121	Wieluń	10	pl
10122	Wieruszów	10	pl
10123	Szadek	10	pl
10124	Aleksandrów Łódzki	10	pl
10125	Stryków	10	pl
10126	Łódź	10	pl
10127	Piotrków Trybunalski	10	pl
10128	Skierniewice	10	pl
12100	Nowy Wiśnicz	12	pl
12101	Brzesko	12	pl
12102	Czchów	12	pl
12103	Alwernia	12	pl
12104	Chrzanów	12	pl
12105	Libiąż	12	pl
12106	Trzebinia	12	pl
12107	Dąbrowa Tarnowska	12	pl
12108	Szczucin	12	pl
12109	Biecz	12	pl
12110	Bobowa	12	pl
12111	Krzeszowice	12	pl
12112	Skała	12	pl
12113	Skawina	12	pl
12114	Słomniki	12	pl
12115	Świątniki Górne	12	pl
12116	Miechów	12	pl
12117	Dobczyce	12	pl
12118	Myślenice	12	pl
12119	Sułkowice	12	pl
12120	Krynica-Zdrój	12	pl
12121	Muszyna	12	pl
12122	Piwniczna-Zdrój	12	pl
12123	Stary Sącz	12	pl
12124	Szczawnica	12	pl
12125	Rabka-Zdrój	12	pl
12126	Olkusz	12	pl
12127	Wolbrom	12	pl
12128	Brzeszcze	12	pl
12129	Chełmek	12	pl
12130	Kęty	12	pl
12131	Zator	12	pl
12132	Nowe Brzesko	12	pl
12133	Proszowice	12	pl
12134	Maków Podhalański	12	pl
12135	Ciężkowice	12	pl
12136	Radłów	12	pl
12137	Ryglice	12	pl
12138	Tuchów	12	pl
12139	Wojnicz	12	pl
12140	Zakliczyn	12	pl
12141	Żabno	12	pl
12142	Andrychów	12	pl
12143	Kalwaria Zebrzydowska	12	pl
12144	Wadowice	12	pl
12145	Niepołomice	12	pl
12146	Wieliczka	12	pl
12147	Kraków	12	pl
12148	Nowy Sącz	12	pl
12149	Tarnów	12	pl
14100	Białobrzegi	14	pl
14101	Wyśmierzyce	14	pl
14102	Glinojeck	14	pl
14103	Pilawa	14	pl
14104	Żelechów	14	pl
14105	Grodzisk Mazowiecki	14	pl
14106	Grójec	14	pl
14107	Mogielnica	14	pl
14108	Nowe Miasto nad Pilicą	14	pl
14109	Warka	14	pl
14110	Kozienice	14	pl
14111	Serock	14	pl
14112	Lipsko	14	pl
14113	Łosice	14	pl
14114	Różan	14	pl
14115	Halinów	14	pl
14116	Kałuszyn	14	pl
14117	Nasielsk	14	pl
14118	Zakroczym	14	pl
14119	Myszyniec	14	pl
14120	Brok	14	pl
14121	Karczew	14	pl
14122	Góra Kalwaria	14	pl
14123	Konstancin-Jeziorna	14	pl
14124	Piaseczno	14	pl
14125	Tarczyn	14	pl
14126	Drobin	14	pl
14127	Gąbin	14	pl
14128	Wyszogród	14	pl
14129	Brwinów	14	pl
14130	Chorzele	14	pl
14131	Przysucha	14	pl
14132	Pułtusk	14	pl
14133	Iłża	14	pl
14134	Skaryszew	14	pl
14135	Mordy	14	pl
14136	Kosów Lacki	14	pl
14137	Szydłowiec	14	pl
14138	Błonie	14	pl
14139	Łomianki	14	pl
14140	Ożarów Mazowiecki	14	pl
14141	Łochów	14	pl
14142	Radzymin	14	pl
14143	Tłuszcz	14	pl
14144	Wołomin	14	pl
14145	Wyszków	14	pl
14146	Zwoleń	14	pl
14147	Bieżuń	14	pl
14148	Żuromin	14	pl
14149	Mszczonów	14	pl
14150	Ostrołęka	14	pl
14151	Płock	14	pl
14152	Radom	14	pl
14153	Siedlce	14	pl
14154	Warszawa	14	pl
16100	Grodków	16	pl
16101	Lewin Brzeski	16	pl
16102	Baborów	16	pl
16103	Głubczyce	16	pl
16104	Kietrz	16	pl
16105	Byczyna	16	pl
16106	Kluczbork	16	pl
16107	Wołczyn	16	pl
16108	Gogolin	16	pl
16109	Krapkowice	16	pl
16110	Zdzieszowice	16	pl
16111	Namysłów	16	pl
16112	Głuchołazy	16	pl
16113	Korfantów	16	pl
16114	Nysa	16	pl
16115	Otmuchów	16	pl
16116	Paczków	16	pl
16117	Dobrodzień	16	pl
16118	Gorzów Śląski	16	pl
16119	Olesno	16	pl
16120	Praszka	16	pl
16121	Niemodlin	16	pl
16122	Ozimek	16	pl
16123	Prószków	16	pl
16124	Biała	16	pl
16125	Głogówek	16	pl
16126	Prudnik	16	pl
16127	Kolonowskie	16	pl
16128	Leśnica	16	pl
16129	Strzelce Opolskie	16	pl
16130	Ujazd	16	pl
16131	Zawadzkie	16	pl
16132	Opole	16	pl
18100	Ustrzyki Dolne	18	pl
18101	Brzozów	18	pl
18102	Brzostek	18	pl
18103	Pilzno	18	pl
18104	Pruchnik	18	pl
18105	Kołaczyce	18	pl
18106	Kolbuszowa	18	pl
18107	Dukla	18	pl
18108	Iwonicz-Zdrój	18	pl
18109	Jedlicze	18	pl
18110	Rymanów	18	pl
18111	Nowa Sarzyna	18	pl
18112	Cieszanów	18	pl
18113	Narol	18	pl
18114	Oleszyce	18	pl
18115	Przecław	18	pl
18116	Radomyśl Wielki	18	pl
18117	Nisko	18	pl
18118	Rudnik nad Sanem	18	pl
18119	Ulanów	18	pl
18120	Kańczuga	18	pl
18121	Sieniawa	18	pl
18122	Ropczyce	18	pl
18123	Sędziszów Małopolski	18	pl
18124	Błażowa	18	pl
18125	Boguchwała	18	pl
18126	Głogów Małopolski	18	pl
18127	Sokołów Małopolski	18	pl
18128	Tyczyn	18	pl
18129	Zagórz	18	pl
18130	Strzyżów	18	pl
18131	Baranów Sandomierski	18	pl
18132	Nowa Dęba	18	pl
18133	Lesko	18	pl
18134	Krosno	18	pl
18135	Przemyśl	18	pl
18136	Rzeszów	18	pl
18137	Tarnobrzeg	18	pl
20100	Lipsk	20	pl
20101	Choroszcz	20	pl
20102	Czarna Białostocka	20	pl
20103	Łapy	20	pl
20104	Michałowo	20	pl
20105	Supraśl	20	pl
20106	Suraż	20	pl
20107	Tykocin	20	pl
20108	Wasilków	20	pl
20109	Zabłudów	20	pl
20110	Rajgród	20	pl
20111	Szczuczyn	20	pl
20112	Kleszczele	20	pl
20113	Stawiski	20	pl
20114	Jedwabne	20	pl
20115	Nowogród	20	pl
20116	Goniądz	20	pl
20117	Knyszyn	20	pl
20118	Mońki	20	pl
20119	Drohiczyn	20	pl
20120	Dąbrowa Białostocka	20	pl
20121	Krynki	20	pl
20122	Sokółka	20	pl
20123	Suchowola	20	pl
20124	Ciechanowiec	20	pl
20125	Czyżew	20	pl
20126	Szepietowo	20	pl
20127	Białystok	20	pl
20128	Łomża	20	pl
20129	Suwałki	20	pl
22100	Bytów	22	pl
22101	Miastko	22	pl
22102	Brusy	22	pl
22103	Czersk	22	pl
22104	Czarne	22	pl
22105	Debrzno	22	pl
22106	Kartuzy	22	pl
22107	Żukowo	22	pl
22108	Prabuty	22	pl
22109	Nowy Staw	22	pl
22110	Nowy Dwór Gdański	22	pl
22111	Kępice	22	pl
22112	Skarszewy	22	pl
22113	Gniew	22	pl
22114	Pelplin	22	pl
22115	Dzierzgoń	22	pl
22116	Sztum	22	pl
22117	Gdańsk	22	pl
22118	Gdynia	22	pl
22119	Słupsk	22	pl
22120	Sopot	22	pl
24100	Siewierz	24	pl
24101	Czechowice-Dziedzice	24	pl
24102	Wilamowice	24	pl
24103	Skoczów	24	pl
24104	Strumień	24	pl
24105	Blachownia	24	pl
24106	Koniecpol	24	pl
24107	Sośnicowice	24	pl
24108	Toszek	24	pl
24109	Kłobuck	24	pl
24110	Krzepice	24	pl
24111	Woźniki	24	pl
24112	Koziegłowy	24	pl
24113	Żarki	24	pl
24114	Pszczyna	24	pl
24115	Krzanowice	24	pl
24116	Kuźnia Raciborska	24	pl
24117	Czerwionka-Leszczyny	24	pl
24118	Łazy	24	pl
24119	Ogrodzieniec	24	pl
24120	Pilica	24	pl
24121	Szczekociny	24	pl
24122	Bielsko-Biała	24	pl
24123	Bytom	24	pl
24124	Chorzów	24	pl
24125	Częstochowa	24	pl
24126	Dąbrowa Górnicza	24	pl
24127	Gliwice	24	pl
24128	Jastrzębie-Zdrój	24	pl
24129	Jaworzno	24	pl
24130	Katowice	24	pl
24131	Mysłowice	24	pl
24132	Piekary Śląskie	24	pl
24133	Ruda Śląska	24	pl
24134	Rybnik	24	pl
24135	Siemianowice Śląskie	24	pl
24136	Sosnowiec	24	pl
24137	Świętochłowice	24	pl
24138	Tychy	24	pl
24139	Zabrze	24	pl
24140	Żory	24	pl
26100	Busko-Zdrój	26	pl
26101	Jędrzejów	26	pl
26102	Małogoszcz	26	pl
26103	Sędziszów	26	pl
26104	Kazimierza Wielka	26	pl
26105	Skalbmierz	26	pl
26106	Bodzentyn	26	pl
26107	Chęciny	26	pl
26108	Chmielnik	26	pl
26109	Daleszyce	26	pl
26110	Końskie	26	pl
26111	Stąporków	26	pl
26112	Opatów	26	pl
26113	Ożarów	26	pl
26114	Ćmielów	26	pl
26115	Kunów	26	pl
26116	Działoszyce	26	pl
26117	Pińczów	26	pl
26118	Koprzywnica	26	pl
26119	Zawichost	26	pl
26120	Suchedniów	26	pl
26121	Wąchock	26	pl
26122	Osiek	26	pl
26123	Połaniec	26	pl
26124	Staszów	26	pl
26125	Włoszczowa	26	pl
26126	Kielce	26	pl
28100	Bisztynek	28	pl
28101	Sępopol	28	pl
28102	Frombork	28	pl
28103	Pieniężno	28	pl
28104	Lidzbark	28	pl
28105	Młynary	28	pl
28106	Pasłęk	28	pl
28107	Tolkmicko	28	pl
28108	Ryn	28	pl
28109	Kisielice	28	pl
28110	Susz	28	pl
28111	Zalewo	28	pl
28112	Korsze	28	pl
28113	Reszel	28	pl
28114	Orneta	28	pl
28115	Mikołajki	28	pl
28116	Nidzica	28	pl
28117	Olecko	28	pl
28118	Barczewo	28	pl
28119	Biskupiec	28	pl
28120	Dobre Miasto	28	pl
28121	Jeziorany	28	pl
28122	Olsztynek	28	pl
28123	Miłakowo	28	pl
28124	Miłomłyn	28	pl
28125	Morąg	28	pl
28126	Biała Piska	28	pl
28127	Orzysz	28	pl
28128	Pisz	28	pl
28129	Ruciane-Nida	28	pl
28130	Pasym	28	pl
28131	Gołdap	28	pl
28132	Węgorzewo	28	pl
28133	Elbląg	28	pl
28134	Olsztyn	28	pl
30100	Margonin	30	pl
30101	Szamocin	30	pl
30102	Krzyż Wielkopolski	30	pl
30103	Trzcianka	30	pl
30104	Wieleń	30	pl
30105	Czerniejewo	30	pl
30106	Kłecko	30	pl
30107	Trzemeszno	30	pl
30108	Witkowo	30	pl
30109	Borek Wielkopolski	30	pl
30110	Gostyń	30	pl
30111	Krobia	30	pl
30112	Pogorzela	30	pl
30113	Poniec	30	pl
30114	Grodzisk Wielkopolski	30	pl
30115	Rakoniewice	30	pl
30116	Wielichowo	30	pl
30117	Jarocin	30	pl
30118	Żerków	30	pl
30119	Stawiszyn	30	pl
30120	Kępno	30	pl
30121	Dąbie	30	pl
30122	Kłodawa	30	pl
30123	Przedecz	30	pl
30124	Golina	30	pl
30125	Kleczew	30	pl
30126	Rychwał	30	pl
30127	Sompolno	30	pl
30128	Ślesin	30	pl
30129	Czempiń	30	pl
30130	Krzywiń	30	pl
30131	Śmigiel	30	pl
30132	Kobylin	30	pl
30133	Koźmin Wielkopolski	30	pl
30134	Krotoszyn	30	pl
30135	Zduny	30	pl
30136	Osieczna	30	pl
30137	Rydzyna	30	pl
30138	Międzychód	30	pl
30139	Sieraków	30	pl
30140	Lwówek	30	pl
30141	Nowy Tomyśl	30	pl
30142	Opalenica	30	pl
30143	Zbąszyń	30	pl
30144	Oborniki	30	pl
30145	Rogoźno	30	pl
30146	Nowe Skalmierzyce	30	pl
30147	Odolanów	30	pl
30148	Raszków	30	pl
30149	Grabów nad Prosną	30	pl
30150	Mikstat	30	pl
30151	Ostrzeszów	30	pl
30152	Łobżenica	30	pl
30153	Ujście	30	pl
30154	Wyrzysk	30	pl
30155	Wysoka	30	pl
30156	Pleszew	30	pl
30157	Buk	30	pl
30158	Kostrzyn	30	pl
30159	Kórnik	30	pl
30160	Mosina	30	pl
30161	Murowana Goślina	30	pl
30162	Pobiedziska	30	pl
30163	Stęszew	30	pl
30164	Swarzędz	30	pl
30165	Bojanowo	30	pl
30166	Jutrosin	30	pl
30167	Miejska Górka	30	pl
30168	Rawicz	30	pl
30169	Zagórów	30	pl
30170	Ostroróg	30	pl
30171	Pniewy	30	pl
30172	Szamotuły	30	pl
30173	Wronki	30	pl
30174	Środa Wielkopolska	30	pl
30175	Dolsk	30	pl
30176	Książ Wielkopolski	30	pl
30177	Śrem	30	pl
30178	Dobra	30	pl
30179	Tuliszków	30	pl
30180	Gołańcz	30	pl
30181	Skoki	30	pl
30182	Wolsztyn	30	pl
30183	Miłosław	30	pl
30184	Nekla	30	pl
30185	Pyzdry	30	pl
30186	Września	30	pl
30187	Jastrowie	30	pl
30188	Krajenka	30	pl
30189	Okonek	30	pl
30190	Kalisz	30	pl
30191	Konin	30	pl
30192	Leszno	30	pl
30193	Poznań	30	pl
\.


--
-- Name: locations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: p13730_foodel
--

SELECT pg_catalog.setval('locations_id_seq', 4, true);


--
-- PostgreSQL database dump complete
--
