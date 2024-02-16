import { useState, useEffect } from 'react';
import {
  Grid,
  Typography,
  Select,
  MenuItem,
  FormControl,
  Box,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button
} from "@mui/material";
import MainCard from "components/MainCard";
import BarChart from "./BarChart";
import AreaChart from "./AreaChart";
import axios from "axios";
import { useParams } from "react-router-dom";
import AnalyticEcommerce from "components/cards/statistics/AnalyticEcommerce";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Link } from 'react-router-dom';

const DashboardDefault = () => {
  const [data, setData] = useState(null);
  const { campaignId } = useParams();
  const [selectedCampaign, setSelectedCampaign] = useState("");
  const [campaigns, setCampaigns] = useState([]);
  const [totalCampaigns, setTotalCampaigns] = useState(0); // State to hold the total number of campaigns
  const [screenshotPercentage, setScreenshotPercentage] = useState(0);
  const [scrapingPercentage, setScrapingPercentage] = useState(0);
  // const history = useHistory();

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
    const selectedCampaignData = campaigns.find(
      (campaign) => campaign.CampaignID === selectedValue
    );
    setData(selectedCampaignData);
    setScreenshotPercentage(selectedCampaignData?.Found_Status_Screenshot || 0);
    setScrapingPercentage(selectedCampaignData?.Found_Status_Scraping || 0);
  };

  const resetCampaignSelection = () => {
    setSelectedCampaign("");
    setData(null);
    setScreenshotPercentage(0);
    setScrapingPercentage(0);
  };

  // Aggregate data for start dates of campaigns
  const aggregateStartDateData = () => {
    const startDateData = {};

    // Aggregate data based on start dates of campaigns
    campaigns.forEach((campaign) => {
      const startDate = new Date(campaign.StartDate).toISOString().split('T')[0];
      startDateData[startDate] = startDateData[startDate] ? startDateData[startDate] + 1 : 1;
    });

    // Convert data to array format for plotting
    const aggregatedData = Object.entries(startDateData).map(([date, count]) => ({
      date,
      count
    }));

    return aggregatedData;
  };

  // Aggregate data for end dates of campaigns
  const aggregateEndDateData = () => {
    const endDateData = {};

    // Aggregate data based on end dates of campaigns
    campaigns.forEach((campaign) => {
      const endDate = new Date(campaign.EndDate).toISOString().split('T')[0];
      endDateData[endDate] = endDateData[endDate] ? endDateData[endDate] + 1 : 1;
    });

    // Convert data to array format for plotting
    const aggregatedData = Object.entries(endDateData).map(([date, count]) => ({
      date,
      count
    }));

    return aggregatedData;
  };

  return (
    <Box p={4}>
      <Grid container spacing={5}>
        <Grid item xs={12}>
          <Typography variant="h2">Dashboard</Typography>
        </Grid>
        <Grid item xs={12}>
          <FormControl sx={{ display: "flex", width: "70%" }}>
            <Select
              value={selectedCampaign}
              onChange={handleCampaignChange}
              displayEmpty
              color="primary"
              sx={{ bgcolor: "#AFEEEE", width: "70%" }}
            >
              <MenuItem value="">
                No Campaign
              </MenuItem>
              {campaigns.map((item) => (
                <MenuItem key={item.CampaignID} value={item.CampaignID}>
                  {item.CampaignName}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          {/* Error message */}
          {selectedCampaign === "" && (
            <Typography variant="h4" color="error" mt={2}>
              Please select a campaign for individual visibility.
            </Typography>
          )}
          <br />
        </Grid>
        {/* Render overall data graph when no campaign is selected */}
        {selectedCampaign === "" && (
          <Grid container spacing={4}>
            {/* Total Campaigns on top right corner */}
            <Grid item xs={12} display='flex' justifyContent="center" >
              <Grid item>
                <AnalyticEcommerce title="Total Campaigns" count={totalCampaigns} />
              </Grid>
            </Grid>
            <Grid item xs={12} md={6}>
              <Typography variant="h4" display='flex' justifyContent='center' >
                Table
              </Typography>
              <Grid item xs={12}>
                <TableContainer component={Paper}>
                  <Table aria-label="campaign data table" style={{ backgroundColor: "#E3F2FD", color: "#1976D2" }}>
                    <TableHead style={{ backgroundColor: "#BBDEFB" }}>
                      <TableRow>
                        <TableCell>Campaign Name</TableCell>
                        <TableCell>Start Date</TableCell>
                        <TableCell>End Date</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {campaigns.slice(0, 7).map((campaign) => (
                        <TableRow key={campaign.CampaignID}>
                          <TableCell>{campaign.CampaignName}</TableCell>
                          <TableCell>{campaign.StartDate}</TableCell>
                          <TableCell>{campaign.EndDate}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer><br></br>
                <Button
                  variant="contained"
                  color="primary"
                  component={Link}
                  to="/Scraping-Report"
                >
                  View More
                </Button>
              </Grid>
            </Grid>
            {/* Render the LineChart for start dates */}
            <Grid item xs={12} md={6}>
              <Typography variant="h4" display='flex' justifyContent='center'>
                Start Dates Trend
              </Typography>
              <MainCard content={false} sx={{ backgroundColor: '#e0ebeb' }}>
                <Box pt={2} pr={2}>
                  {/* Render LineChart with aggregated data */}
                  <ResponsiveContainer width="100%" height={400}>
                    <LineChart
                      data={aggregateStartDateData()}
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
            {/* Render the LineChart for end dates */}
            <Grid item xs={12} md={6}>
              <Typography variant="h4" display='flex' justifyContent='center'>
                End Dates Trend
              </Typography>
              <MainCard content={false} sx={{ backgroundColor: '#e0ebeb' }}>
                <Box pt={2} pr={2}>
                  {/* Render LineChart with aggregated data */}
                  <ResponsiveContainer width="100%" height={400}>
                    <LineChart
                      data={aggregateEndDateData()}
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
                count={`${screenshotPercentage.toFixed(2)}%`}
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <AnalyticEcommerce
                title="Scraping Percentage"
                count={`${scrapingPercentage.toFixed(2)}%`}
              />
            </Grid>
            <Grid item xs={12}>
              <MainCard content={false}>
                <Box pt={1} pr={2}>
                  <BarChart
                    screenshotPercentage={screenshotPercentage}
                    scrapingPercentage={scrapingPercentage}
                  />
                </Box>
              </MainCard>
            </Grid>
            <Grid item xs={12}>
              <MainCard content={false}>
                <Box pt={1} pr={2}>
                  <AreaChart
                    screenshotPercentage={screenshotPercentage}
                    scrapingPercentage={scrapingPercentage}
                  />
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
