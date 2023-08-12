function replyDelete(value) {
  var comment_id = value;
  var delete_warning = confirm("댓글을 삭제하시겠습니까?");

  if (delete_warning == true) {
    // 로그인 여부 확인
    if (isAuthenticated === "True") {
      $.ajax({
        type: "POST",
        url: "{% url 'vote:comment_delete' comment_id %}",
        dataType: "json",
        data: {
          comment_id: comment_id,
          csrfmiddlewaretoken: "{{csrf_token}}",
        },
        success: function (response) {
          if (response.success) {
            $("#" + response.comment_id).remove();
            var replyTr = document.querySelector(
              `.replyTr${response.comment_id}`
            );
            if (replyTr) {
              console.log(replyTr);
              replyTr.remove();
            }
          } else {
            alert(response.error);
          }
        },
        error: function () {
          alert("오류가 발생했습니다.");
        },
      });
    } else {
      alert("로그인을 해주세요");
    }
  }
}
