/**
 * Created by cnidarias on 28.11.17.
 */


var socket = io.connect('http://' + document.domain + ':' + location.port);
var myNewChart;

var count = 0;
var maxArraySize = 200;
var speedMax = 350;
var scaleMax = 10000;


var data = {
    labels : ["0"],
    datasets : [
        {
            borderColor: 'rgba(20, 220, 20, 0.1)',
            backgroundColor: 'rgba(20, 220, 20, 0.5)',
            data : [0]
        },
        {
            borderColor: 'rgba(220, 20, 20, 0.1)',
            backgroundColor: 'rgba(220, 20, 20, 0.5)',
            data : [0]
        }
    ]
};

var options = {
    legend: {
        display: false
    },
    tooltips: {
        enabled: false
    },
    scales: {
        yAxes: [{
            display:false,
            ticks: {
                beginAtZero: true,
                max: scaleMax
            }
        }],
        xAxes: [{
            display:false
        }]
    },
    elements: {
        point: {
            radius: 0
        }
    }
};


socket.on('connect', function() {
    socket.emit('my event', {data: 'I\'m connected!'});
});

socket.on('car_data', function (data) {
    updateChart(data["rpm"], data["speed"]);
});

var updateChart = function(rpm, speed) {
    if (myNewChart === null) return;
    var labels = data["labels"];
    var dataSet1 = data["datasets"][0]["data"];
    var dataSet2 = data["datasets"][1]["data"];

    count++;
    labels.push(count.toString());
    dataSet1.push(rpm);
    dataSet2.push(speed * (scaleMax/speedMax));
    if (count >= maxArraySize) {
        labels.shift();
        dataSet1.shift();
        dataSet2.shift();
    }
    myNewChart.update();
};

$(document).ready(function(){
    //Get the context of the canvas element we want to select
    $("#myChart").height($(window).height());
    $("#myChart").width($(window).width());
    var ctx = document.getElementById("myChart").getContext("2d");
    myNewChart = new Chart(ctx, {type: 'line', data: data, options: options});
});

