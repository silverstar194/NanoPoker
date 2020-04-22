var intervalInMs = 50;

setInterval(
function(){
 $.ajax({url: "https://jsonplaceholder.typicode.com/todos/1", success: function(result){
        $("#x").text(i);
    }});
}, intervalInMs);