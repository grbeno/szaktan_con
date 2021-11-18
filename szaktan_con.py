import sqlite3, os, time
import csvjob, szamitasok, szaktan_pdf #, fix_tablak # saját

""" 0. START - """

# Aktuális mappában...
#os.chdir("c:\\Python\Python38-32\\szaktan_\\")
dir = os.getcwd()
labor_csv = "%s\\input_csv\\labor.csv" % dir
techn_csv = "%s\\input_csv\\techn.csv" % dir
input_tabla = [labor_csv,techn_csv]

# INPUT ellenőrzés -alapszintű
for fajl in input_tabla:
    try:
        f = open(fajl, "rb")
    except:
        print("Hibás vagy nem létező fájl!\nAz input fájlt a következőképpen kell megadni: %s \n" % fajl)
        print("Lépjen ki, majd a szükséges módosítások után indítsa újra a programot! Kilépéshez nyomja le az Entert!")
        input()
        os._exit(1)
    else:
        f.close()

# Ideiglenes táblák
auto_tabla = ["labor","techn","labor_A","Minositesek_npk","Minositesek_mikroelem","Tapanyag_igenyek","Nmax","Szaktan_nezet"]

# ADATBÁZIS létrehozás
conn = sqlite3.connect("szaktan.db")
c = conn.cursor()

# Szaktan nézettábla: futtatásonként megújul
for t in auto_tabla:
    try:
        c.execute("SELECT * FROM %s" % t)
    except:
        continue
    else:
        c.execute("DROP TABLE %s" % t)

# FIX táblák ellenőrzése
try:
    c.execute(""" SELECT Termohelyi_kat_tapell,Fajlagos_Tig,Nmax_Param_nev,NitratMax,Mikro_param,N_adag 
                    FROM TapEll_Min 
                    INNER JOIN Fajlagos_T ON TapEll_Min.Id = Fajlagos_T.Id
                    INNER JOIN Nmax_Min ON TapEll_Min.Id = Nmax_Min.Id
                    INNER JOIN Nmax_T ON TapEll_Min.Id = Nmax_T.Id
                    INNER JOIN Mikro_Min ON TapEll_Min.Id = Mikro_Min.Id
                    INNER JOIN Megosztas_T ON TapEll_Min.Id = Megosztas_T.Id """)
except:
    import fix_tablak # saját # Hibát fog jelezni ha nem minden tábla hiányzik! -> szaktan.db törlése
else:
    pass # ha léteznek elmarad az import!

""" 1. ADATTÁBLÁK FELVITELE ADATBÁZISBA - labor és technológiai adatok """

# CREATE - labor tábla # -> Ha nem kell átlag Blokk TEXT helyett INTEGER!
create_labor = """ CREATE TABLE IF NOT EXISTS labor (
                Id INTEGER PRIMARY KEY NOT NULL, 
                Tabla_lab INTEGER, 
                Kozig TEXT, 
                Blokk TEXT, 
                Hrsz TEXT, 
                Ter REAL, 
                Minta_jele TEXT, 
                PH_KCL REAL, 
                KA INTEGER, 
                SO REAL, 
                MESZ REAL, 
                HUMUSZ REAL, 
                S REAL, 
                NO3 REAL,
                P2O5 REAL, 
                K2O REAL, 
                NA REAL, 
                MG REAL, 
                ZN REAL, 
                CU REAL, 
                MN REAL
                ); """

c.execute(create_labor)

# INSERT INTO - labor tábla
insert_labor = """ INSERT INTO labor (
                Tabla_lab,Kozig,Blokk,Hrsz,Ter,Minta_jele,PH_KCL,KA,SO,MESZ,HUMUSZ,S,NO3,P2O5,K2O,NA,MG,ZN,CU,MN
                ) 
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?); """

labor = csvjob.csvin(input_tabla[0]) # csv fájl feldolgozása
c.executemany(insert_labor, csvjob.tcsere(labor))

