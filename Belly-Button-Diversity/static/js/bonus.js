

// @TODO: Build a Gauge Chart to plot the Weekly Washing Frequency obtained from the /metadata/<sample>route.


function buildGauge(WFREQ) {


    // Enter the washing frequency
    let level = parseFloat(WFREQ) * 20;
    // Claculate degree of WFREQ
    let degrees = 180 - level;
    //length of meter needle
    let radius = 0.5; 
    //Converting degrees to radian
    let radians = (degrees * Math.PI) / 180;
    let x = radius * Math.cos(radians);
    let y = radius * Math.sin(radians);
    // Needle size settings
    let mainPath = "M-.0 -0.05 L  .0 0.05 L";
    let pathX = String(x);
    let space = " ";
    let pathY = String(y);
    let pathEnd = " Z";
    let path = mainPath.concat(pathX, space, pathY, pathEnd);

    //Get element for guage
    let Gauge = document.getElementById("gauge");


    let dataGuage = [
        {
            type: "scatter",
            x:[0],
            y:[0],
            marker: { size: 12, color: "850000" },
            name: "Freq",
            showlegend: false,
            text: level,
            hoverinfo: "text+name"
        },
        {
            values: [50 / 9, 50 / 9, 50 / 9, 50 / 9, 50 / 9, 50 / 9, 50 / 9, 50 / 9, 50 / 9, 50],
            rotation: 90,
            text:["8-9", "7-8", "6-7", "5-6", "4-5", "3-4", "2-3", "1-2", "0-1", ""],
            textinfo: "text",
            textposition: "inside",
            marker: {
                colors: [
                    "rgba(0, 105, 11, .5)",
                    "rgba(10, 120, 22, .5)",
                    "rgba(14, 127, 0, .5)",
                    "rgba(110, 154, 22, .5)",
                    "rgba(170, 202, 42, .5)",
                    "rgba(202, 209, 95, .5)",
                    "rgba(210, 206, 145, .5)",
                    "rgba(232, 226, 202, .5)",
                    "rgba(240, 230, 215, .5)",
                    "rgba(255, 255, 255, 0)"
                ]
            },
            labels:["8-9", "7-8", "6-7", "5-6", "4-5", "3-4", "2-3", "1-2", "0-1", ""],
            hoverinfo: "label",
            hole: 0.5,
            type: "pie",
            showlegend: false
        }
    ];


    var layoutGuage = {
        shapes: [
            {
                type: "path",
                path: path,
                fillcolor: "850000",
                line: {
                    color: "850000"
                }
            }
        ],
        title: "<b>Belly Button Washing Frequency </b> <br> Scrubs per Week",
        height: 500,
        width: 500,
        xaxis: {
            //Making all the settings to false for removing grid structure
            zeroline:false,
            showticklabels: false,
            showgrid: false,
            range: [-1, 1]
        },
        yaxis: {
            //Making all the settings to false for removing grid structure
            zeroline: false,
            showticklabels: false,
            showgrid: false,
            range: [-1, 1]
        }
    };

    

    Plotly.newPlot(Gauge, dataGuage, layoutGuage);


}




