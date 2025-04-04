

const loginForm = document.getElementById("loginForm");
const loadingSpinner = document.getElementById("loadingSpinner").querySelector(".spinner-border");
const loginMessage = document.getElementById("loginMessage");

// Clear and hide elements upon re-opening page or re-submitting
const resetUI = () => {
    loginMessage.textContent = "";
    loadingSpinner.style.display = "none";
};

// Listen for form submission
loginForm.addEventListener("submit", async (event) => {
    // Prevent the default form behavior
    event.preventDefault();

    resetUI(); // Clear previous messages/spinners

    // Extract username/email and password values
    const username = document.getElementById("floatingEmail").value;
    const password = document.getElementById("floatingPassword").value;
    const payload = {
        username,
        password
    };

    // Show the spinner
    loadingSpinner.style.display = "block";
    try {
        // Send POST request to /api/v1/auth
        const response = await fetch("/api/v1/auth", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        // Hide the spinner once a response is received
        loadingSpinner.style.display = "none";

        // Attempt to parse JSON (the server should ideally return JSON)
        const data = await response.json();

        if (!response.ok) {
            // If there's an error, display the server's message (if any)
            loginMessage.style.color = "red";
            loginMessage.textContent = data.message || "Login failed. Check your credentials.";
            return;
        }

        window.location.href = "/index"
    } catch (error) {
        loadingSpinner.style.display = "none";
        loginMessage.style.color = "red";
        loginMessage.textContent =
            "An unexpected error occurred. Please try again later.\n\n" + error;
    }
});
