/*
Copyright:  Vladimir Vons, UA
Author:     Vladimir Vons <VladVons@gmail.com>
Created:    2022.05.03
Fork:       Inc/DbList/DbList.py
*/


class TDbRec {
    constructor(aData = [], aFields = {}) {
        this.Data = aData
        this.Fields = aFields
    }

    GetAsDict() {
        let Res = {}
        for (const [Key, Val] of Object.entries(this.Fields)) {
            Res[Key] = this.Data[Val]
        }
        return Res
    }

    GetAsDictFields(aFields) {
        let Res = {}
        for (const xField of aFields) {
            Res[xField] = this.GetField(xField)
        }
        return Res
    }

    GetAsList() {
        return this.Data
    }

    GetAsListFields(aFields) {
        let Res = []
        for (const xField of aFields) {
            Res.push(this.GetField(xField))
        }
        return Res
    }

    GetField(aName) {
        const Idx = this.Fields[aName]
        return this.Data[Idx]
    }

    GetFields() {
        return Object.keys(this.Fields)
    }

    Init(aFields, aData) {
        for (let i = 0; i < aFields.length; i++) {
            const x = aFields[i]
            this.Fields[x] = i
        }
        this.Data = aData
        return this
    }

    SetAsDict(aData) {
        for (const [Key, Val] of Object.entries(aData)) {
            this.SetField(Key, Val)
        }
        return this
    }

    SetField(aName, aVal) {
        const Idx = this.Fields[aName]
        this.Data[Idx] = aVal
    }
}


class TDbList {
    constructor(aData = {}) {
        //console.log('TDbList', aData)

        this.Empty()
        this.Rec = new TDbRec()

        if (Object.keys(aData).length > 0) {
            this.Import(aData)
        }
    }

    *[Symbol.iterator]() {
        for (let i = 0; i < this.GetSize(); i++) {
            this.RecNo = i
            yield this.Rec
        }
    }

    _RecInit() {
        if (this.GetSize() > 0) {
            this.Rec.Data = this.Data[this._RecNo]
        }
    }

    _RecInRange(aNo) {
        if (aNo < 0) {
            aNo = this.GetSize() + aNo
        }
        return Math.min(aNo, this.GetSize() - 1)
    }

    get RecNo() {
        return this._RecNo
    }

    set RecNo(aNo) {
        if (this.GetSize() == 0) {
            this._RecNo = 0
        }else{
            this._RecNo = this._RecInRange(aNo)
        }
        this._RecInit()
    }

    Clone(aFields = []) {
        if (aFields.length == 0) {
            var Exp = this.Export()
        }else{
            let Data = []
            for (const Rec of this) {
                Data.push(Rec.GetAsListFields(aFields))
            }
            var Exp = {'head': aFields, 'data': Data}
        }
        return new TDbList(Exp)
    }

    Empty() {
        this.Data = []
        this._RecNo = 0
        return this
    }

    Export() {
        return {'head': this.Rec.GetFields(), 'data': this.Data}
    }

    ExportStr() {
        return JSON.stringify(this.Export())
    }

    GetSize() {
        return this.Data.length
    }

    Import(aData) {
        this.Data = aData['data']
        this.Rec.Init(aData['head'], this.Data[0])
        this.RecNo = 0
        return this
    }

    ImportStr(aData) {
        return this.Import(JSON.parse(aData))
    }

    RecAdd(aData = []) {
        const Len = Object.keys(this.Rec.Fields).length
        if (aData.length == 0) {
            aData = Array(Len)
        }else{
            console.assert(aData.length == Len, 'wrong length')
        }

        this.Data.push(aData)
        this._RecNo = this.GetSize() - 1
        this._RecInit()
        return this.Rec
    }

    RecPop(aNo = -1) {
        aNo = this._RecInRange(aNo)
        return new TDbRec(this.Data.splice(aNo, 1), this.Rec.Fields)
    }
}


class TDbListEx extends TDbList {
    ExportDict(aFields = []) {
        if (aFields.length == 0) {
            aFields = this.Rec.GetFields()
        }

        let Res = []
        for (const Rec of this) {
            Res.push(Rec.GetAsDictFields(aFields))
        }
        return Res
    }

    ImportDict(aData, aFields = []) {
        if (aFields.length == 0) {
            aFields = Object.keys(aData[0])
        }

        let Data = []
        for (const xData of aData) {
            let Row = []
            for (const xField of aFields) {
                Row.push(xData[xField])
            }
            Data.push(Row)
        }
        return this.Import({'head': aFields, 'data': Data})
    }

    Sort(aField) {
        const Idx = this.Rec.Fields[aField]
        this.Data = this.Data.sort(
            function(aA, aB) {
                if (aA[Idx] < aB[Idx]) {
                    return -1
                }else if (aA[Idx] > aB[Idx]) {
                    return 1
                } else {
                    return 0
                }
        })
        this.RecNo = 0
        return this
    }
}
