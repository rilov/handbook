/* site UI helpers: theme toggle and tiny helpers */
(function(){
  if (typeof window === 'undefined') return;
  var key = 'handbook-theme';
  var root = document.documentElement;
  var toggleID = 'theme-toggle';
  // Default to light (white) theme unless user has a saved preference
  var current = localStorage.getItem(key) || 'light';
  var headerKey = 'handbook-header-style';
  var headerStyles = ['header-style-no-border','header-style-flat','header-style-accent','header-style-glass','header-style-compact'];
  var currentHeader = localStorage.getItem(headerKey) || 'header-style-accent';

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
    setHeaderStyle(currentHeader);
    t.addEventListener('click', function(){
      current = (current === 'dark') ? 'light' : 'dark';
      setTheme(current);
    });
    // allow quick test cycling of header styles with Shift+H
    document.addEventListener('keydown', function(e){
      if(e.key === 'H' && e.shiftKey){
        var i = headerStyles.indexOf(currentHeader);
        i = (i + 1) % headerStyles.length;
        currentHeader = headerStyles[i];
        setHeaderStyle(currentHeader);
      }
    });
  }

  function setHeaderStyle(style){
    if(!style) return;
    headerStyles.forEach(function(s){ document.body.classList.remove(s); });
    document.body.classList.add(style);
    localStorage.setItem(headerKey, style);
    // small console message so devs know the state when testing
    try{ console.info('Header style set to', style); }catch(e){}
  }

  // Wait for DOM
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
