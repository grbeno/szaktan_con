import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

""" INDEX -> adatsor[index] -> pdf
0: Tnov_nev,
1: Kozig,
2: Hrsz,
3: Blokk,
4: Tabla_lab_A,
5: Ter,
6: Nitrat_erz,
7: Nitrogen_Min,
8: Foszfor_Min,
9: Kalium_Min,
10: MG_min,
11: MN_min,
12: CU_min,
13: ZN_min,
14: Termohelyi_kat_techn,
15: Nitrogen_Fajlagos,
16: Foszfor_Fajlagos,
17: Kalium_Fajlagos,
18: Tnov_term,
19: Nitrogen_Btig,
20: Foszfor_Btig,
21: Kalium_Btig,
22: Nmax_eredmeny
23: Mintaszam
"""

# Mappa ellenőriz/létrehoz
def add_folder(os,_Path):
    try:
        os.mkdir(_Path)
    except OSError:
        msg_1 = "A %s mappa már létezik!" % os.path.relpath(_Path)
        return msg_1
    else:
        msg_0 = "A %s mappa létrehozva!" % os.path.relpath(_Path)
        return msg_0

def pdf_szerkeszt(szaktan_adat,megosztas):

    # Betűtípusok regisztrálása
    pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
    pdfmetrics.registerFont(TTFont('Verdana-Bold', 'verdanab.ttf'))
    pdfmetrics.registerFont(TTFont('Times', 'Times.ttf'))

    # Szaktan eredmények fő mappa
    dir = "%s\\Szaktan_eredmenyek" % os.getcwd()
    print(add_folder(os,dir))
    
    # Eredménylapok mappa
    foldNum = len(next(os.walk(dir))[1]) # mappák száma -> futtatásonként újat!
    mappa = "eredmenylapok%s" % str(foldNum+1) 
    erl_path = "%s\\%s" % (dir,mappa)
    print(add_folder(os,erl_path))

    m, alm = 80, 50 # oldal margók - alsó margó
    width, height = A4 # 595,275 x 841,889
    i, count = 0, 0

    # Tartalomjegyzék változói
    tjegyzek = [["Közig. név","Hrsz.","Tábla","Növény","Oldal"],] # tj. fejléc
    tjegyzekek = [] # tj. tömbök/oldalak
    netto_hely = 735
    tjCol,tjRow = 99, 15
    max_tjRow = netto_hely/tjRow

    for adatsor in szaktan_adat:

        pdf_name = os.path.join( "%s\\%s.pdf" % (erl_path,str(i + 1))) 
        c = canvas.Canvas(pdf_name) # fájl neve

        # Cím - Alcím
        c.setFont('Verdana-Bold', 14)
        c.drawCentredString((width/2.0), height-50, adatsor[0].capitalize())
        c.setFont('Times', 12)
        title_names = "Műtrágyázási szaktanács MÉM-NAK irányelvek alapján"
        c.drawCentredString((width/2.0), height-70, title_names)

        """ AZONOSíTÓK TÁBLÁZAT """

        # Nitrátérzékenység
        if adatsor[6]==1:
            nitrat="Igen"
        elif adatsor[6]==0:
            nitrat="Nem"
        else:
            nitrat="-"

        # Túl hosszú adatok levágása
        maxLen = 35
        if len(adatsor[2]) > maxLen: # hrsz.
            lista = list(adatsor)
            lista[2] = lista[2][:-(len(adatsor[2])-maxLen)]
            adatsor = tuple(lista)

        adat_azonositok = [
            
            ["Közig. név","Helyrajzi szám","Blokkazonosító"], # "Blokkazonosító helyett Mintaszám", ha nem kell átlag!
            [adatsor[1],adatsor[2],adatsor[3]],
            ["Tábla/parcella azonosító","Terület (ha)","Nitrátérzékenység"],
            [adatsor[4],adatsor[5],nitrat]
        ]
        
        c.setFont('Times-Bold', 12)
        c.drawString(m,height-110,"Azonosítók:")
        
        t_azonositok = Table(adat_azonositok, 145, 17)
        t_azonositok.setStyle(TableStyle([            
            
            #('GRID', (0,0), (-1,-1), 0.5, colors.black), # teszt
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('FONTNAME', (0,0),(-1,-1), 'Times'),
            ('BACKGROUND',(0,0),(-1,-1), colors.whitesmoke),
            ('BACKGROUND',(0,0),(-1,0), colors.lightskyblue),
            ('BACKGROUND',(0,2),(2,-2), colors.lightskyblue),

        ]))

        t_azonositok.wrapOn(c, width,height)
        t_azonositok.drawOn(c, m,height-190)
        
        """ TALAJ KATEGÓRIA """

        talajKat_t = ["0","Csernozjom (mezőségi) talajok","Barna erdőtalajok","Kötött réti, öntés talajok és glejes erdőtalajok","Homok és laza talajok","Szikes talajok","Sekély termőrétegű és erősen lejtős és erodált talajok"]
        talajKat = talajKat_t[adatsor[14]] 
        if adatsor[14]==3 or adatsor[14]==5:
            col2 = 290
        else:
            col2 = 145

        talajKat = [
            
            ["Talaj kategória:",talajKat],["GPS adatok:", str(adatsor[23]) + " mintatér"]
        ] # + mintaszám
        
        t_talajKat = Table(talajKat, [145,col2], 25)
        t_talajKat.setStyle(TableStyle([            
            
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            # 0. oszlop
            ('FONTNAME', (0,0),(0,1), 'Times-Bold'),
            ('FONTSIZE', (0,0),(-1,-1), 11),
            # 1. oszlop
            ('FONTNAME', (1,0),(-1,-1), 'Times'),
            ('BACKGROUND',(1,0),(-1,0), colors.khaki),
            
        ]))

        t_talajKat.wrapOn(c, width,height)
        t_talajKat.drawOn(c, m,height-255)


        """ A TALAJ TÁPANYAGELLÁTOTTSÁGA """

        c.setFont('Times-Bold', 12)
        c.drawString(m,height-280,"A talaj tápanyagellátottsága: ")
        
        tapMin = [
            
            ["Makroelemek","Nitrogén","Foszfor","Kálium"],
            ["",adatsor[7],adatsor[8],adatsor[9]],
        ]

        t_tapMin = Table(tapMin, 105, 17)
        t_tapMin.setStyle(TableStyle([            
            
            #('GRID', (0,0), (-1,-1), 0.5, colors.black), # teszt
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('FONTNAME', (0,0),(-1,-1), 'Times'),
            # 0. oszlop és sor
            ('SPAN',(0,0),(0,1)),
            ('ALIGN', (0,0), (0,1), 'LEFT'),
            ('FONTSIZE', (0,0), (0,1), 11),
            ('BACKGROUND',(0,0),(0,1), colors.white),
            
            ('BACKGROUND',(1,0),(-1,0), colors.palegreen),
            ('BACKGROUND',(1,1),(-1,-1), colors.whitesmoke),
            
        ]))

        t_tapMin.wrapOn(c, width, height)
        t_tapMin.drawOn(c, m,height-330)

        """ MIKROELEMEK """
        # 0-ak helyett üres
        for mik in range(10,14):
            if adatsor[mik]=='0':
                lista = list(adatsor)
                lista[mik] = '-'
                adatsor = tuple(lista)

        mikroM = [
            
            ["Mezo- és\nmikroelemek","Mg","Mn","Cu","Zn"],
            ["",adatsor[10],adatsor[11],adatsor[12],adatsor[13]],
        ]
        
        t_mikroM = Table(mikroM, 87, 17)
        t_mikroM.setStyle(TableStyle([            
            
            #('GRID', (0,0), (-1,-1), 0.5, colors.black), # teszt
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('FONTNAME', (0,0),(-1,-1), 'Times'),
            # 0. oszlop és sor
            ('SPAN',(0,0),(0,1)),
            ('ALIGN', (0,0), (0,1), 'LEFT'),
            ('FONTSIZE', (0,0), (0,1), 11),
            ('BACKGROUND',(0,0),(0,1), colors.white),
            
            ('BACKGROUND',(1,0),(-1,0), colors.wheat),
            ('BACKGROUND',(1,1),(-1,-1), colors.whitesmoke),

        ]))

        t_mikroM.wrapOn(c, width, height)
        t_mikroM.drawOn(c, m,height-365)

        """ TÁPANYAGIGÉNYEK """
        
        # Alsó indexálás
        sub = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        
        # Ha bíborhere, akkor...
        if adatsor[0] == "bíborhere":
            fajlagos = "kg/1000kg"
        else:
            fajlagos = "kg/100kg"

        # NMAX ha nincs, akkor '-'
        if adatsor[22] == '-':
            nmax = adatsor[22]
        else:
            nmax = round(adatsor[22])

        tig = [

            ["","","","","","N","P2O5".translate(sub),"K2O".translate(sub),""],
            ["Termőhelyi kategória","",adatsor[14],"Fajlagos tápanyagigény:","",adatsor[15],adatsor[16],adatsor[17],fajlagos],
            ["","","","","","","","",""],
            ["Tervezett termés","",str(adatsor[18])+" t/ha","","","Korrigált\ntápanyagigény*","","Nitrátérzékeny terület\nmaximális N adagja",""],
            ["","","","","","","",""],
            ["Összes nitrogén igény","",str(round(adatsor[19]))+" kg/ha","","N","-","kg/ha",nmax,"kg/ha"],
            ["","","","","","","","",""],
            ["Összes foszfor igény","",str(round(adatsor[20]))+" kg/ha","","P2O5".translate(sub),"-","kg/ha","",""],
            ["","","","","","","","",""],
            ["Összes kálium igény","",str(round(adatsor[21]))+" kg/ha","","K2O".translate(sub),"-","kg/ha","",""],
        ]
        
        t_tig = Table(tig, [100,10,45,56,45], 15) #0.1.2.3.4. oszlopok, 15 sorok
        t_tig.setStyle(TableStyle([            
            
            #('GRID', (0,0), (-1,-1), 0.5, colors.black), # teszt
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('FONTNAME', (0,0),(-1,-1), 'Times'),
            
            # 0. oszlop, tárgymegjelölés
            ('ALIGN', (0,0), (-8,-1), 'LEFT'),
            ('FONTSIZE', (0,0), (0,9), 11),
            # 0. sor - N, P2O5, K2O
            ('FONTSIZE', (0,0), (8,0), 8),
            
            # Tervezett termés
            ('BACKGROUND',(2,3),(2,3), colors.whitesmoke),
            
            # Termőhelyi
            ('GRID', (2,1), (2,1), 0.25, colors.black), 
            ('BACKGROUND', (2,1), (2,1), colors.khaki),
            
            # Fajlagos
            # Szöveg
            ('SPAN',(3,1),(4,1)),
            ('FONTSIZE', (3,1), (4,1), 8.5),
            ('FONTSIZE', (7,1), (7,1), 8.5),
            ('ALIGN', (3,1), (3,1), 'RIGHT'),
            # Számok
            ('FONTNAME', (5,1),(7,1), 'Times-Bold'),
            ('FONTSIZE', (5,1), (7,1), 8),
            ('GRID', (5,1), (7,1), 0.25, colors.black),
            ('BACKGROUND', (5,1), (7,1), colors.palegreen),
            
            # Összes - számok
            ('FONTNAME', (2,1),(2,-1), 'Times-Bold'),
            ('SPAN',(2,3),(3,3)),
            ('GRID', (2,3), (3,3), 0.25, colors.black),
            ('SPAN',(2,5),(3,5)),
            ('GRID', (2,5), (3,5), 0.25, colors.black),
            ('BACKGROUND', (2,5), (3,5), colors.palegreen),
            ('SPAN',(2,7),(3,7)),
            ('GRID', (2,7), (3,7), 0.25, colors.black),
            ('BACKGROUND', (2,7), (3,7), colors.palegreen),
            ('SPAN',(2,9),(3,9)),
            ('GRID', (2,9), (3,9), 0.25, colors.black),
            ('BACKGROUND', (2,9), (3,9), colors.palegreen),
            # N,P2O5,K2O
            ('ALIGN', (4,0), (-5,-1), 'LEFT'),
            ('FONTSIZE', (4,0), (-5,-1), 8),

            # Korrigált tápanyagigény
            ('SPAN',(5,3),(5,4)),
            ('FONTSIZE',(5,3),(5,4), 8),
            
            ('ALIGN', (6,5), (6,-1), 'LEFT'),

            ('GRID', (5,5), (5,5), 0.25, colors.black),
            ('BACKGROUND', (5,5), (5,5), colors.palegoldenrod),
            ('GRID', (5,7), (5,7), 0.25, colors.black),
            ('BACKGROUND', (5,7), (5,7), colors.palegoldenrod),
            ('GRID', (5,9), (5,9), 0.25, colors.black),
            ('BACKGROUND', (5,9), (5,9), colors.palegoldenrod),
            
            # Nitrát max
            ('SPAN',(7,3),(7,4)),
            ('ALIGN', (8,-5), (8,-5), 'LEFT'),
            ('FONTSIZE',(7,3),(7,4), 8),
            ('FONTNAME',(7,5),(7,5), 'Times-Bold'),
            ('GRID', (7,5), (7,5), 0.25, colors.black),
            ('BACKGROUND',(7,5),(7,5), colors.gold),
            
        ]))

        t_tig.wrapOn(c, width, height)
        t_tig.drawOn(c, m,alm+247)
        
        """ MEGOSZTÁS TÁBLÁZAT """

        megoszt_T=[
            
            ["Ősz","","Tavasz","Ősz","Tavasz",],
            ["N%","Nmax kg/ha","N%","P,K%","P,K%",],
            [megosztas[i][0],megosztas[i][1],megosztas[i][2],megosztas[i][3],megosztas[i][4]],
        ]

        c.setFont('Times', 11)
        c.drawString(m+20,alm+197,"Műtrágyázás ideje és módja:")
        t_megosztas = Table(megoszt_T, 55, 14)
        t_megosztas.setStyle(TableStyle([            
            
            #('GRID', (0,0), (-1,-1), 0.5, colors.black), # teszt
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('FONTNAME', (0,0),(-1,-1), 'Times'),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('FONTSIZE', (0,2), (-1,-1), 10), # számok
            ('SPAN',(0,0),(1,0)),
            ('BACKGROUND',(0,0),(-1,0), colors.aquamarine),
            ('BACKGROUND',(0,1),(-1,-1), colors.whitesmoke),
            ('LINEBEFORE',(3,0),(3,2),1.5,colors.aquamarine),
            ('BOX',(0,0),(-1,-1),1.5,colors.aquamarine),
        
        ]))

        t_megosztas.wrapOn(c, width, height)
        t_megosztas.drawOn(c, m+160,alm+180)

        
        """ KORREKCIÓ TEXTBOX """
        adat_korr = [
            
            ["Elővetemény korrekciója:","30-50 kg/ha nitrogén és 25 kg/ha kálium","(pillangós, kukorica, repce, napraforgó)"],
            ["","",""],
            ["Szárleszántás korrekciója:","Kukorica és kalászos gabona szár: 5-10 kg/Kt","káliumoxid hatóanyaggal\nlehet csökkenteni a fenti adagokat"],
            ["","Napraforgó: 20-30 kg/Kt    (t: tonna termés)",""],
            ["","",""],
            ["Istállótrágya korrekciója:","NPK 1. év: 18-20-40 kg NPK/10 t ",""],
            ["","NPK 2. év: 12-15-20 kg/NPK/10 tonna trágya",""],
            ["","",""],
            ["Elővetemény kár korrekciója:","A kiadott PK hatóanyagok csökkenthetők a %-os pusztulás szerint.",""],
        ]

        c.setFont('Times', 11)
        c.drawString(m,alm+135, "*Műtrágya hatóanyag csökkentő tényezők figyelembevételével csökkenthető a környezeti terhelés:")

        t_korr = Table(adat_korr,[125,155],[15,10,15,15,10,15,15,10,15])
        t_korr.setStyle(TableStyle([            
            
            #('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0),(-1,-1), 'Times'),
            ('FONTSIZE',(0,0),(-1,-1), 8.5),
            ('BACKGROUND',(0,0),(2,0), colors.palegoldenrod),
            ('BACKGROUND',(0,2),(2,3), colors.palegoldenrod),
            ('BACKGROUND',(0,5),(2,6), colors.palegoldenrod),
            ('BACKGROUND',(0,8),(2,8), colors.palegoldenrod),
            # 2. oszlop - megjegyzések
            ('FONTNAME', (2,0),(2,-1), 'Times-Italic'),
            # 0. oszlop
            ('SPAN',(0,2),(0,3)),
            ('SPAN',(0,5),(0,6)),
            ('SPAN',(2,2),(2,3)),

            ('ALIGN', (1,8),(-2,-1), 'LEFT'),

        ]))

        t_korr.wrapOn(c, width, height)
        t_korr.drawOn(c, m,alm)
        
        # Oldalszám
        c.setFont('Times', 10)
        oldal = "%s. oldal" % str(i+1)
        c.drawString((width/2.0),20,oldal)

        # Hrsz hosszkorlátozás
        max_tjLen = 25
        if len(adatsor[2]) > max_tjLen: # hrsz.
            lista = list(adatsor)
            lista[2] = lista[2][:-(len(adatsor[2])-max_tjLen)]
            adatsor = tuple(lista)

        # Tartalomjegyzék sorai: közig,hrsz,tábla,növény,oldal
        tjegyzek.append([adatsor[1],adatsor[2],adatsor[4],adatsor[0],oldal])
        # Tartalomjegyzék oldalai
        count += 1
        if count == max_tjRow:
            tjegyzekek.append(tjegyzek)
            tjegyzek = [["Közig. név","Hrsz.","Tábla","Növény","Oldal"],] # tj. fejléc
            count = 0

        i += 1
        c.save()

        #break # teszt: csak az elsőt!

    # Tartalomjegyzék: Maradék sorok új tömbbe/oldalra
    if len(tjegyzek) % max_tjRow != 0:
        tjegyzekek.append(tjegyzek)
        
    """ TARTALOMJEGYZÉK """
    
    # Tartalomjegyzék(ek) mappa
    #tj_path = "%s\\eredmenylapok" % dir
    #tj_path = "%s\\tartalom" % dir
    print(add_folder(os,erl_path))

    i = 0
    for tj in tjegyzekek:

        pdf_tjname = os.path.join( "%s\\%s - tartalom.pdf" % (erl_path,str(i)))
        t = canvas.Canvas(pdf_tjname) # fájl neve 
        t.drawCentredString((width/2.0), height-50, "TARTALOM")

        t_tartalom = Table(tj, tjCol,tjRow)
        t_tartalom.setStyle(TableStyle([            
            
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('FONTNAME', (0,0),(-1,-1), 'Times'),
            ('FONTSIZE',(0,0),(-1,-1), 8.5),
            ('BACKGROUND',(0,0),(-1,0), colors.lightskyblue),
        
        ]))

        t_tartalom.wrapOn(t, width,height)
        t_tartalom.drawOn(t, 50,(netto_hely+alm)-(len(tj)*tjRow)) # táblázat magassága: (bruttó hely - sormagasságok)

        i += 1
        t.save()
    
   
    