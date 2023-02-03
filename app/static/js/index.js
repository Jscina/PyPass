// Contains the listeners for the index.html page
const button = document.getElementById("myButton");

button.addEventListener("click", () => {
    const greeting = document.getElementById("name");
    greeting.innerHTML = "Good job logging in!";
});
