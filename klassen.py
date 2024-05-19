import random

class Usb:

    def __init__(self):
        self.opstart_code = self.genereer_opstart_code()

    def genereer_opstart_code(self):
        return random.randint(100000, 999999)  #return a random 6 digit number als opstart code

class Stembus:

    def __init__(self):
        self.opstart_code = ""
        self.stembiljet_db = []

    def init_stembus(self, USB):
        """
        een methode voor de stembus te initialiseren, het usb object met opstart code is nodig voor dit kan gebeuren
        """
        if USB:
            print("USB gevonden...")
            self.opstart_code = USB.opstart_code
            print("Opstart code opgeslagen...")

    def voeg_stembiljet_toe(self, stembiljet_object):
        self.stembiljet_db.append(stembiljet_object)
    
class Kiezer:

    def __init__(self, kiezer_id):
        self.kiezer_id = kiezer_id
        self.voornaam = self.random_naam()
        self.achternaam = self.random_naam()
        self.leeftijd = self.random_leeftijd()
        self.chipkaart = ""
        self.gestemd = False
        self.stembiljet = {}

    def random_naam(self):
        """
        een method die een random naam selecteert en terug geeft
        """
        namen = ["bob", "jef", "sara", "smith", "john", "simmons", "klara", "lara", "jonathan", "karl", "josef", "jeroen", "lars", "tristan", "peter", "ann", "rodrigo", "peters", "alan"]
        return random.choice(namen)

    def random_leeftijd(self):
        """
        een method die een random nummer tusse 18 en 90 terug geeft
        """
        return random.randint(18, 90)

class Partij():
    
    def __init__(self, partij_naam, kandidaten):
        self.partij_naam = partij_naam
        self.kandidaten = kandidaten
        self.stemmen = 0
        self.gekozen_lijsten = []
        self.aantal_zetels = 0

    def stem_toevoegen(self, gekozen_lijst):
        """
        als er op de partij wordt gestemd voeg een stem toe en de lijst die werdt op gestemd
        """
        self.stemmen += 1
        self.gekozen_lijsten.append(gekozen_lijst)
        

class Stemcomputer:

    def __init__(self, id):
        self.id = id
        self.opstart_code = "" 

    def init_stemcomputer(self, USB):
        """
        een methode voor de stemcomputer te initialiseren, het usb object met opstart code is nodig voor dit kan gebeuren
        """
        if USB:
            print("USB gevonden...")
            self.opstart_code = USB.opstart_code
            print("Opstart code opgeslagen...")
    
    def genereer_stembiljet(self, kiezer, gekozen_lijst, stem_id):
        stembiljet = Stembiljet(kiezer, gekozen_lijst, stem_id )
        #stembiljet aan kiezer geven
        kiezer.stembiljet = stembiljet
        #stem opslagen in databank van stembus


class Chipkaart:
    
    def __init__(self):
        self.code = ""
        self.geinitialiseerd = False
    
    def initialiseer_chipkaart(self, USB):
        if USB:
            #print("USB gevonden...")
            self.code = USB.opstart_code
            print("Opstart code opgeslagen...")
            print("chipkaart geinitialiseerd")
            self.geinitialiseerd = True
    
    def reset_chipkaart(self):
        self.opstart_code = ""
        print("chipkaart deinitialiseerd")
        self.geinitialiseerd = False

class Stembiljet:
    def __init__(self, kiezer, gekozen_lijst, stem_id):
        self.kiezer = kiezer
        self.gekozen_lijst = gekozen_lijst
        self.stem_id = stem_id

    def print_stembiljet(self):
        """
        een methode die de stembiljet content uitprint
        """
        stembiljet_json = {}

        stembiljet_json['stem_id'] = self.stem_id
        stembiljet_json['Kiezer_id'] = self.kiezer.kiezer_id
        stembiljet_json['gekozen_lijst'] = [{"first_name": kandidaat.voornaam, "last_name": kandidaat.achternaam} for kandidaat in self.gekozen_lijst]

        return stembiljet_json

class Scanner():
    
    def __init__(self, stembus):
        self.stembus = stembus

    def scan_stembiljet(self, gescanned_stembiljet):
        print("scanning stembiljet...")
        print(f"geregistreerde stembiljet: {gescanned_stembiljet.print_stembiljet()}")
        self.stembus.stembiljet_db.append(gescanned_stembiljet)
        