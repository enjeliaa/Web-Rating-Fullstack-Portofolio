// Interaktivitas bintang & deskripsi untuk user
document.addEventListener("DOMContentLoaded", () => {
  // ⭐ Update rating dengan klik bintang
  document.querySelectorAll(".stars").forEach(container => {
    const id = container.dataset.id;
    if (!id) return;
    container.querySelectorAll(".star").forEach(star => {
      star.addEventListener("click", () => {
        const value = parseInt(star.dataset.value);
        container.querySelectorAll(".star").forEach(s => s.classList.remove("filled"));
        for (let i = 0; i < value; i++) container.querySelectorAll(".star")[i].classList.add("filled");

        // animasi bergetar lucu ✨
        container.style.transform = "scale(1.15)";
        setTimeout(() => container.style.transform = "scale(1)", 150);

        fetch(`/api/update/${id}`, {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({rating: value})
        }).then(() => {
          showToast("⭐ Rating tersimpan!");
        });
      });
    });
  });

  // 📝 Update deskripsi otomatis
  document.querySelectorAll(".desc-input").forEach(input => {
    const id = input.dataset.id;
    if (!id) return;
    let timer;
    input.addEventListener("input", () => {
      clearTimeout(timer);
      timer = setTimeout(() => {
        fetch(`/api/update/${id}`, {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({desc: input.value})
        }).then(() => {
          showToast("💬 Deskripsi diperbarui!");
        });
      }, 600);
    });
  });
});

// 🍩 Toast popup lucu
function showToast(msg) {
  let toast = document.createElement("div");
  toast.textContent = msg;
  toast.style.position = "fixed";
  toast.style.bottom = "24px";
  toast.style.left = "50%";
  toast.style.transform = "translateX(-50%)";
  toast.style.background = "#f8e4cc";
  toast.style.color = "white";
  toast.style.padding = "10px 18px";
  toast.style.borderRadius = "12px";
  toast.style.fontWeight = "500";
  toast.style.boxShadow = "0 3px 8px rgba(0,0,0,0.2)";
  toast.style.zIndex = "9999";
  toast.style.opacity = "0";
  toast.style.transition = "opacity 0.4s ease";
  document.body.appendChild(toast);
  setTimeout(() => toast.style.opacity = "1", 100);
  setTimeout(() => {
    toast.style.opacity = "0";
    setTimeout(() => toast.remove(), 400);
  }, 1800);
}

