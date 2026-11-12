
async function loadInsights() {

    const container = document.getElementById("ai-insights");

    container.textContent = "Generating your AI spending insights...";

    try {

        const response = await fetch("/api/insights");

        const data = await response.json();

        if (!response.ok || data.status !== "success") {
            throw new Error(data.message || "Could not generate insights.");
        }

        container.textContent = data.insights;

    } catch (error) {

        console.error("AI Insights Error:", error);

        container.textContent = "Unable to load AI insights. Please try again.";

    }
}

document.addEventListener("DOMContentLoaded", loadInsights);
