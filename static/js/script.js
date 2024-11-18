// Select the carousel container
const carousel = document.querySelector('.carousel');
let currentIndex = 0;
const totalItems = document.querySelectorAll('.carousel-item').length;

// Function to move to the next image
function moveToNextImage() {
    currentIndex = (currentIndex + 1) % totalItems; // Loop back to the first item
    carousel.style.transform = `translateX(-${currentIndex * 100}%)`;
}

// Set interval to change the image every 3 seconds
setInterval(moveToNextImage, 3000); // Change image every 3 seconds
