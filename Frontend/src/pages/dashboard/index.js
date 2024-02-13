import React, { useState, useEffect } from 'react';
import { Grid, Stack, Typography, Select, MenuItem, Box, FormControl} from '@mui/material';
import MainCard from 'components/MainCard';
import IncomeAreaChart from './IncomeAreaChart';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import AnalyticEcommerce from 'components/cards/statistics/AnalyticEcommerce';


const DashboardDefault = () => {
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

  const handleCampaignChange = (event) => {
    const selectedValue = event.target.value;
    setSelectedCampaign(selectedValue);
    // Find the selected campaign data from the campaigns list
    const selectedCampaignData = campaigns.find(campaign => campaign.CampaignID === selectedValue);
    setData(selectedCampaignData);
  };

  return (
    <Grid container rowSpacing={4.5} columnSpacing={2.75}>
       <Grid container rowSpacing={4.5} columnSpacing={2.75}>
      row 1
      <Grid item xs={12} sx={{ mb: 1.25 }}>
        <Typography variant="h3">Dashboard</Typography>
      </Grid>
      {data && (
  <>
    {/* <Grid item xs={12} sm={6} md={4} lg={3} sx={{ bgcolor: '#B2EBF2', borderRadius: 1, p: 1 }}>
      <AnalyticEcommerce title="Campaign ID" count={data.CampaignID} />
    </Grid>
    <Grid item xs={12} sm={6} md={4} lg={3} sx={{ bgcolor: '#B2EBF2', borderRadius: 1, p: 1 }}>
      <AnalyticEcommerce title="Campaign Name" count={data.CampaignName} />
    </Grid> */}
    <Grid item xs={12} sm={6} md={4} lg={3} sx={{ bgcolor: '#E6F7FF', borderRadius: 1, p:6 }}>
      <AnalyticEcommerce title="Start Date" count={data.StartDate} />
    </Grid>
    <Grid item xs={12} sm={6} md={4} lg={3} sx={{ bgcolor: '#E6F7FF', borderRadius: 1, p: 6 }}>
      <AnalyticEcommerce title="End Date" count={data.EndDate} />
    </Grid>
    <Grid item xs={12} sm={6} md={4} lg={3} sx={{ bgcolor: '#E6F7FF', borderRadius: 1, p: 6 }}>
      <AnalyticEcommerce title="Screenshot Percentage" count={`${data.Found_Status_Screenshot.toFixed(2)}%`} />
    </Grid>
    <Grid item xs={12} sm={6} md={4} lg={3} sx={{ bgcolor: '#E6F7FF', borderRadius: 1, p: 6 }}>
      <AnalyticEcommerce title="Scraping Percentage" count={`${data.Found_Status_Scraping.toFixed(2)}%`} />
    </Grid>
  </>
)}


      <Grid item md={8} sx={{ display: { sm: 'none', md: 'block', lg: 'none' } }} />

    
      <Grid item xs={12}>
        <FormControl  sx={{ display: 'flex', justifyContent: 'center' }}>
          <Select
            value={selectedCampaign}
            onChange={handleCampaignChange}
            displayEmpty
            color='primary'
            sx={{ bgcolor: '#B2EBF2', display: 'flex', justifyContent: 'center'}}
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
              <IncomeAreaChart 
                screenshotPercentage={data.Found_Status_Screenshot} 
                scrapingPercentage={data.Found_Status_Scraping} 
              />
            ) : (
              <Typography variant="h4">Please select campiagn for graph.</Typography>
            )}
          </Box>
        </MainCard>
      </Grid>
    </Grid>
    </Grid>
  );
};

export default DashboardDefault;
