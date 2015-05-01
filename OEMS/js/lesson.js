$(document).ready(function(){
    create_lesson();
    delete_lesson();
    update_lesson();
})

function create_lesson(){
    $("button#submit_lesson_info").click(function(){
        var category = $("select#category").val();
        var name = $("input#lesson_name").val();
        var info = $("textarea#lesson_info").val();

        form = $("form#create_lesson_form");

        $.ajax({
            type: form.attr("method"),
            url: form.attr("action"),
            data: form.serialize(),
            success: function(data){
                var response = JSON.parse(data);
                if(response.status_phrase == "ok"){
                    Messenger().post({
                        id: "create_lesson",
                        type: "success",
                        message: "创建成功"
                    })
                    $("form#create_lesson_form").load("./ #create_lesson_form", function(){create_lesson();});
                }
                else if(response.status_phrase == "fail"){
                    Messenger().post({
                        id: "create_lesson",
                        type: "error",
                        message: "创建失败"
                    })
                }
            }
        })
    return false;
    })
}

function delete_lesson(){
    $("button#delete_lesson").click(function(){
        var url = $("a#delete_lesson");
        $.ajax({
            type: "get",
            url: url.attr("href"),
            success: function(data){
                var response = JSON.parse(data);
                window.location.href = document.referrer;
            }
        })
        return false;
    })
}

function update_lesson(){
    $("button#submit_updated_lesson").click(function(){
        var form = $("form#update_lesson");
        $.ajax({
            type: form.attr("method"),
            url: form.attr("action"),
            data: form.serialize(),
            success: function(data){
                var response = JSON.parse(data);
                if(response.status_phrase == "ok"){
                    Messenger().post({
                        id: "update_lesson",
                        type: "success",
                        message: "更新成功"
                    })
                    $("form#update_lesson").load("./ #update_lesson", function(){update_lesson();});
                }
                else if(response.status_phrase == "fail"){
                    Messenger().post({
                        id: "update_lesson",
                        type: "error",
                        message: "更新失败"
                    })
                }
            }
        })
        return false;
    })
}
