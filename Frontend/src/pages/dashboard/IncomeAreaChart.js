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
  }
};

const IncomeAreaChart = ({ data }) => {
  const theme = useTheme();
  const { primary, secondary } = theme.palette.text;
  const line = theme.palette.divider;

  const [options, setOptions] = useState(areaChartOptions);
  const [series, setSeries] = useState([]);

  useEffect(() => {
    if (data) {
      setOptions((prevState) => ({
        ...prevState,
        colors: [theme.palette.primary.main],
        xaxis: {
          categories: data.map(({ DateTime }) => DateTime),
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

      const seriesData = Object.keys(data[0])
        .filter(key => key !== 'DateTime')
        .map(key => ({
          name: key,
          data: data.map(item => item[key])
        }));

      setSeries(seriesData);
    }
  }, [data, theme, secondary, line]);

  return (
    <>
      <Box sx={{ p: 2, bgcolor: '#BBDEFB', borderRadius: 1 }}>
        <Typography variant="h3" sx={{ mb: 2 }}> Chart</Typography>
        <ReactApexChart options={options} series={series} type="area" height={450} />
      </Box>
    </>
  );
};

IncomeAreaChart.propTypes = {
  data: PropTypes.arrayOf(
    PropTypes.shape({
      DateTime: PropTypes.string.isRequired,
      Found_Status: PropTypes.string.isRequired
    })
  ).isRequired
};

export default IncomeAreaChart;
