/**
 * inquiry.js
 * Zagadnienie #8 — JavaScript: interaktywność formularza zapytania.
 *
 * Funkcje:
 *  1. Licznik znaków dla pola "wiadomość"
 *  2. Walidacja dat po stronie klienta (check_in < check_out, check_in >= dziś)
 *  3. Ustawienie minimalnej daty check_in na dziś
 */

document.addEventListener("DOMContentLoaded", () => {

  // ── 1. Licznik znaków ──────────────────────────────────────────────────────
  const messageField = document.getElementById("id_message");
  const charCounter  = document.getElementById("char-counter");
  const MAX_CHARS    = 1000;

  if (messageField && charCounter) {
    const updateCounter = () => {
      const len = messageField.value.length;
      charCounter.textContent = `${len} / ${MAX_CHARS}`;
      charCounter.classList.toggle("text-danger", len >= MAX_CHARS);
    };
    messageField.addEventListener("input", updateCounter);
    updateCounter(); // inicjalny stan przy powrocie przeglądarki (back button)
  }


  // ── 2. Walidacja dat po stronie klienta ───────────────────────────────────
  const checkInField  = document.getElementById("id_check_in");
  const checkOutField = document.getElementById("id_check_out");

  if (!checkInField || !checkOutField) return;

  // Dzisiejsza data w formacie YYYY-MM-DD
  const today = new Date().toISOString().split("T")[0];

  // Zagadnienie #8: dynamiczne ustawienie atrybutu min
  checkInField.setAttribute("min", today);

  const validateDates = () => {
    const checkIn  = checkInField.value;
    const checkOut = checkOutField.value;

    // Ustaw minimalny check_out na dzień po check_in
    if (checkIn) {
      const minCheckOut = new Date(checkIn);
      minCheckOut.setDate(minCheckOut.getDate() + 1);
      checkOutField.setAttribute("min", minCheckOut.toISOString().split("T")[0]);
    }

    // Wizualna walidacja Bootstrap
    if (checkIn && checkOut) {
      const valid = checkOut > checkIn;
      checkOutField.classList.toggle("is-invalid", !valid);
      checkOutField.classList.toggle("is-valid",   valid);

      // Komunikat błędu inline
      let feedback = checkOutField.nextElementSibling;
      if (!feedback || !feedback.classList.contains("invalid-feedback")) {
        feedback = document.createElement("div");
        feedback.className = "invalid-feedback";
        checkOutField.after(feedback);
      }
      feedback.textContent = valid
        ? ""
        : "Data wyjazdu musi być późniejsza niż data przyjazdu.";
    }
  };

  checkInField.addEventListener("change", validateDates);
  checkOutField.addEventListener("change", validateDates);


  // ── 3. Reset klas is-valid/is-invalid po zamianie przez HTMX ─────────────
  //  HTMX podmienia innerHTML kontenera — nasłuchujemy htmx:afterSwap,
  //  żeby ponownie podpiąć event listenery po każdym swapie.
  document.body.addEventListener("htmx:afterSwap", (evt) => {
    if (evt.detail.target && evt.detail.target.id === "inquiry-container") {
      // Skrypt się sam wywoła przez DOMContentLoaded już nie zadziała;
      // HTMX nie odpala DOMContentLoaded, więc wywołujemy init ręcznie.
      initInquiryForm();
    }
  });

});


/**
 * Inicjalizacja formularza — wywoływana zarówno przy ładowaniu strony
 * jak i po podmiance przez HTMX.
 */
function initInquiryForm() {
  const messageField = document.getElementById("id_message");
  const charCounter  = document.getElementById("char-counter");
  if (messageField && charCounter) {
    messageField.addEventListener("input", () => {
      const len = messageField.value.length;
      charCounter.textContent = `${len} / 1000`;
      charCounter.classList.toggle("text-danger", len >= 1000);
    });
  }

  const checkInField  = document.getElementById("id_check_in");
  const checkOutField = document.getElementById("id_check_out");
  if (checkInField && checkOutField) {
    const today = new Date().toISOString().split("T")[0];
    checkInField.setAttribute("min", today);
    checkInField.addEventListener("change", () => {
      if (checkInField.value) {
        const min = new Date(checkInField.value);
        min.setDate(min.getDate() + 1);
        checkOutField.setAttribute("min", min.toISOString().split("T")[0]);
      }
    });
  }
}
