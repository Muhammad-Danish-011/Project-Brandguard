import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import ReactApexChart from 'react-apexcharts';
import { Box, Typography, useTheme } from '@mui/material';

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
      colors: [theme.palette.primary.main],
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
      }
    ]);
  }, [screenshotPercentage, scrapingPercentage, theme, secondary, line]);

  return (
    <>
      <Box sx={{ p: 2, bgcolor:'#E6F7FF', borderRadius: 1 }}>
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
