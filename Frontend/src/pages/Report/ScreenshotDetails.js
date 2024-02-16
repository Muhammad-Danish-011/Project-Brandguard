import { useState, React, useEffect } from "react";
import {
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Modal,
  Typography,
} from "@mui/material";
import { useParams } from "react-router-dom";
import { useNavigate } from "react-router-dom";

const DetailPage = () => {
  const { campaignId } = useParams();
  const [campaignDetails, setCampaignDetails] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showScreenshotDetails, setScreenshotDetails] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const navigate = useNavigate();

  const fetchData = async (name) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/${name}/${campaignId}`);

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

  useEffect(() => {
    if (showScreenshotDetails) {
      setCampaignDetails(null);
      fetchData("screenshot_report");
    } else {
      setCampaignDetails(null);
      fetchData("scraping_report");
    }
  }, [showScreenshotDetails]);



  

  const handleCloseModal = () => {
    setSelectedFilePath("");
    setModalOpen(false);
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      <h2>Details Page for Campaign {campaignId}</h2>

      <div>
        <Button
          variant="contained"
          color="primary"
          disabled={showScreenshotDetails}
          onClick={() => {
            setScreenshotDetails(true);
          }}
        >
          Screenshot Details
        </Button>
        <Button
          variant="contained"
          color="primary"
          disabled={!showScreenshotDetails}
          onClick={() => {
            setScreenshotDetails(false);
          }}
        >
          Scraping Details
        </Button>
      </div>

      {showScreenshotDetails ? (
        campaignDetails && (
          <div>
            <h1>Screenshot Details</h1>
            <p>Campaign ID: {campaignDetails.CampaignID}</p>
            <p>Website URL: {campaignDetails.WebsiteURL}</p>
            <p>Campaign Name: {campaignDetails.CampaignName}</p>

            <TableContainer component={Paper}>
              <Table style={{ backgroundColor: "#E3F2FD", color: "#1976D2" }}>
                <TableHead>
                  <TableRow style={{ backgroundColor: "#BBDEFB", color: "#1976D2" }}>
                    <TableCell>Capture Date Time</TableCell>
                    <TableCell>File Path</TableCell>
                    <TableCell>Found Status</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {campaignDetails.AdPositions?.length > 0 ? (
                    campaignDetails.AdPositions?.map(({ Capture_DateTime, FilePath, Found_Status }) => (
                      <TableRow key={Capture_DateTime}>
                        <TableCell>{Capture_DateTime}</TableCell>
                        <TableCell>
                          <Button color="primary" onClick={() => handleFilePathClick(FilePath)}>
                            {FilePath}
                          </Button>
                        </TableCell>
                        <TableCell>{Found_Status}</TableCell>
                      </TableRow>
                    ))
                  ) : (
                    <TableRow>
                      <TableCell>No Screenshots Data</TableCell>
                    </TableRow>
                  )}
                </TableBody>
              </Table>
            </TableContainer>
          </div>
        )
      ) : (
        campaignDetails && (
          <div>
            <h1>Scraping Details</h1>
            <p>Campaign ID: {campaignDetails.CampaignID}</p>
            <p>Website URL: {campaignDetails.WebsiteURL}</p>
            <p>Campaign Name: {campaignDetails.CampaignName}</p>

            <TableContainer component={Paper}>
              <Table style={{ backgroundColor: "#E3F2FD", color: "#1976D2" }}>
                <TableHead>
                  <TableRow style={{ backgroundColor: "#BBDEFB", color: "#1976D2" }}>
                    <TableCell>Capture Date Time</TableCell>
                    <TableCell>Found Status</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {campaignDetails.ScrapeImageStatus?.length > 0 ? (
                    campaignDetails.ScrapeImageStatus?.map(({ DateTime, Found_Status }) => (
                      <TableRow key={DateTime}>
                        <TableCell>{DateTime}</TableCell>
                        <TableCell>{Found_Status}</TableCell>
                      </TableRow>
                    ))
                  ) : (
                    <TableRow>
                      <TableCell>No Scraped Data</TableCell>
                    </TableRow>
                  )}
                </TableBody>
              </Table>
            </TableContainer>
          </div>
        )
      )}

    </div>
  );
};

export default DetailPage;


      {/* {campaignDetails && (
        <div>
          <TableContainer component={Paper}>
            <Table style={{ backgroundColor: '#E3F2FD', color: '#1976D2' }}>
              <TableHead>
                <TableRow style={{ backgroundColor: '#BBDEFB', color: '#1976D2' }}>
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
                          <li key={index}>
                            <div>
                              <strong>Capture Date Time:</strong> {adPosition.Capture_DateTime}
                            </div>
                            <div>
                              <strong>File Path:</strong> {adPosition.FilePath}
                            </div>
                            <div>
                              <strong>Found Status:</strong> {adPosition.Found_Status}
                            </div>
                          </li>
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
      )} */}
   
 
