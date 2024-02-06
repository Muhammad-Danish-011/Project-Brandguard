import React, { useState, useEffect } from 'react';
import { Grid, Stack, Typography, Select, MenuItem, Box } from '@mui/material';
import MainCard from 'components/MainCard';
import IncomeAreaChart from './IncomeAreaChart';
import axios from 'axios';
import { useParams } from 'react-router-dom';

const DashboardDefault = () => {
  const [reportType, setReportType] = useState('screenshot');
  const [data, setData] = useState(null);
  const { campaignId } = useParams();

  useEffect(() => {
    const fetchData = async () => {
      try {
        let response;
        if (reportType === 'screenshot') {
          response = await axios.get(`http://127.0.0.1:5000/screenshot_report/18`);
        } else if (reportType === 'scraping') {
          response = await axios.get(`http://127.0.0.1:5000/scraping_report/18`);
        }
        setData(response.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, [reportType, campaignId]);

  return (
    <Grid container rowSpacing={4.5} columnSpacing={2.75}>
      <Grid item xs={12}>
        <Stack direction="row" spacing={2} alignItems="center">
          <Typography variant="h5">Report Type:</Typography>
          <Select
            value={reportType}
            onChange={(e) => setReportType(e.target.value)}
          >
            <MenuItem value="screenshot">Screenshot</MenuItem>
            <MenuItem value="scraping">Scraping</MenuItem>
          </Select>
        </Stack>
      </Grid>

      <Grid item xs={12}>
        <MainCard content={false}>
          <Box sx={{ pt: 1, pr: 2 }}>
            {data && <IncomeAreaChart data={data.AdPositions || data.ScrapeImageStatus} />}
          </Box>
        </MainCard>
      </Grid>
    </Grid>
  );
};

export default DashboardDefault;
