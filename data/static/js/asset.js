document.addEventListener("DOMContentLoaded", function () {
    const assetForm = document.getElementById("asset-form");
    const notification = document.getElementById("notification");
    const notificationMessage = document.getElementById("notification-message");

    if (!assetForm) {
        console.error("Element with ID 'asset-form' not found.");
        return;
    }

    assetForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const name = document.getElementById("name").value;
        const value = parseFloat(document.getElementById("value").value);
        const acquisitionDate = document.getElementById("acquisition_date").value;
        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

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
            if (response.ok) {
                assetForm.reset(); // Clear the form

                // ✅ Show notification
                notificationMessage.innerText = `Asset "${name}" added successfully!`;
                notification.classList.remove("opacity-0", "translate-x-full"); 
                notification.classList.add("translate-x-0");

                // ⏳ Hide after 3 seconds
                setTimeout(() => {
                    notification.classList.add("opacity-0", "translate-x-full");
                }, 3000);
            } else {
                alert("Error: " + result.error);
            }
        } catch (error) {
            console.error("Error:", error);
        }
    });
});