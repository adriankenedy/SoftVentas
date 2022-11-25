function myFunction() {
    var input, filter, table, tr, td, cell, i, j;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("myTable");
    tr = table.getElementsByTagName("tr");
    for (i = 1; i < tr.length; i++) {
        // Hide the row initially.
        tr[i].style.display = "none";

        td = tr[i].getElementsByTagName("td");
        for (var j = 0; j < td.length; j++) {
            cell = tr[i].getElementsByTagName("td")[j];
            if (cell) {
                if (cell.innerHTML.toUpperCase().indexOf(filter) > -1) {
                    tr[i].style.display = "";
                    break;
                }
            }
        }
    }
}

function buscarProductos() {
    var input, filter, table, tr, td, cell, i, j;
    input = document.getElementById("pbuscar");
    filter = input.value.toUpperCase();
    table = document.getElementById("productosb");
    tr = table.getElementsByTagName("tr");
    for (i = 1; i < tr.length; i++) {
        // Hide the row initially.
        tr[i].style.display = "none";

        td = tr[i].getElementsByTagName("td");
        for (var j = 0; j < td.length; j++) {
            cell = tr[i].getElementsByTagName("td")[j];
            if (cell) {
                if (cell.innerHTML.toUpperCase().indexOf(filter) > -1) {
                    tr[i].style.display = "";
                    break;
                }
            }
        }
    }
}



var $tablaCarrito = $('#tablaCarrito');


function carrito(inv0, inv1, inv2, inv3){
    
    var lote = inv1;

    $tablaCarrito.append(`
    <tr id="prod">
        <td>
            <a id="agregar" class="btn btn-danger" role="button" 
            onclick="descartarCarrito('${lote}')" class="btn btn-danger
            btn-rounded" role="button"><i class="fa-solid fa-trash"></i></a>
        </td>
        <td>
            <div class="col-md-4">
                <input type="text" class="form-control" name="id"  value="${inv0}" >
            </div>
        </td>
        <td>
            <div class="col-md-14">
                <input type="text" class="form-control" name="producto"  value="${inv1}" >
            </div>
        </td>
        <td>
            <div class="col-md-6">
                <input type="text" class="form-control" name="lote"  value="${inv2}" >
            </div>
        </td>
        <td>
            <div class="col-md-6">
                <input id="precioP" type="text" class="form-control" name="precio"  value="${inv3}" >
            </div>
        </td>
        <td>
            <div class="col-md-6">
                <input id="cantidadproducto" type="text" class="form-control" name="cantidad" onkeyup="entidades()">
            </div>
        </td>
        <td>
            <div class="col-md-6">
                <input id="totalPC" type="text" class="form-control" name="totalPC">
            </div>
        </td>
    </tr>
    `);
    
/*
    $('input[name^=precio]').each(function(){
        precioP.push($(this).val());
    });
*/
}

function descartarCarrito(lote){
    var result = confirm(`¿Descartar del carrito: ${lote} ?`);

    if(result){
        $('#prod').remove();
    }
}



function entidades(){
    var t = 0;
    $("#tablaCarrito tr").each(function(index, elem){
        var precio = $(elem).find("#precioP").val();
        var cantidad = $(elem).find("#cantidadproducto").val();
        var totalP = precio * cantidad;
        t += totalP;

        $(elem).find("#totalPC").val(totalP);
        $("#sumaproductos").val(t);

        //console.log(index, precio, cantidad, totalP, t);
    });
     
}

