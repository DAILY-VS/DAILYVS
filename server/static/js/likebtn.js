const likeButton = document.getElementById("like-button");
const pollId = likeButton.getAttribute("data-poll-id");
const heartImage = likeButton.querySelector("img");

likeButton.addEventListener("click", () => {
  // 초기 좋아요 상태 설정
  document.addEventListener("DOMContentLoaded", () => {
    console.log(heartImage);
    const userLikesPoll = localStorage.getItem("userLikesPoll");
    if (userLikesPoll === "true") {
      heartImage.src = "../../static/img/icon/pink_heart.png";
    } else {
      heartImage.src = "../../static/img/icon/blank_heart.png";
    }
  });

  document.addEventListener("DOMContentLoaded", () => {
    const isAuthenticated = "{{ request.user.is_authenticated }}";
    const initialLikes = "{{ user_likes_poll }}";

    if (isAuthenticated === "True") {
      if (initialLikes === "true") {
        heartImage.src = "../../static/img/icon/pink_heart.png";
      } else {
        heartImage.src = "../../static/img/icon/blank_heart.png";
      }
    } else {
      heartImage.src = "../../static/img/icon/blank_heart.png";
    }
  });

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
      if (confirm("로그인이 필요합니다. 로그인 페이지로 이동하시겠습니까?")) {
        var loginUrl = "/account/login/";
        window.location.href = loginUrl; // 로그인 페이지 URL로 이동
      }
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

function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length === 2) return parts.pop().split(";").shift();
}
