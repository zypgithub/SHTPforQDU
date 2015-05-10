$(document).ready(function(){
    create_experiment();
    delete_experiment();
    modify_experiment();
})

function create_experiment(){
    $("button#submit_experiment").click(function(){
        var form = $("form#create_experiment_form");

        $.ajax({
            type: form.attr("method"),
            url: form.attr("action"),
            data: form.serialize(),
            error: function(){
                alert("fail");
            },
            success: function(data){
                var response = JSON.parse(data);
                
                if(response.status_phrase == "ok"){
                    Messenger().post({
                        id: "create_experiment",
                        type: "success",
                        message: "创建成功"
                    })
                    $("form#create_experiment_form").load("./ #create_experiment_form", function(){create_experiment()});
                }
                else if(response.status_phrase == "fail"){
                    Messenger().post({
                        id: "create_experiment",
                        type: "error",
                        message: "创建失败"
                    })
                }
            }
        })
        return false;
    })
}

function delete_experiment(){
    $("button#delete_experiment").click(function(){
        $.ajax({
            type: "get",
            url: $("a#delete_experiment").attr("href"),
            success: function(data){
                var response = JSON.parse(data);
                window.location.href = "/teacher/lesson/" + response.lesson_id;
                if(response.status_phrase == "ok"){
                    Messenger().post({
                        type: "success",
                        message: "删除成功"
                    })
                }
            }
        })
        return false;
    })
}

function modify_experiment(){
    $("button#submit_modified_experiment").click(function(){
        var form = $("form#modify_experiment_form");
        $.ajax({
            type: form.attr("method"),
            url: form.attr("action"),
            data: form.serialize(),
            success: function(data){
                var response = JSON.parse(data);
                if(response.status_phrase == "ok"){
                    Messenger().post({
                        id: "modify_experiment",
                        type: "success",
                        message: "修改成功"
                    })
                    $("form#modify_experiment_form").load("./ #modify_experiment_form", function(){modify_experiment()});
                }
                else if(response.status_phrase == "fail"){
                    Messenger().post({
                        id: "modify_experiment",
                        type: "error",
                        message: "修改失败"
                    })
                }
            }
        })
        return false;
    })
}
