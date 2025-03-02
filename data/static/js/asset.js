document.addEventListener("DOMContentLoaded", function () {
    const assetForm = document.getElementById("asset-form");
    const notification = document.getElementById("notification");
    const notificationMessage = document.getElementById("notification-message");
    const assetContainer = document.getElementById("containing-personal-assets");

    async function fetchAssets() {
        try {
            console.log("Fetching assets...");
            const response = await fetch("/get-assets/");
            console.log("Response status:", response.status);
    
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
    
            const data = await response.json();
            console.log("Fetched assets:", data);
            renderAssets(data.assets);
        } catch (error) {
            console.error("Error fetching assets:", error);
        }
    }

    function renderAssets(assets) {
        assetContainer.innerHTML = ""; // Clear previous content
        assets.forEach(asset => addAssetToUI(asset)); // Render all assets
    }

    function addAssetToUI(asset) {
        const assetElement = document.createElement("div");
        assetElement.className = "bg-black shadow-md p-4 rounded-lg my-2";
        assetElement.innerHTML = `
            <h3 class="text-xl font-bold text-blue-700">${asset.name}</h3>
            <p class="text-blue-200">💰 Value: <strong>${asset.value} €</strong></p>
            <p class="text-blue-200">📅 Acquired on: ${asset.acquisition_date}</p>
            <button class="delete-asset text-red-500 hover:text-red-700 p-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
            </button>
        `;
        assetElement.querySelector(".delete-asset").addEventListener("click", () => deleteAsset(asset.id, assetElement));
        assetContainer.prepend(assetElement); // Add new asset at the top
    }


    async function deleteAsset(assetId, assetElement) {
        try {
            const response = await fetch(`/delete-asset/${assetId}/`, {
                method: "DELETE",
                headers: {
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                }
            });

            if (response.ok) {
                assetElement.remove(); // Remove from UI
                console.log(`Asset ID ${assetId} deleted successfully.`);
            } else {
                alert("Error deleting asset.");
            }
        } catch (error) {
            console.error("Error:", error);
        }
    }

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

                // ✅ Append the new asset **without reloading**
                addAssetToUI(assetData);
            } else {
                alert("Error: " + result.error);
            }
        } catch (error) {
            console.error("Error:", error);
        }
    });

    // ✅ Call `fetchAssets()` on page load
    fetchAssets();
});