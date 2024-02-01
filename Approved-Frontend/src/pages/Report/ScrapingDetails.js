import React, { useState, useEffect } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from "@mui/material";
import { useParams } from "../../../node_modules/react-router-dom/dist/index";

const ScrapingDetails = () => {
 
  const [campaignDetails, setCampaignDetails] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const {campaignId}=useParams();
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(
          `http://127.0.0.1:5000/scraping_report/${campaignId}`
        );

        if (!response.ok) {
          throw new Error(
            `Failed to fetch data. Status: ${response.status}`
          );
        }

        const data = await response.json();
        setCampaignDetails(data);
        setLoading(false);
      } catch (error) {
        setError(error.message);
        setLoading(false);
      }
    };

    fetchData();
  }, [campaignId]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      <h2>Scraping Report for Campaign {campaignId}</h2>
      {campaignDetails ? (
        <div>
          <TableContainer component={Paper}>
            <Table style={{  backgroundColor: '#E3F2FD', color: '#1976D2' }}>
              <TableHead>
              <TableRow style={{ backgroundColor: '#BBDEFB', color: '#1976D2' }}>
                  <TableCell>Website URL</TableCell>
                  <TableCell>Campaign ID</TableCell>
                  <TableCell>Campaign Name</TableCell>
                  <TableCell>Scrape Image Status</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                <TableRow>
                  <TableCell>{campaignDetails.WebsiteURL}</TableCell>
                  <TableCell>{campaignDetails.CampaignID}</TableCell>
                  <TableCell>{campaignDetails.CampaignName}</TableCell>
                  </TableRow>
                  <TableRow>
                  <TableCell></TableCell>
                  <TableCell></TableCell>
                  <TableCell></TableCell>
                  <TableCell>
                    {campaignDetails.ScrapeImageStatus.length > 0 ? (
                      <ul>
                        {campaignDetails.ScrapeImageStatus.map(
                          (scrapeStatus, index) => (
                            <li key={index}>
                              {scrapeStatus.DateTime} - {scrapeStatus.Found_Status}
                            </li>
                          )
                        )}
                      </ul>
                    ) : (
                      "No Scrape Image Status"
                    )}
                  </TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </TableContainer>
        </div>
      ) : (
        <div>No campaign details available.</div>
      )}
    </div>
  );
};

export default ScrapingDetails;
