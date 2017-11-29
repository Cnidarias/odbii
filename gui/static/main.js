/**
 * Created by cnidarias on 28.11.17.
 */


var socket = io.connect('http://' + document.domain + ':' + location.port);
var rpmChart;
var speedChart;

var count = 0;
var maxArraySize = 30;
var speedMax = 350;
var scaleMax = 10000;


var rpmData = {
    labels : ["0"],
    datasets : [
        {
            borderColor: 'rgba(220, 0, 0, 0.4)',
            backgroundColor: 'rgba(20, 220, 20, 0.3)',
            data : [0]
        }
    ]
};

var speedData = {
    labels : ["0"],
    datasets : [
        {
            borderColor: 'rgba(220, 0, 0, 0.4)',
            backgroundColor: 'rgba(20, 220, 20, 0.3)',
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
                beginAtZero: false,
                max: 0,
                min: -scaleMax

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


var options2 = {
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
                max: speedMax
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
    updateChart(-data["rpm"], data["speed"]);
});

var updateChart = function(rpm, speed) {
    if (rpmChart === null) return;
    var labels = rpmData["labels"];
    var labels2 = speedData["labels"];
    var dataSet1 = rpmData["datasets"][0]["data"];
    var dataSet2 = speedData["datasets"][0]["data"];

    count++;
    labels.push(count.toString());
    labels2.push(count.toString());
    dataSet1.push(rpm);
    dataSet2.push(speed);
    if (count >= maxArraySize) {
        labels.shift();
        labels2.shift();
        dataSet1.shift();
        dataSet2.shift();
    }
    rpmChart.update();
    speedChart.update();
};

$(document).ready(function(){
    //Get the context of the canvas element we want to select
    $("#rpmChart").height($(window).height()/2);
    $("#rpmChart").width($(window).width());
    var ctx = document.getElementById("rpmChart").getContext("2d");
    rpmChart = new Chart(ctx, {type: 'line', data: rpmData, options: options});

    $("#speedChart").height($(window).height()/2);
    $("#speedChart").css('top', $(window).height/2);
    $("#speedChart").width($(window).width());

    var ctx = document.getElementById("speedChart").getContext("2d");
    speedChart = new Chart(ctx, {type: 'line', data: speedData, options: options2});
});

