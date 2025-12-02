// ------------------------------
// GLOBAL NOTIFICATION SYSTEM
// ------------------------------

window.notify = function (text) {

    const container = document.getElementById("notification-container");

    const note = document.createElement("div");
    note.className = "notification";
    note.textContent = text;

    container.appendChild(note);

    // Fade + remove
    setTimeout(() => {
        note.classList.add("fade-out");
        setTimeout(() => note.remove(), 400);
    }, 2000);
};
