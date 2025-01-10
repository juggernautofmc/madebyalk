// NAV SCRIPT
const navButton = document.querySelector('.navbutton');
const navItems = document.querySelector('.navitems');

navButton.addEventListener('click', () => {
    navItems.classList.toggle('hidden');
    let isExpanded = navItems.getAttribute('aria-expanded') == 'false';
    navItems.setAttribute('aria-expanded', isExpanded);
});

// HIGHLIGHTS HOME PAGE SCRIPT
const time = 7000;
const images = ['images/slide_1.jpg', 'images/slide_2.jpg', 'images/slide_3.jpg'];
const captions = ['CLEAN<br>CUSTOM<br>APPAREL', 'SOCIAL<br>MEDIA<br>BANNERS', 'CUSTOM<br>MADE<br>SAMPLERS'];
const pos = ['0px -20px', '-380px 100px', '-180px 0px'];
const scale = ['100%', '180%', '121%'];
const slide_1 = document.querySelector('#SLIDE_1');
const slide_2 = document.querySelector('#SLIDE_2');
const slide_3 = document.querySelector('#SLIDE_3');
const slides = [slide_1, slide_2, slide_3];
const img = document.querySelector('.highlights');
const text = document.querySelector('#highlight-text');
var selectedSlide = document.querySelector('.selected');
var index = 0;

function slider(i) {
    img.style.backgroundImage = "url('" + images[i] + "')";
    img.style.backgroundPosition = pos[i];
    img.style.backgroundSize = scale[i];
    selectedSlide.classList.toggle('selected');
    slides[i].classList.toggle('selected');
    selectedSlide = document.querySelector('.selected');
    text.innerHTML = captions[i];
    if (i === 2) {
        index = 0
    } else {
        index = i + 1;
    }
}

let interval = setInterval(() => slider(index), time);

slide_1.addEventListener('click', () => {
    slider(0);
    clearInterval(interval);
    interval = setInterval(() => slider(index), time);
});

slide_2.addEventListener('click', () => {
    slider(1);
    clearInterval(interval);
    interval = setInterval(() => slider(index), time);
});

slide_3.addEventListener('click', () => {
    slider(2);
    clearInterval(interval);
    interval = setInterval(() => slider(index), time);
});

// Add touch event listeners
img.addEventListener('touchstart', (e) => {
    startX = e.touches[0].clientX; // Record the start point
});

img.addEventListener('touchmove', (e) => {
    endX = e.touches[0].clientX; // Update as the touch moves
});

img.addEventListener('touchend', () => {
    if (startX - endX > 400) {
        // Swipe left (show next slide)
        slider((index) % 3);
        
    } else if (endX - startX > 400) {
        // Swipe right (show previous slide)
        slider(((index - 2) + 3) % 3);
    }
    clearInterval(interval); // Reset the auto-sliding timer
    interval = setInterval(() => slider(index), time);
});