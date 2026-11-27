// Native playback works without JavaScript; this adds a remembered speed control.
document.querySelectorAll('.audio-player').forEach((player) => {
  const audio = player.querySelector('audio');
  const label = player.querySelector('.speed-control');
  const select = label?.querySelector('select');
  if (!audio || !select) return;

  const allowed = ['0.75', '1', '1.25', '1.5', '2'];
  let rate = '1';
  try {
    const saved = localStorage.getItem('engineering-audio-speed');
    if (allowed.includes(saved)) rate = saved;
  } catch (_) { /* Storage may be unavailable; playback still works. */ }
  select.value = rate;
  audio.defaultPlaybackRate = Number(rate);
  audio.playbackRate = Number(rate);
  label.hidden = false;

  select.addEventListener('change', () => {
    audio.defaultPlaybackRate = Number(select.value);
    audio.playbackRate = Number(select.value);
    try { localStorage.setItem('engineering-audio-speed', select.value); }
    catch (_) { /* A preference should never block playback. */ }
  });
});
