matzore_series = [
    {
        name: 'matzore',
        data: []
    }
];

matzore = Highcharts.chart('matzore', {
    chart: {
        type: 'line',
    },
    title: {
        text: 'Ματζόρε'
    },
    tooltip: {
        formatter: function () {
            return this.series.name + ': <span style="font-size:1.1em; color: ' + this.point.color + '; font-weight: bold">'
                + this.y + '</span><br>'
                + 'Time: <span style="font-size:1em; font-weight: bold">'
                + moment(this.x).format('h:mm') + '</span>'
        }
    },
    xAxis: {
        type: 'datetime',
        labels: {
            formatter: function () {
                return moment(this.value).format('h:mm')
            }
        },
    },
    plotOptions: {
        series: {
            marker: {
                enabled: false
            },
            enableMouseTracking: true

        },
        line: {
            dataLabels: {
                enabled: false
            },
            enableMouseTracking: true
        }
    },

    credits: {
        enabled: false
    },
    series: [
        {
            name: 'Ματζόρε',
            data: [],
            step: true,
        }
    ]
});

function monitor() {
    $.get("get_traffic", function (data) {
        matzore_series[0].data = data.data;
        matzore_series[0].data = matzore_series[0].data.filter(record => record[0] > new Date(timestamp - 10800000));//3 hours
        matzore.series[0].update({data: matzore_series[0].data}, true);
    });

    var socket = io();
    socket.on('connect', function () {
        socket.emit('monitor_traffic', {data: 'I\'m connected!'});
    });
    socket.on('get_traffic', result => {
        let timestamp = Date.now();

        matzore_series[0].data.push(result.data);
        matzore_series[0].data = matzore_series[0].data.filter(record => record[0] > new Date(timestamp - 10800000));//3 hours

        matzore.series[0].update({data: matzore_series[0].data}, true);

        //--Title
        let matzore_title = `Ματζόρε: ${result.data[1]} ακροατές`;
        matzore.setTitle({text: matzore_title});
    });
}

monitor();