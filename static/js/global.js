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

// ===============================
// NFC SHARING
// ===============================

window.shareViaNFC = async function(songId) {
    const url = `${window.location.origin}/musicplayer/${songId}`;

    // Check NFC support
    if (!("NDEFWriter" in window)) {
        notify("NFC not supported on this device");
        return;
    }

    try {
        const writer = new NDEFWriter();

        await writer.write({
            records: [
                { recordType: "url", data: url }
            ]
        });

        notify("NFC tag written! Tap another device.");
    } 
    catch (err) {
        notify("NFC write failed");
        console.error(err);
    }
};
