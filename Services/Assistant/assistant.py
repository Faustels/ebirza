import random
from unidecode import unidecode
from Services.Price.PriceController import GetData

# list for greetings
g1 = [
    "Sveiki",
    "Labas",
    "Laba diena"
]
g2 = [
    "Čia galite užduoti jums iškilusius klausimus apie mūsų puslapį ir elektros kainas",
    "Čia galite pasiteirauti apie elektros kainas Lietuvoje",
    "Esu pasiruošes atsakyti į jūsų klausimus"
]

# list for questions

q1 = [
    "kokios siandien elektros kainos",
    "elektros kaina lietuvoje",
    "is ko susideda elektros kaina",
    "elektros kainos",
    "elektros kainos siandien",
    "elektros kaina siandien"
]
q2 = [
    "kas esate jus",
    "ka veikia jusu imone",
    "papasakokite apie save"
]

q3 = [
    "is ko susideda elektros kaina",
    "elektros kainos dedamosios",
    "elektros kainos dedamosios lietuvoje"
    "kokios yra elektros kainos dedamosios",
    "kokios yra elektros kainos dedamosios lietuvoje"

]

q4 = [
    "kaip veikia jusu irankiai",
    "ka daro jusu irankiai",
    "ka daro saules prognozavimo irenginys"
]

q5 = [
    "kaip su jumis susisiekti",
    "noriu susisiekti su jumis",
    "kokie jusu kontaktai",
    "kontaktai"
]

q6 = [
    "ar turite patarimu",
    "patarimai",
    "kokie patarimai sutaupyti"
    "patarkite kaip sutaupyti"
]
# list for answers


a1 = [
    ["Elektros kaina Lietuvoje yra ", " €/mWh. Jei norite sužinoti daugiau, spauskite <a href='kaina'>čia.</a>"],
    ["Elektros kaina Lietuvoje dabar yra ", " €/mWh. Jei norite sužinoti daugiau, spauskite <a href='kaina'>čia.</a>"],
    ["Prognozuojama elektros kaina dabar yra ", " €/mWh. Jei norite sužinoti daugiau, spauskite <a href='kaina'>čia.</a>"]

]

a2 = [
    "Mes esame ShinyTrade Lietuva - svetainė, skatinanti žaliosios energijos vartojimą bei prognozuojanti Lietuvos"
    " elektros rinkos kainas realiu laiku. Daugiau apie mus galite sužinoti <a href='apiemus'>čia</a>."
]

a3 = [
    "Elektros kaina Lietuvoje susideda iš ...., jei norite sužinoti daugiau, spauskite <a href=''>čia.</a>"
]

a4 = [
    "Visą informaciją apie mūsų įrankius galite surasti <a href='paslaugos'>čia.</a>"
]

a5 = [
    "Su mumis galite susisiekti el. paštu shinytradelietuva@gmail.com arba tel. numeriu +37061234567 ."
]

a6 = [
    "Patarimus, kaip sutaupyti elektros energijos, galite rasti <a href='patarimai'>čia.</a>"
]


def list_Ai():
    X1 = g1[random.randint(0, 2)]
    X2 = g2[random.randint(0, 2)]
    return X1 + '! ' + X2 + "."


def list_Ci():
    X4 = a1[random.randint(0, 2)]
    temp, price = GetData(0)
    ans = X4[0] + "{:.2f}" + X4[1]
    ans = ans.format(price)
    return ans


def list_Di():
    X5 = a2[0]
    return X5


def list_Gi():
    X6 = a3[0]
    return X6


def list_Hi():
    X7 = a4[0]
    return X7


def list_Ii():
    X8 = a5[0]
    return X8


def list_Ji():
    X9 = a6[0]
    return X9


def list_Q(text):
    return 'Patikslinkite, ka turite omenyje, sakydami ' + '\'' + text + '\'' + '?'


def Query(text):
    oldText = text
    text = unidecode(text.lower())
    if not text:
        return "Paklauskite manes klausimų, aš pabandysiu į juos atsakyti."
    else:
        if g1[0] in text or g1[1] in text or g1[2] in text:
            return list_Ai()
        elif q1[0] in text or q1[1] in text or q1[2] in text or q1[3] in text or q1[4] in text or q1[5] in text:
            return list_Ci()
        elif q2[0] in text or q2[1] in text or q2[2]:
            return list_Di()
        elif q3[0] in text or q3[1] in text or q3[2] or q3[3] in text or q3[4] in text:
            return list_Gi()
        elif q4[0] in text or q4[1] in text or q4[2] in text:
            return list_Hi()
        elif q5[0] in text or q5[1] in text or q5[2] or q5[3] in text:
            return list_Ii()
        elif q6[0] in text or q6[1] in text or q6[2] or q6[3] in text:
            return list_Ji()
        else:
            return list_Q(oldText)
