# Jukola

#### Virhe per osuus
| Osuus  | Virhesekunnit per tunti |
| ------------- | ------------- |
| 1  | 170s  |
| 2  | 192s  |
| 3  | 187s  |
| 4  | 224s  |
| 5  | 221s  |
| 6  | 197s  |
| 7  | 180s  |

--> Lyhyimmillä osuuksilla tehdään eniten virhettä


#### Virhe per rastinumero
| Rastinumero  | Virhesekunnit | Rastivälin kesto | Virhesekunnit per tunti |
| ------------- | ------------- | ------------- | ------------- |
| 1   | 16s  | 529s | 109s |
| 2   | 12s  | 221s | 210s |
| 3   |  8s  | 168s | 183s |
| 4   | 12s  | 219s | 197s |
| 5   | 11s  | 185s | 226s |
| 6   |  9s  | 178s | 199s |
| 7   | 12s  | 199s | 223s |
| 8   | 11s  | 196s | 212s |
| 9   | 12s  | 185s | 241s |
| 10  | 12s  | 200s | 228s |
| 11  | 10s  | 172s | 213s |
| 12  | 10s  | 202s | 186s |
| 13  |  8s  | 178s | 178s |
| 14  | 11s  | 208s | 196s |
| 15  |  9s  | 168s | 212s |
| 16  |  9s  | 174s | 197s |


#### Virhe per hajontatyyppi
| rastin tyyppi  | Virhesekunnit per tunti |
| ------------- | ------------- |
| Yhteinen -> yhteinen | 163s  |
| Hajonta -> yhteinen   | 172s  |
| Yhteinen -> Hajonta   | 220s  |
| Hajonta -> Hajonta   | 225s  |

--> Hajontarasteille tehdään 30% enemmän virhettä


#### Virhe per joukkueen sijoitus
![Virhe per joukkueen sijoitus](https://github.com/senttula/Jukola_analyses/blob/main/mistake_per_team_placement_.png)

--> kärkijoukkueilla ~2,5 minuuttia virhettä per tunti, muilla alle 4.

#### Virhe per vuosi
| Vuosi  | Virhesekunnit per tunti |
| ------------- | ------------- |
| 2000  | 156s  |
| 2001  | 183s  |
| 2002  | 210s  |
| 2003  | 169s  |
| 2004  | 128s  |
| 2005  | 170s  |
| 2006  | 214s  |
| 2007  | 273s  |
| 2008  | 210s  |
| 2009  | 156s  |
| 2010  | 274s  |
| 2011  | 172s  |
| 2012  | 180s  |
| 2013  | 174s  |
| 2014  | 172s  |
| 2015  | 192s  |
| 2016  | 186s  |
| 2017  | 168s  |
| 2018  | 206s  |
| 2019  | 210s  |
| 2021  | 216s  |

--> Lapua ja Kytäjä vaikeimpia


#### Potentiaalisten voittajien määrä vuosittain
| Vuosi  | Voittajakandidaattien määrä |
| ------------- | ------------- |
| 2000  | 25  |
| 2001  | 22  |
| 2002  | 26  |
| 2003  | 28  |
| 2004  |  7  |
| 2005  | 14  |
| 2006  | 27  |
| 2007  | 38  |
| 2008  | 32  |
| 2009  | 33  |
| 2010  | 18  |
| 2011  | 11  |
| 2012  | 23  |
| 2013  | 20  |
| 2014  | 10  |
| 2015  | 21  |
| 2016  | 50  |
| 2017  |  9  |
| 2018  | 14  |
| 2019  | 18  |
| 2021  | 17  |


#### Letkajuoksun määrä per osuus
| Osuus  | Letkajuoksu % |
| ------------- | ------------- |
| 1  | 89% |
| 2  | 68% |
| 3  | 56% |
| 4  | 40% |
| 5  | 33% |
| 6  | 31% |
| 7  | 35% |



Analyyseihin otettu mukaan vain henkilöt joiden osuussijoitus tai joukkueen sijoitus on alle 70.

Väliajat ladattu [Jukolan](https://results.jukola.com/tulokset/fi/) sivuilta ja [prosessoitu](https://github.com/senttula/Jukola_analyses/blob/main/xml_to_csv.py)

Analyysien [koodi](https://github.com/senttula/Jukola_analyses/blob/main/main.py)
