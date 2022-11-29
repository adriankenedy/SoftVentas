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

function carrito(inv0, inv1, inv2, inv3, inv5){
    
    var lote = inv1;
    var existencias = inv5;

    if(existencias > 0 ){
        $tablaCarrito.append(`
        <tr entidad="${inv0}" id="prod">
            <td>
                <a id="agregar" class="btn btn-danger" role="button" 
                class="btn btn-danger
                btn-rounded" role="button"><i class="fa-solid fa-trash"></i></a>
            </td>
            <td>
                <div class="col-md-6">
                    <input type="text" class="form-control" name="id"  value="${inv0}" >
                </div>
            </td>
            <td>
                <div class="col-md-18">
                    <input id="pnombre" type="text" class="form-control" name="producto"  value="${inv1}" >
                </div>
            </td>
            <td>
                <div class="col-md-8">
                    <input type="text" class="form-control" name="lote"  value="${inv2}" >
                </div>
            </td>
            <td>
                <div class="col-md-6">
                    <input id="existencias" type="text" class="form-control" name="existencias"  value="${inv5}" >
                </div>
            </td>
            <td>
                <div class="col-md-8">
                    <input id="precioP" type="text" class="form-control" name="precio"  value="${inv3}" >
                </div>
            </td>
            <td>
                <div class="col-md-6">
                    <input id="cantidadproducto" type="text" class="form-control" name="cantidad" onkeyup="entidades()">
                </div>
            </td>
            <td>
                <div class="col-md-8">
                    <input id="totalPC" type="text" class="form-control" name="totalPC">
                </div>
            </td>
        </tr>
        `);

    }else{
        alert(`ADVERTENCIA!
        No hay existencias para el producto ${inv1}.
        Revisar almacen.`);
        return false;

    }
}


$("#tablaCarrito").on('click', '#agregar', function(){
    var $tr = $(this).closest('tr');
    var tp = $tr.find('#totalPC').val();
    var sumav = $("#sumaproductos").val();
    var nombrep = $tr.find("#pnombre").val();

    var restaventa = sumav - tp;

    let result = confirm(`¿Descartar del carrito: ${nombrep} ?`);

    if(result){
        $("#sumaproductos").val(restaventa);
        $tr.remove();
    }

    //console.log(sumav, tp, restaventa);
})




function entidades(){
    var t = 0;

    $("#tablaCarrito tr").each(function(index, elem){
        var precio = $(elem).find("#precioP").val();
        var cantidad = $(elem).find("#cantidadproducto").val();
        var totalP = precio * cantidad;
        t += totalP;

        $(elem).find("#totalPC").val(totalP);

        $("#sumaproductos").val(t);
       
        
    });
     
}



$("#tVenta").click(function(){
    var vC = $("#tablaCarrito tr").length;
    let cantidad = "";
    let pnombre = "";
    let total = "";

    $("#tablaCarrito tr").each(function(index, ele){
        cantidad = $(ele).find("#cantidadproducto").val();
        pnombre = $(ele).find("#pnombre").val();
        total = $(ele).find("#totalPC").val();
        existencias = $(ele).find("#existencias").val();

    });

    if(vC > 0){
        var tv =  confirm("¿Terminar venta?");
        
        if(tv == true){
            
            if(cantidad === "" && total === "" || total == null){
                alert(`ADVERTENCIA!
                Debe agregar una cantidad al producto ${pnombre}`);
                return false;
        
            }else if (cantidad > existencias){
                alert(`ADVERTENCIA!
                La cantidad ingresada es mayor a las existencias del producto ${pnombre}`);
                return false;
            }

        }else{
            return false;
        }
        
    }else{
        alert(`ADVERTENCIA!
        Debe agregar como minimo un producto.`);
        return false;
    }
    
});
