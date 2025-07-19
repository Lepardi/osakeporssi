# Osakepörssi

## Sovelluksen toiminnot
  * Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.  --Toteutettu
  * Käyttäjä pystyy listaamaan uusia yrityksiä pörssiin.  --Toteutettu
  * Käyttäjä pystyy valitsemaan yritystä listatessa tälle yhden luokittelun.  --Toteutettu
  * Käyttäjä pystyy muokkaamaan ja poistamaan listaamiansa yrityksiä.  --Toteutettu
  * Käyttäjä näkee sovellukseen listatut yritykset.  --Toteutettu
  * Käyttäjä pystyy hakemaan yrityksiä hakusanalla.  --Toteutettu
  * Käyttäjä pystyy tekemään yrityksen osakkeista myynti- ja ostotarjouksia. --Ei toteutettu
  * Sovelluksessa on sivu jossa näytetään olemassa olevat myynti- ja ostotarjoukset.  --Ei toteutettu
  * Sovelluksessa on käyttäjäsivut, joissa näkee käyttäjän listaamat yritykset.   --Toteutettu
  * Käyttäjäsivulla näytetään kuinka paljon käyttäjällä on voimassa olevia myynti- tai ostotarjouksia. --Ei toteutettu

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