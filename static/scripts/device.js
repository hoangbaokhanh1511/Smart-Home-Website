document.addEventListener('DOMContentLoaded', function () {
    fetch('/api/warningTemperature')
        .then(res => res.json())
        .then(data => {
            const alertWarning = document.getElementById('max')
            const status_warning_temp = document.getElementById('status_warning_temp')

            status_warning_temp.innerHTML = data.status ? "On" : "Off"
            alertWarning.innerHTML = data.value + "℃"

        })
        .catch(err => { console.error(err) })

    fetch('/api/warningGas')
        .then(res => res.json())
        .then(data => {
            const alertWarning = document.getElementById('gasMax')
            const status_warning_gas = document.getElementById('status_warning_gas')

            status_warning_gas.innerHTML = data.status ? "On" : "Off"
            alertWarning.innerHTML = data.value + " (ppm)"

        })
        .catch(err => { console.error(err) })

    fetch('/api/fan')
        .then(res => res.json())
        .then(data => {
            const statusTag1 = document.getElementById('status-fan1')
            const statusTag2 = document.getElementById('status-fan2')
            const show1 = data.fan1 ? "On" : "Off"
            const show2 = data.fan2 ? "On" : "Off"
            statusTag1.innerHTML = show1
            statusTag2.innerHTML = show2
        })

    fetch('/api/light')
        .then(res => res.json())
        .then(data => {
            const statusTag = document.getElementById('status-light')
            const show = data.status ? "On" : "Off"
            statusTag.innerHTML = show
        })
        .catch(err => { console.error(err) })

})


const temp_form = document.getElementById('temp-form')
temp_form.addEventListener('submit', function (e) {
    e.preventDefault()
    const Value = document.getElementById('temp').value
    settingWarningTemperature(Value)
})

function settingWarningTemperature(Value) {
    fetch('/api/warningTemperature', {
        method: "PUT",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            value: Value
        })
    })
        .then(res => res.json())
        .then(data => {
            const inputForm = document.getElementById('temp')
            inputForm.value = ""

            const alertWarning = document.getElementById('max')
            alertWarning.innerHTML = data.value + "℃"

            const status = document.getElementById('status-temp-form')
            status.innerHTML = "Cài đặt thành công"
            status.style.color = "#55fb83"
            // status.style.fontWeight = "bold"


        })
        .catch(err => {
            console.error(err)
        })
}

const required_tempMax = document.getElementById('required_tempMax')
const off_tempMax = document.getElementById('off_tempMax')
const status_tempMax = document.getElementById('status_tempMax')
const status_warning_temp = document.getElementById('status_warning_temp')

required_tempMax.addEventListener('click', function (e) {
    e.preventDefault()
    const alertWarning = document.getElementById('max').innerText
    if (alertWarning != "None") {
        status_tempMax.innerHTML = "Cài đặt thành công"
        status_tempMax.style.color = "#55fb83"
        status_warning_temp.innerHTML = "On"
        tranfer_warning(true)

    }
    else {
        status_tempMax.innerHTML = "Cài đặt thất bại"
        status_tempMax.style.color = "#ff5757"
    }
})

off_tempMax.addEventListener('click', function (e) {
    status_warning_temp.innerHTML = "Off"
    tranfer_warning(false)
    status_tempMax.innerHTML = "Cài đặt thành công"
    status_tempMax.style.color = "#55fb83"
})

function tranfer_warning(value) {
    fetch('/api/warningTemperature', {
        method: "PUT",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            status: value
        })
    })
}

const required_gasMax = document.getElementById('required_gasMax')
const off_gasMax = document.getElementById('off_gasMax')
const status_gasMax = document.getElementById('status_gasMax')
const status_warning_gas = document.getElementById('status_warning_gas')

required_gasMax.addEventListener('click', function (e) {
    e.preventDefault()
    const alertWarning = document.getElementById('gasMax').innerText
    if (alertWarning != "None") {
        status_gasMax.innerHTML = "Cài đặt thành công"
        status_gasMax.style.color = "#55fb83"
        status_warning_gas.innerHTML = "On"
        tranfer_warning_gas(true)

    }
    else {
        status_gasMax.innerHTML = "Cài đặt thất bại"
        status_gasMax.style.color = "#ff5757"
    }
})

off_gasMax.addEventListener('click', function (e) {
    status_warning_gas.innerHTML = "Off"
    tranfer_warning_gas(false)
    status_gasMax.innerHTML = "Cài đặt thành công"
    status_gasMax.style.color = "#55fb83"
})

function tranfer_warning_gas(value) {
    fetch('/api/warningGas', {
        method: "PUT",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            status: value
        })
    })
}

const warning_description = document.getElementById('warning_description')
warning_description.addEventListener('click', function (e) {
    e.preventDefault()
    alert("Các mức cảnh báo:\n- Mức An Toàn 0-200\n- Mức Cảnh Báo Thấp 200-500\n- Mức Cảnh Báo Cao > 500")
})

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

            const alertWarningGas = document.getElementById('gasMax')
            alertWarningGas.innerHTML = data.value + " (ppm)"

            status.innerHTML = "Cài đặt thành công"
            status.style.color = "#55fb83"
            // status.style.fontWeight = "bold"
        })
        .catch(err => {
            console.error(err)
        })
}

function gas() {
    fetch('/api/mqt2')
        .then(res => res.json())
        .then(data => {
            const mqt2 = document.getElementById('mqt2')
            mqt2.innerHTML = data.value
            mqt2.style.color = "rgb(67, 255, 57)"
            mqt2.style.fontSize = "40px"
        })
        .catch(err => {
            console.error(err)
        })
}
setTimeout(gas, 3000)


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

function clock() {
    let now = new Date();
    let hours = now.getHours();
    let minutes = now.getMinutes();

    hours = hours < 10 ? '0' + hours : hours;
    minutes = minutes < 10 ? '0' + minutes : minutes;
    document.getElementById('time').innerText = hours + ' : ' + minutes

    let currentTime = now.getDate() + '/' + (now.getMonth() + 1) + '/' + now.getFullYear();
    document.getElementById('date').innerText = currentTime;
}
clock()
setInterval(clock, 1000)

function realtime() {
    fetch('/api/dht11')
        .then(response => response.json())
        .then(data => {
            const temp = data.temperature
            const hum = data.humidity
            if (temp && hum) {
                document.getElementById('temperature').innerHTML = temp + "℃"
                document.getElementById('humidity').innerHTML = hum + "%"
            }

            else {
                document.getElementById('temperature').innerHTML = "No data"
                document.getElementById('humidity').innerHTML = "No data"
            }


        })
        .catch(err => {
            console.error('Lỗi khi gửi yêu cầu: ', err);
        });
}
setTimeout(realtime, 2000)

