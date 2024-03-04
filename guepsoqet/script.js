document.addEventListener("DOMContentLoaded", () => {
    const websocket = new WebSocket("ws://localhost:8765");
    const ctx = document.getElementById("sensorUltrasonico").getContext("2d");
    const chart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: [],
            datasets: [
                {
                    label: "Sensor Data",
                    backgroundColor: "rgb(51, 141, 255)",
                    borderColor: "rgb(93, 164, 255)",
                    data: [],
                },
            ],
        },
        options: {},
    });

    websocket.onopen = () => console.log("Conectado al servidor WebSocket");

    websocket.onmessage = (event) => {
        const message = event.data;
        console.log("Mensaje recibido:", message);
    
        // Actualiza la interfaz de usuario según el estado del LED
        const toggleBtn = document.getElementById("toggleBtn");
    
        // Manejar los mensajes "0" y "1"
        if(message === "1" || message === "0") {
            toggleBtn.checked = message === "1";
        }
    
        // Manejar los mensajes "2", "3" y "4"
        if(message === "2" || message === "3" || message === "4") {
            // Lógica para manejar las imágenes SVG del sensor ultrasónico
            var led0 = document.getElementById("led0");
    
            if (message === "2") {
                led0.src = "img/NUEVOROJO-ON.svg";
            } else if (message === "3") {
                led0.src = "img/NUEVOAMARILLO-ON.svg";
            } else if (message === "4") {
                led0.src = "img/NUEVOVERDE-ON.svg";
            }
        }
    
       
        if(!isNaN(message)) {
            chart.data.labels.push(new Date().toLocaleTimeString());
            chart.data.datasets[0].data.push(parseFloat(message));
            chart.update();
        }
    
        
    };

    document.getElementById("toggleBtn").addEventListener("change", function () {
        const command = this.checked ? "1" : "0";
        websocket.send(command);
        console.log("Enviado:", command);
    });
});