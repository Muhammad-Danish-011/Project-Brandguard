import React from 'react';
import PropTypes from 'prop-types';
import ReactApexChart from 'react-apexcharts';
import { Box, Typography } from '@mui/material';

const IncomeBarChart = ({ data }) => {
  const seriesData = data.map(item => item.ScreenshotFindPercentage);
  const categories = data.map(item => item.DateTime);

  const chartOptions = {
    chart: {
      id: 'income-bar-chart',
      toolbar: {
        show: false
      }
    },
    xaxis: {
      categories: categories
    }
  };

  return (
    <Box sx={{ p: 2, bgcolor: '#BBDEFB', borderRadius: 1 }}>
      <Typography variant="h3" sx={{ mb: 2 }}>Income Distribution</Typography>
      <ReactApexChart options={chartOptions} series={[{ data: seriesData }]} type="bar" height={450} />
    </Box>
  );
};

IncomeBarChart.propTypes = {
  data: PropTypes.arrayOf(
    PropTypes.shape({
      DateTime: PropTypes.string.isRequired,
      ScreenshotFindPercentage: PropTypes.number.isRequired
    })
  ).isRequired
};

export default IncomeBarChart;
