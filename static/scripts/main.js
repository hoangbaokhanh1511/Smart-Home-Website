// Xử lý cảm biến chuyển động
function pir() {
  fetch('/user_dashboard/api/motion')
    .then(response => response.json())
    .then(data => {
      const status = (data.status ? "Motion Detected!" : "No Motion")
      document.getElementById('pir').innerHTML = "Pir HC-SR501: " + status
    })
    .catch(err => {
      console.error(err)
    })
}
pir()
setInterval(pir, 3000) // => cứ mỗi 3s check 1 lần


// Xử lý cảm biến đo nhiệt độ và độ ẩm
function realtime() {
  fetch('/user_dashboard/api/weather')
    .then(response => response.json())
    .then(data => {
      document.getElementById('main_weather').innerHTML = "Trạng Thái Thời Tiết Hiện Tại: " + data.main
      document.getElementById('temperature').innerHTML = "Nhiệt độ hiện tại: " + data.temperature + "℃"
      document.getElementById('humidity').innerHTML = "Độ ẩm hiện tại: " + data.humidity + "%"
      document.getElementById('feels_like').innerHTML = "Nhiệt Độ cảm nhận: " + (data.feels_like).toFixed(2)  + "℃"
      document.getElementById('rain').innerHTML = "Lượng mưa trong 1 giờ qua: " + data.rain + " mm"
      document.getElementById('visibility').innerHTML = "Tầm nhìn khả thi: " + (data.visibility / 1000) + 'km'
    })
    .catch(err => {
      console.error('Lỗi khi gửi yêu cầu: ', err);
    });
}
realtime()
setInterval(realtime, 3600000) // => đo 1 lần mỗi 1h

//Xử lý các button về đèn
function change_status_led(name, state) {
  fetch('/user_dashboard/api/change_status_led', {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      led_name: name,
      state: state
    })

  })
    .then(response => response.json())
    .then(data => {
      console.log(data)
    })

    .catch(err => {
      console.error(err)
    })

}

// Lắng nghe sự kiện nhấn button
document.getElementById('Led_Main_On').addEventListener("click", function (event) {
  change_status_led("Led_Main", true)
})
document.getElementById('Led_Main_Off').addEventListener("click", function (event) {
  change_status_led("Led_Main", false)
})
document.getElementById('Led_D7_On').addEventListener("click", function (event) {
  change_status_led("Led_D7", true)
})
document.getElementById('Led_D7_Off').addEventListener("click", function (event) {
  change_status_led("Led_D7", false)
})
document.getElementById('Led_D8_On').addEventListener("click", function (event) {
  change_status_led("Led_D8", true)
})
document.getElementById('Led_D8_Off').addEventListener("click", function (event) {
  change_status_led("Led_D8", false)
})

// Hiển thị giờ hiện tại
function clock(){
  let now = new Date();
  let hours = now.getHours();
  let minutes = now.getMinutes();
  let seconds = now.getSeconds();

  hours = hours < 10 ? '0' + hours : hours;
  minutes = minutes < 10 ? '0' + minutes : minutes;
  seconds = seconds < 10 ? '0' + seconds : seconds;

  let currentTime = hours + ':' + minutes + ':' + seconds + ' - ' + now.getDate() + '/' + (now.getMonth() + 1) + '/' + now.getFullYear();


  document.getElementById('clock').innerText ="UTC+07:00 - " + currentTime;
}

setInterval(clock,1000)