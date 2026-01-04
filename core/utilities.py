from core.Component.Bees.BeeTypes import BEE_TYPES


def evenSplit(nfleur: int , maxNectar :int) -> int:
    return maxNectar//(nfleur*2)

def getBeeStats(string:str):
    string.lower()
    bee_class = BEE_TYPES[string]
    return bee_class()

def randomName():
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

