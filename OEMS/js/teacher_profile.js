$(document).ready(function (){
    modify_profile();
})

function modify_profile(){
    $("#modify_profile").click(function (){
        form = $("form#teacher_profile");
        messenger = Messenger();

        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            success: function (data){
                var response = JSON.parse(data);
                if(response.status == "ok"){
                    messenger.post({
                        message: "修改成功！",
                        type: "success"
                    })
                    $("form#teacher_profile").load("./ #teacher_profile",
                        function(){modify_profile();});
                }
                else if(response.status == "fail")
                    messenger.post({
                        message: "修改失败！",
                        type: "error"
                    })
            },
        });
        return false;
    })
}


