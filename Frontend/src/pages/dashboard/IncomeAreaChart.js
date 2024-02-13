import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import ReactApexChart from 'react-apexcharts';
import { Box, Typography } from '@mui/material';
import { useTheme } from '@mui/material/styles'; // Import useTheme from Material-UI

const areaChartOptions = {
  chart: {
    height: 550,
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
      colors: [theme.palette.primary.main, '#FF5733'], // Additional color for line
      xaxis: {
        categories: ['Screenshot', 'Scraping'], // Categories for screenshot and scraping
        labels: {
          style: {
            colors: [secondary],
            fontWeight: 'bold'
          }
        },
        axisBorder: {
          show: true,
          color: line
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
        data: [formattedScreenshotPercentage]
      },
      {
        name: 'Scraping',
        data: [formattedScrapingPercentage]
      },
      {
        name: 'Threshold', // Add a line for threshold
        type: 'line', // Set type to line
        data: [formattedScreenshotPercentage, formattedScrapingPercentage], // Define data points for the line
        strokeWidth: 2, // Adjust line width
        dashArray: 4, // Set dash style for the line
        markers: {
          size: 5 // Hide markers
        },
        color: '#007bff' // Adjust line color
      }
    ]);
  }, [screenshotPercentage, scrapingPercentage, theme, secondary, line]);

  return (
    <>
      <Box sx={{ p: 2, bgcolor: '#E6F7FF', borderRadius: 1 }}>
        <Typography variant="h3" sx={{ mb: 4 }}>Chart</Typography>
        <ReactApexChart options={options} series={series} type="area" height={450} />
      </Box>
    </>
  );
};


IncomeAreaChart.propTypes = {
  screenshotPercentage: PropTypes.number.isRequired,
  scrapingPercentage: PropTypes.number.isRequired
};

export default IncomeAreaChart;
