import React from 'react';
import Chart from 'react-apexcharts';

const lineChartData = {
  series: [
    {
      name: "Sales",
      data: [400, 300, 200, 278, 189, 239, 349, 200, 300, 400, 500, 600],
    },
  ],
  options: {
    title: {
      text: 'Monthly Sales',
      align: 'left',
    },
    xaxis: {
      categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    },
  },
};

export default function LineChartComponent() {
  return (
    <div id="chart">
      <Chart options={lineChartData.options} series={lineChartData.series} type="line" height={350} />
    </div>
  );
}
