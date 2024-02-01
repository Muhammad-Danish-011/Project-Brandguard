import React, { useState, useEffect } from "react";
import {
  Box,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  FormControl,
  Select,
  MenuItem,
  Button,
  CircularProgress,
} from "@mui/material";

import { useNavigate } from "react-router-dom";

const headCells = [
  {
    id: "campaignId",
    align: "left",
    disablePadding: false,
    label: "Campaign Id",
  },
  {
    id: "campaignName",
    align: "left",
    disablePadding: false,
    label: "Campaign Name",
  },
  {
    id: "startDate",
    align: "left",
    disablePadding: false,
    label: "Start Date",
  },
  { id: "endDate", align: "left", disablePadding: false, label: "End Date" },
  { id: "websites", align: "left", disablePadding: false, label: "Websites" },
  {
    id: "Found_Status_Screenshot",
    align: "left",
    disablePadding: false,
    label: "Found Status Screenshot",
  },
  {
    id: "Found_Status_Scraping",
    align: "left",
    disablePadding: false,
    label: "Found Status Scraping",
  },
  // {
  //   id: "AdVisibility",
  //   align: "left",
  //   disablePadding: false,
  //   label: "Ad Visibility %",
  // },
];

// ... (imports remain unchanged)

export default function CampaignTable() {
  const [order, setOrder] = useState("asc");
  const [orderBy, setOrderBy] = useState("campaignName");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedCampaign, setSelectedCampaign] = useState("");

  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await fetch("http://127.0.0.1:5000/general_report");
        const result = await response.json();
        setData(result);
        console.log(result);
        setError(null);
      } catch (error) {
        setError("Error fetching data from the API");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleRequestSort = (property) => {
    const isAsc = orderBy === property && order === "asc";
    setOrder(isAsc ? "desc" : "asc");
    setOrderBy(property);
  };

  const handleCampaignChange = (event) => {
    setSelectedCampaign(event.target.value);
  };

  return (
    <Box>
      <Typography variant="h2" className="header">
        All Campaigns Report
      </Typography>

      {loading && <CircularProgress />}

      {error && (
        <Typography variant="body1" color="error">
          {error}
        </Typography>
      )}

      {!loading && !error && data !== null && data.length > 0 && (
        <>
          <FormControl>
            <Select
              value={selectedCampaign}
              onChange={handleCampaignChange}
              displayEmpty
            >
              <MenuItem value="">Select Campaign</MenuItem>
              {data.map((item) => (
                <MenuItem key={item.CampaignID} value={item.CampaignID}>
                  {item.CampaignName}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <TableContainer>
            <Table  style={{  backgroundColor: '#E3F2FD', color: '#1976D2' }}>
              <TableHead style={{ backgroundColor: '#BBDEFB', color: '#1976D2' }}>
              <TableRow >
                  {headCells.map((headCell) => (
                    <TableCell
                      key={headCell.id}
                      align={headCell.align}
                      padding={headCell.disablePadding ? "none" : "normal"}
                    >
                      <Typography
                        variant="subtitle3"
                        fontWeight="bold"
                        
                        onClick={() => handleRequestSort(headCell.id)}
                        style={{ cursor: "pointer" }}
                      >
                        {headCell.label}
                      </Typography>
                    </TableCell>
                  ))}
                </TableRow>
              </TableHead>
              <TableBody>
                {data
                  .filter((item) =>
                    selectedCampaign
                      ? item.CampaignID === selectedCampaign
                      : true
                  )
                  .map((row, index) => (
                    <TableRow key={index}>
                      <TableCell>{row.CampaignID}</TableCell>
                      <TableCell>{row.CampaignName}</TableCell>
                      <TableCell>{row.StartDate}</TableCell>
                      <TableCell>{row.EndDate}</TableCell>

                      <TableCell>
                        {row.WebsiteURL.map((url) => (
                          <div key={url}>{url}</div>
                        ))}
                      </TableCell>
                      <TableCell>{row.Found_Status_Scraping}</TableCell>
                      <TableCell>{row.Found_Status_Screenshot}</TableCell>

                      {/* <TableCell>{row.MatchingPercentage}</TableCell>
                      <TableCell>{row.ScreenshotPosition}</TableCell>
                      <TableCell>{row.AdVisibility}</TableCell> */}
                      <TableCell>
                        <Button
                          variant="contained"
                          color="primary"
                          onClick={() => {
                            navigate(`/details/${row.CampaignID}`);
                        
                              
                             
                          }}
                        >
                          View Details
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
              </TableBody>
            </Table>
          </TableContainer>
        </>
      )}
    </Box>
  );
}
