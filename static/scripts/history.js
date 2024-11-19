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

// Pagination   
document.addEventListener("DOMContentLoaded", function () {
    const rowsPerPage = 10;
    const tableBody = document.getElementById("table-body");
    const pagination = document.getElementById("pagination");

    // Lấy danh sách các dòng
    const rows = Array.from(tableBody.querySelectorAll("tr"));
    const totalPages = Math.ceil(rows.length / rowsPerPage);

    let currentPage = 1;

    function renderTable(page) {
        // Ẩn tất cả các dòng
        rows.forEach((row, index) => {
            row.style.display = "none";
            if (index >= (page - 1) * rowsPerPage && index < page * rowsPerPage) {
                row.style.display = ""; // Hiển thị dòng của trang hiện tại
            }
        });
    }

    function updatePagination() {
        // Xóa nút cũ và tạo lại nút cho từng trang
        const prevPage = document.getElementById("prev-page");
        const nextPage = document.getElementById("next-page");
        const pageItems = Array.from(pagination.querySelectorAll(".page-item")).filter(
            item => item !== prevPage && item !== nextPage
        );
        pageItems.forEach(item => item.remove());

        for (let i = 1; i <= totalPages; i++) {
            const pageItem = document.createElement("li");
            pageItem.classList.add("page-item", i === currentPage ? "active" : "");
            pageItem.innerHTML = `<a class="page-link" href="#">${i}</a>`;
            pageItem.addEventListener("click", () => {
                currentPage = i;
                renderTable(currentPage);
                updatePagination();
            });
            pagination.insertBefore(pageItem, nextPage);
        }

        // Vô hiệu hóa nút "Previous" và "Next" nếu cần
        prevPage.classList.toggle("disabled", currentPage === 1);
        nextPage.classList.toggle("disabled", currentPage === totalPages);
    }

    document.getElementById("prev-page").addEventListener("click", function (e) {
        e.preventDefault();
        if (currentPage > 1) {
            currentPage--;
            renderTable(currentPage);
            updatePagination();
        }
    });

    document.getElementById("next-page").addEventListener("click", function (e) {
        e.preventDefault();
        if (currentPage < totalPages) {
            currentPage++;
            renderTable(currentPage);
            updatePagination();
        }
    });

    // Khởi tạo hiển thị
    renderTable(currentPage);
    updatePagination();
});