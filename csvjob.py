import csv

""" 1. ADATTÁBLÁK FELVITELE ADATBÁZISBA - labor és technológiai adatok """

def csvin(fname):
    """ Beolvassa a csv fájl adatait egy tömbbe -> list:*tuple"""
    with open(fname, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader) # 1.sort kihagyja
        tabla_adat = [tuple(i) for i in reader]
    return tabla_adat


""" 2. ÁTLAGOK KISZÁMíTÁSA - TÁBLÁK AZONOS DIMENZIÓRA HOZÁSA """

def tofloat(inp,delim1=',',delim2='.'):
    """ tcsere segéd függvénye!
        Tizedeselválasztókat(.,) és '<'-t lecseréli a törteknél. 
        Egészeknél nem cserél '<'-t !!! <- figyelni """ 
    try:
        res = float(inp)
        # Törtek visszaalakítása!
        if delim1 == '.' and delim2 == ',':
            res = str(inp).replace(delim1,delim2).strip('<')
    except:
        res = ""
        if inp.find(delim1)!=-1:
            res = inp.replace(delim1,delim2).strip('<') 
        try: 
            float(res) # csak a törtekre!
        except ValueError:
            return inp
        else:
            return res
    else:
        return res

def tcsere(tabla_adat,delim1=',',delim2='.'):
    """ Tizedeselválasztókat cseréli """
    temp = [list(sor) for sor in tabla_adat] # listává konvertál a módosíthatóság miatt
    for i in range(len(tabla_adat)):
        j = 0
        for j in range(len(tabla_adat[i])):
            temp[i][j] = tofloat(tabla_adat[i][j],delim1,delim2)
    tabla_adat = [tuple(sor) for sor in temp] # vissza tuple-ba
    return tabla_adat


""" 3. MINŐSíTÉSEK (N,P,K) -ra """

def transpose(adat):
    """ Több dimenziós tömböt transzponál """
    data_T = []
    result = map(list, zip(*adat))
    for r in result:
        data_T.append(tuple(r))
    return data_T
