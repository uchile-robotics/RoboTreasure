
var seg_preg = 15
var seg_pregunta = 1 + seg_preg;
var seg_preparacion = 3;
var display_seg = 0;
var preguntas = ["¿1?", "¿2?", "¿3?"]
var numero_preg = 0;
var estados = ["Tiempo restante:","Ya!","Listos","Preparados"];
var interval = null;
var interval2 = null;
var status = "stopped";
var tiempo_respuesta = 0;
var puntaje = 0;

function stopWatchPreparacion(){
	if(seg_preparacion > 0){
		document.getElementById("pregunta").innerHTML = "Pregunta "+(numero_preg+1).toString();
		seg_preparacion--;
	}   
    if(seg_preparacion < 10){
        display_seg = "0" + seg_preparacion.toString() + "s";
		document.getElementById("display").innerHTML = display_seg;
    }
	document.getElementById("estado").innerHTML = estados[seg_preparacion]
    if(seg_preparacion  === 0){
		document.getElementById("pregunta").innerHTML = preguntas[numero_preg];
		if(seg_pregunta > 0){
			seg_pregunta--;
		}   
		if(seg_pregunta < 10){
			display_seg = "0" + seg_pregunta.toString() + "s";	
		}	
		else{
			display_seg = seg_pregunta + "s";
		}	
		document.getElementById("display").innerHTML = display_seg;
	}
}

function Correcto(){
	document.getElementById("estado").innerHTML = "Preparados"
	if(numero_preg < preguntas.length-1){
		document.getElementById("pregunta").innerHTML = "Pregunta "+(numero_preg+2).toString();	
		
		tiempo_respuesta = seg_pregunta 
		puntaje = puntaje + tiempo_respuesta*10
		document.getElementById("puntaje").innerHTML = "Puntaje: "+puntaje.toString()
		
		seg_preg = 15;
		seg_pregunta = seg_preg + 1
		seg_preparacion = 3;
		document.getElementById("display").innerHTML = "03s";
		document.getElementById("startStop").innerHTML = "Start";
		status = "stopped";
		numero_preg+=1
		window.clearInterval(interval);
		document.getElementById("startStop").innerHTML = "Start";
		status = "stopped";
	}
	else{
		tiempo_respuesta = seg_pregunta 
		puntaje = puntaje + tiempo_respuesta*10
		document.getElementById("puntaje").innerHTML = "Puntaje: "+puntaje.toString()
		window.clearInterval(interval);
		document.getElementById("startStop").innerHTML = "Start";
		status = "stopped";
		document.getElementById("pregunta").innerHTML = "Fin"
		document.getElementById("estado").innerHTML = "-";
		document.getElementById("display").innerHTML = "-";
		document.getElementById("startStop").innerHTML = "-";
		document.getElementById("siguiente").innerHTML = "-";
		status = "stopped";

	}
}

function Incorrecto(){
	document.getElementById("estado").innerHTML = "Preparados"
	if(numero_preg < preguntas.length-1){
		document.getElementById("pregunta").innerHTML = "Pregunta "+(numero_preg+2).toString();	
		seg_preg = 15;
		seg_pregunta = seg_preg + 1
		seg_preparacion = 3;
		document.getElementById("display").innerHTML = "03s";
		document.getElementById("startStop").innerHTML = "Start";
		status = "stopped";
		numero_preg+=1
		window.clearInterval(interval);
		document.getElementById("startStop").innerHTML = "Start";
		status = "stopped";
	}
	else{
		window.clearInterval(interval);
		document.getElementById("startStop").innerHTML = "Start";
		status = "stopped";
		document.getElementById("pregunta").innerHTML = "Fin"
		document.getElementById("estado").innerHTML = "-";
		document.getElementById("display").innerHTML = "-";
		document.getElementById("startStop").innerHTML = "-";
		document.getElementById("siguiente").innerHTML = "-";
		status = "stopped";
	}
}

function startStop(){
	if(status === "stopped"){
		interval = window.setInterval(stopWatchPreparacion, 1000);
		document.getElementById("startStop").innerHTML = "Stop";
		status = "started";
	}
	else{
		window.clearInterval(interval);
		document.getElementById("startStop").innerHTML = "Start";
		tiempo_respuesta = seg_pregunta
		status = "stopped";
	}
}