# CREATE - technológia tábla
create_techn = """CREATE TABLE IF NOT EXISTS techn (
                Id INTEGER PRIMARY KEY NOT NULL, 
                Tabla_techn TEXT, 
                Termohelyi_kat_techn INTEGER, 
                Tnov_nev TEXT, 
                Tnov_term REAL,
                Evet_nev TEXT, 
                Evet_term REAL, 
                Evet_N REAL, 
                Evet_P2O5 REAL, 
                Evet_K2O REAL, 
                Evet_szarlsz INTEGER, 
                Evet_szarlb REAL, 
                Evet_kar REAL, 
                Ontozes REAL, 
                Ontozes_hat REAL,
                Istallotr REAL, 
                Egyb_szervtr REAL, 
                Nitrat_erz INTEGER
                );  """

c.execute(create_techn)

# INSERT INTO - technológia tábla
insert_techn = """ INSERT INTO techn (
                Tabla_techn,Termohelyi_kat_techn,Tnov_nev,Tnov_term,Evet_nev,Evet_term,Evet_N,Evet_P2O5,Evet_K2O,Evet_szarlsz,Evet_szarlb,Evet_kar,Ontozes,Ontozes_hat,Istallotr,Egyb_szervtr,Nitrat_erz
                ) 
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?); """

techn = csvjob.csvin(input_tabla[1]) # csv fájl feldolgozása
c.executemany(insert_techn, csvjob.tcsere(techn)) # tcsere: tizedesvesszőt pontra

""" 2. TÁBLA/PARCELLA ÁTLAGOK KISZÁMíTÁSA - TÁBLÁK AZONOS DIMENZIÓRA HOZÁSA """

# GROUP BY - labor tábla - parcella átlagok kiszámítása # group by Tabla,Hrsz teszt:id
group_atlag = """ SELECT Id,Tabla_lab,Kozig,Blokk,Hrsz,Ter,
                    COUNT(*) as mintaszam,
                    round(AVG(PH_KCL),2) as PH_KCL_A,
                    round(AVG(KA),0) as KA_A,
                    round(AVG(SO),2) as SO_A,
                    round(AVG(MESZ),2) as MESZ_A,
                    round(AVG(HUMUSZ),2) as HUMUSZ_A,
                    round(AVG(S),2) as S_A,
                    round(AVG(NO3),2) as NO3_A,
                    round(AVG(P2O5),2) as P2O_A,
                    round(AVG(K2O),2) as K2O_A,
                    round(AVG(NA),2) as NA_A,
                    round(AVG(MG),2) as MG_A,
                    round(AVG(ZN),2) as ZN_A,
                    round(AVG(CU),2) as CU_A,
                    round(AVG(MN),2) as MN_A
                    FROM labor
                    GROUP BY Tabla_lab
                    ORDER BY Id
                    """

c.execute(group_atlag)

# A SELECT lekérdezés tömbbe másolása
labor_atlagok = c.fetchall()

# CREATE - labor átlagok tábla
create_labor_A = """CREATE TABLE IF NOT EXISTS labor_A ( 
                    Id INTEGER PRIMARY KEY NOT NULL,
                    Id_labor INTEGER NOT NULL,
                    Tabla_lab_A TEXT, 
                    Kozig TEXT, 
                    Blokk TEXT, 
                    Hrsz TEXT, 
                    Ter REAL, 
                    Mintaszam INTEGER,
                    PH_KCL REAL, 
                    KA INTEGER, 
                    SO REAL, 
                    MESZ REAL, 
                    HUMUSZ REAL, 
                    S REAL, 
                    NO3 REAL,
                    P2O5 REAL, 
                    K2O REAL, 
                    NA REAL, 
                    MG REAL, 
                    ZN REAL, 
                    CU REAL, 
                    MN REAL
                );  """

c.execute(create_labor_A)

# INSERT INTO - labor_A tábla
insert_labor_A = """ INSERT INTO labor_A (
                Id_labor,Tabla_lab_A,Kozig,Blokk,Hrsz,Ter,Mintaszam,PH_KCL,KA,SO,MESZ,HUMUSZ,S,NO3,P2O5,K2O,NA,MG,ZN,CU,MN
                ) 
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?); """

c.executemany(insert_labor_A, labor_atlagok)


""" 3. MINŐSíTÉSEK (N,P,K)-ra """

npk_tapEll = [('Nitrogen','KA','HUMUSZ'),('Foszfor','MESZ','P2O5'),('Kalium','KA','K2O')]
npk_minosites = []

