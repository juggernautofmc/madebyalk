// EMAIL SCRIPT
document.addEventListener('DOMContentLoaded', () => {
const flaskData = document.getElementById('submitted-data').dataset;

let success = JSON.parse(flaskData.success);
const key = flaskData.key;
emailjs.init(key);

if (success) {
    let ID = JSON.parse(flaskData.id);
    let customerName = flaskData.name;
    let companyName = flaskData.company;
    let serv = flaskData.service;
    let email = flaskData.email;
    let details = flaskData.details;

    let emailParams = {
        id: ID,
        to_name: customerName,
        user_email: email,
        company_name: companyName,
        service: serv,
        message: details
    };
    
    emailjs.send("service_cxcl4of", "template_0lsqlog", emailParams, key)
    .then((response) => {
        console.log("Email to client: Success!", response.status, response.text);
        emailjs.send("service_cxcl4of", "template_e4h1sos", emailParams, key)
        .then((response) => {
            console.log("Email to system: Success!", response.status, response.text);
            alert("Thank you for submitting! A confirmation email has just been sent out to you.");
            window.location.href = "/contact";
        })
        .catch((error) => {
            console.error("Error", error)
            alert("Error: Confirmation email is unable to be sent");
        })
    })
    .catch((error) => {
        console.error("Error:", error);
        alert("Email address entered is not valid. Please check to make sure you entered it in correctly.");
        window.location.href = "/contact";
    }); 
}
});

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
const infographics = document.querySelector('#in');
const txt1 = document.querySelector('#txt1');
const txt2 = document.querySelector('#txt2');
const txt3 = document.querySelector('#txt3');
const txt4 = document.querySelector('#txt4');

function expand(txt, button) {
    let isExpanded = txt.getAttribute('aria-expanded') == 'false';
    if (isExpanded) {
        button.style.backgroundImage = "url('static/images/retract-arrow.png')";
    } else {
        button.style.backgroundImage = "url('static/images/arrow.png')";
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

infographics.addEventListener('click', () => {
    expand(txt4, infographics);
})

// FORM FILE SELECTION

const serviceType = document.getElementById('service-type');
const fileUpload = document.querySelector('.dialog-box');
const instructions = document.querySelector('.dialog-box h4');
const inputGroup = document.getElementById('input-group');
let isApparel = false;

serviceType.addEventListener('change', () => {
    const serviceValue = serviceType.value;

    if (serviceValue === 'Apparel' && !isApparel) {
        // Switch to "Apparel" view
        instructions.innerHTML = 'Upload Vector Files for Apparel';
        fileUpload.classList.remove('collapsed'); // Open if collapsed
        inputGroup.style.height = '600px';
        isApparel = true;
    } else {
        // Reset to default
        fileUpload.classList.add('collapsed'); // Collapse only when switching away
        inputGroup.style.height = '450px';
        isApparel = false;
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

// CONTACT FORM SUBMISSION
const form = document.getElementById('input-group');

form.addEventListener('submit', async () => {
    formData = new FormData();

    let name = document.getElementById('name').value;
    let companyName = document.getElementById('company_name').value;
    let serviceType = document.getElementById('service_type').value;
    let email = document.getElementById('email').value;
    let file = document.getElementById('fileInput').value;
    let message = document.getElementById('message').value;

    formData.append('name', name);
    formData.append('company_name', companyName);
    formData.append('service_type', serviceType);
    formData.append('email', email);

    const { url } = await put(file.name, file.files[0], { access: 'public' });

    file_path = url;

    formData.append('file', file_path);
    formData.append('message', message);

    fetch('/submit', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = "/submit";  // Redirect to Flask route
        } else {
            alert("Form submission failed: " + data.error);
        }
    });
});