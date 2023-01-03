## Szaktan konzolos verzió (az első szaktan!)

This is a Python and Sql based nutrition management software for hungarian soil experts.

## Fontos tudnivalók:
<br/>
 * A fixtable_csv/ fájlok módosítása, frissítése után, még a program futtatása előtt törölni kell a szaktan.db-t!<br/><br/>
 * A techn.csv-ben a 'Tnov_nev' oszlopába a növények neveit kis betűvel kell beírni!<br/><br/>
 * A 'tabla_lab' és 'tabla_techn' oszlopban szereplő azonosítók, meg kell hogy egyezenek az input csv fájlokban!<br/><br/>

## Futtatás

```$ pipenv shell```

```$ pipenv install -r requirements.txt```

```$ python szaktan_con.py```

Az eredmények a Szaktan_eredmények mappában!