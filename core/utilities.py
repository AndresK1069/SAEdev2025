from core.Component.Bees.BeeTypes import BEE_TYPES


def evenSplit(nfleur: int , maxNectar :int) -> int:
    """
        Calcule une répartition équitable du nectar entre les fleurs.

        La méthode divise le nectar maximal disponible (`maxNectar`) par
        deux fois le nombre de fleurs (`nfleur`) pour obtenir une quantité
        équitable à attribuer à chaque fleur.

        Paramètres
        ----------
        nfleur : int
            Nombre total de fleurs.
        maxNectar : int
            Quantité maximale de nectar disponible.

        Retours
        -------
        int
            Quantité de nectar à attribuer à chaque fleur.
        """
    return maxNectar//(nfleur*2)

def getBeeStats(string:str):
    """
        Retourne une instance d'abeille correspondant au type donné.

        La méthode prend une chaîne représentant le type d'abeille,
        la convertit en minuscules, récupère la classe correspondante
        dans le dictionnaire `BEE_TYPES` et retourne une instance de cette classe.

        Paramètres
        ----------
        string : str
            Nom du type d'abeille à récupérer (par exemple "worker", "queen", etc.).

        Retours
        -------
        Bee
            Une instance de l'abeille correspondant au type spécifié.

        Exceptions
        ----------
        KeyError
            Levée si le type d'abeille fourni n'existe pas dans `BEE_TYPES`.
    """
    string = string.lower()
    bee_class = BEE_TYPES[string]
    return bee_class()

def randomName():
    """
        Génère un nom complet aléatoire.

        La méthode sélectionne aléatoirement un prénom dans la liste `first_names`
        et un nom de famille dans la liste `last_names`, puis les combine pour
        former un nom complet.

        Retours
        -------
        str
            Nom complet aléatoire sous la forme "Prénom Nom".
    """
    import random
    first_names = (
        "John", "Andy", "Joe", "Michael", "David", "Chris", "James", "Robert", "William", "Daniel",
        "Matthew", "Joshua", "Andrew", "Ryan", "Jacob", "Nicholas", "Anthony", "Alexander", "Tyler", "Zachary",
        "Kevin", "Brian", "Eric", "Jason", "Justin", "Mark", "Thomas", "Steven", "Timothy", "Jonathan",
        "Adam", "Charles", "Benjamin", "Aaron", "Nathan", "Dylan", "Kyle", "Richard", "Patrick", "Sean",
        "Samuel", "Gregory", "Jeremy", "Brandon", "Cameron", "Austin", "Jordan", "Jose", "Juan", "Luis",
        "Carlos", "Jorge", "Jesus", "Miguel", "Diego", "Alejandro", "Sergio", "Fernando", "Raul", "Manuel",
        "Francisco", "Antonio", "Ricardo", "Roberto", "Marco", "Enrique", "Victor", "Mario", "Edgar", "Julian",
        "Ethan", "Logan", "Liam", "Owen", "Noah", "Caleb", "Gavin", "Luke", "Isaac", "Nathaniel",
        "Dominic", "Christian", "Evan", "Aiden", "Blake", "Colin", "Alex", "Henry", "Tyson", "Troy",
        "Garrett", "Spencer", "Shane", "Trevor", "Cody", "Derek", "Corey", "Eli", "Marcus", "Jared",
        "Wyatt", "Hunter", "Conor", "Declan", "Finn", "Grayson", "Kai", "Levi", "Max", "Nolan",
        "Omar", "Paulo", "Quinn", "Rafael", "Ruben", "Simon", "Tobias", "Ulises", "Victor", "Walter",
        "Xavier", "Yahir", "Zane", "Asher", "Beau", "Clayton", "Damian", "Emmett", "Felix", "Gideon",
        "Holden", "Ian", "Jace", "Kaden", "Landon", "Mason", "Nico", "Orion", "Preston", "Quentin",
        "Roman", "Silas", "Tanner", "Uriel", "Vincent", "Wesley", "Xander", "Yosef", "Zander", "Avery",
        "Bryson", "Callum", "Dallas", "Elliot", "Finnley", "Graham", "Harrison", "Isaias", "Jaxon", "Kael",
        "Lawson", "Malcolm", "Nathanial", "Oliver", "Phoenix", "Quincy", "Reid", "Seth", "Tobiah", "Uriah",
        "Victoriano", "Walker", "Xzavier", "Yandel", "Zaiden", "Alfred", "Barrett", "Colten", "Darius", "Ezequiel",
        "Francis", "Giovanni", "Hector", "Ignacio", "Joaquin", "Kameron", "Lukas", "Matthias", "Nehemiah", "Owen",
        "Peyton", "Quintin", "Ronald", "Stefan", "Troy", "Ulric", "Vance", "Weston", "Xavian", "Yehuda",
        "Zion", "Anderson", "Braxton", "Cyrus", "Dante", "Emiliano", "Fabian", "Gonzalo", "Hugo", "Ismael",
        "Jeremiah", "Kendrick", "Leonel", "Marcelo", "Nathanael", "Octavio", "Pablo", "Ramon", "Salvador", "Thiago"
    )
    last_names = (
        "Johnson", "Smith", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
        "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
        "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
        "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
        "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts",
        "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker", "Cruz", "Edwards", "Collins", "Reyes",
        "Stewart", "Morris", "Morales", "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper",
        "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson",
        "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray", "Mendoza", "Ruiz", "Hughes",
        "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers", "Long", "Ross", "Foster", "Jimenez",
        "Powell", "Jenkins", "Perry", "Russell", "Sullivan", "Bell", "Coleman", "Butler", "Henderson", "Barnes",
        "Gonzales", "Fisher", "Vasquez", "Simmons", "Romero", "Jordan", "Patterson", "Alexander", "Hamilton", "Graham",
        "Reynolds", "Griffin", "Wallace", "Moreno", "West", "Cole", "Hayes", "Bryant", "Herrera", "Gibson",
        "Ellis", "Tran", "Medina", "Aguilar", "Stevens", "Murray", "Ford", "Castro", "Marshall", "Owens",
        "Harrison", "Fernandez", "McDonald", "Woods", "Washington", "Kennedy", "Wells", "Vargas", "Henry", "Chen",
        "Freeman", "Webb", "Tucker", "Guzman", "Burns", "Crawford", "Olson", "Simpson", "Porter", "Hunter",
        "Gordon", "Mendez", "Silva", "Shaw", "Snyder", "Mason", "Dixon", "Munoz", "Hunt", "Hicks",
        "Holmes", "Palmer", "Wagner", "Black", "Robertson", "Boyd", "Rose", "Stone", "Salazar", "Fox",
        "Zimmerman", "Medrano", "Fleming", "Hoffman", "Carlson", "Navarro", "Maldonado", "Camacho", "Craig", "Lozano",
        "Campos", "Pena", "Richards", "Willis", "Patton", "Allison", "McCoy", "Castillo", "Le", "Masters", "Higgins",
        "Franklin", "Caldwell", "Luna", "Levine", "Banks", "Meyer", "Baldwin", "Valdez", "Mckinney", "Figueroa", "Day"
    )

    full_name = random.choice(first_names) + " " + random.choice(last_names)
    return full_name

