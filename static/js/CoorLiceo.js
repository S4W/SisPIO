
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
        $("#information, #agregar,#modificar").hide();
        $("#enviarEmail, #cargar").hide();
<<<<<<< HEAD
        $("#cambioContra, #reporte").hide();
=======
        $("#cambioContra").hide();
>>>>>>> 190879287305cbfd57f756e33e77d536d3eee0ec
        $("#noticias, #consultar").hide();
        $("#miPerfil").show();
        $(".nav").find(".active").removeClass("active");
        $(".perfil").parent().addClass("active");
    });
   
    $(".perfil").click(function(){
        $("#information, #agregar, #cargar").hide();
        $("#enviarEmail").hide();
<<<<<<< HEAD
        $("#noticias, #reporte").hide();
=======
        $("#noticias").hide();
>>>>>>> 190879287305cbfd57f756e33e77d536d3eee0ec
        $("#cambioContra, #consultar").hide();
        $("#miPerfil").show();
         $(".nav").find(".active").removeClass("active");
        $(".perfil").parent().addClass("active");
    });
    $("#principal").click(function(){
        $("#information").show();
        $("#noticias, #agregar, #cargar").hide();
        $("#enviarEmail,#modificar").hide();
<<<<<<< HEAD
        $("#cambioContra, #reporte").hide();
=======
        $("#cambioContra").hide();
>>>>>>> 190879287305cbfd57f756e33e77d536d3eee0ec
        $("#miPerfil, #consultar").hide();
    });
    $("#pass").click(function(){
        $("#information, #agregar, #cargar").hide();
        $("#enviarEmail,#modificar").hide();
<<<<<<< HEAD
        $("#noticias, #reporte").hide();
        $("#cambioContra").show();
        $("#miPerfil, #consultar").hide();
    });
     $("#comp").click(function(){
        $("#information, #agregar, #cargar").hide();
        $("#enviarEmail").hide();
        $("#noticias,#modificar").hide();
         $("#reporte").show();
        $("#cambioContra").hide();
        $("#miPerfil, #consultar").hide();
    });
=======
        $("#noticias").hide();
        $("#cambioContra").show();
        $("#miPerfil, #consultar").hide();
    });
>>>>>>> 190879287305cbfd57f756e33e77d536d3eee0ec
    $("#upload").click(function(){
        $("#information, #agregar, #cargar").hide();
        $("#enviarEmail").hide();
        $("#noticias,#modificar").hide();
<<<<<<< HEAD
        $("#cambioContra, #reporte").hide();
=======
        $("#cambioContra").hide();
>>>>>>> 190879287305cbfd57f756e33e77d536d3eee0ec
        $("#cargar").show();
        $("#miPerfil, #consultar").hide();
    });
    $("#lookfor").click(function(){
        $("#information, #agregar, #cargar").hide();
        $("#enviarEmail,#modificar").hide();
        $("#noticias").hide();
        $("#cambioContra").hide();
        $("#consultar").show();
<<<<<<< HEAD
        $("#miPerfil, #reporte").hide();
=======
        $("#miPerfil").hide();
>>>>>>> 190879287305cbfd57f756e33e77d536d3eee0ec
    });
    $("#add").click(function(){
        $("#information, #cargar").hide();
        $("#enviarEmail").hide();
        $("#noticias, #consultar").hide();
        $("#agregar").show();
        $("#cambioContra,#modificar").hide();
<<<<<<< HEAD
        $("#miPerfil, #reporte").hide();
=======
        $("#miPerfil").hide();
>>>>>>> 190879287305cbfd57f756e33e77d536d3eee0ec
    });
    $("#edit").click(function(){
        $("#information, #cargar").hide();
        $("#enviarEmail").hide();
        $("#noticias, #consultar").hide();
        $("#modificar").show();
        $("#cambioContra,#agregar").hide();
<<<<<<< HEAD
        $("#miPerfil, #reporte").hide();
=======
        $("#miPerfil").hide();
>>>>>>> 190879287305cbfd57f756e33e77d536d3eee0ec
    });
    $("#news").click(function(){
        $("#information, #agregar, #cargar, #consultar").hide();
        $("#enviarEmail,#modificar").hide();
        $("#noticias").show();
        $("#cambioContra").hide();
<<<<<<< HEAD
        $("#miPerfil, #reporte").hide();
=======
        $("#miPerfil").hide();
>>>>>>> 190879287305cbfd57f756e33e77d536d3eee0ec
    });
    $("#contacto, #enviar").click(function(){
        $("#information, #agregar, #cargar").hide();
        $("#enviarEmail").show();
        $("#cambioContra, #consultar").hide();
<<<<<<< HEAD
        $("#noticias, #reporte").hide();
=======
        $("#noticias").hide();
>>>>>>> 190879287305cbfd57f756e33e77d536d3eee0ec
        $("#miPerfil,#modificar").hide();
        $(".nav").find(".active").removeClass("active");
        $("#contacto").parent().addClass("active");
    });
});