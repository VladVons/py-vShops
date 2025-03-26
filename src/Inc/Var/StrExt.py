# Created: 2025.03.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


def LevenshteinDistance(aText1: str, aText2: str) -> int:
    Len1, Len2 = len(aText1), len(aText2)
    dp = [[0] * (Len2 + 1) for _ in range(Len1 + 1)]

    for i in range(Len1 + 1):
        for j in range(Len2 + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif aText1[i - 1] == aText2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[Len1][Len2]
