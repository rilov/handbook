(function(){
  var input = document.getElementById('topic-search');
  if (!input) return;
  var list = document.querySelectorAll('.topic-list-item');
  
  input.addEventListener('input', function(){
    var q = input.value.trim().toLowerCase();
    if (!q) {
      list.forEach(function(li){li.style.display=''});
      return;
    }
    list.forEach(function(li){
      var text = (li.innerText || li.textContent).toLowerCase();
      if (text.indexOf(q) !== -1) {
        li.style.display = '';
      } else {
        li.style.display = 'none';
      }
    });
  });
})();
