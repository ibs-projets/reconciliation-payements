<script>
    $(document).ready(function(){
        $(".mod").on("click",function(){
            var module = $(this).attr("module");
            $.ajax({
                type: "post",
                url: "{% url 'reco_gest:changer_module' %}",
                data: {
                    "csrfmiddlewaretoken": "{{ csrf_token }}",
                    "module": module
                },
                success: function(module){console.log(reponse["module"]);},
                error: function(){
                    alert("Problème dans le choix du module");
                }
            });
        });
    });
</script>