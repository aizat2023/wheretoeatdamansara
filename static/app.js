const spinner = document.getElementById("spinner");
const spinBtn = document.getElementById("spinBtn");
const againBtn = document.getElementById("spinAgainBtn");

async function requestSpin() {
  const r = await fetch("/spin", { method: "POST" });
  if (!r.ok) {
    const j = await r.json().catch(() => ({}));
    spinner.textContent = j.error || "Add some places first.";
    return null;
  }
  const { result } = await r.json();
  return result;
}

function animateSpin(names, finalName) {
  // Fake spin: cycle quickly through provided names, then land on finalName
  const cycle = names.length ? names.slice() : [finalName];
  let i = 0, steps = 25 + Math.floor(Math.random()*10);
  const interval = setInterval(() => {
    spinner.textContent = cycle[i % cycle.length];
    i++;
    if (i > steps) {
      clearInterval(interval);
      spinner.textContent = "🎯 " + finalName;
      spinBtn.style.display = "none";
      againBtn.style.display = "inline-block";
    }
  }, 80);
}

spinBtn?.addEventListener("click", async () => {
  spinBtn.disabled = true;
  spinner.textContent = "Spinning...";
  const finalName = await requestSpin();
  spinBtn.disabled = false;
  if (!finalName) return;
  // Use the pills on the page as the “names” to cycle through visually
  const pillTexts = [...document.querySelectorAll(".pill")].map(el => el.textContent.trim());
  animateSpin(pillTexts, finalName);
});

againBtn?.addEventListener("click", async () => {
  againBtn.style.display = "none";
  spinBtn.style.display = "inline-block";
  spinBtn.click();
});
