$(document).ready(function (){
    create_lesson_category();
})

function create_lesson_category(){
    $("#create_button").click(function (){
        var input_name = $('#lesson_category_name').val();
        form = $("form#create_lesson_category");
        if(input_name.length <= 60 && input_name.length > 0){
            $.ajax({
                type: form.attr("method"),
                url: form.attr("action"),
                data: form.serialize(),
                success:function (data){
                    var response = JSON.parse(data);
                    if (response.status == "OK"){
                        Messenger().post("创建成功！")
                        $("#category_list").load("./ #category_list")
                        $('#lesson_category_name').val("");
                    }
                    else if(response.content == "existed"){
                        Messenger().post({
                            message: "科目已经存在,请重新输入",
                            type: "error"
                        })
                    }
                }
            })
        }
        else if(input_name.length > 60)
            alert("科目名长度超过60个字符！请重新输入！");       
        else 
            alert("请输入科目名称！");
        return false;
    })
}
