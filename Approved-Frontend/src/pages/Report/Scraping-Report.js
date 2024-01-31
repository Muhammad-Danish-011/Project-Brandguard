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
  { id: "website", align: "left", disablePadding: false, label: "Websites" },
  {
    id: "MatchingPercentage",
    align: "left",
    disablePadding: false,
    label: "Matching Percentage %",
  },
  {
    id: "screenshotPosition",
    align: "left",
    disablePadding: false,
    label: "Screenshot Position",
  },
  {
    id: "AdVisibility",
    align: "left",
    disablePadding: false,
    label: "Ad Visibility %",
  },
];

const mockApiData = [
  {
    campaignName: "Campaign 1",
    campaignId: 123,
    startDate: "2024-01-01",
    endDate: "2024-02-01",
    websites: "www.daraz.pk",
    screenshotPosition: "Top Left",
    AdVisibility: 80,
    MatchingPercentage: 75,
  },
  {
    campaignName: "Campaign 2",
    campaignId: 124,
    startDate: "2024-01-01",
    endDate: "2024-02-01",
    websites: "www.amazon.com",
    screenshotPosition: "Top Right",
    AdVisibility: 75,
    MatchingPercentage: 75,
  },
  // ... (other data entries)
];


export default function CampaignTable() {
  const [order, setOrder] = useState("asc");
  const [orderBy, setOrderBy] = useState("campaignName");
  const [data, setData] = useState([]);
  const [selectedCampaign, setSelectedCampaign] = useState("");
  const [selectedReportType, setSelectedReportType] = useState("screenshot");

  const navigate = useNavigate();

  useEffect(() => {
    setData(() => {
      if (selectedReportType === "none") {
        return mockApiData;
      } else if (!selectedCampaign) {
        return mockApiData;
      } else if (selectedCampaign) {
        return mockApiData.filter((item) => item.campaignId === selectedCampaign);
      } else {
        return [];
      }
    });
  }, [selectedCampaign, selectedReportType]);

  const handleRequestSort = (property) => {
    const isAsc = orderBy === property && order === "asc";
    setOrder(isAsc ? "desc" : "asc");
    setOrderBy(property);
  };

  const handleCampaignChange = (event) => {
    setSelectedCampaign(event.target.value);
  };

  const handleReportTypeChange = (event) => {
    setSelectedReportType(event.target.value);
  };

  function descendingComparator(a, b, orderBy) {
    if (b[orderBy] < a[orderBy]) {
      return -1;
    }
    if (b[orderBy] > a[orderBy]) {
      return 1;
    }
    return 0;
  }

  function getComparator(order, orderBy) {
    return order === "desc"
      ? (a, b) => descendingComparator(a, b, orderBy)
      : (a, b) => -descendingComparator(a, b, orderBy);
  }

  function stableSort(array, comparator) {
    const stabilizedThis = array.map((el, index) => [el, index]);
    stabilizedThis.sort((a, b) => {
      const order = comparator(a[0], b[0]);
      if (order !== 0) {
        return order;
      }
      return a[1] - b[1];
    });
    return stabilizedThis.map((el) => el[0]);
  }

  const filteredHeadCells = headCells.filter((headCell) => {
    if (selectedReportType === "screenshot") {
      return (
        headCell.id === "website" ||
        headCell.id === "endDate" ||
        headCell.id === "startDate" ||
        headCell.id === "campaignName" ||
        headCell.id === "campaignId" ||
        headCell.id === "screenshotPosition" ||
        headCell.id === "AdVisibility"
      );
    } else if (selectedReportType === "scraping") {
      return (
        headCell.id === "website" ||
        headCell.id === "endDate" ||
        headCell.id === "startDate" ||
        headCell.id === "campaignName" ||
        headCell.id === "campaignId" ||
        headCell.id === "MatchingPercentage"
      );
    } else {
      return true;
    }
  });

  return (
    <Box>
      <Typography variant="h2" className="header">
        {selectedReportType === "screenshot"
          ? "Screenshot Report"
          : selectedReportType === "scraping"
          ? "Scraping Report"
          : "Report"}
      </Typography>

      <FormControl>
        <Select
          value={selectedCampaign}
          onChange={handleCampaignChange}
          displayEmpty
        >
          <MenuItem value="">Select Campaign</MenuItem>
          {mockApiData.map((item) => (
            <MenuItem key={item.campaignId} value={item.campaignId}>
              {item.campaignName}
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      <FormControl>
        <Select
          value={selectedReportType}
          onChange={handleReportTypeChange}
          displayEmpty
        >
          <MenuItem value="">Select Report Type</MenuItem>
          <MenuItem value="screenshot">Screenshot Report</MenuItem>
          <MenuItem value="scraping">Scraping Report</MenuItem>
        </Select>
      </FormControl>

      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              {filteredHeadCells.map((headCell) => (
                <TableCell
                  key={headCell.id}
                  align={headCell.align}
                  padding={headCell.disablePadding ? "none" : "normal"}
                >
              <Typography
  variant="subtitle3"
  fontWeight="bold"
  color="primary"
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
            {stableSort(data, getComparator(order, orderBy)).map((row, index) => (
              <TableRow key={index}>
                {selectedReportType === "scraping" && (
                  <>
                    <TableCell>{row.campaignId}</TableCell>
                    <TableCell>{row.campaignName}</TableCell>
                    <TableCell>{row.startDate}</TableCell>
                    <TableCell>{row.endDate}</TableCell>
                    <TableCell>{row.websites}</TableCell>
                    <TableCell>{row.MatchingPercentage}</TableCell>
                  </>
                )}

                {selectedReportType === "screenshot" && (
                  <>
                    <TableCell>{row.campaignId}</TableCell>
                    <TableCell>{row.campaignName}</TableCell>
                    <TableCell>{row.startDate}</TableCell>
                    <TableCell>{row.endDate}</TableCell>
                    <TableCell>{row.websites}</TableCell>
                    <TableCell>{row.screenshotPosition}</TableCell>
                    <TableCell>{row.AdVisibility}</TableCell>
                  </>
                )}

                {selectedReportType === "" && (
                  <>
                    <TableCell>{row.campaignId}</TableCell>
                    <TableCell>{row.campaignName}</TableCell>
                    <TableCell>{row.startDate}</TableCell>
                    <TableCell>{row.endDate}</TableCell>
                    <TableCell>{row.websites}</TableCell>
                    <TableCell>{row.MatchingPercentage}</TableCell>
                    <TableCell>{row.screenshotPosition}</TableCell>
                    <TableCell>{row.AdVisibility}</TableCell>
                  </>
                )}

                {/* Add a button in each row to navigate to details page */}
                <TableCell>
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={() => navigate(`/details/${row.campaignId}`)}
                  >
                    View Details
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>

  
  

  );
}
