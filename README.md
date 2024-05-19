github link: https://github.com/LukaWynants/Kiessysteem 

# Objecten initialiseren en creeren

## kiessysteem object
Het kiessyteem object is een klasse dat het geheele stem simulatie beheert.

het wordt geinitialiseert volgens:

    kiessysteem = Kiessysteem(1200, 5)

waarbij de eerste waarde het aantal kiezers is dat je wilt initialiseren en de tweede waarde het aantal partijen is.

### Initialisatie van het kiessysteem object:
#### USB
Het USB object wordt geïnitialiseerd bij het aanmaken van het Kiessysteem object in de dunderinit methode. Het krijgt willekeurig een 9 digit opstartcode toegewezen bij initialisatie.

#### Rest van de objecten
Nadat de USB is geinitialiseerd worden de volgende objecten gecreerd:
1. Een Stembus object die de stembiljet objecten zal beheren
2. Een lijst van 1200 kiezers objecten
3. Een lijst van 5 partij objecten met elks een lijst van 10 kandidaten
4. Een lijst met 3 stemcomputer objecten
5. Een lijst van 60 chipkaart objecten

Output van de console:

![Alt text](pictures/opstartscherm.png)

## Stem process simulatie

Nadat het kiessyteem object is geinitialiseerd wordt de start_stem_simulatie methode geropen met:
    
    # het kiessyteem object moet geinitialiseerd zijn voor je de start_stem_simulatie methode aanroept
    kiessysteem = Kiessysteem(1200, 5)

    kiessysteem.start_stem_simulatie()
    
De stemsimulatie methode begint met een while loop die checked of het atribuut voor alle kiezers het value:

    self.gestemd = True 

heeft

![Alt text](pictures/stemprocess.png)

## zetel verdeling 

![Alt text](pictures/zetel_calculatie.png)