# Tápanyagellátottsági minősítések <- npk_tapEll
for (elem,param1,param2) in npk_tapEll:
    
    # Labor paraméterek lekérdezése pl.: N -> KA,H%
    select_lparam_tapEll = "SELECT %s,%s,Termohelyi_kat_techn FROM labor_A INNER JOIN techn ON labor_A.Id = techn.Id" % (param1,param2)
    c.execute(select_lparam_tapEll)
    lparam_tapEll = c.fetchall()
    temp = []
    
    # Minősítési határértékek lekérdezése
    for (p1,p2,tkat) in lparam_tapEll:
        select_min_npk = "SELECT Lab_param_0,Lab_param_1,Minosites FROM TapEll_Min WHERE TapEll_param='%s' AND Termohelyi_kat_tapell='%s'"  % (elem,tkat)
        c.execute(select_min_npk)
        minTabla_npk = c.fetchall()
        # Minősítések tábla:határértékek <- labor paraméterek(p1,p2)
        temp.append(szamitasok.minosit(minTabla_npk,p1,p2,elem))
    
    npk_minosites.append(tuple(temp))  

# CREATE - Minositesek_npk tabla
create_minositesek = """ CREATE TABLE IF NOT EXISTS Minositesek_npk (
                Id INTEGER PRIMARY KEY NOT NULL,
                Nitrogen_Min TEXT, 
                Foszfor_Min TEXT, 
                Kalium_Min TEXT 
                ); """

c.execute(create_minositesek)

# INSERT INTO - Minositesek_npk tabla
insert_minositesek = """ INSERT INTO Minositesek_npk (
                Nitrogen_Min,Foszfor_Min,Kalium_Min
                ) 
                VALUES (?,?,?); """

c.executemany(insert_minositesek, csvjob.transpose(npk_minosites)) # transzponált lista 


""" 4. MINŐSíTÉSEK MIKROELEMEKRE - (Mg,Zn,Mn,Cu) """

mikroelem = [("Magnézium","MG"),("Cink","ZN"),("Mangán","PH_KCL"),("Réz","HUMUSZ")]
MgZn_min, MnCu = [], []

for (elem,lparam) in mikroelem:
    
    # Kötöttség és egyéb labor paraméterek...
    select_lparam_mikro = "SELECT KA,%s FROM labor_A" % lparam
    c.execute(select_lparam_mikro)
    lparam_mikro = c.fetchall()
    
    # Kötöttség intervallumok
    select_p1div_mikro = "SELECT KA FROM Mikro_Min WHERE Mikro_param='%s'" % elem
    c.execute(select_p1div_mikro)
    p1div = c.fetchall()
    
    temp_MgZn_min, temp_MnCu = [], []

    for (p1,p2) in lparam_mikro: # p1 = KA
        
        # (p1) Kötöttség intervallum lekérdezése
        get_ka_mikro = szamitasok.intv_mikro(p1div,p1)
       
        # (p2) Másodlagos laborparaméter divíziók Mg,Zn,pH,H%
        select_p2div = "SELECT Lparam FROM Mikro_Min WHERE Mikro_param='%s' AND KA='%s'" % (elem,get_ka_mikro)
        c.execute(select_p2div)
        p2div = c.fetchall()
        intv_p2 = szamitasok.intv_mikro(p2div,p2,elem)
    
        # Minősítések lekérdezése -> Mg,Zn - Határértékek lekérdezése -> Mn,Cu
        select_min_mikro = "SELECT Minosites FROM Mikro_Min WHERE Mikro_param='%s' AND KA='%s' AND Lparam='%s'" % (elem,get_ka_mikro,intv_p2)
        c.execute(select_min_mikro)
        minosites_mikro = c.fetchone()
        if minosites_mikro == None: # ha nincs eredmény
            minosites_mikro = '0'
        
        # Magnézium és Cink - Mangán és Réz külön tömbökbe!
        if elem == "Magnézium" or elem == "Cink":
            temp_MgZn_min.append(minosites_mikro[0])
        else:
            temp_MnCu.append(minosites_mikro[0])

    if elem == "Magnézium" or elem == "Cink":
        MgZn_min.append(tuple(temp_MgZn_min))
    else:
        MnCu.append(tuple(temp_MnCu)) # határértékekkel tér vissza!

