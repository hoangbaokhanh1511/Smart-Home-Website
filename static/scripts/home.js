// Hiển thị giờ hiện tại
function clock() {
    let now = new Date();
    let hours = now.getHours();
    let minutes = now.getMinutes();
    let seconds = now.getSeconds();

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
realtime()
setInterval(realtime, 5000) // => đo 1 lần mỗi 5s

function mqt135() {
    fetch('/api/mqt135')
        .then(response => response.json())
        .then(data => {
            var value_of_mqt135 = data.value;
            if (value_of_mqt135 == 0) {
                document.getElementById('overal').innerHTML = "<b>No Data</b>"
            }
            else {
                document.getElementById('co2').innerHTML = "<b> Nồng độ CO<sub>2</sub> : " + data.value + " (ppm)</b>";

                var section = document.getElementById('overal');

                if (value_of_mqt135 <= 1000) {

                    section.innerHTML = `
                        <div class = 'd-flex p-3 justify-content-center gap-3 ' id='box'>
                        <div class="emoji">🙂</div>
                        <div style='color: #00e569; font-size:25px' class="text">Good</div>
                        </div>
                    `;
                    document.getElementById('box').style.backgroundColor = 'rgba(0, 229, 105, 0.3)'
                } else if (value_of_mqt135 <= 2000) {
                    section.innerHTML = `
                        <div class = 'd-flex p-3 gap-3 justify-content-center' id='box'>
                        <div class="emoji">🤒</div>
                        <div style='color:yellow; font-size:25px' class="text">Medium</div>
                        </div>
                    `;
                    document.getElementById('box').style.backgroundColor = 'rgba(220, 53, 69, 0.3)'

                } else {
                    section.innerHTML = `
                        <div class = 'd-flex p-3 justify-content-center gap-3' id='box'>
                            <div class="emoji">😵</div>
                            <div style="font-size:25px" class="text-danger">Danger</div>
                        </div>`;
                    document.getElementById('box').style.backgroundColor = 'rgba(255, 255, 0, 0.3)'

                }

            }

        })
        .catch(err => {
            console.error(err);
        });
}
mqt135();
setInterval(mqt135, 5000);

function pir() {
    fetch('/api/motion')
        .then(response => response.json())
        .then(data => {
            const status = data.status
            const element = document.getElementById('status_pir')
            if (status === true) {
                element.innerHTML = "Motion Detected!"
            }
            else {
                element.innerHTML = "No Motion!"
            }
        })
        .catch(err => {
            console.error(err)
        })
}
pir()
setInterval(pir, 5000) // => cứ mỗi 5s check 1 lần


// Thời tiết
var chart
function get_weather() {
    fetch('/api/weather_forecast')
        .then(response => response.json())
        .then(data => {
            updateChart(data)
            draw(data[0], 'Day1')

            update_box_weather(data[0], 'Day1')
            update_box_weather(data[1], 'Day2')
            update_box_weather(data[2], 'Day3')
            update_box_weather(data[3], 'Day4')
            update_box_weather(data[4], 'Day5')

        })
        .catch(err => {
            console.error(err);
        });
}

get_weather();

function update_box_weather(data, target) {

    var lst = data[target]
    var temp = lst.Weather.Temperature
    var hump = lst.Weather.Humidity
    var date_in_week = lst.Day
    var Icon_img = lst.Weather.Icon


    var maxTemp = Math.max(...temp)
    var idx = temp.indexOf(maxTemp)


    document.getElementById(target).innerHTML = date_in_week
    document.getElementById(target + 'img').src = Icon_img[idx]
    document.getElementById(target + 'temp').innerHTML = Math.round(maxTemp) + '°C'
    document.getElementById(target + 'hump').innerHTML = hump[idx] + '%'

}

function updateChart(data) {
    var day1 = data[0]
    var day2 = data[1]
    var day3 = data[2]
    var day4 = data[3]
    var day5 = data[4]

    var btn1 = document.getElementById('day1')
    var btn2 = document.getElementById('day2')
    var btn3 = document.getElementById('day3')
    var btn4 = document.getElementById('day4')
    var btn5 = document.getElementById('day5')


    btn1.addEventListener('click', () => draw(day1, 'Day1'))
    btn2.addEventListener('click', () => draw(day2, 'Day2'))
    btn3.addEventListener('click', () => draw(day3, 'Day3'))
    btn4.addEventListener('click', () => draw(day4, 'Day4'))
    btn5.addEventListener('click', () => draw(day5, 'Day5'))
}


function fill_title(icon, temp, hump, wind, time, day, main) {
    document.getElementById('img_title').src = icon
    document.getElementById('temperature_title').innerHTML = "Nhiệt độ: " + Math.round(temp) + "°C"
    document.getElementById('humidity_title').innerHTML = "Độ ẩm: " + hump + '%'
    document.getElementById('wind_title').innerHTML = "Gió: " + wind + 'km/h'
    document.getElementById('time_title').innerHTML = time + ' ' + day
    document.getElementById('main_weather_title').innerHTML = main
    document.getElementById('Title').innerHTML = "Thời Tiết"
}

function draw(day, target, date_in_week) {
    var data = day[target]

    var Times = data.Times.map(time => {
        return time.substring(0, 5)
    })
    var Humidity = data.Weather.Humidity
    var Temperature = data.Weather.Temperature
    var Speed = data.Wind.Speed
    var Main = data.Weather.Description
    var Icon = data.Weather.Icon_title

    var maxTemp = Math.max(...Temperature)
    var idx = Temperature.indexOf(maxTemp)

    fill_title(Icon[idx], Temperature[idx], Humidity[idx], Speed[idx], Times[idx], data.Day, Main[idx])
    if (chart) {
        chart.destroy(); // Hủy biểu đồ cũ trước khi tạo mới
    }

    var ctx = document.getElementById('myChart').getContext('2d');
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Times,
            datasets: [{
                pointRadius: 5,
                label: "Nhiệt độ (°c)",
                fill: true,
                backgroundColor: "rgb(236, 236, 65, 0.4)",
                borderColor: "yellow",
                data: Temperature
            }]
        },
        options: {
            legend: { display: false },
            title: {
                display: true,
                text: data.Day,
                fontSize: 16,
                fontColor: 'white'
            },
            scales: {
                Temperature: [{
                    ticks: {
                        min: 20, max: 45
                    }
                }],
                xAxes: [{
                    ticks: {
                        fontColor: 'white',
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Thời Gian',
                        fontColor: 'white',

                    }
                }],
                yAxes: [{
                    ticks: {
                        fontColor: 'white',
                        stepSize: 2,

                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Nhiệt độ',
                        fontColor: 'white'
                    }
                }],

            },
            /* event là đối tượng tiêu chuẩn của JS
                activeElements là mảng chứa các ptu của biểu đồ hiện đang được chọn
                Sự kiện click là 1 nhần nên sẽ lấy từ vị trí đầu tiên
            */
            onClick: (event, activeElements) => {
                if (activeElements.length > 0) {
                    const element = activeElements[0]; // lấy điểm click point trên biểu đồ

                    const index = element._index; // lấy vị trí trên biểu đồ

                    // lấy các thông số tương ứng
                    const temperature_title = Temperature[index]
                    const humidity_title = Humidity[index]
                    const time_title = Times[index].substring(0, 5)
                    const wind_title = Speed[index]
                    const main_title = Main[index]
                    const Icon_title = Icon[index]


                    fill_title(Icon[index], Temperature[index], Humidity[index], Speed[index], Times[index], data.Day, Main[index])

                }
            }
        }

    })

}
// Cập nhật lịch sử chuyển động
function fetch_pir() {
    fetch('/api/data_pir_5')
        .then(response => response.json())
        .then(data => {
            show_pir_data(data)
        })
        .catch(err => {
            console.error(err)
        })
}

setInterval(fetch_pir, 2000)
// => 2s cập nhật lịch sử 1 lần


function show_pir_data(data) {
    const time = data.time
    console.log(time)
    const box = document.getElementById('data_pir')

    box.innerHTML = ''
    if (time.length === 0) {
        box.innerHTMl = `
            <tr>
                <th scope='col'>
                    Không có dữ liệu
                <th>
            </tr>
        `
    }
    else {

        const row = document.createElement('tr');
        const cell1 = document.createElement('td');
        cell1.textContent = 'Thời Gian';
        row.appendChild(cell1);
        box.appendChild(row);
        // Đoạn trên là add thêm title


        for (let i = 0; i < time.length; i++) {
            const row = document.createElement('tr');
            const cell1 = document.createElement('td');
            cell1.textContent = time[i];
            row.appendChild(cell1);
            box.appendChild(row);
        }
    }
}
