/** 비밀번호 표시 여부 **/
$(function(){
    if (document.getElementById('change-eye')) {
        $('#change-eye').click(function(){
            let cls = document.getElementById('change-eye').className
            if (cls == 'fa-solid fa-eye'){
                document.getElementById('change-eye').className = 'fa-solid fa-eye-slash';
                document.getElementById('password').type = 'text';
            }
            else{
                document.getElementById('change-eye').className = 'fa-solid fa-eye';
                document.getElementById('password').type = 'password';
            }
        });
    }
    if (document.getElementById('change-eye1')) {
        $('#change-eye1').click(function(){
            let cls = document.getElementById('change-eye1').className
            if (cls == 'fa-solid fa-eye'){
                document.getElementById('change-eye1').className = 'fa-solid fa-eye-slash';
                document.getElementById('check_password').type = 'text';
            }
            else{
                document.getElementById('change-eye1').className = 'fa-solid fa-eye';
                document.getElementById('check_password').type = 'password';
            }
        });
    } 
});

/** Cookie에서 토큰 가져오기 **/
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}