""" Magnézium és Réz minősítései """

# labor -> Mn, Cu
select_lparam_mncu = "SELECT MN,CU FROM labor_A"
c.execute(select_lparam_mncu)
lparam_mncu = c.fetchall()

MnCu_min = []
# Mn - minősítés
temp, i = [], 0
for elem in lparam_mncu:
    Mn_min = szamitasok.minosit_MnCu(MnCu[0][i],elem[0],"Mangán")
    temp.append(Mn_min)
    i+=1
MnCu_min.append(tuple(temp))

# Cu - minősítés
temp, i = [], 0
for elem in lparam_mncu:
    Cu_min = szamitasok.minosit_MnCu(MnCu[1][i],elem[1],"Réz")
    temp.append(Cu_min)
    i+=1
MnCu_min.append(tuple(temp))

# CREATE - Minositesek_mikroelem tábla
create_minositesek_mikroelem = """ CREATE TABLE IF NOT EXISTS Minositesek_mikroelem (
                Id INTEGER PRIMARY KEY NOT NULL,
                MG_min TEXT, 
                ZN_min TEXT, 
                MN_min TEXT,
                CU_min TEXT
                ); """

c.execute(create_minositesek_mikroelem)

# INSERT INTO - Minositesek_mikroelem tábla
insert_minositesek_mikroelem = """ INSERT INTO Minositesek_mikroelem (
                MG_min,ZN_min,MN_min,CU_min
                )
                VALUES(?,?,?,?);"""

minositesek_mikroelem_tabla = csvjob.transpose(MgZn_min + MnCu_min) # transzponált összevont listák (Mg,Zn + Mn,Cu minősítések)
c.executemany(insert_minositesek_mikroelem,minositesek_mikroelem_tabla) 


""" 5. NÖVÉNYEK FAJLAGOS TÁPANYAGIGÉNYE """
""" 5.1. Bruttó tápanyagigény kiszámítása """

npk_btig = [("Nitrogen","Nitrogen_Min"),("Foszfor","Foszfor_Min"),("Kalium","Kalium_Min")]
ftig = []

# Adatok lekérdezése fajlagos tápanyagigény meghatározásához
for (elem,npk_min) in npk_btig:
    select_npk_btig = "SELECT Tnov_nev, Termohelyi_kat_techn, %s FROM techn INNER JOIN Minositesek_npk ON techn.Id = Minositesek_npk.Id" % npk_min
    c.execute(select_npk_btig)
    adat_npk_btig = c.fetchall()
    temp = []

    # Fajlagos tápanyagigények lekérdezése
    for (tnov,tkat,min_) in adat_npk_btig:
        select_fajlagos = "SELECT Fajlagos_Tig FROM Fajlagos_T WHERE (Noveny='%s' AND Elem='%s' AND Termohelyi_kat='%s' AND Minosites='%s')" % (tnov,elem,tkat,min_)
        c.execute(select_fajlagos)
        ertek_fajlagos = c.fetchone()
        if ertek_fajlagos == None: # ha nincs eredmény
            ertek_fajlagos = '0'
        temp.append(float(csvjob.tofloat(ertek_fajlagos[0]))) # -> tuple 0.elemét lebegőpontossá!

    ftig.append(tuple(temp))

# Növény termésterve -> Tnov_term
select_tnovt = "SELECT Tnov_term FROM techn"
c.execute(select_tnovt)
adat_tnovt = c.fetchall()
tnovt = [float(i[0]) for i in adat_tnovt]

# Bruttó tápanyagigény = N,P,K_fajlagos * Tnov_term * 10
btig = szamitasok.btig_szorzas(ftig,tnovt)

""" 5.2. Nettó tápanyagigény kiszámítása """
# Korrekciós értékek meghatározása...

# Nettó tápanyagigények számítása...

