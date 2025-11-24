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
// Called by backend when user clicks a track
// ------------------------------------
window.loadTrack = function(track) {
    audio.src = track.audio_url;
    audio.play();

    // Update footer
    footerTitle.textContent = track.title;
    footerArtist.textContent = track.artist;
    footerCover.style.backgroundImage = `url('${track.cover_url}')`;
};

// ------------------------------------
// PLAY / PAUSE
// ------------------------------------
playBtn.addEventListener("click", () => {
    if (audio.paused) audio.play();
    else audio.pause();
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
// VOLUME CONTROL
// ------------------------------------
volumeSlider.addEventListener("input", () => {
    audio.volume = volumeSlider.value / 100;
});

// Format seconds into M:SS
function formatTime(sec) {
    sec = Math.floor(sec);
    const m = Math.floor(sec / 60);
    const s = sec % 60;
    return `${m}:${s.toString().padStart(2, '0')}`;
}