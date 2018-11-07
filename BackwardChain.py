# BackwardChain.py
#
# Oct 18 2018

# Variable Settings
testCase = 'filepathhere'

import sys

# -------------------------------------------------------------------
def filePrompt():
    """
    This function prompts the user for a file path

    :return: fileName: a string containing the file location
    """
    # Ask User for file Input
    fileName = input(" \n Please enter a valid file location: ")
    if len(fileName) == 0:
        print("This is not valid input")

    return fileName


# -------------------------------------------------------------------
def readDataFile(inputFile):
    """
    This function opens the file, read its content in to a list,
    close the file and return a data list.

    :param aFileLocation: the input file name
    :return aDataList: a list holding the content of the data file
    """
    # Open the file
    dataFile = open(inputFile, "r")

    # Read file content into a list
    aDataList = list(dataFile)

    # Always close the file pls
    dataFile.close()

    return aDataList


# -------------------------------------------------------------------
def KBparsing(aDataList):
    """
    This function parse the raw data into the format for easier processing
    :param aDataList: raw string list containing symbols
    :return: string list with no symbols
    """
    size = len(aDataList)
    # Removing "[", "]", blank spaces, and "," from the string list
    for i in range(0, size):
        aDataList[i] = aDataList[i].replace("[", "").replace("]", "").replace(" ", "").replace(",", "").replace("\n","")

    return aDataList


# -------------------------------------------------------------------
def inputPrompt():
    """
    This function prompts the user before validating the given input
    :return: a valid input
    """
    user_input = input("\n Please enter an atom OR enter 'STOP' to stop: ")
    if user_input.isalpha():

        # User wants to exist the program
        if user_input == "STOP":
            print("\n You are exiting the program")
            print(" Good-Bye")

        # Atom must contain only one character
        elif len(user_input) == 1:
            # insensitive case matching
            user_input = user_input.casefold()
            print("\n The atom you have entered is: ", user_input)
            print(" ")
        else:
            print("\n atom must be one character. Please try again.")
            user_input = inputPrompt()

    # Invalid User input
    else:
        print("\n You have entered an invalid input. Please try again.")
        user_input = inputPrompt()

    return user_input


# -------------------------------------------------------------------
def solve(goals, knowledge_base, valid_atoms, invalid_atoms, used_atoms):
    """
    This is the main function used to solve an atom

    :param goals: list of atoms to solve
    :param rules: knowledge base given
    :param valid_atoms: a list that stores all previously valid atoms
    :param invalid_atoms: a list that stores all previously invalid atoms
    :param used_atoms: a list to store all atoms checked
    :return: whether or not that atom is a logical consequence of the set of rules
    """

    # True when every questionable atom is solved
    if len(goals) == 0:
        return True

    # Popping the first atom from the list
    current_atom_to_solved = goals.pop(0)
    found = False

    # Check if the atom is solved already
    if current_atom_to_solved in valid_atoms:
        used_atoms.append(current_atom_to_solved)
        return True
    if current_atom_to_solved in invalid_atoms:
        used_atoms.append(current_atom_to_solved)
        return False

    # Checking for duplicate heads
    for i in range(0, len(knowledge_base)):
        if current_atom_to_solved == knowledge_base[i][0]:
            found = True

            # Existing fact
            if len(knowledge_base[i]) == 1:
                if current_atom_to_solved in valid_atoms:
                    used_atoms.append(current_atom_to_solved)
                    return True
                else:
                    # First time seeing the atom
                    valid_atoms.append(current_atom_to_solved)
                    used_atoms.append(current_atom_to_solved)
                    return True

            # Appending atoms to investigate
            for j in range(1, len(knowledge_base[i])):
                if knowledge_base[i][j] in goals:
                    continue
                else:
                    # First time seeing the new atom
                    goals.append(knowledge_base[i][j])

    # If atom is not in any of the rules, atom is not solvable
    if not found:
        invalid_atoms.append(current_atom_to_solved)
        used_atoms.append(current_atom_to_solved)
        return False

    # Investigate the rest of the atoms
    if solve(goals, knowledge_base, valid_atoms, invalid_atoms, used_atoms):
        if current_atom_to_solved in valid_atoms:
            used_atoms.append(current_atom_to_solved)
            return True
        else:
            valid_atoms.append(current_atom_to_solved)
            used_atoms.append(current_atom_to_solved)
            return True

    else:
        invalid_atoms.append(current_atom_to_solved)
        used_atoms.append(current_atom_to_solved)

    return False


# -------------------------------------------------------------------
def display_result(input, found, used_atoms):
    """
    This function displays individual input and give the result of
    whether or not the current atom is a logical consequence of the set of rules.

    :param input: the current atom
    :param found: found or not found in the knowledge base
    :return:
    """
    reversed_list = used_atoms[::-1]

    if found:
        print(" -----------------------------------------------------------------------------------------")
        print(" Atom '%s' IS a logical consequence of the set of rules" % input)
        print(" Atoms checked '%s': " % input, reversed_list)
        print(" -----------------------------------------------------------------------------------------")
    else:
        print(" -----------------------------------------------------------------------------------------")
        print(" Atom '%s' IS NOT a logical consequence of the set of rules" % input)
        print(" Atoms checked '%s' : " % input, reversed_list)
        print(" -----------------------------------------------------------------------------------------")


# -------------------------------------------------------------------
def final_result(all_input, valid_list, invalid_list):
    """
    This function display the final results in ascending-order using three different lists

    :param all_input: list containing all inputs
    :param valid_list: list containing all valid atoms
    :param invalid_list: list containing all invalid atoms
    :return:
    """
    print("\n FINAL RESULT")
    print(" -----------------------------------------------------------------------------------------")
    print(" All valid inputs given: ", all_input)
    print(" All solvable atoms found: ", sorted(valid_list))
    print(" All non-solvable atoms: ", sorted(invalid_list))
    print(" -----------------------------------------------------------------------------------------")

# -------------------------------------------------------------------
def validateInput():
    """
    Validating input from command line
    
    :return: file name
    """
    if len(sys.argv) == 1:
        file_name = filePrompt()
    elif len(sys.argv) == 2:
        file_name = sys.argv[1]
    else:
        print("\n Invalid number of arguments \n")
        sys.exit(-1)

    return file_name


# ------------------------------------ Main Program ------------------------------------------------- #
# Retrieving datafile from command line input
fileName = validateInput()
#fileName = testCase

# Reading data from the txt file
dataList = readDataFile(fileName)

# Parsing the data list into useful data
KBparsing(dataList)

# Lists to save the previous solved atoms to avoid redundant work
valid_atoms = []
invalid_atoms = []
all_input = []
used_atoms = []

# Prompt input to begin program
user_input = inputPrompt()
while (user_input != "STOP"):
    atom = user_input
    all_input.append(atom)
    goals = [atom]

    # Start of recursion
    found = solve(goals, dataList, valid_atoms, invalid_atoms, used_atoms)
    display_result(user_input, found, used_atoms)

    # clear the list
    used_atoms = []
    user_input = inputPrompt()

# Displaying final result
final_result(all_input, valid_atoms,invalid_atoms)

