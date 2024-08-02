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
setInterval(pir, 5000) // => cứ mỗi 5s check 1 lần


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
realtime()
setInterval(realtime, 5000) // => đo 1 lần mỗi 5s

function mqt135() {
  fetch('/user_dashboard/api/mqt135')
  .then(response => response.json())
  .then(data => {
    var value_of_mqt135 = data.value;

    document.getElementById('mqt').innerHTML = "Nồng độ Co2: " + data.value + " (ppm)";

    var section = document.getElementById('Section');


    if (value_of_mqt135 <= 1000) {
      section.innerHTML = `
      <div class="row">
        <div class="text">Đánh giá: </div>
        <div class="box1">
          <div class="emoji">🙂</div>
          <div class="text">Good</div>
        </div>
      </div>`;
    } else if (value_of_mqt135 <= 2000) {
      section.innerHTML = `
      <div class="row">
        <div class="text">Đánh giá: </div>
        <div class="box2">
          <div class="emoji">🤒</div>
          <div class="text">Medium</div>
        </div>
      </div>`;
    } else {
      section.innerHTML = `
      <div class="row">
        <div class="text">Đánh giá: </div>
        <div class="box3">
          <div class="emoji">😵</div>
          <div class="text">Danger</div>
        </div>
      </div>`;
    }

  })
  .catch(err => {
    console.error(err);
  });
}
mqt135();
setInterval(mqt135, 2000);


//Xử lý các button về đèn
function change_status_led(name, data) {
  fetch('/user_dashboard/api/change_status_led', {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      led_name: name,
      value: data
    })

  })
    .then(response => response.json())
    .then(data => {})
    .catch(err => {
      console.error(err)
    })

}

// Lắng nghe sự kiện nhấn button
document.getElementById('Led_Main_On').addEventListener("click", function (event) {
  change_status_led("Led_Main", 0)
  document.getElementById('fade_led_Main').value = 1023
})
document.getElementById('Led_Main_Off').addEventListener("click", function (event) {
  change_status_led("Led_Main", 1023)
  document.getElementById('fade_led_Main').value = 0
})
document.getElementById('Led_D7_On').addEventListener("click", function (event) {
  change_status_led("Led_D7", 1023)
  document.getElementById('fade_led_D7').value = 1023
})
document.getElementById('Led_D7_Off').addEventListener("click", function (event) {
  change_status_led("Led_D7", 0)
  document.getElementById('fade_led_D7').value = 0
})
document.getElementById('Led_D8_On').addEventListener("click", function (event) {
  change_status_led("Led_D8", 1023)
  document.getElementById('fade_led_D8').value = 1023
})
document.getElementById('Led_D8_Off').addEventListener("click", function (event) {
  change_status_led("Led_D8", 0)
  document.getElementById('fade_led_D8').value = 0
})

// Hiển thị giờ hiện tại
function clock() {
  let now = new Date();
  let hours = now.getHours();
  let minutes = now.getMinutes();
  let seconds = now.getSeconds();

  hours = hours < 10 ? '0' + hours : hours;
  minutes = minutes < 10 ? '0' + minutes : minutes;
  seconds = seconds < 10 ? '0' + seconds : seconds;

  let currentTime = hours + ':' + minutes + ':' + seconds + ' - ' + now.getDate() + '/' + (now.getMonth() + 1) + '/' + now.getFullYear();

  document.getElementById('clock').innerText = "UTC+07:00 - " + currentTime;
}
clock()
setInterval(clock, 1000)


function dataPir() {
  fetch('/view/history_pir')
    .then(response => response.text())
    .then(data => {
      document.getElementById('infor').innerHTML = data
    })
    .catch(err => {
      console.error(err)
    })
}

if (document.getElementById('status').textContent == "ON") {
  dataPir()
  setInterval(dataPir, 10000)
}

function five_days(){
  fetch('/view/weather')
  .then(respone => respone.text())
  .then(data => {
    document.getElementById('five_days_weather').innerHTML = data
  })
  .catch(err => {
    console.error(err)
  })
}
five_days()


// Xử lý độ sáng cho các đèn

function Light (status, data){
  if (data == 0) document.getElementById(status).innerHTML = "Tắt Đèn!"
  else if (data >= 1 && data <= 511) document.getElementById(status).innerHTML = "Sáng Yếu!"
  else if (data >= 512 && data <= 1000) document.getElementById(status).innerHTML = "Sáng Vừa!"
  else document.getElementById(status).innerHTML = "Sáng Đèn!"
}


// => Led Main
document.getElementById('Option_Main').addEventListener('click', function() {
  document.getElementById('custom_light_Main').style.display = 'flex'
})

document.getElementById('fade_led_Main').addEventListener('input', function() {
  data = this.value
  Light('status_main',data)
})

document.getElementById('confirm_Main').addEventListener('click', function() {
  document.getElementById('custom_light_Main').style.display = 'none'
  // excuted_led('Led_Main', document.getElementById('fade_led_Main').value)
  change_status_led("Led_Main",Number(document.getElementById('fade_led_Main').value))
})



// => Led thứ nhất
document.getElementById('Option_D7').addEventListener('click', function() {
  document.getElementById('custom_light_D7').style.display = 'flex'
})

document.getElementById('fade_led_D7').addEventListener('input', function() {
  data = this.value
  Light('status_d7',data)
})

document.getElementById('confirm_D7').addEventListener('click', function() {
  document.getElementById('custom_light_D7').style.display = 'none'
  change_status_led("Led_D7",Number(document.getElementById('fade_led_D7').value))
})



// => Led Thứ hai
document.getElementById('Option_D8').addEventListener('click', function() {
  document.getElementById('custom_light_D8').style.display = 'flex'
})

document.getElementById('fade_led_D8').addEventListener('input', function() {
  data = this.value
  Light('status_d8',data)
})

document.getElementById('confirm_D8').addEventListener('click', function() {
  document.getElementById('custom_light_D8').style.display = 'none'
  change_status_led("Led_D8",Number(document.getElementById('fade_led_D8').value))
})