/*Pagina principal. Validacion de datos usuario y password
index.html
*/

$(document).ready(function(){
    $(".contacto").hide();

    $('.navbar li').click(function(e) {
        $('.navbar li.active').removeClass('active');
        var $this = $(this);
        if (!$this.hasClass('active')) {
            $this.addClass('active');
        }
    e.preventDefault();
    });

    $("#contacto").click(function(){
        $(".inicio").hide();
        $(".contacto").show();
    });
    
     $("#inicio").click(function(){
        $(".contacto").hide();
        $(".inicio").show();
    
    
    });
});



        
/*Comparacion de contrase;as en la vista welcome.html*/
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
        
        

 

    $(document).ready(function(){
        /*Cambio de seleccion en el menu izquierdo welcome.html y cualquier otro*/
    $(".nav-stacked a").on("click", function(){
       $(".nav").find(".active").removeClass("active");
       $(this).parent().addClass("active");
    });
    

});