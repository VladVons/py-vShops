/*
opyright:    Vladimir Vons, UA
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2022.05.03

Fork: Inc/DB/TDbList.py
*/


class TDbFields {
    constructor(aFields = []) {
        this.Data = {};
        this.IdxOrd = {};
        this.AddList(aFields);
    }

    Add(aName, aType, aDef) {
        const Def = {'str': '', 'int': 0, 'float': 0.0, 'bool': false, 'tuple': [], 'list': [], 'dict': {}};
        aDef = Def[aType];
        const Len = Object.keys(this.Data).length;
        this.Data[aName] = [Len, aType, aDef];
        this.IdxOrd[Len] = [aName, aType, aDef];
    }

    AddList(aFields) {
        aFields.forEach((aItem) => {
            this.Add(aItem[0], aItem[1], aItem[2]);
        });
    }

    GetNo(aName) {
        return this.Data[aName][0];
    }

    Export() {
        let Res = [];
        const Len = Object.keys(this.Data).length;
        for (let i = 0; i < Len; i++) {
            Res.push(this.IdxOrd[i]);
        }
        return Res;
    }
}

class TDbRec {
    constructor(aParent) {
        this.Parent = aParent;
        this.Data = [];
    }

    Flush() {
        this.Parent.Data[this.Parent.RecNo] = this.Data;
    }

    SetData(aData) {
        this.Data = aData;
    }

    Init() {
        const Fields = this.Parent.Fields;
        const Len = Object.keys(Fields.Data).length;
        this.Data = new Array(Len);
        for (let i = 0; i < Len; i++) {
            this.Data[i] = Fields.IdxOrd[i][2];
        }
    }

    GetField(aName) {
        const Idx = this.Parent.Fields.GetNo(aName);
        return this.Data[Idx];
    }

    SetField(aName, aValue) {
        const Idx = this.Parent.Fields.GetNo(aName);
        this.Data[Idx] = aValue;
    }

    GetAsDict() {
        let Res = {}
        for (const [Key, Value] of Object.entries(this.Parent.Fields.Data)) {
            Res[Key] = this.Data[Value[0]];
        }
        return Res;
    }
}


class TDbList {
    constructor(aData = {}) {
        //console.log('TDbList', aData);

        this.Empty();
        this.Rec = new TDbRec(this);

        if (Object.keys(aData).length > 0) {
            this.Import(aData);
        }
    }

    *[Symbol.iterator]() {
        for (let i = 0; i < this.GetSize(); i++) {
            this.RecNo = i;
            yield this.Rec;
        }
    }

    _RecInit() {
        if (! this.IsEmpty()) {
            this.Rec.SetData(this.Data[this._RecNo]);
        }
    }

    get RecNo() {
        return this._RecNo;
    }

    set RecNo(aNo) {
        if (this.IsEmpty()) {
            this._RecNo = 0;
        }else{
            if (aNo < 0) {
                aNo = this.GetSize() + aNo;
                this._RecNo = Math.min(aNo, this.GetSize() - 1);
            }
        }
        this._RecNo = aNo;
        this._RecInit();
    }

    IsEmpty() {
        return (this.GetSize() == 0);
    }

    Empty() {
        this.Data = [];
        this._RecNo = 0;
    }

    Import(aData) {
        this.Tag = aData['tag'];
        this.Data = aData['data'];
        this.Fields = new TDbFields(aData['head']);
        this.RecNo = 0;
        return this;
    }

    Export() {
        return {'data': this.Data, 'head': this.Fields.Export(), 'tag': this.Tag};
    }

    GetSize() {
        return this.Data.length;
    }

    RecAdd(aData = []) {
        if (aData.length > 0) {
            this.Rec.SetData(aData);
        } else {
            this.Rec.Init();
        }

        this.Data.push(this.Rec);
        this._RecNo = this.GetSize() - 1;
        return this.Rec;
    }

    Sort(aField) {
        const Idx = this.Fields.GetNo(aField);
        this.Data = this.Data.sort(function(aA, aB) {
            if (aA[Idx] < aB[Idx]) {
                return -1;
            }else if (aA[Idx] > aB[Idx]) {
                return 1;
            } else {
                return 0;
            }
        });
        this.RecNo = 0;
    }

    Shuffle() {
        this.Data = this.Data.sort(() => {
            const Rand = Math.random() > 0.5;
            return (Rand ? 1 : -1);
        });
        this.RecNo = 0;
        return this.Rec;
    }
}


/*
Data1 = '{"data": [["user2", 22, true], ["user1", 11, false], ["user3", 33, true], ["user4", 44, true]], "head": [["user", "str", ""], ["age", "int", 0], ["male", "bool", true]], "tag": 1}'
Data2 = JSON.parse(Data1)
Dbl = new TDbList(Data2)
console.log('AsDict', Dbl.Rec.GetAsDict())

Dbl.Sort('user')
for (let Rec of Dbl) {
    console.log(Rec.GetField('user'));
}

Dbl.RecAdd(['user5', 33, false])
Dbl.RecAdd()'user'
Dbl.Rec.SetField('user', 'pink')
Dbl.Rec.Flush()
console.log('size', Dbl.GetSize())

Dbl.Shuffle()
Data = Dbl.Export()
console.log(Data)
*/