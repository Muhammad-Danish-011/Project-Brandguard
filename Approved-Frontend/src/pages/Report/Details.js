import React, { useState, useEffect } from "react";
import { Button } from "@mui/material";

const DetailPage = ({ campaignId }) => {
  const [campaignDetails, setCampaignDetails] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/screenshot_report/${campaignId}`);
        
        if (!response.ok) {
          throw new Error(`Failed to fetch data. Status: ${response.status}`);
        }

        // Check if the response is JSON
        const contentType = response.headers.get("content-type");
        if (!contentType || !contentType.includes("application/json")) {
          // Handle non-JSON response
          const text = await response.text();
          console.error("Non-JSON response:", text);
          throw new Error("Invalid response format");
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

  const handleScrapeDetails = () => {
    // Implement scraping logic here
    console.log('Scraping details...');
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      <div style={{ marginBottom: '10px' }}>
        <Button onClick={handleScrapeDetails}>Scraping Details</Button>
      </div>
      <h2>Details Page for Campaign {campaignId}</h2>
      {campaignDetails && (
        <div>
          {/* Display campaign details based on the received data */}
          <p>Campaign Name: {campaignDetails.campaignName}</p>
          <p>Start Date: {campaignDetails.startDate}</p>
          {/* Add more details as needed */}
        </div>
      )}
    </div>
  );
};

export default DetailPage;
