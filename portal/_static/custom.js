var buttons = document.querySelectorAll('.modal-btn')
var backdrop = document.querySelector('.modal-backdrop')
var modals = document.querySelectorAll('.modal')

function openModal(i) {
  backdrop.style.display = 'block'
  modals[i].style.display = 'block'
}

function closeModal(i) {
  backdrop.style.display = 'none'
  modals[i].style.display = 'none'
}

for (i = 0; i < buttons.length; i++) {
  buttons[i].addEventListener(
    'click',
    (function (j) {
      return function () {
        openModal(j)
      }
    })(i)
  )
  backdrop.addEventListener(
    'click',
    (function (j) {
      return function () {
        closeModal(j)
      }
    })(i)
  )
}

function filter(classes) {
  for (var i = 0; i < classes.length; i++) {
      var elements = document.getElementsByClassName(classes[i]);
      console.log([elements.length, classes[i]]);
      for (var j = 0; j < elements.length; j++) {
          e = elements[j];
          if (e.style.display === "none !important") {
              e.style.display = "flex !important";
          } else {
              e.style.display = "none !important";
          }
      }
  }
}
