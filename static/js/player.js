// ------------------------------------
// GLOBAL AUDIO ELEMENT
// ------------------------------------
const audio = document.getElementById("global-audio");

// FOOTER UI ELEMENTS
const playBtn = document.getElementById("btn-play");
const progressBar = document.getElementById("progress-bar");
const currentTimeEl = document.getElementById("current-time");
const totalTimeEl = document.getElementById("total-time");
const volumeSlider = document.getElementById("volume-slider");

// NOW PLAYING UI
const footerTitle = document.getElementById("footer-title");
const footerArtist = document.getElementById("footer-artist");
const footerCover = document.getElementById("footer-cover");


// ------------------------------------
// LOAD A NEW TRACK
// ------------------------------------
window.loadTrack = function(track) {

    audio.src = track.audio_url;
    audio.play();

    footerTitle.textContent = track.title;
    footerArtist.textContent = track.artist;
    footerCover.style.backgroundImage = `url('${track.cover_url}')`;

    // NEW → Notify user
    notify(`Now playing: ${track.title} – ${track.artist}`);

    // --- NEW: Send to playback history ---
    fetch("/api/history", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            title: track.title,
            artist: track.artist,
            cover_url: track.cover_url
        })
    });
};


// ------------------------------------
// PLAY / PAUSE
// ------------------------------------
playBtn.addEventListener("click", () => {
    if (audio.paused) {
        audio.play();
        notify("Playback resumed");
    } else {
        audio.pause();
        notify("Playback paused");
    }
});

audio.addEventListener("play", () => playBtn.textContent = "⏸");
audio.addEventListener("pause", () => playBtn.textContent = "⏯");


// ------------------------------------
// PROGRESS BAR + TIME UI
// ------------------------------------
audio.addEventListener("loadedmetadata", () => {
    progressBar.max = Math.floor(audio.duration);
    totalTimeEl.textContent = formatTime(audio.duration);
});

audio.addEventListener("timeupdate", () => {
    progressBar.value = audio.currentTime;
    currentTimeEl.textContent = formatTime(audio.currentTime);
});

progressBar.addEventListener("input", () => {
    audio.currentTime = progressBar.value;
});


// ------------------------------------
// VOLUME CONTROL  + NOTIFICATION
// ------------------------------------
volumeSlider.addEventListener("input", () => {
    const vol = volumeSlider.value;
    audio.volume = vol / 100;

    notify(`Volume: ${vol}%`);
});


// ------------------------------------
// EXTRA BUTTON NOTIFICATIONS
// ------------------------------------
document.getElementById("btn-next").onclick = () => notify("Next track");
document.getElementById("btn-prev").onclick = () => notify("Previous track");
document.getElementById("btn-shuffle").onclick = () => notify("Shuffle toggled");
document.getElementById("btn-repeat").onclick = () => notify("Repeat toggled");


// ------------------------------------
// FORMAT TIME
// ------------------------------------
function formatTime(sec) {
    sec = Math.floor(sec);
    const m = Math.floor(sec / 60);
    const s = sec % 60;
    return `${m}:${s.toString().padStart(2, '0')}`;
}

// ------------------------------------
// LOG HISTORY TO BACKEND
// ------------------------------------
fetch("/api/history", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
        title: track.title,
        artist: track.artist,
        cover_url: track.cover_url
    })
});
