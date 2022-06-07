document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.modal');
    var instances = M.Modal.init(elems, {});
    for (instance of instances){
        instance.open()
        }
  });


proxy = document.getElementById('id_proxy_server');
    proxy.addEventListener('change', function () {
        var chk = event.target
      if (chk.tagName === 'INPUT' && chk.type === 'checkbox' && chk.checked) {
        divs = document.querySelectorAll('.hide');
        for (elem of divs) {
            elem.classList.remove("hide");
        }
      }
      if (chk.tagName === 'INPUT' && chk.type === 'checkbox' && ! chk.checked) {
        divs = document.querySelectorAll(".row");
        for (elem of divs) {
            elem.classList.add("hide");
        }
      }
})