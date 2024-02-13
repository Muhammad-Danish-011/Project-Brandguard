import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import ReactApexChart from 'react-apexcharts';
import { Box, Typography } from '@mui/material';
import { useTheme } from '@mui/material/styles'; // Import useTheme from Material-UI

const areaChartOptions = {
  chart: {
    height: 500,
    type: 'area',
    toolbar: {
      show: false
    }
  },
  dataLabels: {
    enabled: false
  },
  stroke: {
    curve: 'smooth',
    width: 2
  },
  grid: {
    strokeDashArray: 0
  },
  xaxis: {
    type: 'category' // Set x-axis type to category
  },
  tooltip: {
    x: {
      formatter: function(val) { // Customize tooltip to display date-time
        return new Date(val).toLocaleString(); // Format date-time using toLocaleString
      }
    }
  }
};
const IncomeAreaChart = ({ screenshotPercentage, scrapingPercentage }) => {
  const theme = useTheme();
  const { secondary } = theme.palette.text;
  const line = theme.palette.divider;

  const [options, setOptions] = useState(areaChartOptions);
  const [series, setSeries] = useState([]);

  useEffect(() => {
    setOptions((prevState) => ({
      ...prevState,
      colors: ['#007bff', '#87CEEB', '#FF5733'], // Adjust colors to complement white and sky blue
      xaxis: {
        categories: ['Screenshot', 'Scraping'],
        labels: {
          style: {
            colors: [secondary],
            fontWeight: 'bold'
          }
        },
        axisBorder: {
          show: true,
          color: line // Adjust x-axis line color
        }
      },
      yaxis: {
        labels: {
          style: {
            colors: [secondary],
            fontWeight: 'bold'
          }
        }
      },
      grid: {
        borderColor: line
      },
      tooltip: {
        theme: 'light'
      }
    }));
    const formattedScreenshotPercentage = `${screenshotPercentage.toFixed(2)}%`;
    const formattedScrapingPercentage = `${scrapingPercentage.toFixed(2)}%`;
    setSeries([
      {
        name: 'Screenshot',
        type: 'line',
        data: [formattedScreenshotPercentage, 0],
        strokeWidth: 3, // Increase line thickness
        dashArray: 0, // No dash style
        markers: {
          size: 6, // Increase marker size
          strokeWidth: 0, // No marker border
          fillColors: ['#0047AB'], // Marker fill color
          strokeColors: ['#fff'] // Marker border color
        },
        color: '#0047AB', // Line color for screenshot
      },
      {
        name: 'Scraping',
        type: 'line',
        data: [formattedScrapingPercentage, 0],
        strokeWidth: 3, // Increase line thickness
        dashArray: 5, // No dash style
        markers: {
          size: 6, // Increase marker size
          strokeWidth: 0, // No marker border
          fillColors: ['#D50000'], // Marker fill color
          strokeColors: ['#fff'] // Marker border color
        },
        color: '#D50000', // Line color for scraping
      }
    ]);
    
  }, [screenshotPercentage, scrapingPercentage, theme, secondary, line]);
  
  return (
    <>
      <Box sx={{ p: 6, bgcolor: '#E6F7FF', borderRadius: 0 }}>
        <Typography variant="h3" sx={{ mb: 4 }}>GRAPHICAL REPRESENTATION:</Typography>
        <ReactApexChart options={options} series={series} type="area" height={500} />
      </Box>
    </>
  );
};



IncomeAreaChart.propTypes = {
  screenshotPercentage: PropTypes.number.isRequired,
  scrapingPercentage: PropTypes.number.isRequired
};

export default IncomeAreaChart;
