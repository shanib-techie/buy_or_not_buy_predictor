// Same-origin by default (FastAPI serves this page). If the API lives elsewhere,
// set e.g. const API_BASE = "https://your-api.onrender.com";
const API_BASE = "";

const form = document.getElementById("form");
const btn = document.getElementById("btn");
const errorEl = document.getElementById("error");
const emptyEl = document.getElementById("empty");
const outEl = document.getElementById("out");
const tilesEl = document.getElementById("tiles");

for (let i = 0; i < 20; i++) tilesEl.appendChild(document.createElement("i"));

function showError(msg) { errorEl.textContent = msg; errorEl.hidden = !msg; }

function render(p) {
  const buy = Math.round(p * 100);
  document.getElementById("pct").textContent = buy;
  document.getElementById("pBuy").textContent = buy + "%";
  document.getElementById("pNo").textContent = (100 - buy) + "%";

  const v = document.getElementById("verdict");
  const likely = p >= 0.5;
  v.textContent = likely ? "Likely to buy" : "Unlikely to buy";
  v.className = "verdict " + (likely ? "yes" : "no");

  tilesEl.classList.toggle("low", !likely);
  [...tilesEl.children].forEach((t, i) => t.classList.toggle("on", i < Math.round(p * 20)));

  emptyEl.hidden = true;
  outEl.hidden = false;
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  showError("");

  const age = Number(form.age.value);
  const income = Number(form.income.value);
  const score = Number(form.score.value);
  const gender = form.gender.value;

  if (!form.age.value || age < 18 || age > 100) return showError("Enter an age between 18 and 100.");
  if (form.income.value === "" || income < 0) return showError("Enter the annual income in k$ (0 or more).");
  if (!form.score.value || score < 1 || score > 100) return showError("Enter a spending score between 1 and 100.");

  btn.disabled = true;
  btn.textContent = "Predicting…";
  try {
    const res = await fetch(API_BASE + "/prediction", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ age, annual_income: income, spending_score: score, gender })
    });
    if (!res.ok) throw new Error("Server returned " + res.status);
    const data = await res.json();
    const p = data.probability ?? data.probability_buy;
    if (typeof p !== "number") throw new Error("Unexpected response from server.");
    render(p);
  } catch (err) {
    showError("Couldn't get a prediction. Check that the API is running. (" + err.message + ")");
  } finally {
    btn.disabled = false;
    btn.textContent = "Predict purchase";
  }
});
