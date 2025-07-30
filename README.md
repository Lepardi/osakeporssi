# Osakepörssi

## Sovelluksen toiminnot
  * Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
  * Käyttäjä pystyy listaamaan uusia yrityksiä pörssiin.
  * Käyttäjä pystyy valitsemaan yritystä listatessa tälle yhden luokittelun.
  * Käyttäjä pystyy muokkaamaan ja poistamaan listaamiansa yrityksiä.
  * Käyttäjä näkee sovellukseen listatut yritykset.
  * Käyttäjä pystyy hakemaan yrityksiä hakusanalla.
  * Käyttäjä pystyy tekemään yrityksen osakkeista myynti- ja ostotarjouksia.
  * Sovelluksessa on sivu jossa näytetään olemassa olevat myynti- ja ostotarjoukset.
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