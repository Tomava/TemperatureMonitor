import React from 'react';
import { Line } from 'react-chartjs-2';
import { Chart, registerables } from 'chart.js';
import 'chartjs-adapter-date-fns';
import zoomPlugin from 'chartjs-plugin-zoom';

// Register the necessary adapters and controllers
Chart.register(...registerables, zoomPlugin);

const LineGraph = ({ data }) => {
  const insideData = data.InsideData
  const outsideData = data.OutsideData

  const timestamps = insideData.map((point) => new Date(point.time));
  const insideTemperatures = insideData.map((point) => point.temperature);
  const outsideTemperatures = outsideData.map((point) => point.temperature);

  const chartData = {
    labels: timestamps,
    datasets: [
      {
        label: 'Inside',
        data: insideTemperatures,
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
        borderColor: 'rgb(255, 99, 132)',
        borderWidth: 1,
      },
      {
        label: 'Outside',
        data: outsideTemperatures,
        backgroundColor: 'rgba(53, 162, 235, 0.5)',
        borderColor: 'rgb(53, 162, 235)',
        borderWidth: 1,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: true,
    scales: {
      x: {
        type: 'time',
        time: {
          unit: 'day',
        },
        display: true,
        ticks: {
          major: {
            enabled: true,
          },
        },
      },
      y: {
        display: true,
        ticks: {
          beginAtZero: true,
        },
      },
    },
    plugins: {
      zoom: {
        zoom: {
          wheel: {
            enabled: true,
          },
          pinch: {
            enabled: true,
          },
          mode: 'xy',
        },
        pan: {
          enabled: true,
          mode: 'xy',
        },
      },
    },
  };

  return (
    <div style={{ width: '100%', height: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
      <div style={{ width: '80%', height: '80%' }}>
        <Line data={chartData} options={chartOptions} />
      </div>
    </div>
  );
};

export default LineGraph;
