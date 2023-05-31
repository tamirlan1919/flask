let img = document.getElementById('img')
let video = document.querySelector('video')

console.log(img)

img.onclick = function(){
    video.setAttribute('controls','True')
    video.play()
    img.style.display = 'none'
}


let selectElement = document.getElementById("city-select");
      
selectElement.addEventListener("change", function() {
  let selectedOption = selectElement.options[selectElement.selectedIndex];

  let phoneNumberElement = document.getElementById("phone-number");
  phoneNumberElement.textContent = selectedOption.getAttribute("data-phone");
});

function opennav(){

document.getElementById('modal-nav').style.display = 'block'
document.getElementById('list').style.display = 'none'
document.getElementById('exit').style.display = 'block'

}

function closenav(){
document.getElementById('modal-nav').style.display = 'none'
document.getElementById('exit').style.display = 'none'
document.getElementById('list').style.display = 'block'
}
function closebut(){

document.getElementById('modal-nav').style.display = 'none'
document.getElementById('list').style.display = 'block'
}


var modal = document.getElementById("myModal");
var btn = document.getElementById("openModalBtn");
var btn2 = document.getElementById("openModalBtnn");

var span = document.getElementsByClassName("close")[0];
var form = document.getElementById("myForm");

btn.onclick = function() {
  modal.style.display = "block";
};
btn2.onclick = function(){
    modal.style.display = "block";

}

span.onclick = function() {
  modal.style.display = "none";
};

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
};

form.addEventListener("submit", function(e) {
  e.preventDefault();
  var name = form.elements["name"].value;
  var phone = form.elements["phone"].value;
  
  // Здесь вы можете добавить логику для обработки отправки данных формы
  // Например, отправка данных на сервер или выполнение других операций
  
  modal.style.display = "none";
  form.reset();
});
