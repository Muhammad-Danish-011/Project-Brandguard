import { useEffect, useState } from 'react';
import ReactApexChart from 'react-apexcharts';
import { useTheme } from '@mui/material/styles';
import { Box, Typography } from '@mui/material';

const BarChart = ({ screenshotPercentage, scrapingPercentage }) => {
  const theme = useTheme();
  const { secondary } = theme.palette.text;
  const info = theme.palette.info.light;

  // Update the series data with income percentages
  const [series, setSeries] = useState([
    {
      data: [screenshotPercentage, scrapingPercentage]
    }
  ]);

  const [options, setOptions] = useState({
    chart: {
      type: 'bar',
      height: 365,
      toolbar: {
        show: false
      }
    },
    plotOptions: {
      bar: {
        columnWidth: '50%', // Adjust the width of the bars
        borderRadius: 4,
        horizontal: true // Display bars horizontally
      }
    },
    dataLabels: {
      enabled: false
    },
    xaxis: {
      categories: ['Screenshot', 'Scraping'], // Updated categories for income types
      axisBorder: {
        show: false
      },
      axisTicks: {
        show: false
      },
      labels: {
        formatter: function(val) {
          return `${val}%`; // Format X-axis labels as percentages
        }
      }
    },
    yaxis: {
      labels: {
        formatter: function(val) {
          return `${val}%`; // Format Y-axis labels as percentages
        }
      }
    },
    grid: {
      show: false
    }
  });

  useEffect(() => {
    setSeries([
      {
        data: [screenshotPercentage, scrapingPercentage]
      }
    ]);
  }, [screenshotPercentage, scrapingPercentage]);

  return (
    <div id="chart">
      <Box sx={{ p: 4, bgcolor: '#E6F7FF', borderRadius: 0 }}>
        <Typography variant="h3" sx={{ mb: 4 }}>BAR CHART REPRESENTATION:</Typography>
        <ReactApexChart options={options} series={series} type="bar" height={365} />
      </Box>
    </div>
  );
};

export default BarChart;
