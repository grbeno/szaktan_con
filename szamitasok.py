
""" SEGÉDFÜGGVÉNYEK - MINŐSíTÉSEK-hez """

def split_intv(intv):
    """ "," alapján szétválasztja a karakterláncot, 
        majd konvertál: ->float ->int """
    lista = intv.split(",")
    for i in range(2):
        if lista[i].find('.')!=-1:
            lista[i] = float(lista[i])
        else:
            lista[i] = int(lista[i]) 
    return (lista[0],lista[1])

def is_btw(lower,upper,p):
    """ Megvizsgálja, hogy p a lower és upper intervallumban van-e? """
    if(p >= lower and p <= upper):
        return True

def err_msg(elem,p1):
    """ 1. labor paraméter(p1) ellenőrzése """
    if elem == "Foszfor":
        return "<hiba!> Mész: %s - Az érték túl nagy!" % p1
    else:
        return "<hiba!> KA: %s - Az érték túl nagy!" % p1

def strtof_lparam(p1,p2,elem):
    """ p1 -> 1 tizedes(.1) p2 ha nem N -> (.0), ha N -> (.2) """
    p1 = round(float(p1),1)
    if elem != "Nitrogen":
        p2 = round(float(p2))
    else:
        p2 = round(float(p2),2)
    return (p1,p2)


""" 3. MINŐSíTÉSEK (N,P,K)-ra """

def minosit(adat,p1,p2,elem=None):
    """ A beérkező adatokra vonatkozóan (labor paraméterek: p1,p2) input ellenőrzés szükséges. 
        Érvénytelen adat esetén (pl. szöveg) hiba történik! [ValueError] 
        *elem: opcionális argumentum, ha nincs megadva (None), 
        akkor a nitrogén maximumhoz (6.) szükséges minősítéssel tér vissza a függvény! """

    # Tizedesjegyek <- labor paraméterek
    if elem != None:
        lparam = strtof_lparam(p1,p2,elem)
        p1 = lparam[0]
        p2 = lparam[1]
    else:
        p1 = round(float(p1))
        p2 = round(float(p2),2)

    step = 0
    for (intv_0,intv_1,minosites) in adat:   
        # Határértékek szétválasztása
        left = split_intv(intv_0)
        right = split_intv(intv_1)   
        
        # 0. sor (KA,MESZ) - bal vagy jobb? -> döntés
        if step == 0:
            if is_btw(left[0],left[1],p1):
                col = 0
            elif is_btw(right[0],right[1],p1):
                col = 1
            else:
                return err_msg(elem,p1)
        
        # 1. sortól...
        if step > 0:
            # A col/0,1/-/bal,jobb/ oszlopot vizsgálja
            if col == 0:
                if is_btw(left[0],left[1],p2):
                    return minosites       
            elif col == 1:
                if is_btw(right[0],right[1],p2):
                    return minosites               
        
        step += 1
    
    # utolsó intervallum maximuma
    if elem != None:
        if p2 > left[1] or p2 > right[1]:
            return "sok"


""" 4. MINŐSíTÉSEK MIKROELEMEKRE - (Mg,Zn,Mn,Cu) """

def intv_mikro(adat,p,elem=None): # p = KA + Mg,Zn,pH,H%
    """ Mg, Zn -> minősítések - Mn, Cu -> határértékek 
        ha elem=None, akkor 0-ra kerekít. <- KA """
    if p==0: # ha laborparaméter=0
        return '0'
    if elem != None:
        if elem == "Cink" or elem == "Réz":
            p = round(float(p),1)
        else:
            p = round(float(p))
    else:
        round(float(p)) # KA
    res= ""
    for sor in adat:
        # p melyik intervallumban van -> return: minősítés/intervallum
        intv = sor[0].split(',')
        if is_btw(float(intv[0]),float(intv[1]),p) == True:
            res = sor[0]   
    if res != "":    
        return res

def minosit_MnCu(adat,p,elem): # p = Mn,Cu
    """ Minősítések Mn, Cu határértékek alapján 
        (lásd: minosit_mikro -> minősítések) """
    if p==0: # ha laborparaméter=0
        return '0'
    if elem == "Réz":
        p = round(float(p),1) # Cu
    else:
        p = round(float(p)) # Mn
    # p melyik intervallumban van -> return: minősítés
    #for sor in adat:
    intv = adat.split(',')
    if is_btw(float(intv[0]),float(intv[1]),p) == True:
        return "nem megfelelő"
    else:
        return "megfelelő"
        
    return '0'


""" 5. NÖVÉNYEK FAJLAGOS TÁPANYAGIGÉNYE"""

""" 5.1. Bruttó tápanyagigény kiszámítása """
def btig_szorzas(a,b):
    """ 2 tömb szorzása - nem egyenlő terjedelmű tömbök esetén <- a = 2dim, b = 1dim! """
    res = []
    dim = 10 # argumentumként, ha szükséges!
    for i in range(len(a)):
        temp = []
        for j in range(len(a[i])):
            temp.append(round(float(a[i][j])*float(b[j]),2)*dim)
        res.append(tuple(temp))
    return res

""" 5.. Korrekció kiszámítása """

""" 5.. Nettó tápanyagigény kiszámítása """