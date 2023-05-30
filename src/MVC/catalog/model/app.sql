create or replace function check_ean(a_code text) returns boolean
as $$
    def GetCrc(aCode: str) -> int:
        Body = aCode[:-1]
        Data = [(3, 1)[i % 2] * int(x) for i, x in enumerate(reversed(Body))]
        return (10 - sum(Data)) % 10

    def CheckEan(aCode: str) -> bool:
        return  (8 <= len(aCode) <= 14) and \
                (aCode.isdigit()) and \
                (aCode[-1] == str(GetCrc(aCode)))

    return CheckEan(a_code)
$$ language plpython3u;
