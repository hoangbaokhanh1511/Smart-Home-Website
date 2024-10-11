function turnOnLight(e) {
    e.preventDefault()
    updateStatusLight(true)
}

function turnOffLight(e) {
    e.preventDefault()
    updateStatusLight(false)
}

function updateStatusLight(status) {
    fetch('/api/light', {
        method: "PUT",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: status }),
    })
        .then(res => res.json())
        .then(data => {
            const statusTag = document.getElementById('status-light')
            const show = data.status ? "On" : "Off"
            statusTag.innerHTML = show
        })
        .catch(err => {
            console.error(err)
        })
}

function turnOnFan1(e) {
    e.preventDefault()
    updateStatusFan1(true)
}
function turnOffFan1(e) {
    e.preventDefault()
    updateStatusFan1(false)
}

function updateStatusFan1(status) {
    fetch('/api/fan', {
        method: "PUT",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ fan1: status }),
    })
        .then(res => res.json())
        .then(data => {
            console.log(data)
            const statusTag = document.getElementById('status-fan1')
            const show = data.fan1 ? "On" : "Off"
            statusTag.innerHTML = show
        })
        .catch(err => {
            console.error(err)
        })
}

function turnOnFan2(e) {
    e.preventDefault()
    updateStatusFan2(true)
}
function turnOffFan2(e) {
    e.preventDefault()
    updateStatusFan2(false)
}

function updateStatusFan2(status) {
    fetch('/api/fan', {
        method: "PUT",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ fan2: status }),
    })
        .then(res => res.json())
        .then(data => {
            console.log(data)
            const statusTag = document.getElementById('status-fan2')
            const show = data.fan2 ? "On" : "Off"
            statusTag.innerHTML = show
        })
        .catch(err => {
            console.error(err)
        })
}

const temp_form = document.getElementById('temp-form')
temp_form.addEventListener('submit', function (e) {
    e.preventDefault()
    const startValue = document.getElementById('start-temp').value
    const endValue = document.getElementById('end-temp').value

    settingWarningTemperature(startValue, endValue)
})

function settingWarningTemperature(startValue, endValue) {
    fetch('/api/warningTemperature', {
        method: "PUT",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            min: startValue,
            max: endValue
        })
    })
        .then(res => res.json())
        .then(data => {
            const inputForm1 = document.getElementById('start-temp')
            const inputForm2 = document.getElementById('end-temp')
            inputForm1.value = ""
            inputForm2.value = ""

            const statusMin = document.getElementById('min')
            const statusMax = document.getElementById('max')
            statusMin.innerHTML = data.min
            statusMax.innerHTML = data.max

            const status = document.getElementById('status-temp-form')
            status.innerHTML = "Cài Đặt Thành Công"
            status.style.color = "green"
        })
        .catch(err => {
            console.error(err)
        })
}

const gas_form = document.getElementById('gas-form')
gas_form.addEventListener('submit', function (e) {
    e.preventDefault()
    const value = document.getElementById('valueGas').value

    settingWarningGas(value)
})

function settingWarningGas(value) {
    fetch('/api/warningGas', {
        method: "PUT",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            value: value
        })
    })
        .then(res => res.json())
        .then(data => {
            const status = document.getElementById('status-gas-form')
            const inputForm = document.getElementById('valueGas')
            inputForm.value = ""
            status.innerHTML = "Cài Đặt Thành Công"
            status.style.color = "green"
        })
        .catch(err => {
            console.error(err)
        })
}

const search_form_btn = document.getElementById('search')
const delete_form_btn = document.getElementById('delete')

search_form_btn.addEventListener('click', function (e) {
    e.preventDefault()
    const show_form_date = document.getElementById('search-form-block')
    show_form_date.style.display = "block"

    const solve_date = document.getElementById('search-form')
    solve_date.addEventListener('submit', function (e) {
        e.preventDefault()
        const startDate = document.getElementById('startDate').value
        const endDate = document.getElementById('endDate').value

        console.log(startDate)
        console.log(endDate)
        show_form_date.style.display = 'none'
    })
})



delete_form_btn.addEventListener('click', function (e) {
    e.preventDefault()
})