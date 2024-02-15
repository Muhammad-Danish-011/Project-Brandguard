import PropTypes from 'prop-types';
import { useState, useEffect } from 'react';
import ReactApexChart from 'react-apexcharts';
import { Box, Typography } from '@mui/material';
import { useTheme } from '@mui/material/styles';

const IncomeAreaChart = ({ screenshotPercentage, scrapingPercentage }) => {
  const theme = useTheme();
  const { secondary } = theme.palette.text;
  const line = theme.palette.divider;

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
      lineCap: 'round',
      width: 4,
      colors: [theme.palette.primary.main, theme.palette.primary[700]] 
    },
    grid: {
      strokeDashArray: 0,
 
        borderColor: line
      
    },
    fill: {
      type: 'gradient',
      gradient: {
        shade: 'dark',
        type: 'vertical', 
        shadeIntensity: 10,
        opacityFrom: 100,
        opacityTo: 100,
        gradientToColors: ['#0047AB', '#D50000'],
        stops: [0, 90, 100]
      }
    },
    xaxis: {
      type: 'category'
    },
    yaxis: {
      max: 100 // Set maximum value of y-axis to 100
    },
    tooltip: {
      theme: 'light',
      x: {
        formatter: function(val) {
          return new Date(val).toLocaleString();
        }
      }
    }
  };

  const [options, setOptions] = useState(areaChartOptions);
  const [series, setSeries] = useState([]);

  useEffect(() => {
    const formattedScreenshotPercentage = `${screenshotPercentage.toFixed(2)}%`;
    const formattedScrapingPercentage = `${scrapingPercentage.toFixed(2)}%`;



    setOptions((prevState) => ({
      ...prevState,
      xaxis: {
        ...prevState.xaxis,
        categories: ['Screenshot', 'Scraping']
      }
    }));

    setOptions((prevState) => ({
      ...prevState,
      fill: {
        ...prevState.fill,
        gradientToColors: ['#0047AB', '#D50000'] // Update gradient colors based on data
      }
    }));
    setSeries([
      {
        name: 'Screenshot',
        type: 'line',
        data: [formattedScreenshotPercentage, 0],
        strokeWidth: 50,
        dashArray: 0,
        markers: {
          size: 6,
          strokeWidth: 0,
          fillColors: [theme.palette.primary.main],
          strokeColors: ['#fff']
        },
        color: theme.palette.primary.main
      },
      {
        name: 'Scraping',
        type: 'line',
        data: [formattedScrapingPercentage, 0],
        strokeWidth: 50,
        dashArray: 5,
        markers: {
          size: 6,
          strokeWidth: 0,
          fillColors: [theme.palette.primary[700]],
          strokeColors: ['#fff']
        },
        color: theme.palette.primary[700]
      }
    ]);
    
  }, [screenshotPercentage, scrapingPercentage, theme]);

  return (
    <>
      <Box sx={{ p: 6, bgcolor: '#e0ebeb', borderRadius: 0 }}>
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
