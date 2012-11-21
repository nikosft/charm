from userFuncs import *
from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
import sys

group = None

N = 2

secparam = 80

WVector = {}
C0 = {}
g2 = {}
g1 = {}
LVector = {}
Y = {}
XVector = {}
omega = {}
y = {}
YVector = {}

def setup(n):
    global g2
    global g1
    global Y
    global y

    M = {}
    V = {}
    m = {}
    r = {}
    t = {}
    v = {}
    R = {}
    T = {}

    input = n
    g1 = group.random(G1)
    g2 = group.random(G2)
    egg = pair(g1, g2)
    y = group.random(ZR)
    Y = (egg ** y)
    for i in range(0, n):
        t[i] = group.random(ZR)
        v[i] = group.random(ZR)
        r[i] = group.random(ZR)
        m[i] = group.random(ZR)
        T[i] = (g1 ** t[i])
        V[i] = (g1 ** v[i])
        R[i] = (g1 ** r[i])
        M[i] = (g1 ** m[i])
    pk = [g1, g2, n, Y, T, V, R, M]
    msk = [y, t, v, r, m]
    output = (pk, msk)
    return output

def keygen(pk, msk, yVector):
    global g2
    global g1
    global LVector
    global y
    global YVector

    a = {}
    LVector = {}
    YVector = {}

    input = [pk, msk, yVector]
    g1 = pk[0]
    g2 = pk[1]
    n = pk[2]
    y = msk[0]
    numNonDontCares = 0
    for i in range(0, n):
        if ( ( (yVector[i]) != (2) ) ):
            numNonDontCares = (numNonDontCares + 1)
    if ( ( (numNonDontCares) == (0) ) ):
        sk = (g2 ** y)
        output = sk
        return output
    sumUSaisUSsoFar = 0
    endForLoop = (numNonDontCares - 1)
    for i in range(0, endForLoop):
        a[i] = group.random(ZR)
        sumUSaisUSsoFar = (sumUSaisUSsoFar + a[i])
    a[numNonDontCares-1] = (y - sumUSaisUSsoFar)
    currentUSaUSindex = 0
    for i in range(0, n):
        if ( ( (yVector[i]) == (0) ) ):
            YVector[i] = (g2 ** (a[currentUSaUSindex] / msk[3][i]))
            LVector[i] = (g2 ** (a[currentUSaUSindex] / msk[4][i]))
            currentUSaUSindex = (currentUSaUSindex + 1)
        if ( ( (yVector[i]) == (1) ) ):
            YVector[i] = (g2 ** (a[currentUSaUSindex] / msk[1][i]))
            LVector[i] = (g2 ** (a[currentUSaUSindex] / msk[2][i]))
            currentUSaUSindex = (currentUSaUSindex + 1)
        if ( ( (yVector[i]) == (2) ) ):
            YVector[i] = group.init(G2)
            LVector[i] = group.init(G2)
    sk2 = [YVector, LVector]
    output = sk2
    return output

def encrypt(Message, xVector, pk):
    global WVector
    global C0
    global g1
    global Y
    global XVector
    global omega

    WVector = {}
    sUSi = {}
    XVector = {}

    input = [Message, xVector, pk]
    g1 = pk[0]
    n = pk[2]
    Y = pk[3]
    s = group.random(ZR)
    for i in range(0, n):
        sUSi[i] = group.random(ZR)
    omega = (Message * (Y ** -s))
    C0 = (g1 ** s)
    for i in range(0, n):
        if ( ( (xVector[i]) == (0) ) ):
            XVector[i] = (pk[6][i] ** (s - sUSi[i]))
            WVector[i] = (pk[7][i] ** sUSi[i])
        if ( ( (xVector[i]) == (1) ) ):
            XVector[i] = (pk[4][i] ** (s - sUSi[i]))
            WVector[i] = (pk[5][i] ** sUSi[i])
    CT = [omega, C0, XVector, WVector]
    output = CT
    return output

def decrypt(CT, sk):

    input = [CT, sk]
    omega, C0, XVector, WVector = CT
    if ( ( (isList(sk)) == (0) ) ):
        Message = (omega * pair(C0, sk))
        output = Message
        return output
    YVector, LVector = sk
    dotProd = group.init(GT)
    n = len(YVector)
    for i in range(0, n):
        if ( ( (( (YVector[i]) != (group.init(G2)) )) and (( (LVector[i]) != (group.init(G2)) )) ) ):
            dotProd = (dotProd * (pair(XVector[i], YVector[i]) * pair(WVector[i], LVector[i])))
    Message2 = (omega * dotProd)
    output = Message2
    return output

def SmallExp(bits=80):
    return group.init(ZR, randomBits(bits))

def main():
    global group
    group = PairingGroup(secparam)

    (pk, msk) = setup(4)
    sk = keygen(pk, msk, [2, 2, 0, 1])
    M = group.random(GT)
    print(M)
    print("\n\n")
    CT = encrypt(M, [1, 1, 0, 1], pk)
    M2 = decrypt(CT, sk)
    print(M2)
    if (M == M2):
        print("success")
    else:
        print("failed")


if __name__ == '__main__':
    main()

