
    	/**** WELCOME ESTUDIANTE ******/

    $(".glyphicon, #userinfo" ).click(function(){
        $("#information").hide();
        $("#enviarEmail").hide();
        $("#testVocacional").hide();
        $("#cambioContra").hide();
        $("#miPerfil").show();
        $(".nav").find(".active").removeClass("active");
        $("#perfil").parent().addClass("active");
    });
   /*Para el welcome.html estudiante*/
    $("#principal").click(function(){
        $("#information").show();
        $("#enviarEmail").hide();
        $("#cambioContra").hide();
        $("#testVocacional").hide();
        $("#miPerfil").hide();
    });
    /*Registro datos estudiantes*/
    $("#perfil").click(function(){
        $("#information").hide();
        $("#enviarEmail").hide();
        $("#cambioContra").hide();
        $("#testVocacional").e();
        $("#cambioContra").hide();
        $("#testVocacional").show();
        $("#miPerfil").hide();
    });
    /*Cambio de contrase;a*/
     $("#pass").click(function(){
        $("#information").hide()hide();
        $("#miPerfil").show();
    });
    /*Prueba vocacional*/
    $("#test").click(function(){
        $("#information").hide();
        $("#enviarEmail").hide();
        $("#cambioContra").hide();
        $("#testVocacional").show();
        $("#miPerfil").hide();
    });
    /*Cambio de contrase;a*/
     $("#pass").click(function(){
        $("#information").hide();
        $("#enviarEmail").hide();
        $("#cambioContra").show();
        $("#testVocacional").hide();
        $("#miPerfil").hide();
    });
     /*enviar email*/
    $("#contacto, #enviar").click(function(){
        $("#information").hide();
        $("#enviarEmail").show();
        $("#testVocacional").hide();
        $("#cambioContra").hide();
        $("#miPerfil").hide();
        $(".nav").find(".active").removeClass("active");
        $("#contacto").parent().addClass("active");
    });
    	
   