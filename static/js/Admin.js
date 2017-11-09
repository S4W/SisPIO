/*
        Menu izquierdo admin
        
        */
        var acc = document.getElementsByClassName("accordion");
                        var i;

                        for (i = 0; i < acc.length; i++) {
                            acc[i].onclick = function(){
                                this.classList.toggle("active");
                                var panel = this.nextElementSibling;
                                if (panel.style.display === "block") {
                                    panel.style.display = "none";
                                } else {
                                    panel.style.display = "block";
                                }
                            }
                        }


        /*Comparacion de contrase;as
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
        confirm_password.onkeyup = validatePassword;*/
        
        
    /*Cambio de seleccion en el menu izquierdo*/
    $(".btn-group-vertical button").on("click", function(){
       $(".btn").find(".active").removeClass("active");
       $(this).parent().addClass("active");
    });
        
    $(document).ready(function(){
    $("#manualSede, #manualEmail").hide();
    /*Boton Agregar manual seleccion de tipo persona*/
     $("#cargarProfesor").click(function(){
        console.log("profesor");
        $("#manualLiceo, #manualPromedio, #manualSede").hide();

    });
     $("#cargarEstudiante").click(function(){
        console.log("estudiante");
        $("#manualLiceo, #manualPromedio").show();
        $("#manualEmail").hide();

    });
     $("#cargarSede").click(function(){
        console.log("coord sede");
        $("#manualLiceo, #manualPromedio, #manualEmail").hide();
        $("#manualSede").show();

    });
     $("#cargarLiceo").click(function(){
        console.log("coord liceo");
        $("#manualPromedio, #manualSede").hide();
        $("#manualLiceo, #manualEmail").show();

    });
     $("#cargarAdmin").click(function(){
        console.log("admin");
        $("#manualPromedio, #manualSede, #manualLiceo").hide();
        $("#manualEmail").show();

    });

     /*Menus*/
    $(".glyphicon, #userinfo" ).click(function(){
        $("#information, #agregar,#modificar,#cohorte").hide();
        $("#enviarEmail, #cargar,#eliminar").hide();
        $("#cambioContra, #reporte").hide();
        $("#noticias, #consultar, #institucion, #eliminarInstitucion").hide();
        $("#miPerfil").show();
        $(".nav").find(".active").removeClass("active");
        $(".perfil").parent().addClass("active");
    });
   
    $(".perfil").click(function(){
        $("#information, #agregar, #cargar, #eliminar").hide();
        $("#enviarEmail, #institucion,#cohorte").hide();
        $("#noticias, #reporte").hide();
        $("#cambioContra, #consultar, #eliminarInstitucion").hide();
        $("#miPerfil").show();
         $(".nav").find(".active").removeClass("active");
        $(".perfil").parent().addClass("active");
    });
    $("#principal").click(function(){
        $("#information").show();
        $("#noticias, #agregar, #cargar, #eliminar").hide();
        $("#enviarEmail,#modificar, #institucion").hide();
        $("#cambioContra, #reporte,#cohorte").hide();
        $("#miPerfil, #consultar,#cohorte, #eliminarInstitucion").hide();
    });
    $("#pass").click(function(){
        $("#information, #agregar, #cargar").hide();
        $("#enviarEmail,#modificar, #institucion").hide();
        $("#noticias, #reporte, #eliminar").hide();
        $("#cambioContra").show();
        $("#miPerfil, #consultar, #cohorte,#eliminarInstitucion").hide();
    });
     $("#comp").click(function(){
        $("#information, #agregar, #cargar").hide();
        $("#enviarEmail,#institucion").hide();
        $("#noticias,#modificar,#cohorte").hide();
         $("#reporte").show();
        $("#cambioContra,#eliminar").hide();
        $("#miPerfil, #consultar, #eliminarInstitucion").hide();
    });
     $("#inst").click(function(){
        $("#information, #agregar, #cargar").hide();
        $("#enviarEmail,#eliminar,#cohorte").hide();
        $("#noticias,#modificar, #cargar").hide();
        $("#cambioContra, #reporte").hide();
        $("#institucion").show();
        $("#miPerfil, #consultar, #eliminarInstitucion").hide();
    });
    $("#upload").click(function(){
        $("#information, #agregar, #cargar").hide();
        $("#enviarEmail,#eliminar,#cohorte").hide();
        $("#noticias,#modificar, #institucion").hide();
        $("#cambioContra, #reporte").hide();
        $("#cargar").show();
        $("#miPerfil, #consultar, #eliminarInstitucion").hide();
    });
    $("#lookfor").click(function(){
        $("#information, #agregar, #cargar").hide();
        $("#enviarEmail,#modificar,#cohorte").hide();
        $("#noticias,#permiso,#institucion").hide();
        $("#cambioContra, #eliminar").hide();
        $("#consultar").show();
        $("#miPerfil, #reporte, #eliminarInstitucion").hide();
    });
    $("#add").click(function(){
        $("#information, #cargar,#cohorte").hide();
        $("#enviarEmail, #eliminar").hide();
        $("#noticias, #consultar, #institucion").hide();
        $("#agregar").show();
        $("#cambioContra,#modificar").hide();
        $("#miPerfil, #reporte, #eliminarInstitucion").hide();
    });
    $("#edit").click(function(){
        $("#information, #cargar, #eliminar").hide();
        $("#enviarEmail,#cohorte").hide();
        $("#noticias, #consultar, #institucion").hide();
        $("#modificar").show();
        $("#cambioContra,#agregar").hide();
        $("#miPerfil, #reporte, #eliminarInstitucion").hide();
    });
    $("#delete").click(function(){
        $("#information, #cargar").hide();
        $("#enviarEmail, #modificar").hide();
        $("#noticias, #consultar, #institucion").hide();
        $("#eliminar").show();
        $("#cambioContra,#agregar,#cohorte").hide();
        $("#miPerfil, #reporte, #eliminarInstitucion").hide();
    });
    $("#news").click(function(){
        $("#information, #agregar, #cargar, #consultar").hide();
        $("#enviarEmail,#modificar, #institucion").hide();
        $("#noticias").show();
        $("#cambioContra, #eliminar").hide();
        $("#miPerfil, #reporte,#cohorte, #eliminarInstitucion").hide();
    });
    $("#cohor").click(function(){
        $("#information, #agregar, #cargar, #consultar").hide();
        $("#enviarEmail,#modificar, #institucion").hide();
        $("#cohorte").show();
        $("#cambioContra, #eliminar, noticias").hide();
        $("#miPerfil, #reporte, #eliminarInstitucion").hide();
    });
    $("#deleteInst").click(function(){
        $("#information, #agregar, #cargar").hide();
        $("#enviarEmail,#modificar, #institucion").hide();
        $("#noticias, #reporte, #eliminar, #cambioContra,#cohorte").hide();
        $("#eliminarInstitucion").show();
        $("#miPerfil, #consultar").hide();
    });
    $("#contacto, #enviar").click(function(){
        $("#information, #agregar, #cargar").hide();
        $("#enviarEmail").show();
        $("#cambioContra, #consultar, #institucion, #eliminarInstitucion").hide();
        $("#noticias, #reporte, #eliminar").hide();
        $("#miPerfil,#modificar,#cohorte").hide();
        $(".nav").find(".active").removeClass("active");
        $("#contacto").parent().addClass("active");
    });
});
