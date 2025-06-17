
    // Gestion du dark mode
    const themeToggle = document.getElementById('theme-toggle');
    const themeToggleMobile = document.getElementById('theme-toggle-mobile');
    const html = document.documentElement;
    
    function toggleTheme() {
      html.classList.toggle('dark');
      localStorage.setItem('darkMode', html.classList.contains('dark'));
    }
    
    if (localStorage.getItem('darkMode') === 'true') {
      html.classList.add('dark');
    } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      html.classList.add('dark');
      localStorage.setItem('darkMode', 'true');
    }
    
    themeToggle.addEventListener('click', toggleTheme);
    themeToggleMobile.addEventListener('click', toggleTheme);
    
    // Menu mobile
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    mobileMenuButton.addEventListener('click', () => {
      mobileMenu.classList.toggle('open');
    });
    
    // Fermer le menu mobile en cliquant à l'extérieur
    document.addEventListener('click', (e) => {
      if (!mobileMenu.contains(e.target) && !mobileMenuButton.contains(e.target)) {
        mobileMenu.classList.remove('open');
      }
    });
    const toggleMobileMenu = () => {
    const menu = document.getElementById('mobile-menu');
    menu.classList.toggle('hidden');
    window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    document.getElementById('mobile-menu-button')?.addEventListener('click', toggleMobileMenu);
