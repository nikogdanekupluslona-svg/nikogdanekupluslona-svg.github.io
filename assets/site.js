(function () {
  var btn = document.getElementById("nav-toggle");
  var nav = document.getElementById("site-nav");
  if (btn && nav) {
    btn.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  var shot = document.getElementById("value-shot");
  var checks = document.getElementById("value-checks");
  if (shot && checks) {
    var items = checks.querySelectorAll("li");
    items.forEach(function (item) {
      item.addEventListener("click", function () {
        items.forEach(function (el) {
          el.classList.remove("is-active");
        });
        item.classList.add("is-active");
        var src = item.getAttribute("data-shot");
        var alt = item.getAttribute("data-alt");
        if (src) shot.src = src;
        if (alt) shot.alt = alt;
      });
      item.setAttribute("role", "button");
      item.setAttribute("tabindex", "0");
      item.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          item.click();
        }
      });
    });
  }

  document.querySelectorAll(".faq-list details").forEach(function (d) {
    d.addEventListener("toggle", function () {
      if (!d.open) return;
      document.querySelectorAll(".faq-list details").forEach(function (other) {
        if (other !== d) other.open = false;
      });
    });
  });
})();
