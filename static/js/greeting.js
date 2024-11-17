// greeting.js
window.addEventListener('DOMContentLoaded', (event) => {
    // Get the current time
    const currentTime = new Date();
    const hours = currentTime.getHours();
    const minutes = currentTime.getMinutes();

    // Get the greeting element
    const greetingElement = document.getElementById("greeting");

    // Determine the appropriate greeting based on the time
    let greetingMessage = "";

    if (hours >= 0 && hours < 12) {
        greetingMessage = "Good morning,";
    } else if (hours === 12 && minutes <= 45) {
        greetingMessage = "Good afternoon,";
    } else if (hours > 12 && hours < 16) {
        greetingMessage = "Good afternoon,";
    } else {
        greetingMessage = "Good evening,";
    }

    // Set the greeting text
    greetingElement.textContent = greetingMessage;
});
