
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
    $("#manualSede").hide();
    /*Boton Agregar manual seleccion de tipo persona*/
     $("#cargarProfesor").click(function(){
        console.log("profesor");
        $("#manualLiceo, #manualPromedio, #manualSede").hide();

    });
     $("#cargarEstudiante").click(function(){
        console.log("estudiante");
        $("#manualLiceo, #manualPromedio").show();

    });
     $("#cargarSede").click(function(){
        console.log("coord sede");
        $("#manualLiceo, #manualPromedio").hide();
        $("#manualSede").show();

    });
     $("#cargarLiceo").click(function(){
        console.log("coord liceo");
        $("#manualPromedio, #manualSede").hide();
        $("#manualLiceo").show();

    });

     
     /*Menus*/
    $(".glyphicon, #userinfo" ).click(function(){
        $("#information, #agregar,#modificar").hide();
        $("#enviarEmail, #cargar,#eliminar").hide();
        $("#cambioContra, #reporte").hide();
        $("#noticias, #consultar, #institucion").hide();
        $("#miPerfil").show();
        $(".nav").find(".active").removeClass("active");
        $(".perfil").parent().addClass("active");
    });
   
    $(".perfil").click(function(){
        $("#information, #agregar, #cargar, #eliminar").hide();
        $("#enviarEmail, #institucion").hide();
        $("#noticias, #reporte").hide();
        $("#cambioContra, #consultar").hide();
        $("#miPerfil").show();
         $(".nav").find(".active").removeClass("active");
        $(".perfil").parent().addClass("active");
    });
    $("#principal").click(function(){
        $("#information").show();
        $("#noticias, #agregar, #cargar, #eliminar").hide();
        $("#enviarEmail,#modificar, #institucion").hide();
        $("#cambioContra, #reporte").hide();
        $("#miPerfil, #consultar").hide();
    });
    $("#pass").click(function(){
        $("#information, #agregar, #cargar").hide();
        $("#enviarEmail,#modificar, #institucion").hide();
        $("#noticias, #reporte, #eliminar").hide();
        $("#cambioContra").show();
        $("#miPerfil, #consultar").hide();
    });
     $("#comp").click(function(){
        $("#information, #agregar, #cargar").hide();
        $("#enviarEmail,#institucion").hide();
        $("#noticias,#modificar").hide();
         $("#reporte").show();
        $("#cambioContra,#eliminar").hide();
        $("#miPerfil, #consultar").hide();
    });
     $("#inst").click(function(){
        $("#information, #agregar, #cargar").hide();
        $("#enviarEmail,#eliminar").hide();
        $("#noticias,#modificar, #cargar").hide();
        $("#cambioContra, #reporte").hide();
        $("#institucion").show();
        $("#miPerfil, #consultar").hide();
    });
    $("#upload").click(function(){
        $("#information, #agregar, #cargar").hide();
        $("#enviarEmail,#eliminar").hide();
        $("#noticias,#modificar, #institucion").hide();
        $("#cambioContra, #reporte").hide();
        $("#cargar").show();
        $("#miPerfil, #consultar").hide();
    });
    $("#lookfor").click(function(){
        $("#information, #agregar, #cargar").hide();
        $("#enviarEmail,#modificar").hide();
        $("#noticias,#permiso,#institucion").hide();
        $("#cambioContra, #eliminar").hide();
        $("#consultar").show();
        $("#miPerfil, #reporte").hide();
    });
    $("#add").click(function(){
        $("#information, #cargar").hide();
        $("#enviarEmail, #eliminar").hide();
        $("#noticias, #consultar, #institucion").hide();
        $("#agregar").show();
        $("#cambioContra,#modificar").hide();
        $("#miPerfil, #reporte").hide();
    });
    $("#edit").click(function(){
        $("#information, #cargar, #eliminar").hide();
        $("#enviarEmail").hide();
        $("#noticias, #consultar, #institucion").hide();
        $("#modificar").show();
        $("#cambioContra,#agregar").hide();
        $("#miPerfil, #reporte").hide();
    });
    $("#delete").click(function(){
        $("#information, #cargar").hide();
        $("#enviarEmail, #modificar").hide();
        $("#noticias, #consultar, #institucion").hide();
        $("#eliminar").show();
        $("#cambioContra,#agregar").hide();
        $("#miPerfil, #reporte").hide();
    });
    $("#news").click(function(){
        $("#information, #agregar, #cargar, #consultar").hide();
        $("#enviarEmail,#modificar, #institucion").hide();
        $("#noticias").show();
        $("#cambioContra, #eliminar").hide();
        $("#miPerfil, #reporte").hide();
    });
    $("#contacto, #enviar").click(function(){
        $("#information, #agregar, #cargar").hide();
        $("#enviarEmail").show();
        $("#cambioContra, #consultar, #institucion").hide();
        $("#noticias, #reporte, #eliminar").hide();
        $("#miPerfil,#modificar").hide();
        $(".nav").find(".active").removeClass("active");
        $("#contacto").parent().addClass("active");
    });
});