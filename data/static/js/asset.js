document.addEventListener("DOMContentLoaded", function () {
    const assetForm = document.getElementById("asset-form");

    if (!assetForm) {
        console.error("Element with ID 'asset-form' not found.");
        return;
    }

    assetForm.addEventListener("submit", async function (event) {
        event.preventDefault(); // Prevent page refresh

        const name = document.getElementById("name").value;
        const value = parseFloat(document.getElementById("value").value);
        const acquisitionDate = document.getElementById("acquisition_date").value;
        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value; // Get CSRF token

        const assetData = {
            name: name,
            value: value,
            acquisition_date: acquisitionDate,
            history: [[acquisitionDate, value]]
        };

        try {
            const response = await fetch("/create-asset/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                },
                body: JSON.stringify(assetData),
            });

            const result = await response.json();
            const successMessage = document.getElementById("success-message");

            if (response.ok) {
                successMessage.innerText = `Asset "${name}" added successfully!`;
                successMessage.classList.remove("hidden"); // Show message
                assetForm.reset(); // Clear the form
            } else {
                alert("Error: " + result.error);
            }
        } catch (error) {
            console.error("Error:", error);
        }
    });
});