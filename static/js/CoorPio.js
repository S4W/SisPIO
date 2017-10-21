 /*Comparacion de contrase;as*/
        var password = document.getElementById("password")
          , confirm_password = document.getElementById("confirm_password");

        function validatePassword(){
          if(password.value != confirm_password.value) {
            confirm_password.setCustomValidity("Las contraseñas no coinciden");
          } else {
            confirm_password.setCustomValidity('');
          }
        }

        password.onchange = validatePassword;
        confirm_password.onkeyup = validatePassword;
        
        
        /*Cambio de seleccion en el menu izquierdo*/
    $(".nav-stacked a").on("click", function(){
       $(".nav").find(".active").removeClass("active");
       $(this).parent().addClass("active");
    });
        
    $(document).ready(function(){
       
    $(".glyphicon, #userinfo" ).click(function(){
        $("#information").hide();
        $("#enviarEmail").hide();
        $("#cambioContra").hide();
        $("#noticias, #consultar").hide();
        $("#miPerfil").show();
        $(".nav").find(".active").removeClass("active");
        $(".perfil").parent().addClass("active");
    });
   
    $(".perfil").click(function(){
        $("#information").hide();
        $("#enviarEmail").hide();
        $("#noticias").hide();
        $("#cambioContra, #consultar").hide();
        $("#miPerfil").show();
         $(".nav").find(".active").removeClass("active");
        $(".perfil").parent().addClass("active");
    });
    $("#principal").click(function(){
        $("#information").show();
        $("#noticias").hide();
        $("#enviarEmail").hide();
        $("#cambioContra").hide();
        $("#miPerfil, #consultar").hide();
    });
    $("#pass").click(function(){
        $("#information").hide();
        $("#enviarEmail").hide();
        $("#noticias").hide();
        $("#cambioContra").show();
        $("#miPerfil, #consultar").hide();
    });
    $("#lookfor").click(function(){
        $("#information").hide();
        $("#enviarEmail").hide();
        $("#noticias").hide();
        $("#cambioContra").hide();
        $("#consultar").show();
        $("#miPerfil").hide();
    });
    $("#news").click(function(){
        $("#information").hide();
        $("#enviarEmail").hide();
        $("#noticias").show();
        $("#cambioContra").hide();
        $("#miPerfil").hide();
    });
    $("#contacto, #enviar").click(function(){
        $("#information").hide();
        $("#enviarEmail").show();
        $("#cambioContra, #consultar").hide();
        $("#noticias").hide();
        $("#miPerfil").hide();
        $(".nav").find(".active").removeClass("active");
        $("#contacto").parent().addClass("active");
    });
});