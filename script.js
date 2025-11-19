const panels = document.querySelectorAll(".panel-img");

window.addEventListener("scroll", () => {
  const windowH = window.innerHeight;

  panels.forEach(panel => {
    const rect = panel.getBoundingClientRect();
    const panelCenter = rect.top + rect.height / 2;
    const screenCenter = windowH / 2;

    const dist = Math.abs(panelCenter - screenCenter);

    let vis = 1 - dist / (windowH * 0.5);
    vis = Math.max(0, Math.min(1, vis));

    panel.style.opacity = vis;
    panel.style.transform = `
      translateY(${40 - vis * 40}px)
      scale(${1.85 - vis * 0.85})
    `;

    const text = panel.querySelector(".txt");
    if (text) {
      text.style.opacity = vis;
    }
  });
});
