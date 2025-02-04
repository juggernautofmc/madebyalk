// NAV SCRIPT
const navButton = document.querySelector('.navbutton');
const navItems = document.querySelector('.navitems');

navButton.addEventListener('click', () => {
    navItems.classList.toggle('hidden');
    let isClicked = navItems.getAttribute('aria-expanded') == 'false';
    navItems.setAttribute('aria-expanded', isClicked);
});