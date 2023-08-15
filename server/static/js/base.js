document.addEventListener("DOMContentLoaded", function () {
  const hamburger = document.querySelector("#hamburger-icon");
  const sidebar = document.querySelector("#sidebar");
  const hideSidebar = document.querySelector("#hide-sidebar-icon");

  hamburger.addEventListener("click", function () {
    console.log("사이드바 등장!");
    sidebar.classList.add("show");
  });

  hideSidebar.addEventListener("click", function () {
    console.log("사이드바 사라짐!");
    sidebar.classList.remove("show");

    // Wait for the transition to end before removing the animation class
    sidebar.addEventListener("transitionend", function () {
      sidebar.classList.remove("show");
      sidebar.removeEventListener("transitionend", arguments.callee);
    });
  });
});