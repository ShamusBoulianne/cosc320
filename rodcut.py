import random


# Translated from pseudocode found in CLRS
def extendedBottomUpCutRod(p, n):
    r = [0]*(n+1)
    s = [0]*(n+1)
    r[0] = 0
    for j in range(1, n+1):
        q = -1
        for i in range(1, j+1):
            if q < p[i] + r[j-i]:
                q = p[i] + r[j-i]
                s[j] = i
        r[j] = q
    return [r, s]


def printCutRodSolution(p, n):
    rs = extendedBottomUpCutRod(p, n)
    while n > 0:
        print(rs[1][n])
        n = n - rs[1][n]


# generate random price array of size 100
# care is taken so that prices increase with length
p = [0]
for i in range(1, 100):
    p.append(random.randint(p[i-1]+1, p[i-1]+i))
n = 20
r = extendedBottomUpCutRod(p, n)[0]
s = extendedBottomUpCutRod(p, n)[1]
print('p: ' + str(p))
print('r: ' + str(r))
print('s: ' + str(s))
