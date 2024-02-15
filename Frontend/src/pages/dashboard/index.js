import { useState, useEffect } from 'react';
import {
  Grid,
  Typography,
  Select,
  MenuItem,
  FormControl,
  Box
} from "@mui/material";
import MainCard from "components/MainCard";
import BarChart from "./BarChart";
import AreaChart from "./AreaChart";
import axios from "axios";
import { useParams } from "react-router-dom";
import AnalyticEcommerce from "components/cards/statistics/AnalyticEcommerce";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const DashboardDefault = () => {
  const [data, setData] = useState(null);
  const { campaignId } = useParams();
  const [selectedCampaign, setSelectedCampaign] = useState("");
  const [campaigns, setCampaigns] = useState([]);
  const [totalCampaigns, setTotalCampaigns] = useState(0); // State to hold the total number of campaigns
  const [screenshotPercentage, setScreenshotPercentage] = useState(0);
  const [scrapingPercentage, setScrapingPercentage] = useState(0);

  useEffect(() => {
    const fetchCampaigns = async () => {
      try {
        const response = await axios.get(
          "http://127.0.0.1:5000/general_report"
        );
        setCampaigns(response.data);
        setTotalCampaigns(response.data.length); // Set total number of campaigns
      } catch (error) {
        console.error("Error fetching campaigns:", error);
      }
    };

    fetchCampaigns();
  }, []);

  const handleCampaignChange = (event) => {
    const selectedValue = event.target.value;
    setSelectedCampaign(selectedValue);
    // Find the selected campaign data from the campaigns list
    const selectedCampaignData = campaigns.find(
      (campaign) => campaign.CampaignID === selectedValue
    );
    setData(selectedCampaignData);
    setScreenshotPercentage(selectedCampaignData.Found_Status_Screenshot);
    setScrapingPercentage(selectedCampaignData.Found_Status_Scraping);
  };

  // Aggregate data from all campaigns
  const aggregateData = () => {
    const aggregatedData = [];
    // Aggregate data based on date
    campaigns.forEach((campaign) => {
      const startDate = new Date(campaign.StartDate);
      const endDate = new Date(campaign.EndDate);
      const duration = (endDate - startDate) / (1000 * 60 * 60 * 24); // Duration in days
      for (let i = 0; i <= duration; i++) {
        const date = new Date(startDate);
        date.setDate(startDate.getDate() + i);
        const formattedDate = date.toISOString().split('T')[0];
        const existingData = aggregatedData.find((item) => item.date === formattedDate);
        if (existingData) {
          existingData.count++;
        } else {
          aggregatedData.push({ date: formattedDate, count: 1 });
        }
      }
    });
    return aggregatedData;
  };

  return (
    <Box>
      <Grid container spacing={4}>
        <Grid item xs={12}>
          <Typography variant="h2">Dashboard</Typography>
        </Grid>
        <Grid item xs={12}>
          <FormControl sx={{ display: "flex", justifyContent: "center", alignItems: "center", Width: "70%" }}>
            <Select
              value={selectedCampaign}
              onChange={handleCampaignChange}
              displayEmpty
              color="primary"
              sx={{
                bgcolor: "#E0F7FA",
              }}
            >
              <MenuItem value="" disabled>
                Select Campaign
              </MenuItem>
              {campaigns.map((item) => (
                <MenuItem key={item.CampaignID} value={item.CampaignID}>
                  {item.CampaignName}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <br />
          {selectedCampaign === "" && (
            <Typography variant="h4" color="error" display="flex" justifyContent="center" alignItems="center">
              Please select a campaign for individual visibility.
            </Typography>
          )}
        </Grid>
        {/* Display total number of campaigns */}
        <Grid item xs={12} sm={6} md={3}>
          <AnalyticEcommerce title="Total Campaigns" count={totalCampaigns} />
        </Grid>
        {/* Render overall data graph when no campaign is selected */}
        {selectedCampaign === "" && (
          <Grid item xs={12}>
            <MainCard content={false}>
              <Box sx={{ pt: 1, pr: 2 }}>
                <Typography variant="h4">
                  Overall Campaign Trend
                </Typography>
                {/* Render LineChart with aggregated data */}
                <ResponsiveContainer width="100%" height={400}>
                  <LineChart
                    data={aggregateData()}
                    margin={{ top: 5, right: 20, left: 10, bottom: 5 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="count" stroke="#8884d8" />
                  </LineChart>
                </ResponsiveContainer>
              </Box>
            </MainCard>
          </Grid>
        )}
        {/* Render individual campaign data if a campaign is selected */}
        {data && selectedCampaign !== "" && (
          <>
            <Grid item xs={12} sm={6} md={3}>
              <AnalyticEcommerce title="Start Date" count={data.StartDate} />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <AnalyticEcommerce title="End Date" count={data.EndDate} />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <AnalyticEcommerce
                title="Screenshot Percentage"
                count={`${data.Found_Status_Screenshot.toFixed(2)}%`}
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <AnalyticEcommerce
                title="Scraping Percentage"
                count={`${data.Found_Status_Scraping.toFixed(2)}%`}
              />
            </Grid>
            {/* Include the BarChart component */}
            <Grid item xs={12}>
              <MainCard content={false}>
                <Box sx={{ pt: 1, pr: 2 }}>
                  {data !== null ? (
                    <BarChart
                      screenshotPercentage={screenshotPercentage}
                      scrapingPercentage={scrapingPercentage}
                    />
                  ) : (
                    <Typography variant="h4">
                      Please select a campaign for the graph.
                    </Typography>
                  )}
                </Box>
              </MainCard>
            </Grid>
            {/* Include the AreaChart component */}
            <Grid item xs={12}>
              <MainCard content={false}>
                <Box sx={{ pt: 1, pr: 2 }}>
                  {data !== null ? (
                    <AreaChart
                      screenshotPercentage={screenshotPercentage}
                      scrapingPercentage={scrapingPercentage}
                    />
                  ) : (
                    <Typography variant="h4">
                      Please select a campaign for the graph.
                    </Typography>
                  )}
                </Box>
              </MainCard>
            </Grid>
          </>
        )}
      </Grid>
    </Box>
  );
};

export default DashboardDefault;
