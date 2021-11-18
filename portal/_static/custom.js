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


function change() {
  var affiliationCbs = document.querySelectorAll(".affiliation input[type='checkbox']");
  var domainsCbs = document.querySelectorAll(".domains input[type='checkbox']");
  var formatsCbs = document.querySelectorAll(".formats input[type='checkbox']");
  var packagesCbs = document.querySelectorAll(".packages input[type='checkbox']");

  var filters = {
    affiliation: getClassOfCheckedCheckboxes(affiliationCbs),
    domains: getClassOfCheckedCheckboxes(domainsCbs),
    formats: getClassOfCheckedCheckboxes(formatsCbs),
    packages: getClassOfCheckedCheckboxes(packagesCbs)
  };

  filterResults(filters);
}

function getClassOfCheckedCheckboxes(checkboxes) {
  var classes = [];

  if (checkboxes && checkboxes.length > 0) {
    for (var i = 0; i < checkboxes.length; i++) {
      var cb = checkboxes[i];

      if (cb.checked) {
        classes.push(cb.getAttribute("rel"));
      }
    }
  }

  return classes;
}

function filterResults(filters) {
  var rElems = document.querySelectorAll(".tagged-card");
  var hiddenElems = [];

  if (!rElems || rElems.length <= 0) {
    return;
  }

  for (var i = 0; i < rElems.length; i++) {
    var el = rElems[i];

    if (filters.affiliation.length > 0) {
      var isHidden = true;

      for (var j = 0; j < filters.affiliation.length; j++) {
        var filter = filters.affiliation[j];

        if (el.classList.contains(filter)) {
          isHidden = false;
          break;
        }
      }

      if (isHidden) {
        hiddenElems.push(el);
      }
    }

    if (filters.domains.length > 0) {
      var isHidden = true;

      for (var j = 0; j < filters.domains.length; j++) {
        var filter = filters.domains[j];

        if (el.classList.contains(filter)) {
          isHidden = false;
          break;
        }
      }

      if (isHidden) {
        hiddenElems.push(el);
      }
    }

    if (filters.formats.length > 0) {
      var isHidden = true;

      for (var j = 0; j < filters.formats.length; j++) {
        var filter = filters.formats[j];

        if (el.classList.contains(filter)) {
          isHidden = false;
          break;
        }
      }

      if (isHidden) {
        hiddenElems.push(el);
      }
    }

    if (filters.packages.length > 0) {
      var isHidden = true;

      for (var j = 0; j < filters.packages.length; j++) {
        var filter = filters.packages[j];

        if (el.classList.contains(filter)) {
          isHidden = false;
          break;
        }
      }

      if (isHidden) {
        hiddenElems.push(el);
      }
    }
  }

  for (var i = 0; i < rElems.length; i++) {
    rElems[i].classList.replace("d-none", "d-flex");
  }

  if (hiddenElems.length <= 0) {
    return;
  }

  for (var i = 0; i < hiddenElems.length; i++) {
    hiddenElems[i].classList.replace("d-flex", "d-none");
  }
}


function clearCbs() {
  var affiliationCbs = document.querySelectorAll(".affiliation input[type='checkbox']");
  var domainsCbs = document.querySelectorAll(".domains input[type='checkbox']");
  var formatsCbs = document.querySelectorAll(".formats input[type='checkbox']");
  var packagesCbs = document.querySelectorAll(".packages input[type='checkbox']");

  for (var i = 0; i < affiliationCbs.length; i++) {
    affiliationCbs[i].checked=false;
  }

  for (var i = 0; i < domainsCbs.length; i++) {
    domainsCbs[i].checked=false;
  }

  for (var i = 0; i < formatsCbs.length; i++) {
    formatsCbs[i].checked=false;
  }

  for (var i = 0; i < packagesCbs.length; i++) {
    packagesCbs[i].checked=false;
  }

  change();
}