# CREATE - Tápanyagigények tábla
create_tapanyag_igenyek = """ CREATE TABLE IF NOT EXISTS Tapanyag_igenyek (
                Id INTEGER PRIMARY KEY NOT NULL,
                Nitrogen_Fajlagos REAL, 
                Foszfor_Fajlagos REAL, 
                Kalium_Fajlagos REAL,
                Nitrogen_Btig REAL,
                Foszfor_Btig REAL, 
                Kalium_Btig REAL 
                ); """

c.execute(create_tapanyag_igenyek)

# INSERT INTO - Tápanyagigények tábla
insert_tapanyag_igenyek = """ INSERT INTO Tapanyag_igenyek (
                Nitrogen_Fajlagos,Foszfor_Fajlagos,Kalium_Fajlagos,Nitrogen_Btig,Foszfor_Btig,Kalium_Btig
                ) 
                VALUES (?,?,?,?,?,?); """

tig_tabla = csvjob.transpose(ftig + btig) # transzponált összevont listák (fajlagos + bruttó)
c.executemany(insert_tapanyag_igenyek,tig_tabla ) 


""" 6. NITROGÉN MŰTRÁGYA ADAG MAXIMUMÁNAK MEGHATÁROZÁSA  """

# Laborparaméterek Nmax meghatározáshoz 
select_lparam_Nmax = "SELECT KA,HUMUSZ,Termohelyi_kat_techn,Tnov_nev FROM labor_A INNER JOIN techn ON labor_A.Id = techn.Id"
c.execute(select_lparam_Nmax)
lparam_Nmax = c.fetchall()

minosites_Nmax_list = []
nmax = []

for (p1,p2,tkat,tnov) in lparam_Nmax:
    
    # Minősítések Nitrogén maximumok meghatározásához
    select_minTabla_Nmax = "SELECT Nmax_Lab_param_0,Nmax_Lab_param_1,Nmax_Minosites FROM Nmax_Min WHERE Termohelyi_kat='%s'"  % tkat
    c.execute(select_minTabla_Nmax)
    minTabla_Nmax = c.fetchall()
    min_Nmax = szamitasok.minosit(minTabla_Nmax,p1,p2)
    minosites_Nmax_list.append(min_Nmax) # minősítések külön tömbben is!
    
    # Nitrogén maximumok meghatározása
    select_Nmax_T = "SELECT NitratMax FROM Nmax_T WHERE (Termohelyi_kat='%s' AND Noveny='%s' AND Minosites='%s')" % (tkat,tnov,min_Nmax)
    c.execute(select_Nmax_T)
    ertek_Nmax_T = c.fetchone()
    if ertek_Nmax_T == None:
        ertek_Nmax_T = '-'
    nmax.append(ertek_Nmax_T[0])

nmax = [tuple(nmax)]

# CREATE - Nitrogén maximumok tábla
create_nmax = "CREATE TABLE IF NOT EXISTS Nmax (Id INTEGER PRIMARY KEY NOT NULL,Nmax_eredmeny REAL );"
c.execute(create_nmax)

# INSERT INTO - Nitrogén maximumok tábla
insert_nmax = "INSERT INTO Nmax (Nmax_eredmeny) VALUES (?);"

nmax_tabla = csvjob.transpose(nmax) # transzponált összevont listák (nmax)
c.executemany(insert_nmax, nmax_tabla ) 


""" 7. MEGOSZTÁS TÁBLÁZATOK """

# Laborparaméterek
select_lparam_megosztas = "SELECT Termohelyi_kat_techn,Tnov_nev,KA FROM techn INNER JOIN labor_A ON techn.Id = labor_A.id"
c.execute(select_lparam_megosztas)
lparam_megosztas = c.fetchall()
megosztas = [] # pdf-re!


for (tkat,tnov,ka) in lparam_megosztas:
    # Kötöttség divíziók
    select_ka_div = "SELECT KA_intv FROM Megosztas_T WHERE Noveny='%s' AND Termohelyi_kat='%s'" % (tnov,tkat)
    c.execute(select_ka_div)
    ka_div = c.fetchall()
    get_ka_megosztas = szamitasok.intv_mikro(ka_div,ka)
    # Megosztások <- növény,thk,KA
    select_megosztas = "SELECT Megosztas FROM Megosztas_T WHERE Noveny='%s' AND Termohelyi_kat='%s' AND KA_intv='%s'" % (tnov,tkat,get_ka_megosztas) #Evszak,N_adag,
    c.execute(select_megosztas)
    mgszts = c.fetchall()
    if len(mgszts) == 0: # ha nincs eredmény
        mgszts = ('-', '-', '-', '-', '-')
    temp = []
    for j in range(len(mgszts)):
        temp.append(mgszts[j][0])
    megosztas.append(temp)

