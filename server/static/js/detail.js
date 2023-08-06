const detailOptions = document.querySelectorAll(".detail-option");

detailOptions.forEach((option, index) => {
  option.addEventListener("click", () => {
    const radioInput = document.getElementById(`choice${index + 1}`);
    radioInput.checked = true;
    detailOptions.forEach((opt) => {
      opt.classList.remove("selected");
    });
    option.classList.add("selected");
  });
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
