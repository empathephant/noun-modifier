from sg_pl_pairs import pairs
from irregular_nouns import irregulars
irregularReverse = {v: k for k, v in irregulars.items()}
from assignment_1_eval import evaluate2
OES_WORDS = set(i.strip() for i in open('OES_WORDS.txt').read().split(','))
OS_WORDS = set(i.strip() for i in open('OS_WORDS.txt').read().split(','))
NON_PLURALIZE = set(i.strip() for i in open('NON_PLURALIZE.txt').read().split(','))

def DetermineSingular(nounEntered):
    pluralEndings = {

    }

    if nounEntered in NON_PLURALIZE:
        singNoun = nounEntered
    elif nounEntered in irregularReverse:
        singNoun = irregularReverse[nounEntered]
    else:
        lastTwoChar = nounEntered[-2:]
        if lastTwoChar in pluralEndings:
            singNoun = pluralEndings[lastTwoChar](nounEntered)
        else:
            lastChar = nounEntered[-1]
            if lastChar in pluralEndings:
                singNoun = pluralEndings[lastChar](nounEntered)
            else:
                singNoun = StandardSing(nounEntered)
    return singNoun

def DeterminePlural(nounEntered):
    singEndings = {
        'x': EsPlural, 's': EsPlural, 'z': EsPlural, 'ch': EsPlural,
        'ay': StandardPlural, 'ey': StandardPlural, 'iy': StandardPlural, 'oy': StandardPlural, 'uy': StandardPlural,
        'fe': FeVesPlural, 'f': FVesPlural, 'y': IesPlural,
        'o': HandleOWords,
        'us': IPlural,
        'on': APlural, 'um': UmAPlural,
        'is': IsPlural,
        'ex': IcesPlural, 'ix': IcesPlural,
        'a': AePlural
    }

    if nounEntered in NON_PLURALIZE:
        pluralNoun = nounEntered
    elif nounEntered in irregulars:
        pluralNoun = irregulars[nounEntered]
    else:
        lastTwoChar = nounEntered[-2:]
        if lastTwoChar in singEndings:
            pluralNoun = singEndings[lastTwoChar](nounEntered)
        else:
            lastChar = nounEntered[-1]
            if lastChar in singEndings:
                pluralNoun = singEndings[lastChar](nounEntered)
            else:
                pluralNoun = StandardPlural(nounEntered)
    return pluralNoun

def StandardPlural(nounEntered):
    pluralNoun = nounEntered + 's'
    return pluralNoun

def StandardSing(nounEntered):
    singNoun = nounEntered[:-1]
    return singNoun

def EsPlural(nounEntered):
    pluralNoun = nounEntered + 'es'
    return pluralNoun

def IesPlural(nounEntered):
    pluralNoun = nounEntered[:-1]
    pluralNoun = pluralNoun + "ies"
    return pluralNoun

def OesPlural(nounEntered):
    stdPlural = StandardPlural(nounEntered)
    esPlural = EsPlural(nounEntered)
    pluralNoun = stdPlural + " or " + esPlural
    return pluralNoun

def HandleOWords(nounEntered):
    if nounEntered in OES_WORDS:
        pluralNoun = OesPlural(nounEntered)
    elif nounEntered in OS_WORDS:
        pluralNoun = StandardPlural(nounEntered)
    else:
        pluralNoun = EsPlural(nounEntered)
    return pluralNoun

def VesPlural(stem):
    pluralNoun = stem + 'ves'
    return pluralNoun

def FVesPlural(nounEntered):
    pluralNoun = nounEntered[:-1]
    pluralNoun = VesPlural(pluralNoun)
    return pluralNoun

def FeVesPlural(nounEntered):
    pluralNoun = nounEntered[:-2]
    pluralNoun = VesPlural(pluralNoun)
    return pluralNoun

def IPlural(nounEntered):
    formalPlural = nounEntered[:-2] + 'i'
    informalPlural = EsPlural(nounEntered)
    return formalPlural + " or " + informalPlural

def APlural(nounEntered):
    stem = nounEntered[:-2]
    return stem + 'a'

def IsPlural(nounEntered):
    stem = nounEntered[:-2]
    return EsPlural(stem)

def IcesPlural(nounEntered):
    stem = nounEntered[:-2]
    formalPlural = stem + 'ices'
    informalPlural = EsPlural(nounEntered)
    return formalPlural + " or " + informalPlural

def UmAPlural(nounEntered):
    formalPlural = APlural(nounEntered)
    informalPlural = StandardPlural(nounEntered)
    return formalPlural + " or " + informalPlural

def AePlural(nounEntered):
    formalPlural = nounEntered + 'e'
    informalPlural = StandardPlural(nounEntered)
    return formalPlural + " or " + informalPlural

def ConvertToPlural(nounEntered):
    print("You entered: " + nounEntered)
    pluralNoun = DeterminePlural(nounEntered)
    print("The plural of " + nounEntered + " is " + pluralNoun + ".\n")

def ConvertToSingular(nounEntered):
    print("You entered: " + nounEntered)
    singNoun = DetermineSingular(nounEntered)
    print(nounEntered + " is already plural. The singular form of " + nounEntered + " is " + singNoun + ".\n")

def evaluate(pl_func=DeterminePlural, pair_data=pairs):
    """Evaluate the performance of pluralize function based on pairs data.

    pl_func -- function that pluralizes input word (default=pluralize)
    pair_data -- list of 2-tuples: [(sg1, pl1), (sg2, pl2),...] (default=pairs)
    """
    total = len(pair_data)
    # Determine how many lexemes have more than one plural form.
    # duplicates = len(set([i for i, j in pair_data]))
    correct = 0
    for sg, pl in pair_data:
        predicted_pl = pl_func(sg)
        if pl == predicted_pl or pl in predicted_pl:
            correct += 1
            print('correct:', sg, predicted_pl, '({})'.format(pl), sep='\t')
        else:
            print('Incorrect:', sg, predicted_pl, '({})'.format(pl), sep='\t')
    print('Your score:', correct, '/', total, '{:.2%}'.format(correct / total), '\n')

def addWord():
    print("adding word feature here")

def ExecuteMenu(userChoice):
    if userChoice == "evaluate":
        testNumber = input("\nWould you like to use test 1 or 2?")
        if testNumber == '1':
            evaluate()
        elif testNumber == '2':
            evaluate2(DeterminePlural)
        else:
            print("Not a valid test.")
    elif userChoice == "add":
        addWord()
    else:
        ConvertToPlural(userChoice)

def DisplayMenu():
    print("\nThe plural of menu is menus.\n")
    print('"evaluate" - test the accuracy of the pluralize function')
    print('"quit" - end the program')
    print('"add" - add an irregular plural to the dictionary\n')
    userChoice = input("Choose from the options above or enter a noun to pluralize:\n")
    ExecuteMenu(userChoice)

print("Hello!\n")
nounEntered = input("Please enter a noun, or type \'menu\' for a list of commands: ")
while nounEntered != "quit":
    if nounEntered == "menu":
        DisplayMenu()
    elif nounEntered[-1] == 's':
        ConvertToSingular(nounEntered)
    else:
        ConvertToPlural(nounEntered)
    nounEntered = input("Enter another noun, or type \'quit\' to end the program: ")
print("\nGoodbye!")
