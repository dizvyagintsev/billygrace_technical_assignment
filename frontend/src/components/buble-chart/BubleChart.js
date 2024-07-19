import React from 'react';
import Chart from 'react-apexcharts';

const bubbleChartData = {
  series: [
    {
      name: 'Product1',
      data: [
        [100, 200, 20],
        [120, 100, 30],
        [170, 300, 40],
        [140, 250, 50],
        [150, 400, 60],
        [110, 280, 70],
      ],
    },
  ],
  options: {
    title: {
      text: 'Product Sales Bubble Chart',
      align: 'left',
    },
    xaxis: {
      tickAmount: 12,
      type: 'category',
    },
    yaxis: {
      max: 500,
    },
  },
};

export default function BubbleChartComponent() {
  return (
    <div id="chart">
      <Chart options={bubbleChartData.options} series={bubbleChartData.series} type="bubble" height={350} />
    </div>
  );
}
