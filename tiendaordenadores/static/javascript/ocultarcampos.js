window.addEventListener("load", function() {
    // Llamamos a la función de mostrar/ocultar al cargar la página
    toggleMarcaVendedor(document.getElementById("id_rol").value);

    // Añadimos un event listener para que se ejecute cada vez que el rol cambie
    document.getElementById("id_rol").addEventListener("change", function(e) {
        toggleMarcaVendedor(e.target.value);
    });
});

function toggleMarcaVendedor(rol) {
    var campoMarcaVendedor = document.getElementById("marca-vendedor");
    
    // Si el rol es "vendedor" (valor 4), mostramos el campo, de lo contrario lo ocultamos
    if (rol == "4") {
        campoMarcaVendedor.style.display = "block";  // Mostrar campo
    } else {
        campoMarcaVendedor.style.display = "none";  // Ocultar campo
    }
}
