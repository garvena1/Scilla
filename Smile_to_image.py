import os
import csv

import chimera
from chimera import runCommand as rc
from chimera.selection import currentAtoms
from chimera.selection import setCurrent
from chimera.printer import saveImage


# --------BOND LENGTHS--------------------------------------------
#These commands adjust the bond lengths of double and triple bonds so they look distinct

# CO, CC, SO, CS
doubleBonds = [float(1.208), float(1.310), float(1.554), float(1.421)]

# CC, CN, CS
tripleBonds = [float(1.174), float(1.136), float(1.050)]

# ----------------------------------------------------------------


# csv_path is the path to csv containing [name, smiles_string]
csv_path = ''

molecules = []

with open(csv_path) as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        molecules.append(row)

for molecule in molecules:

# This loop iterates over all smiles strings in Original CSV file
# and generates 64 images of each molecule by rotating along x, y, and z axis
# Input : List of lists containing [name, smiles string]
# Output : 64 images in directory specified below

    try:
        # fetch molecule and SMILES
        name = molecule[0]
        smiles = molecule[1]
        
        # Set output directory for images that are generated
        directory = '' + name
        if not os.path.exists(directory):
            os.makedirs(directory)

        # close all existing models
        rc('close all;wait')

        # initialize molecule
        mol = chimera.openModels.open(smiles, type="SMILES")[0]
        bonds = mol.bonds

        rc('set bgColor light gray;wait')
        rc('represent bs;wait')
        rc('setattr b radius 0.075;wait')

        rc('color red @C=;wait')
        rc('color green @H=;wait')
        rc('color blue @O=;wait')
        rc('color yellow @N=;wait')
        rc('color purple @S=;wait')
        rc('color white @F=;wait')
        rc('color brown @Cl=;wait')

        # rc('aromatic disk')

        # modify model to display double and triple bonds
        rc('select #0')
        atoms = currentAtoms()

        bondsList = []

        for a in atoms:
            for b in bonds:
                if b not in bondsList:
                    bondsList = bondsList + [b]

        for bond in bondsList:
            setCurrent(bond)
            length = bond.length()
            length = format(length, '.3f')

            if float(length) in doubleBonds:
                rc('setattr b radius 0.2 sel;wait')
            elif float(length) in tripleBonds:
                rc('setattr b radius 0.3 sel;wait')

        rc('windowsize 800 800;wait')
        rc('setzoom 30.0;wait')
        rc('center;wait')

        # take images of molecule
        i = 0

        image = saveImage(directory + '/' + str(i) + '.jpg', 224, 224, format="JPEG", quality=80)

        for x in range(0, 4):
            rc('turn x 90 center 0,0,0;wait')
            for y in range(0, 4):
                rc('turn y 90 center 0,0,0;wait')
                for z in range(0, 4):
                    rc('turn z 90 center 0,0,0;wait')
                    rc('windowsize 800 800;wait')
                    rc('setzoom 30.0;wait')
                    rc('center;wait')
                    rc('~select;wait')
                    image = saveImage(directory + '/' + str(i) + '.jpg', 224, 224, format="JPEG", quality=80)

                    i = i + 1

        rc('~select;wait')
    except:
        pass
