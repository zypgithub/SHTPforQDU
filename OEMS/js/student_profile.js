$(document).ready(function(){
    update_student_profile();
})
function update_student_profile(){
    $("button#update_student_profile").click(function(){
        var school_id = $("input#school_id").val();
        var grade = $("input#grade").val();
        var major = $("input#major").val();
        var class_num = $("input#class_num").val();
        var phone_num = $("input#phone_num").val();

        form = $("form#student_profile");
        messenger = Messenger();

        $.ajax({
            type: form.attr("method"),
            url: form.attr("action"),
            data: form.serialize(),
            success:function(data){
                var response = JSON.parse(data);
                if(response.status_phrase == "ok"){
                    messenger.post({
                        id: "update_status",
                        type: "success",
                        message: "更新成功"
                    })
                    $("form#student_profile").load("./ #student_profile", function(){update_student_profile();});
                }
                else if(response.status_phrase == "fail"){
                    messenger.post({
                        id: "update_status",
                        type: "error",
                        message: "更新失败"
                    })
                }
            }
        })
    return false;
    })
}
