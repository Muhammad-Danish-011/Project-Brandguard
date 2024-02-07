import React, { useState, useEffect } from 'react';
import { Grid, Stack, Typography, Select, MenuItem, Box, FormControl } from '@mui/material';
import MainCard from 'components/MainCard';
import IncomeAreaChart from './IncomeAreaChart';
import axios from 'axios';
import { useParams } from 'react-router-dom';

const DashboardDefault = () => {
  const [reportType, setReportType] = useState('screenshot');
  const [data, setData] = useState(null);
  const { campaignId } = useParams();
  const [selectedCampaign, setSelectedCampaign] = useState("");
  const [campaigns, setCampaigns] = useState([]);

  useEffect(() => {
    const fetchCampaigns = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/general_report');
        setCampaigns(response.data);
      } catch (error) {
        console.error('Error fetching campaigns:', error);
      }
    };

    fetchCampaigns();
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      try {
        let response;
        if (selectedCampaign) {
          if (reportType === 'screenshot') {
            response = await axios.get(`http://127.0.0.1:5000/screenshot_report/${selectedCampaign}`);
          } else if (reportType === 'scraping') {
            response = await axios.get(`http://127.0.0.1:5000/scraping_report/${selectedCampaign}`);
          }
          setData(response.data);
        } else {
          setData(null); 
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, [reportType, selectedCampaign]);

  const handleCampaignChange = (event) => {
    const selectedValue = event.target.value;
    if (!selectedValue) {
      alert('This campaign has no data for graph.');
    } else {
      setSelectedCampaign(selectedValue);
    }
  };

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
        <FormControl>
          <Select
            value={selectedCampaign}
            onChange={handleCampaignChange}
            displayEmpty
          >
            <MenuItem value="">Select Campaign</MenuItem>
            {campaigns.map((item) => (
              <MenuItem key={item.CampaignID} value={item.CampaignID}>
                {item.CampaignName}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Grid>
      <Grid item xs={12}>
        <MainCard content={false}>
          <Box sx={{ pt: 1, pr: 2 }}>
            {data !== null ? (
              <IncomeAreaChart data={data.AdPositions || data.ScrapeImageStatus} />
            ) : (
              <Typography variant="body1">No data available for graph.</Typography>
            )}
          </Box>
        </MainCard>
      </Grid>
    </Grid>
  );
};

export default DashboardDefault;
