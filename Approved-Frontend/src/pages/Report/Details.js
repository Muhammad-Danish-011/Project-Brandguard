import { useState, React ,useEffect } from "react";
import { Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from "@mui/material";
import { useParams } from "../../../node_modules/react-router-dom/dist/index";

const DetailPage = () => {
  const {campaignId}=useParams();
  const [campaignDetails, setCampaignDetails] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    console.log("campaignId:", campaignId);
    const fetchData = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/screenshot_report/${campaignId}`);
        
        if (!response.ok) {
          throw new Error(`Failed to fetch data. Status: ${response.status}`);
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
      
      <h2>Details Page for Campaign {campaignId}</h2>
      {campaignDetails && (
  <div>
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Website URL</TableCell>
            <TableCell>Campaign ID</TableCell>
            <TableCell>Campaign Name</TableCell>
            <TableCell>Ad Positions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          <TableRow>
            <TableCell>{campaignDetails.WebsiteURL}</TableCell>
            <TableCell>{campaignDetails.CampaignID}</TableCell>
            <TableCell>{campaignDetails.CampaignName}</TableCell>
            <TableCell>
              {campaignDetails.AdPositions.length > 0 ? (
                <ul>
                  {campaignDetails.AdPositions.map((adPosition, index) => (
                    <li key={index}>{adPosition}</li>
                  ))}
                </ul>
              ) : (
                "No Ad Positions"
              )}
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </TableContainer>
  </div>
  
)}   
  <div style={{ marginBottom: '10px' }}>
        <Button variant="contained" color="primary" onClick={() => console.log("Scraping Details")}>
          Scraping Details
        </Button>
      </div> 
</div>
  );
};

export default DetailPage;
