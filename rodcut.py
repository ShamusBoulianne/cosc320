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


p = [0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30]
out = extendedBottomUpCutRod(p, 10)
print(out[0])
print(out[1])
printCutRodSolution(p, 10)
