import sqlite3, os
import csvjob

""" FIX - nem változó ADATTÁBLÁK FELVITELE """

# ADATBÁZIS létrehozás
conn = sqlite3.connect("szaktan.db")
c = conn.cursor()

# Útvonalak
dir = os.getcwd()
tapell_csv = "%s\\fixtabla_csv\\TapEll_Min.csv" % dir
fajlagos_csv = "%s\\fixtabla_csv\\fajlagos_T.csv" % dir
nmaxm_csv = "%s\\fixtabla_csv\\Nmax_Min.csv" % dir
nmaxt_csv = "%s\\fixtabla_csv\\Nmax_T.csv" % dir
mikrom_csv = "%s\\fixtabla_csv\\Mikro_Min.csv" % dir
megoszt_csv = "%s\\fixtabla_csv\\Megosztas_T.csv" % dir

# CREATE - NPK Tápanyagellátottság-minősítések tábla
create_TapEll_Min = """CREATE TABLE IF NOT EXISTS TapEll_Min (
                Id INTEGER PRIMARY KEY NOT NULL, 
                TapEll_param TEXT, 
                Termohelyi_kat_tapell INTEGER,  
                Lab_param_0 TEXT, 
                Lab_param_1 TEXT,
                Minosites TEXT, 
                Param_nev TEXT
                );  """

c.execute(create_TapEll_Min)

# INSERT INTO - NPK Tápanyagellátottság-minősítések tábla
insert_TapEll_Min = """ INSERT INTO TapEll_Min (
                Id,TapEll_param,Termohelyi_kat_tapell,Lab_param_0,Lab_param_1,Minosites,Param_nev
                ) 
                VALUES (?,?,?,?,?,?,?); """

TapEll_Min = csvjob.csvin(tapell_csv) # csv fájl feldolgozása
c.executemany(insert_TapEll_Min, TapEll_Min)

# CREATE - Fajlagos tápanyagigények tábla
create_fajlagos_T = """ CREATE TABLE IF NOT EXISTS Fajlagos_T (
                Id INTEGER PRIMARY KEY NOT NULL, 
                Noveny TEXT, 
                Elem TEXT,
                Termohelyi_kat INTEGER, 
                Minosites TEXT,
                Fajlagos_Tig REAL
                );  """

c.execute(create_fajlagos_T)

# INSERT INTO - Fajlagos tápanyagigények tábla
insert_fajlagos_T = """ INSERT INTO Fajlagos_T (
                Id,Noveny,Elem,Termohelyi_kat,Minosites,Fajlagos_Tig
                ) 
                VALUES (?,?,?,?,?,?); """ 

fajlagos_T = csvjob.csvin(fajlagos_csv) # csv fájl feldolgozása
c.executemany(insert_fajlagos_T, fajlagos_T)

# CREATE - Minősítések tábla nitrogén maximum meghatározásához
create_Nmax_Min = """ CREATE TABLE IF NOT EXISTS Nmax_Min (
                Id INTEGER PRIMARY KEY NOT NULL, 
                Termohelyi_kat INTEGER,
                Nmax_Lab_param_0 TEXT, 
                Nmax_Lab_param_1 TEXT,
                Nmax_Minosites TEXT,
                Nmax_Param_nev TEXT
                );  """

c.execute(create_Nmax_Min)

# INSERT INTO - Minősítések tábla nitrogén maximum meghatározásához
insert_Nmax_Min = """ INSERT INTO Nmax_Min (
                Id,Termohelyi_kat,Nmax_Lab_param_0,Nmax_Lab_param_1,Nmax_Minosites,Nmax_Param_nev
                ) 
                VALUES (?,?,?,?,?,?); """ 

Nmax_Min = csvjob.csvin(nmaxm_csv) # csv fájl feldolgozása
c.executemany(insert_Nmax_Min, Nmax_Min)

# CREATE - Tábla nitrogén maximum meghatározásához
create_Nmax_T = """ CREATE TABLE IF NOT EXISTS Nmax_T (
                Id INTEGER PRIMARY KEY NOT NULL, 
                Termohelyi_kat INTEGER,
                Noveny TEXT, 
                Minosites TEXT,
                NitratMax INTEGER
                );  """

c.execute(create_Nmax_T)

# INSERT INTO - Tábla nitrogén maximum meghatározásához
insert_Nmax_T = """ INSERT INTO Nmax_T (
                Id,Termohelyi_kat,Noveny,Minosites,NitratMax
                ) 
                VALUES (?,?,?,?,?); """ 

Nmax_T = csvjob.csvin(nmaxt_csv) # csv fájl feldolgozása
c.executemany(insert_Nmax_T, Nmax_T)

# CREATE - Mikroelemek minősítése
create_Mikro_Min = """ CREATE TABLE IF NOT EXISTS Mikro_Min (
                Id INTEGER PRIMARY KEY NOT NULL, 
                Mikro_param TEXT,
                KA TEXT, 
                Lparam TEXT,
                Minosites TEXT,
                Param_nev TEXT
                );  """

c.execute(create_Mikro_Min)

# INSERT INTO - Mikroelemek minősítése
insert_Mikro_Min = """ INSERT INTO Mikro_Min (
                Id,Mikro_param,KA,Lparam,Minosites,Param_nev
                ) 
                VALUES (?,?,?,?,?,?); """ 

Mikro_Min = csvjob.csvin(mikrom_csv) # csv fájl feldolgozása
c.executemany(insert_Mikro_Min, Mikro_Min)

# CREATE - Megosztás tábla
create_Megosztas_T = """ CREATE TABLE IF NOT EXISTS Megosztas_T (
                Id INTEGER PRIMARY KEY NOT NULL, 
                Noveny TEXT,
                Termohelyi_kat TEXT, 
                KA_intv TEXT,
                Evszak TEXT,
                N_adag TEXT,
                Megosztas TEXT
                );  """

c.execute(create_Megosztas_T)

# INSERT INTO - Megosztás tábla
insert_Megosztas_T = """ INSERT INTO Megosztas_T (
                Id,Noveny,Termohelyi_kat,KA_intv,Evszak,N_adag,Megosztas
                ) 
                VALUES (?,?,?,?,?,?,?); """ 

Megosztas_T = csvjob.csvin(megoszt_csv) # csv fájl feldolgozása
c.executemany(insert_Megosztas_T, Megosztas_T)


conn.commit()
conn.close()