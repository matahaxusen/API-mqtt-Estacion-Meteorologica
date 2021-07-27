var server_address = "http://35.242.198.119:5000/";

var get_last = function () {
  $.get(server_address +"sensor_data", function (data){
      $(".result").html("Temperature: " + data.temperature + "C | Humidity: " + data.humidity + "%")
  });
}
var get_measures = function () {
  $.get(server_address +"sensor_list", function (data){
    var aux = "<tr><th>ID</th><th>Humedad</th><th>Temperatura</th><th>Ubicacion</th><th>Fecha</th><th>Dispositivo</th></tr>";
    for(var i=0;i<Object.size(data); i++){
        aux += "<tr>";
        aux += "<td>" + data[i][0] + "</td>";
        aux += "<td>" + data[i][1]+ "</td>";
        aux += "<td>" + data[i][2] + "</td>";
        aux += "<td>" + data[i][3]+ "</td>";
        aux += "<td>" + data[i][4] + "</td>";
        aux += "<td>" + data[i][5] + "</td>";
        aux += "</tr>";
    }
    //alert(aux);
    $(".result").html(aux);
  });
}

get_measures()

function date_checker(fecha,fecha_inicio, fecha_fin){
     var fecha_partida = fecha.split(' ');
     var descomposcion_tres_partes = fecha_partida[0].split('/');
     descomposcion_tres_partes = new Date(parseInt(descomposcion_tres_partes[2], 10),parseInt(descomposcion_tres_partes[1],10)-1,parseInt(descomposcion_tres_partes[0],10));
    var tres_partes_inicio = fecha_inicio.split('-');
    tres_partes_inicio = new Date(parseInt(tres_partes_inicio[0],10),parseInt(tres_partes_inicio[1],10)-1,parseInt(tres_partes_inicio[2],10));
    var tres_partes_fin = fecha_fin.split('-');
    tres_partes_fin = new Date(parseInt(tres_partes_fin[0], 10),parseInt(tres_partes_fin[1],10)-1, parseInt(tres_partes_fin[2],10));
    if (descomposcion_tres_partes>=tres_partes_inicio && descomposcion_tres_partes<=tres_partes_fin){
        return true;
    }else return false;
}


function busqueda() {
    var fechainicio = document.getElementById("fechainicio").value;
    var fechafin = document.getElementById("fechafin").value;
    document.getElementById("result").style.display = "none";
    document.getElementById("busqueda").style.display = "block";
  $.get(server_address +"busqueda", function(data){
        var aux = "<tr><th>ID</th><th>Humedad</th><th>Temperatura</th><th>Ubicacion</th><th>Fecha</th><th>Dispositivo</th></tr>";
        var contador = 0;
        for(var i=0;i<Object.size(data); i++){
            if (date_checker(String(data[i][4]),String(fechainicio),String(fechafin)) == true){
                contador++;
                aux += "<tr>";
                aux += "<td>" + data[i][0] + "</td>";
                aux += "<td>" + data[i][1] + "</td>";
                aux += "<td>" + data[i][2] + "</td>";
                aux += "<td>" + data[i][3] + "</td>";
                aux += "<td>" + data[i][4] + "</td>";
                aux += "<td>" + data[i][5] + "</td>";
                aux += "</tr>";
            }else {
                //pass
            }
        }
        if (contador == 0){
        aux = "No se han encontrado registros en esas fechas"
    }
    $(".busqueda").html(aux)
  });
}

var get_devices = function () {
  $.get(server_address +"devices_list", function (data){
    var aux = "<tr><th>ID</th><th>Dispositivo</th><th>Status</th><th>Ultimo registro</th><th>Ubicación</th></tr>";
    for(var i=0;i<Object.size(data); i++){
        aux += "<tr>";
        aux += "<td>" + data[i][0] + "</td>";
        aux += "<td>" + data[i][1] + "</td>";
        aux += "<td>" + data[i][2] + "</td>";
        aux += "<td>" + data[i][3] + "</td>";
        aux += "<td>" + data[i][4] + "</td>";
        aux += "</tr>";
    }
    //alert(aux);
    $(".devices").html(aux)
    });
}

/*
$.get(server_address+"hello_world",function(data){
    $(".greet").html(data.msg);
});

 */


function sleep(milliseconds) {
 var start = new Date().getTime();
 for (var i = 0; i < 1e7; i++) {
  if ((new Date().getTime() - start) > milliseconds) {
   break;
  }
 }
}

Object.size = function(obj) {
  var size = 0,
    key;
  for (key in obj) {
    if (obj.hasOwnProperty(key)) size++;
  }
  return size;
};

get_devices()
setInterval(get_measures, 5000);
