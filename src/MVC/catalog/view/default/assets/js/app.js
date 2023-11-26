function showTooltip(aMsg, aId = null) {
    const tooltip = document.createElement("div");
    tooltip.classList.add("tooltip");
    tooltip.textContent = aMsg;
    if (aId) {
        const element = document.getElementById(aId)
        const rect = element.getBoundingClientRect()

        /*
        // ToDo. extra width
        tooltip.style.left = rect.left + 'px'
        tooltip.style.top = (rect.top + rect.height) + 'px'
        tooltip.style.right = 0
        console.log(tooltip.style.width)
        */
    }

    document.body.appendChild(tooltip);

    // apply the initial styles
    tooltip.offsetWidth;

    tooltip.classList.add("active");

    setTimeout(function () {
        tooltip.classList.remove("active");
        setTimeout(function () {
            document.body.removeChild(tooltip);
        }, 300);
    }, 2000);
}

class TDict {
    constructor() {
        this.data = {}
    }

    getValue(aPath) {
        const keys = aPath.split('/').filter(key => key !== '')
        let obj = this.data
        for (let key of keys) {
            obj = obj[key]
            if (obj === undefined) {
                return obj
            }
        }
        return obj
    }

    setValue(aPath, aVal) {
        const keys = aPath.split('/').filter(key => key !== '')
        let obj = this.data
        for (var key of keys.slice(0, -1)) {
            if (!obj.hasOwnProperty(key)) {
                obj[key] = {};
            }
            obj = obj[key]
        }

        let keyLast = keys[keys.length - 1]
        obj[keyLast] = aVal;
    }

    updValue(aPath, aVal) {
        let obj = this.getValue(aPath)
        if (obj != undefined && obj.constructor == Object && aVal.constructor == Object){
            aVal = { ...obj, ...aVal}
        }
        this.setValue(aPath, aVal)
    }
}
