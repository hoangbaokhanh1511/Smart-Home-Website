document.getElementById('add').addEventListener("click", function (event) {
  show_form('/add')
})
document.getElementById('remove').addEventListener("click", function (event) {
  show_form('/remove')
})

function show_form(event){
  fetch(event)
  .then(response => response.text())
  .then(data => {
    document.getElementById('form').innerHTML = data
  })
  .catch (err => {
    console.error(err)
  })
}