#print(megosztasok) # teszt


""" 8. EREDMÉNYKÖZLŐLAP - PDF szerkesztés """

# A pdf-re írandó adatok lekérdezése
select_szaktan_adat = """ SELECT Tnov_nev,
                            Kozig,
                            Hrsz,
                            Blokk,
                            Tabla_lab_A,
                            Ter,
                            Nitrat_erz,
                            Nitrogen_Min,
                            Foszfor_Min,
                            Kalium_Min,
                            MG_min,
                            MN_min,
                            CU_min,
                            ZN_min,
                            Termohelyi_kat_techn,
                            Nitrogen_Fajlagos,
                            Foszfor_Fajlagos,
                            Kalium_Fajlagos,
                            Tnov_term,
                            Nitrogen_Btig,
                            Foszfor_Btig,
                            Kalium_Btig,
                            Nmax_eredmeny,
                            Mintaszam
                        FROM labor_A 
                            INNER JOIN techn ON labor_A.Id = techn.Id 
                            INNER JOIN Minositesek_npk ON labor_A.Id = Minositesek_npk.Id 
                            INNER JOIN Nmax ON labor_A.Id = Nmax.Id 
                            INNER JOIN Minositesek_mikroelem ON labor_A.Id = Minositesek_mikroelem.Id 
                            INNER JOIN Tapanyag_igenyek ON labor_A.Id = Tapanyag_igenyek.Id; """

c.execute(select_szaktan_adat)
szaktan_adat = c.fetchall()
#print(szaktan_adat) # teszt

# CREATE - Szaktan nézettábla
create_szaktan_nezet = """CREATE TABLE IF NOT EXISTS Szaktan_nezet (
                Id INTEGER PRIMARY KEY NOT NULL,
                Tnov_nev TEXT,
                Kozig TEXT,
                Hrsz TEXT,
                Blokk TEXT,
                Tabla_lab_A TEXT,
                Ter REAL,
                Nitrat_erz INTEGER,
                Nitrogen_Min TEXT,
                Foszfor_Min TEXT,
                Kalium_Min TEXT,
                MG_min TEXT,
                MN_min TEXT,
                CU_min TEXT,
                ZN_min TEXT,
                Termohelyi_kat_techn INTEGER,
                Nitrogen_Fajlagos REAL,
                Foszfor_Fajlagos REAL,
                Kalium_Fajlagos REAL,
                Tnov_term REAL,
                Nitrogen_Btig REAL,
                Foszfor_Btig REAL,
                Kalium_Btig REAL,
                Nmax_eredmeny REAL,
                Mintaszam INTEGER
                ); """

c.execute(create_szaktan_nezet)

# INSERT INTO - Szaktan nézettábla
insert_szaktan_nezet = """ INSERT INTO Szaktan_nezet (
                Tnov_nev,Kozig,Hrsz,Blokk,Tabla_lab_A,Ter,Nitrat_erz,Nitrogen_Min,Foszfor_Min,Kalium_Min,MG_min,MN_min,CU_min,ZN_min,Termohelyi_kat_techn,Nitrogen_Fajlagos,Foszfor_Fajlagos,Kalium_Fajlagos,Tnov_term,Nitrogen_Btig,Foszfor_Btig,Kalium_Btig,Nmax_eredmeny,Mintaszam
                ) 
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?); """ 

c.executemany(insert_szaktan_nezet,szaktan_adat) 

""" OUTPUT: PDF elkészítése """

# Pdf szerkesztő függvény
szaktan_pdf.pdf_szerkeszt(szaktan_adat,megosztas)


conn.commit()
conn.close()

print("\nProgram vége: A pdf eredménylapokat a <Szaktan_eredmenyek> mappában, az adatokat a <szaktan.db> fájlban keresse!\n")
#input()
time.sleep(2.5)