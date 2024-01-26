import React, { useState, useEffect } from "react";
import { Link as RouterLink } from "react-router-dom";
import {
  Box,
  Link,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";

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
  { id: "images", align: "left", disablePadding: false, label: "Images" },
  {
    id: "MatchingPercentage",
    align: "left",
    disablePadding: false,
    label: "Matching Percentage %",
  },
];

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

const mockApiData = [
  {
    campaignName: "Campaign 1",
    campaignId: 123,
    startDate: "2024-01-01",
    endDate: "2024-02-01",
    websites: "www.daraz.pk",
    images: "new.png",
    screenshotPosition: "Top Left",
    MatchingPercentage: 80,
  },
  {
    campaignId: 456,
    campaignName: "Campaign 2",
    startDate: "2024-02-01",
    endDate: "2024-03-01",
    websites: "www.daraz.pk",
    images: "new.png",
    screenshotPosition: "Bottom Right",
    MatchingPercentage: 75,
  },
  {
    campaignId: 789,
    campaignName: "Campaign 3",
    startDate: "2024-03-01",
    endDate: "2024-04-01",
    websites: "www.daraz.pk",
    images: "new.png",
    screenshotPosition: "Top Right",
    MatchingPercentage: 85,
  },
  {
    campaignId: 1011,
    campaignName: "Campaign 4",
    startDate: "2024-04-01",
    endDate: "2024-05-01",
    websites: "www.daraz.pk",
    images: "new.png",
    screenshotPosition: "Bottom Left",
    MatchingPercentage: 90,
  },
  {
    campaignId: 1213,
    campaignName: "Campaign 5",
    startDate: "2024-05-01",
    endDate: "2024-06-01",
    websites: "www.daraz.pk",
    images: "new.png",
    screenshotPosition: "Center",
    MatchingPercentage: 70,
  },
  {
    campaignId: 1415,
    campaignName: "Campaign 6",
    startDate: "2024-06-01",
    endDate: "2024-07-01",
    websites: "www.daraz.pk",
    images: "new.png",
    screenshotPosition: "Top Center",
    MatchingPercentage: 95,
  },
  {
    campaignId: 1617,
    campaignName: "Campaign 7",
    startDate: "2024-07-01",
    endDate: "2024-08-01",
    websites: "www.daraz.pk",
    images: "new.png",
    screenshotPosition: "Bottom Center",
    MatchingPercentage: 60,
  },
  {
    campaignId: 1819,
    campaignName: "Campaign 8",
    startDate: "2024-08-01",
    endDate: "2024-09-01",
    websites: "www.daraz.pk",
    images: "new.png",
    screenshotPosition: "Right Center",
    MatchingPercentage: 75,
  },
  {
    campaignId: 2021,
    campaignName: "Campaign 9",
    startDate: "2024-09-01",
    endDate: "2024-10-01",
    websites: "www.daraz.pk",
    images: "new.png",
    screenshotPosition: "Left Center",
    MatchingPercentage: 85,
  },
  {
    campaignId: 2223,
    campaignName: "Campaign 10",
    startDate: "2024-10-01",
    endDate: "2024-11-01",
    websites: "www.daraz.pk",
    images: "new.png",
    screenshotPosition: "Random",
    MatchingPercentage: 80,
  },
  // Add more data as needed
];

export default function CampaignTable() {
  const [order, setOrder] = useState("asc");
  const [orderBy, setOrderBy] = useState("campaignName");
  const [data, setData] = useState([]);

  useEffect(() => {
    // Simulate fetching data from API
    setData(mockApiData);
  }, []);

  const handleRequestSort = (property) => {
    const isAsc = orderBy === property && order === "asc";
    setOrder(isAsc ? "desc" : "asc");
    setOrderBy(property);
  };

  return (
    <Box>
      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              {headCells.map((headCell) => (
                <TableCell
                  key={headCell.id}
                  align={headCell.align}
                  padding={headCell.disablePadding ? "none" : "normal"}
                >
                  <Typography
                    variant="subtitle3"
                    fontWeight="bold"
                    color="primary"
                  >
                    {headCell.disablePadding ? (
                      headCell.label
                    ) : (
                      <Link
                        color="inherit"
                        component={RouterLink}
                        to=""
                        onClick={() => handleRequestSort(headCell.id)}
                      >
                        {headCell.label}
                      </Link>
                    )}
                  </Typography>
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {stableSort(data, getComparator(order, orderBy)).map(
              (row, index) => (
                <TableRow key={index}>
                  <TableCell>{row.campaignId}</TableCell>
                  <TableCell>{row.campaignName}</TableCell>
                  <TableCell>{row.startDate}</TableCell>
                  <TableCell>{row.endDate}</TableCell>
                  <TableCell>{row.websites}</TableCell>
                  <TableCell>{row.images}</TableCell>
                  <TableCell>{row.MatchingPercentage}</TableCell>
                  
                </TableRow>
              )
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}
