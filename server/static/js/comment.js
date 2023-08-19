
// const openReply1 = (commentId) => {
//   console.log('here!!!!!!!!!!');
//   //var commentId = btn.getAttribute("data-comment-id");
//   var parentContainer = document.querySelector(`#reply-${commentId}`);
//   var nestedInputContainer = document.querySelector(`.nested-reply-input-container`);

//   if (parentContainer) {
//     if (
//       parentContainer.style.display === "none" ||
//       parentContainer.style.display === ""
//     ) {
//       parentContainer.style.display = "block";
//       if (nestedInputContainer) {
//         nestedInputContainer.style.display = "block";
//       }
//     } else {
//       parentContainer.style.display = "none";
//       if (nestedInputContainer) {
//         nestedInputContainer.style.display = "none";
//       }
//     }
//   }
// }

const openReply = (commentId) => {
  console.log('here!!!!!!!!!!');
  //var commentId = btn.getAttribute("data-comment-id");
  var parentContainer = document.querySelector(
    ".nested-reply-container[data-parent-id='" + commentId + "']"
  );
  var nestedInputContainer = document.querySelector(
    ".nested-reply-input-container[data-parent-id='" + commentId + "']"
  );

  if (parentContainer) {
    if (
      parentContainer.style.display === "none" ||
      parentContainer.style.display === ""
    ) {
      parentContainer.style.display = "block";
      if (nestedInputContainer) {
        nestedInputContainer.style.display = "block";
      }
    } else {
      parentContainer.style.display = "none";
      if (nestedInputContainer) {
        nestedInputContainer.style.display = "none";
      }
    }
  }
}

//대댓글 토글
document.addEventListener("DOMContentLoaded", function () {
  var toggleButtons = document.querySelectorAll(".reply-toggle-btn");

  toggleButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      console.log('jewkfjweklfjwke')
      var commentId = this.getAttribute("data-comment-id");
      var parentContainer = document.querySelector(
        ".nested-reply-container[data-parent-id='" + commentId + "']"
      );
      var nestedInputContainer = document.querySelector(
        ".nested-reply-input-container[data-parent-id='" + commentId + "']"
      );

      if (parentContainer) {
        if (
          parentContainer.style.display === "none" ||
          parentContainer.style.display === ""
        ) {
          parentContainer.style.display = "block";
          if (nestedInputContainer) {
            nestedInputContainer.style.display = "block";
          }
        } else {
          parentContainer.style.display = "none";
          if (nestedInputContainer) {
            nestedInputContainer.style.display = "none";
          }
        }
      }
    });
    
    // 대댓글 수 초기화
    var commentId = button.getAttribute("data-comment-id");
    updateNestedCount(commentId);
  });

  // 페이지 로드 시 모든 댓글의 대댓글 수 초기화
  var allCommentButtons = document.querySelectorAll(".reply-toggle-btn");
  allCommentButtons.forEach(function (button) {
    var commentId = button.getAttribute("data-comment-id");
    updateNestedCount(commentId);
  });
});



//대댓글 수 카운트
function updateNestedCount(comment_id) {
  var url = "/calculate-nested-count/" + comment_id + "/";
  $.ajax({
    type: "GET",
    url: url, // 서버에서 대댓글 수를 계산하는 뷰의 URL
    dataType: "json",
    success: function (response) {
      var nestedCountSpan = $("#nestedCount" + comment_id);
      nestedCountSpan.text(response.nested_count);
    },
    error: function () {
      // 에러 처리
    },
  });
}

// 현재 시간과 댓글 작성 시간의 차이 계산
function calculateRelativeTime(createdAt) {
  const now = new Date();
  const created = new Date(createdAt);
  const diff = now - created;

  if (diff < 1000) {
    return "방금 전";
  } else if (diff < 60000) {
    return Math.floor(diff / 1000) + "초 전";
  } else if (diff < 3600000) {
    return Math.floor(diff / 60000) + "분 전";
  } else if (diff < 86400000) {
    return Math.floor(diff / 3600000) + "시간 전";
  } else {
    return Math.floor(diff / 86400000) + "일 전";
  }
}

var createdTime = new Date(response.created_at); // 서버로부터 전달받은 시간을 JavaScript Date 객체로 변환

// 현재 시간과의 시간 간격 계산
var timeDifference = Date.now() - createdTime;
var seconds = Math.floor(timeDifference / 1000);
var minutes = Math.floor(seconds / 60);
var hours = Math.floor(minutes / 60);
var days = Math.floor(hours / 24);

var timeAgo = "";

if (days > 0) {
  timeAgo = days + "일 전";
} else if (hours > 0) {
  timeAgo = hours + "시간 전";
} else if (minutes > 0) {
  timeAgo = minutes + "분 전";
} else {
  timeAgo = "방금 전";
}

