from klassen import *
import time
import jinja2

class Kiessysteem:

    def __init__(self, aantal_kiezers, aantal_partijen, aantal_zetels):
        self.aantal_kiezers = aantal_kiezers
        self.aantal_partijen = aantal_partijen
        self.aantal_zetels = aantal_zetels
        self.USB = Usb()
        self.stembus = self.initialiseer_stembus()
        self.kiezers = self.creer_kiezers()
        self.partijen = self.creer_partijen()
        self.stemcomputers = self.creer_stemcomputers()
        self.chipkaarten = self.creer_chipkaarten()
        self.stem_id = 0

    def initialiseer_stembus(self):
        """
        Een methode die de steem bus creerd en initialiseert met het usb object
        """
        stembus = Stembus()
        print("initialiseren van de stembus...")
        stembus.init_stembus(self.USB)
        print("stembus geinitialiseerd...")

        return stembus

    def creer_kiezers(self):
        """
        Een methode die een lijst van 1200 kiezer objecten aanmaakt
        """
        # 1200 kiezers aanmaken
        kiezers = [] # lijstje voor de 1200 kiezers

        for i in range(1, self.aantal_kiezers+1):
            kiezers.append(Kiezer(i)) 

        return kiezers

    def creer_partijen(self):
        """
        Een methode die n lijsten aanmaakt van n verschillende partijen met 10 kandidaten per partij
        """
        
        kandidaten_lijst = []
        partijen = []
        kiezers = self.kiezers.copy()
        
        while len(kandidaten_lijst) < self.aantal_partijen:
            
            partij = []
            #voeg 10 kandidaten toe
            while len(partij) < 10:
                

                kiezer = random.choice(kiezers)
                kiezers.remove(kiezer)
                partij.append(kiezer)


            kandidaten_lijst.append(partij)

        for i, kandidaten in enumerate(kandidaten_lijst):
            partijen.append(Partij(str(i), kandidaten))

        return partijen
    
    def creer_stemcomputers(self):
        """
        een methode die 3 stem computers initialiseerd, met de usb 

        """
        stemcomputers = []
        print("initialiseren van 3 stemcomputers...")
        for i in range(1, 4):
            
            stemcomputer = Stemcomputer(i)
            stemcomputer.init_stemcomputer(self.USB)
            stemcomputers.append(stemcomputer)
            print(f"stemcomputer nummer: {i} geinitialiseerd...")

        return stemcomputers

    def creer_chipkaarten(self):
        """
        Een methode die the chipkaart objecten creerd
        """
        chipkaarten = []
        #initialiseer 60 chip kaarten
        for i in range(60):
            chipkaarten.append(Chipkaart())

        return chipkaarten
    
    def stem(self, kiezer):
        """
        Een methode die een kiezer object een random stem laat maken tussen een zelf opgestelde random lijst of een al opgestelde lijst
        """
        
        #determine of the stemmer een voor de opgestelde lijst gaat kiezen of zelf een lijst maakt
        kies_random = random.choice([True, False])  # True voor opgestelde lijst, False voor zelf lijst maken

        if kies_random:
            gekozen_partij = (random.choice(self.partijen))
            gekozen_lijst = gekozen_partij.kandidaten
        else:
            gekozen_partij = random.choice(self.partijen)
            #herschik de lijst met random
            gekozen_lijst = random.sample(gekozen_partij.kandidaten, len(gekozen_partij.kandidaten))


        return gekozen_lijst, gekozen_partij

    def start_stem_simulatie(self):
        """
        Een methode die de stem simulatie start
        """
        print("simulatie start in 2s...")
        time.sleep(2)

        kiezers = self.kiezers.copy()
        
        #deze while lus blijft uitvoeren tot alle kiezers hebben gestemd
        while any(not kiezer.gestemd for kiezer in kiezers):
            
            #for loop die een chipkaart geeft aan een kiezer en initialiseert
            for kiezer, chipkaart  in zip(kiezers, self.chipkaarten):
                
                if kiezer.gestemd == False:
                    print(f"initialiseer chipkaart voor kiezer {kiezer.kiezer_id}")
                    chipkaart.initialiseer_chipkaart(self.USB)

                else:
                    print(f"{kiezer.kiezer_id} heeft al gestemd")


                #user krijgts random stemcomputer dat die moet gebruiken
                stemcomputer = random.choice(self.stemcomputers)
                print(f"Kiezer {kiezer.kiezer_id} steekt het chipkaart in stemcomputer: {stemcomputer.id}")

                #nakijken of de chipkaart geldig is
                if chipkaart.code == stemcomputer.opstart_code:
                    print(f"Kiezer {kiezer.kiezer_id} heeft 1 geldige stem")
                        
                    gekozen_lijst, gekozen_partij = self.stem(kiezer)

                    #stem toevoegen aan de partij, en gekozen lijst toevoegen
                    gekozen_partij.stem_toevoegen(gekozen_lijst)

                    #1ste persoon van de lijst krijgt de stem
                    gekozen_kandidaat = gekozen_lijst[0]
                    gekozen_kandidaat.stemmen += 1
                    print(f"Gekozen kandidaat: {gekozen_kandidaat.kiezer_id}")

                    print(f"kiezer: {kiezer.kiezer_id} heeft gestemd")
                    kiezer.gestemd = True

                    #deinitializeer de chipkaart
                    chipkaart.reset_chipkaart()
            
                    #genereer een stembiljet en geef aan kiezer
                    stemcomputer.genereer_stembiljet(kiezer, gekozen_lijst, self.stem_id)
                    print("stembiljet gegenereerd...")
                    self.stem_id += 1

                    #scan stembiljet:
                    scanner = Scanner(self.stembus)
                    scanner.scan_stembiljet(kiezer.stembiljet)
                    print("_________________")
                        
                else:
                    print(chipkaart.code)
                    print(stemcomputer.opstart_code)
                    print("chipkaart is niet geldig...")

            #remove de 60 kiezers die net hebben gestemd
            kiezers = kiezers[60:]   

    def calculeer_zetels(self):
        """
        een methode die de zetels berekend met de D'Hondt methode

        source: https://en.wikipedia.org/wiki/D%27Hondt_method#:~:text=most%2Doverrepresented%20party.-,Example,from%20100%2C000%20down%20to%2025%2C000. 
        """
        
        aantal_zetels = self.aantal_zetels #hypothetisch 15 zetels voor 50 kandidaten
        berekeningen = [] #lijst voor de berekeningen van de quotiënten

        print("calculeren van de zetels...")
        print(f"totaal aantal zetels: {aantal_zetels}")

        #bereken de aantal quotienten op basis van de aantal zetel, 
        #eg voor 3 zetels quotient1 = stemmen/1, quotient2= stemmen/2, quotient3 = stemmen/3,  voor elke partij
        for i in range(1, aantal_zetels + 1):
            for partij in self.partijen:
                quotient = partij.stemmen / i
                #creer een dictionary om de partij aan hun quotient berekening vast te maken 
                quotient_dict = dict(quotient = quotient, partij = partij)
                berekeningen.append(quotient_dict)

        #sorteer de eerste 15 hoogste quotienten
        for i in range(1, aantal_zetels+1):
            hoogste_quotient = 0
            
            for quotient_berekening in berekeningen:
                #als de quotient hoger is dan de current hoogste, maak de quotient de nieuwe hoogste
                if quotient_berekening["quotient"] > hoogste_quotient:
                    hoogste_dict = quotient_berekening
                    hoogste_quotient = quotient_berekening["quotient"]
                    hoogste_partij = quotient_berekening["partij"]
                    

            # remove de hoogste quotient
            berekeningen.remove(hoogste_dict)

            print(f"Partij {hoogste_partij.partij_naam} heeft een zetel gekregen...")
            print(f"quotient: {hoogste_quotient}")
            hoogste_partij.aantal_zetels += 1
        
        # print de zetels
        for partij in self.partijen:
            print(f"Partij {partij.partij_naam} : {partij.aantal_zetels} zetel(s)")

    def verdeel_zetels(self):
        """
        Een methode die de lijst van kandidaten in een partij object herschikt op volgorde van de aantal stemmen en een zetel uit te geven aan de top kandidaten van de lijst
        """
        # loop over elke partij object
        for partij in self.partijen:
            
            # sorteer de kandidaten op basis van de aantal stemmen, kandidaat met hoogste stemmen heeft dan index 0...
            gesorteerde_kandidaten = sorted(partij.kandidaten, key=lambda obj: obj.stemmen)

            # for loop voor zetels uit te geven
            for uitgegeven_zetel in range(0, partij.aantal_zetels):
                # append de kandidaat aan de gekozen kandidaat van de partij
                gekozen_kandidaat = gesorteerde_kandidaten[uitgegeven_zetel].voornaam +" "+ gesorteerde_kandidaten[uitgegeven_zetel].achternaam + " Stemmen: " + str(gesorteerde_kandidaten[uitgegeven_zetel].stemmen)
                partij.gekozen_kandidaten.append(gekozen_kandidaat)
            
            
    def creer_html(self):
        """
        een methode die al de partijen, stemmen en zetels in een html bestand rendered met Jinja2
        """

        # HTML template waar data zal worden ingevoerd
        template_bestand = "templates/template.html"
        # output file van waar de html naar wordt gestuurd
        output_bestand = "output.html"

        # inhoud van de template lezen
        with open(template_bestand, "r") as file:
            template_text = file.read()

        # template in een jinja template opject stoppen
        template = jinja2.Template(template_text)

        # Template variabelen 
        data = {
            "totaal_aantal_zetels" : self.aantal_zetels,
            "Partij_een": "Partij " + self.partijen[0].partij_naam,
            "Stemmen_een": self.partijen[0].stemmen,
            "zetels_een": self.partijen[0].aantal_zetels,
            "gekozen_kandidaten_een": self.partijen[0].gekozen_kandidaten,
            "Partij_twee": "Partij " + self.partijen[1].partij_naam,
            "Stemmen_twee": self.partijen[1].stemmen,
            "zetels_twee": self.partijen[1].aantal_zetels,
            "gekozen_kandidaten_twee": self.partijen[1].gekozen_kandidaten,
            "Partij_drie": "Partij " + self.partijen[2].partij_naam,
            "Stemmen_drie": self.partijen[2].stemmen,
            "zetels_drie": self.partijen[2].aantal_zetels,
            "gekozen_kandidaten_drie": self.partijen[2].gekozen_kandidaten,
            "Partij_vier": "Partij " + self.partijen[3].partij_naam,
            "Stemmen_vier": self.partijen[3].stemmen,
            "zetels_vier": self.partijen[3].aantal_zetels,
            "gekozen_kandidaten_vier": self.partijen[3].gekozen_kandidaten,
            "Partij_vijf": "Partij " + self.partijen[4].partij_naam,
            "Stemmen_vijf": self.partijen[4].stemmen,
            "zetels_vijf": self.partijen[4].aantal_zetels,
            "gekozen_kandidaten_vijf": self.partijen[4].gekozen_kandidaten,
        }

        # Render de template met de data
        rendered_html = template.render(data)

        # Schrijf de gerenderde HTML naar een nieuw bestand
        with open(output_bestand, "w") as file:
            file.write(rendered_html)

        print(f"HTML-output is gegenereerd en opgeslagen in {output_bestand}")



if __name__ == "__main__":

    # initialiseer de objecten 
    # 1: aantal kiezers (1200), 2: aantal partijen (5), 3: aantal zetels (7)
    kiessysteem = Kiessysteem(1200, 5, 7)
    
    # start de Stem simulatie
    kiessysteem.start_stem_simulatie()

    #calculeer de aantal zetels elke partij krijgt
    kiessysteem.calculeer_zetels()

    #verdeel de zetels
    kiessysteem.verdeel_zetels()

    #creer het html bestand
    kiessysteem.creer_html()