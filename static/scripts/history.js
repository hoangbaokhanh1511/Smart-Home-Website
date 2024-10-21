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
        show_form_date.style.display = "none"

        fetch('/main/history', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ startDate: startDate, endDate: endDate }),
        })
            .then(response => response.json())
            .then(data => {
                let tableBody = document.querySelector("tbody")
                tableBody.innerHTML = "";
                if (data.length > 0) {

                    data.forEach(element => {
                        let row = `<tr>
                                    <td><input type="checkbox" class="delete-checkbox"
                                            data-timestamp="{{ element.timestamp }}" style="display: none;"></td>
                                    <td>Đã Phát Hiện Chuyển Động</td>
                                    <td>${element.timestamp}</td>
                                </tr>`
                        tableBody.innerHTML += row
                    })
                } else {
                    tableBody.innerHTML = `<th colspan="2">No data</th>`
                }
            })
            .catch(error => console.error('Error:', error))
    })
})

document.getElementById('selectAll').addEventListener('change', function () {
    const checkboxes = document.querySelectorAll('.delete-checkbox')
    checkboxes.forEach(checkbox => checkbox.checked = this.checked)
})

document.getElementById('delete').addEventListener('click', function () {

    document.querySelectorAll('.delete-checkbox').forEach(function (checkbox) {
        checkbox.style.display = 'inline-block'
    });
    document.getElementById('confirmDeleteBtn').style.display = 'inline-block'
});

document.getElementById('confirmDeleteBtn').addEventListener('click', function () {
    const selectedCheckboxes = document.querySelectorAll('.delete-checkbox:checked')
    const timestampsToDelete = Array.from(selectedCheckboxes).map(checkbox => checkbox.dataset.timestamp)

    if (timestampsToDelete.length > 0) {
        fetch('/main/history/delete', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ timestamps: timestampsToDelete }),
        })
            .then(response => response.json())
            .then(data => {

                console.log(data.message)

                location.reload()
            })
            .catch(error => console.error('Error:', error))
    } else {
        alert('Vui lòng chọn ít nhất một mục để xóa.')
    }
})

function clock() {
    let now = new Date()
    let hours = now.getHours()
    let minutes = now.getMinutes()
    let seconds = now.getSeconds()

    hours = hours < 10 ? '0' + hours : hours
    minutes = minutes < 10 ? '0' + minutes : minutes
    seconds = seconds < 10 ? '0' + seconds : seconds
    document.getElementById('time').innerText = hours + ':' + minutes + ':' + seconds
}
clock()
setInterval(clock, 1000)