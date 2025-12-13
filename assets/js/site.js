/* site UI helpers: theme toggle and tiny helpers */
(function(){
  if (typeof window === 'undefined') return;
  var key = 'handbook-theme';
  var root = document.documentElement;
  var toggleID = 'theme-toggle';
  var current = localStorage.getItem(key) || (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');

  function setTheme(theme){
    if(!theme) return;
    if(theme === 'dark'){
      document.body.classList.add('dark-mode');
      document.getElementById(toggleID).textContent = '🌞';
    } else {
      document.body.classList.remove('dark-mode');
      document.getElementById(toggleID).textContent = '🌙';
    }
    localStorage.setItem(key, theme);
  }

  function init(){
    var t = document.getElementById(toggleID);
    if(!t) return;
    setTheme(current);
    t.addEventListener('click', function(){
      current = (current === 'dark') ? 'light' : 'dark';
      setTheme(current);
    });
  }

  // Wait for DOM
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
