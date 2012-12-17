from keygen import *
from config import *
import SDLPreProcessor
import sys, os

sys.path.extend(['../../', '../../codegen'])

import codegen_PY
import codegen_CPP

PREPROCESSED_STRING = "_PREPROCESSED"

def writeLOCFromKeygenToFile(LOCFromKeygen, inputSDLScheme):
    f = open(inputSDLScheme + finalSDLSuffix, 'w')

    for line in LOCFromKeygen:
        lenLine = len(line)
        if (line[(lenLine - 1)] != "\n"):
            f.write(line + "\n")
        else:
            f.write(line)

    f.close()

def main(inputSDLScheme, outputFile, outputUserDefFile):
    (linesOfCodeFromKeygen, blindingFactors_NonLists, blindingFactors_Lists) = keygen(inputSDLScheme)
    writeLOCFromKeygenToFile(linesOfCodeFromKeygen, inputSDLScheme)
    SDLPreProcessor.SDLPreProcessor_main(inputSDLScheme + finalSDLSuffix, inputSDLScheme + finalSDLSuffix + PREPROCESSED_STRING)
    codegen_PY.codegen_PY_main(inputSDLScheme + finalSDLSuffix + PREPROCESSED_STRING, outputFile + ".py", outputUserDefFile)
    codegen_CPP.codegen_CPP_main(inputSDLScheme + finalSDLSuffix + PREPROCESSED_STRING, outputFile + ".cpp")

if __name__ == "__main__":
    lenSysArgv = len(sys.argv)

    if ( (lenSysArgv != 4) or (sys.argv[1] == "-help") or (sys.argv[1] == "--help") ):
        sys.exit("Usage:  python " + sys.argv[0] + " [name of input SDL file] [name of output file] [name of output Python file for user-defined functions].")

    main(sys.argv[1], sys.argv[2], sys.argv[3])
