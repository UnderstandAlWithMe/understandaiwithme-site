// Admin time calculator + AI readiness quiz. No tracking, nothing leaves the browser.
(function () {
  var money = function (n) {
    var c = (document.getElementById("currency") || {}).value || "USD";
    try { return new Intl.NumberFormat(undefined, { style: "currency", currency: c, maximumFractionDigits: 0 }).format(n); }
    catch (e) { return Math.round(n).toLocaleString(); }
  };
  var num = function (el) { var v = parseFloat(el.value); return isFinite(v) && v > 0 ? v : 0; };

  // ---------- Calculator ----------
  var calc = document.getElementById("calc");
  if (calc) {
    var out = document.getElementById("calc-out");
    var run = function () {
      var people = num(calc.people) || 1;
      var rate = num(calc.rate);
      var rows = Array.prototype.slice.call(calc.querySelectorAll("[data-task]"));
      var weekly = 0, top = null, topH = 0;
      rows.forEach(function (r) {
        var h = num(r) * people;
        weekly += h;
        if (h > topH) { topH = h; top = r; }
      });
      if (!weekly) { out.classList.add("hidden"); return; }
      var yearly = weekly * 46; // working weeks after holidays
      var cost = yearly * rate;
      var saved = yearly * 0.4;
      out.classList.remove("hidden");
      out.querySelector("[data-o=hours]").textContent = Math.round(yearly).toLocaleString() + " hours";
      out.querySelector("[data-o=cost]").textContent = rate ? money(cost) : "add an hourly cost";
      out.querySelector("[data-o=weekly]").textContent = (Math.round(weekly * 10) / 10) + " h";
      out.querySelector("[data-o=days]").textContent = Math.round(yearly / 7.5) + " days";
      out.querySelector("[data-o=saved]").textContent = Math.round(saved).toLocaleString() + " h" + (rate ? " (" + money(saved * rate) + ")" : "");
      out.querySelector("[data-o=top]").textContent = top.getAttribute("data-label");
      out.querySelector("[data-o=topshare]").style.width = Math.round((topH / weekly) * 100) + "%";
      out.querySelector("[data-o=toppct]").textContent = Math.round((topH / weekly) * 100) + "% of your admin time";
      var link = out.querySelector("[data-o=fix]");
      link.href = "/fix/" + top.getAttribute("data-task") + "/";
      link.textContent = "See the fastest fix for " + top.getAttribute("data-short").toLowerCase() + " →";
    };
    calc.addEventListener("input", run);
    calc.addEventListener("change", run);
    calc.addEventListener("submit", function (ev) { ev.preventDefault(); run(); out.scrollIntoView({ behavior: "smooth", block: "start" }); });
    run();
  }

  // ---------- Quiz ----------
  var quiz = document.getElementById("quiz");
  if (quiz) {
    var qs = quiz.querySelectorAll(".q");
    var bar = document.getElementById("quiz-bar");
    var label = document.getElementById("quiz-count");
    var res = document.getElementById("quiz-out");
    var answered = function () { return quiz.querySelectorAll("input:checked").length; };
    quiz.addEventListener("change", function () {
      var n = answered();
      bar.style.width = Math.round((n / qs.length) * 100) + "%";
      label.textContent = n + " of " + qs.length + " answered";
    });
    quiz.addEventListener("submit", function (ev) {
      ev.preventDefault();
      if (answered() < qs.length) {
        var first = Array.prototype.find.call(qs, function (q) { return !q.querySelector("input:checked"); });
        first.scrollIntoView({ behavior: "smooth", block: "center" });
        label.textContent = "Please answer every question (" + answered() + " of " + qs.length + ")";
        return;
      }
      var score = 0, max = 0, pain = "not-sure";
      quiz.querySelectorAll("input:checked").forEach(function (i) {
        if (i.name === "pain") { pain = i.value; return; }
        score += parseInt(i.value, 10);
      });
      qs.forEach(function (q) { if (!q.querySelector("[name=pain]")) max += 3; });
      var pct = Math.round((score / max) * 100);
      var band = pct >= 67 ? "ready" : pct >= 34 ? "quick" : "basics";
      res.classList.remove("hidden");
      res.querySelector("[data-o=score]").textContent = pct + "/100";
      res.querySelector("[data-o=bar]").style.width = pct + "%";
      res.querySelectorAll("[data-band]").forEach(function (el) { el.classList.toggle("hidden", el.getAttribute("data-band") !== band); });
      var picked = quiz.querySelector("[name=pain]:checked");
      var fix = res.querySelector("[data-o=fix]");
      fix.href = "/fix/" + pain + "/";
      fix.textContent = "Your next step: " + picked.getAttribute("data-short") + " →";
      res.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  }
})();
