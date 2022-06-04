# Venla

#### Virhe per osuus
| Osuus  | Virhesekunnit per tunti |
| ------------- | ------------- |
| 1  | 198s  |
| 2  | 227s  |
| 3  | 215s  |
| 4  | 218s  |

#### Virhe per rastinumero
| Rastinumero  | Virhesekunnit | Rastivälin kesto | Virhesekunnit per tunti |
| ------------- | ------------- | ------------- | ------------- |
| 1   | 21s  | 445s | 171s |
| 2   | 11s  | 191s | 207s |
| 3   | 11s  | 161s | 254s |
| 4   | 12s  | 165s | 262s |
| 5   |  9s  | 184s | 181s |
| 6   | 10s  | 205s | 191s |
| 7   | 11s  | 167s | 237s |
| 8   | 14s  | 188s | 270s |
| 9   | 12s  | 196s | 231s |
| 10  | 12s  | 151s | 300s |
| 11  |  9s  | 157s | 220s |
| 12  |  8s  | 155s | 201s |
| 13  |  9s  | 145s | 241s |
| 14  |  7s  | 141s | 180s |
| 15  |  6s  | 150s | 165s |
| 16  |  7s  | 157s | 160s |


#### Virhe per hajontatyyppi
| rastin tyyppi  | Virhesekunnit per tunti |
| ------------- | ------------- |
| Yhteinen -> yhteinen | 155s  |
| Hajonta -> yhteinen   | 159s  |
| Yhteinen -> Hajonta   | 264s  |
| Hajonta -> Hajonta   | 303s  |

--> Hajontarasteille tehdään 80% enemmän virhettä


#### Virhe per joukkueen sijoitus
![Virhe per joukkueen sijoitus](https://github.com/senttula/Jukola_analyses/blob/main/mistake_per_team_placement_ve.png)

--> kärkijoukkueilla ~2,5 minuuttia virhettä per tunti, muilla neljän luokkaa.

#### Virhe per vuosi
| Vuosi  | Virhesekunnit per tunti |
| ------------- | ------------- |
| 2000  | 210s  |
| 2001  | 319s  |
| 2002  | 228s  |
| 2003  | 212s  |
| 2004  | 109s  |
| 2005  | 240s  |
| 2006  | 232s  |
| 2007  | 334s  |
| 2008  | 231s  |
| 2009  | 170s  |
| 2010  | 260s  |
| 2011  | 205s  |
| 2012  | 153s  |
| 2013  | 180s  |
| 2014  | 174s  |
| 2015  | 183s  |
| 2016  | 183s  |
| 2017  | 243s  |
| 2018  | 192s  |
| 2019  | 167s  |
| 2021  | 222s  |


#### Potentiaalisten voittajien määrä vuosittain
| Vuosi  | Voittajakandidaattien määrä |
| ------------- | ------------- |
| 2000  |  24  |
| 2001  |   8  |
| 2002  |  35  |
| 2003  |  12  |
| 2004  |  11  |
| 2005  |  14  |
| 2006  |   5  |
| 2007  | 110  |
| 2008  |  38  |
| 2009  |  28  |
| 2010  |  11  |
| 2011  |  18  |
| 2012  |  12  |
| 2013  |  14  |
| 2014  |   3  |
| 2015  |  27  |
| 2016  |  57  |
| 2017  |  27  |
| 2018  |  12  |
| 2019  |  27  |
| 2021  |  17  |

--> Virkiä Jukolassa monella joukkuueella oli voiton mahdollisuudet

#### Letkajuoksun määrä per osuus
| Osuus  | Letkajuoksu % |
| ------------- | ------------- |
| 1  | 87% |
| 2  | 37% |
| 3  | 22% |
| 4  | 16% |



Analyyseihin otettu mukaan vain henkilöt joiden osuussijoitus tai joukkueen sijoitus on alle 70.

Väliajat ladattu [Jukolan](https://results.jukola.com/tulokset/fi/) sivuilta ja [prosessoitu](https://github.com/senttula/Jukola_analyses/blob/main/xml_to_csv.py)

Analyysien [koodi](https://github.com/senttula/Jukola_analyses/blob/main/main.py)
