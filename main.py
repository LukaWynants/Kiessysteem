from klassen import *
import time

class Kiessysteem:

    def __init__(self):
        self.USB = Usb()
        self.stembus = Stembus()
        self.kiezers = self.creer_kiezers()
        self.partijen = self.creer_partijen()
        self.stemcomputers = self.creer_stemcomputers()
        self.chipkaarten = self.creer_chipkaarten()
        self.stem_id = 0

    def initialiseer_stembus(self):
        print("initialiseren van de stembus...")
        self.stembus.init_stembus(self.USB)

    def creer_kiezers(self):
        """
        een methode die een lijst van 1200 kiezer objecten aanmaakt
        """
        # 1200 kiezers aanmaken
        kiezers = [] # lijstje voor de 1200 kiezers

        for i in range(1,1201):
            kiezers.append(Kiezer(i)) 

        return kiezers

    def creer_partijen(self):
        """
        een methode die 5 lijsten aanmaakt van 5 verschillende partijen
        """
        
        kandidaten_lijst = []
        partijen = []
        kiezers = self.kiezers.copy()
        
        while len(kandidaten_lijst) < 5:
            
            partij = []
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

        for i in range(1, 4):
            
            stemcomputer = Stemcomputer(i)
            print(f"stemcomputer nummer: {i} geinitialiseerd...")
            stemcomputer.init_stemcomputer(self.USB)
            stemcomputers.append(stemcomputer)

        return stemcomputers

    def creer_chipkaarten(self):
        chipkaarten = []
        #initialiseer 60 chip kaarten
        for i in range(60):
            chipkaarten.append(Chipkaart())

        return chipkaarten
    
    def stem(self, kiezer):
        
        #determine of the stemmer een voor de opgestelde lijst gaat kiezen of zelf een lijst maakt
        kies_random = random.choice([True, False])  # True voor opgestelde lijst, False voor zelf lijst maken

        if kies_random:
            gekozen_partij = (random.choice(self.partijen))
            gekozen_lijst = gekozen_partij.kandidaten
        else:
            gekozen_partij = random.choice(self.partijen)
            #herschik de lijst met random
            gekozen_lijst = random.sample(gekozen_partij.kandidaten, len(gekozen_partij.kandidaten))


        return gekozen_lijst

    def start_stem_simulatie(self):
        #initialiseer de stembus
        self.initialiseer_stembus()
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
                print(f"{kiezer.kiezer_id} steekt het chipkaart in stemcompiter: {stemcomputer.id}")

                #nakijken of de chipkaart geldig is
                if chipkaart.code == stemcomputer.opstart_code:
                    print(f"{kiezer.kiezer_id} heeft 1 geldige stem")
                        
                    gekozen_lijst = self.stem(kiezer)

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

if __name__ == "__main__":

    kiessysteem = Kiessysteem()

    kiessysteem.start_stem_simulatie()
