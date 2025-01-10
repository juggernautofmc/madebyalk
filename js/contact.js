// NAV SCRIPT
const navButton = document.querySelector('.navbutton');
const navItems = document.querySelector('.navitems');

navButton.addEventListener('click', () => {
    navItems.classList.toggle('hidden');
    let isClicked = navItems.getAttribute('aria-expanded') == 'false';
    navItems.setAttribute('aria-expanded', isClicked);
});

// SERVICES DROPDOWN

const branding = document.querySelector('#br');
const apparel = document.querySelector('#ap');
const socialMedia = document.querySelector('#sm');
const sampler = document.querySelector('#vd');
const txt1 = document.querySelector('#txt1');
const txt2 = document.querySelector('#txt2');
const txt3 = document.querySelector('#txt3');
const txt4 = document.querySelector('#txt4');

function expand(txt, button) {
    let isExpanded = txt.getAttribute('aria-expanded') == 'false';
    if (isExpanded) {
        button.style.backgroundImage = "url('images/retract-arrow.png')";
    } else {
        button.style.backgroundImage = "url('images/arrow.png')";
    }
    txt.classList.toggle('collapsed');
    txt.setAttribute('aria-expanded', isExpanded);
}

branding.addEventListener('click', () => {
    expand(txt1, branding);
});

apparel.addEventListener('click', () => {
    expand(txt2, apparel);
});

socialMedia.addEventListener('click', () => {
    expand(txt3, socialMedia);
});

sampler.addEventListener('click', () => {
    expand(txt4, sampler);
});

// FORM FILE SELECTION

const serviceType = document.getElementById('service-type');
const fileUpload = document.querySelector('.dialog-box');
const instructions = document.querySelector('.dialog-box h4');
const inputGroup = document.getElementById('input-group');
let isApparel = false;
let isSampler = false;

serviceType.addEventListener('change', () => {
    const serviceValue = serviceType.value;

    if (serviceValue === 'Apparel' && !isApparel) {
        // Switch to "Apparel" view
        instructions.innerHTML = 'Upload Vector Files for Apparel';
        if (!isSampler) fileUpload.classList.remove('collapsed'); // Open if collapsed
        inputGroup.style.height = '600px';
        isApparel = true;
        isSampler = false;
    } else if (serviceValue === 'Sampler' && !isSampler) {
        // Switch to "Sampler" view
        instructions.innerHTML = 'Upload Video Clips for Sampler';
        if (!isApparel) fileUpload.classList.remove('collapsed'); // Open if collapsed
        inputGroup.style.height = '600px';
        isSampler = true;
        isApparel = false;
    } else if (serviceValue !== 'Apparel' && serviceValue !== 'Sampler' && (isApparel || isSampler)) {
        // Reset to default if neither "Apparel" nor "Sampler" is selected
        fileUpload.classList.add('collapsed'); // Collapse only when switching away
        inputGroup.style.height = '450px';
        isApparel = false;
        isSampler = false;
    }
});


const fileInput = document.getElementById('fileInput');
const fileName = document.getElementById('fileName');

fileInput.addEventListener('change', handleFileSelect);

function handleFileSelect(event) {
    const files = event.target.files; // Get selected files
    const fileListDiv = document.getElementById('fileList');
    fileListDiv.innerHTML = ''; // Clear the previous file list
  
    if (files.length > 0) {
      const fileList = document.createElement('ul'); // Create a list for displaying files
      fileList.style.listStyle = 'none';
      for (let i = 0; i < files.length; i++) {
        const listItem = document.createElement('li');
        listItem.textContent = `${files[i].name}`;
        fileList.appendChild(listItem);
      }
      fileListDiv.appendChild(fileList);
    } else {
      fileListDiv.textContent = 'No files selected.';
    }
  }