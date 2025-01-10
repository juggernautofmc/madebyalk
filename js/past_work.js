// NAV SCRIPT
const navButton = document.querySelector('.navbutton');
const navItems = document.querySelector('.navitems');

navButton.addEventListener('click', () => {
    navItems.classList.toggle('hidden');
    let isClicked = navItems.getAttribute('aria-expanded') == 'false';
    navItems.setAttribute('aria-expanded', isClicked);
});


// PORTFOLIO SCRIPT

function createSlider(project, buttonGroup, imageContainer, image) {
    const images = project.images; // Images array from the project
  
    // Get all slide buttons for this particular slider
    const slides = buttonGroup.querySelectorAll('li');
  
    function slider(i) {
      // Ensure we're only updating the image inside this particular container
      const currentImage = imageContainer.querySelector('.portfolio-image');
      currentImage.src = images[i]; // Update the image's `src` for the selected slide
  
      // Remove the 'selected' class only within the current buttonGroup
      buttonGroup.querySelector('.selected')?.classList.remove('selected');
  
      // Add 'selected' class to the current slide button
      slides[i].classList.add('selected');
    }
  
    slides.forEach((slide, i) => {
      slide.addEventListener('click', () => {
        slider(i); // Show the selected image when button is clicked
      });
    });
  }
  
  fetch('portfolios/portfolio_data.json')
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json(); // Convert the response to JSON
    })
    .then(projects => {
      const container = document.querySelector('.portfolio-container');
  
      if (!container) {
        console.error("Error: '.portfolio-container' not found in the document.");
        return;
      }
  
      projects.forEach(project => {
        const entryDiv = document.createElement('div');
        entryDiv.classList.add('portfolio-entry');
  
        const imageContainer = document.createElement('div');
        imageContainer.classList.add('image-container');
  
        if (Array.isArray(project.images) && project.images.length > 0) {
          if (project.images[0].startsWith('https')) {
            let vid = document.createElement('iframe');
            vid.src = project.images[0];
            vid.width = "300";
            vid.height = "167.75";
            vid.frameBorder = "0";
            vid.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
            vid.referrerPolicy = "strict-origin-when-cross-origin";
            vid.setAttribute("allowfullscreen", "");
            imageContainer.appendChild(vid);
          } else {
            let image = document.createElement('img');
            image.classList.add('portfolio-image');
            image.src = project.images[0];
            imageContainer.appendChild(image);
  
            let buttonGroup = null; // Declare outside to ensure scope
  
            // Create slider buttons if multiple images exist
            if (project.images.length > 1) {
              buttonGroup = document.createElement('ol');
              buttonGroup.classList.add('portfolio-buttons');
  
              for (let i = 0; i < project.images.length; i++) {
                const button = document.createElement('li');
                button.style.margin = "5px";
                button.style.scale = "80%";
                button.style.display = "inline-block";
                button.style.boxShadow = "0px 0px 40px black";
                button.classList.add('slider');
                if (i === 0) {
                  button.classList.add('selected');
                }
                buttonGroup.appendChild(button);
              }
  
              createSlider(project, buttonGroup, imageContainer, image); // Attach slider event handlers
              imageContainer.appendChild(buttonGroup); // Append buttons after setting up slider
            }
          }
        } else {
          console.warn(`No images found for project: ${project.title}`);
        }
  
        const title = document.createElement('h1');
        title.classList.add('portfolio-text');
        title.textContent = project.title;
  
        const desc = document.createElement('span');
        desc.classList.add('portfolio-text');
        desc.style.fontSize = "10px";
        desc.textContent = project.description;
  
        entryDiv.appendChild(imageContainer);
        entryDiv.appendChild(title);
        entryDiv.appendChild(desc);
  
        container.appendChild(entryDiv);
      });
    })
    .catch(error => {
      console.error('Error loading portfolio:', error);
    });
  