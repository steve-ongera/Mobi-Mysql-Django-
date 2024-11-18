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


 // Function to show the message and slide it in from the right
 window.addEventListener('DOMContentLoaded', (event) => {
    const messagePopup = document.querySelector('.message-popup');

    if (messagePopup) {
        // Add 'show' class to slide in the message box from the right
        messagePopup.classList.add('show');

        // After 3 seconds, start the fade-out and slide-out animation
        setTimeout(() => {
            messagePopup.classList.add('fade-out');
        }, 3000); // Wait for 3 seconds before sliding out and fading
    }
});