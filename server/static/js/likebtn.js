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

      showMessage(message);

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

// 메시지 표시 함수
function showMessage(message) {
  const messageContainer = document.getElementById("message-container");
  messageContainer.textContent = message;
  // 메시지를 표시한 후 일정 시간(예: 3000ms) 후에 메시지를 지워줄 수 있습니다.
  setTimeout(() => {
    messageContainer.textContent = "";
  }, 3000);
}