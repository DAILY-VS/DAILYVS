document.addEventListener("DOMContentLoaded", function () {
  const genderToggle = document.getElementById("genderToggle");
  const genderChart = document.getElementById("genderChart");

  genderToggle.addEventListener("click", function () {
    genderChart.classList.toggle("show");
    const chevron = genderToggle.querySelector("img");
    chevron.classList.toggle("rotate");
  });
});
