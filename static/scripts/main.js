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
setInterval(pir, 3000) // => cứ mỗi 3s check 1 lần


// Xử lý cảm biến đo nhiệt độ và độ ẩm
function realtime() {
  fetch('/user_dashboard/api/weather')
    .then(response => response.json())
    .then(data => {
      document.getElementById('temperature').innerHTML = "Nhiệt độ hiện tại: " + data.temperature + "℃"
      document.getElementById('humidity').innerHTML = "Độ ẩm hiện tại: " + data.humidity + "%"
    })
    .catch(err => {
      console.error('Lỗi khi gửi yêu cầu: ', err);
    });
}

setInterval(realtime, 5000) // => đo 1 lần mỗi 5s

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