# Osakepörssi

## Sovelluksen toiminnot
  * Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
  * Käyttäjä pystyy listaamaan uusia yrityksiä pörssiin.
  * Käyttäjä pystyy valitsemaan yritystä listatessa tälle yhden luokittelun.
  * Käyttäjä pystyy muokkaamaan ja poistamaan listaamiansa yrityksiä.
  * Käyttäjä näkee sovellukseen listatut yritykset.
  * Käyttäjä pystyy hakemaan yrityksiä hakusanalla.
  * Käyttäjä pystyy tekemään yrityksen osakkeista myynti- ja ostotarjouksia.
  * Sovelluksessa on sivut joissa näytetään olemassa olevat myynti- ja ostotarjoukset.
  * Sovelluksessa on käyttäjäsivut, joissa näkee käyttäjän listaamat yritykset.
  * Käyttäjäsivulla näytetään kuinka paljon käyttäjällä on voimassa olevia myynti- tai ostotarjouksia.

## Sovelluksen asennus

Asenna `flask`-kirjasto:

```
$ pip install flask
```

Luo tietokannan taulut:

```
$ sqlite3 database.db < schema.sql
```

Voit käynnistää sovelluksen näin:

```
$ flask run
```

## Sovelluksen toiminta suurella tietomäärällä

Skriptin seed.py avulla sovellukseen luodaan miljoona yritystä ja 10 osto- ja myyntitarjousta per yritys.
Voit luoda testidataa näin:
```
$ python seed.py
```

Ilman indeksointia etusivun lataaminen vie noin 30 sekuntia per sivu tekijän tietokoneella. 
Ilman indeksointia kunkin käyttäjän sivun lataaminen vie noin 6 sekuntia tekijä tietokoneella.
Ilman indeksointia myynti- ja ostotarjous sivujen lataaminen vie noin 1.5-2 sekuntia per sivu tekijän tietokoneella. 

Kun tietokantaan luodaan indeksit helpottamaan yritysten hakua id:n perusteella sell_order ja buy_order tauluista, nopeutuu etusivun sivujen lataaminen noin 0.3 sekunttiin.
Kun tietokantaan luodaan myös indeksit helpottamaan käyttäjien hakua id:n perusteella sell_order ja buy_order tauluista, nopeutuu käyttäjäsivujen lataaminen noin 0.5-1 sekunttiin.
Näiden indeksien lisääminen ei vaikuttanut myynti- ja ostotarjous sivujen latausnopeuksiin.

Indeksit on luotu seuraavasti ja ne lisätään tietokantaan schema.sql tiedoston mukana:
```
CREATE INDEX idx_sell_order_companies ON sell_orders (company_id);
CREATE INDEX idx_buy_order_companies ON buy_orders (company_id);
CREATE INDEX idx_sell_order_users ON sell_orders (seller_id);
CREATE INDEX idx_buy_order_users ON buy_orders (buyer_id);
```
