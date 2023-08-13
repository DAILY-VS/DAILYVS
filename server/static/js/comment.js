// comment.js

$(document).ready(function () {
  var page = 1; // 초기 페이지 번호

  // 스크롤 이벤트 리스너 등록
  $(window).scroll(function () {
    if ($(window).scrollTop() + $(window).height() >= $(document).height()) {
      loadMoreData(page);
      page++;
    }
  });

  // 새로운 데이터를 불러오는 함수
  function loadMoreData(page) {
    $.ajax({
      url: "/get_comments/?page=" + page, // Django API 뷰 URL
      type: "GET",
      beforeSend: function () {
        $(".loader").show(); // 로딩 스피너 표시
      },
      success: function (data) {
        if (data.comments.length > 0) {
          var comments = data.comments;
          var html = "";

          for (var i = 0; i < comments.length; i++) {
            html +=
              '<div class="comment">' +
              "<p>" +
              comments[i].content +
              "</p>" +
              "<p>" +
              comments[i].created_at +
              "</p>" +
              "</div>";
          }

          $(".replyTody").append(html); // 새로운 댓글을 추가합니다.
        }
        $(".loader").hide(); // 로딩 스피너 숨김
      },
      error: function () {
        // 오류 처리
      },
    });
  }
});

//대댓글 토글
document.addEventListener("DOMContentLoaded", function () {
  var toggleButtons = document.querySelectorAll(".reply-toggle-btn");

  toggleButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      var commentId = this.getAttribute("data-comment-id");
      var parentContainer = document.querySelector(
        ".nested-reply-container[data-parent-id='" + commentId + "']"
      );
      var nestedInputContainer = document.querySelector(
        " .nested-reply-input-container" + commentId
      );
      console.log(nestedInputContainer);

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
