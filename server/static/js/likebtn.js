const likeButton = document.getElementById("like-button");
const pollId = likeButton.getAttribute("data-poll-id");
let userLikesPoll = likeButton.getAttribute("data-user-likes") === "True";

likeButton.addEventListener("click", () => {
  axios
    .post(
      "/like/",
      { poll_id: pollId },
      {
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
        },
      }
    )
    .then((response) => {
      const message = response.data.message;
      const likeCount = response.data.like_count;

      const heartImage = likeButton.querySelector("img");
      if (message === "좋아요 취소") {
        heartImage.src = "../../static/img/icon/blank_heart.png";
        userLikesPoll = false;
        localStorage.setItem("userLikesPoll", "false");
      } else {
        heartImage.src = "../../static/img/icon/pink_heart.png";
        userLikesPoll = true;
        localStorage.setItem("userLikesPoll", "true");
      }

      document.querySelector("#like-count").textContent = likeCount;
      likeButton.setAttribute("data-user-likes", userLikesPoll);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});

document.addEventListener("DOMContentLoaded", () => {
  const heartImage = likeButton.querySelector("img");
  const userLikesPoll = localStorage.getItem("userLikesPoll");
  if (userLikesPoll === "true") {
    heartImage.src = "../../static/img/icon/pink_heart.png";
  } else {
    heartImage.src = "../../static/img/icon/blank_heart.png";
  }
});
