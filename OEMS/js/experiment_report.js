$(document).ready(function(){
    evalute_experiment_report();
})

function evalute_experiment_report(){
    $("button#submit_evaluation").click(function(){
        var form = $("form#evaluate_experiment_report");
        $.ajax({
            type: form.attr("method"),
            url: form.attr("action"),
            data: form.serialize(),
            success: function(data){
                var response = JSON.parse(data);
                if(response.status_phrase == "ok"){
                    Messenger().post({
                        id: "evaluate_report",
                        type: "success",
                        message: "批阅成功"
                    })
                    $("div#experiment_report_info").load("./ #experiment_report_info");
                }
            }
        })
        return false;
    })
}
