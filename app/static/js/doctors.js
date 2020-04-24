$(document).ready(function(){
    $.ajax({
        url: "http://192.168.1.102/get-doctors/",
        data:{
            areas : ["1","2"],
            keyword : "",
            experience : 20,
            type : 1
        },
        type: 'GET',
        dataType: 'jsonp',
        cors: true ,
        contentType:'application/json',
        secure: true,
        headers: {
          'Access-Control-Allow-Origin': '*',
        },
        cache: false,
        success: function(data){
          console.log(data);
        }
      });
});