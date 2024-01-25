import React, { useState } from "react";
import {
  Button,
  Card,
  CardHeader,
  CardContent,
  Grid,
  Input,
  TextField,
  Typography,
} from "@mui/material";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

const Register = () => {
  const [webUrls, setWebUrls] = useState([""]);
  const [exactPageUrls, setExactPageUrls] = useState([""]);
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [showPopup, setShowPopup] = useState(false);

  const handleInputChange = (e, name, index) => {
    const { value } = e.target;

    if (name === "webUrls") {
      const newWebUrls = [...webUrls];
      newWebUrls[index] = value;
      setWebUrls(newWebUrls);
    } else if (name === "exactPageUrls") {
      const newExactPageUrls = [...exactPageUrls];
      newExactPageUrls[index] = value;
      setExactPageUrls(newExactPageUrls);
    }
    
  };

  const addUrlField = (name) => {
    if (name === "webUrls") {
      setWebUrls([...webUrls, ""]);
    } else if (name === "exactPageUrls") {
      setExactPageUrls([...exactPageUrls, ""]);
    }
   
  };

  const handleStartDateChange = (newDate) => {
    setStartDate(newDate);
  };

  const handleEndDateChange = (newDate) => {
    setEndDate(newDate);
  };

  const handleSaveClick = () => {
    setShowPopup(true);
    
  };

  const closePopup = () => {
    setShowPopup(false);
  };


  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        minHeight: "10vh",
      }}
    >
      <Card style={{ width: "400px", padding: "16px" }}>
        <Typography variant="h2">Scheduling for Ad:</Typography>

        <CardHeader />

        <CardContent>
          <form>
            <Grid container spacing={1}>
              {/* Web URLs */}
              <Grid container spacing={2}>
                {webUrls.map((url, index) => (
                  <Grid item xs={12} key={index}>
                    <TextField
                      fullWidth
                      label={`Web URL ${index + 1}`}
                      placeholder="Web URL"
                      type="url"
                      value={url}
                      onChange={(e) => handleInputChange(e, "webUrls", index)}
                      disabled={exactPageUrls[index] && exactPageUrls[index].trim() !== ""}

                      variant="outlined"
                      margin="normal"
                    />
                  </Grid>
                ))}
                <Grid item xs={12}>
                  <Button
                    variant="contained"
                    color="primary"
                    fullWidth
                    onClick={() => addUrlField("webUrls")}
                    
                  >
                    Add URL
                  </Button>
                </Grid>
              </Grid>

              {/* Exact Page URLs */}
              <Grid container spacing={2}>
                {exactPageUrls.map((url, index) => (
                  <Grid item xs={12} key={index}>
                    <TextField
                      fullWidth
                      label={`Exact URL ${index + 1}`}
                      placeholder="Exact URL"
                      type="url"
                      value={url}
                      onChange={(e) => handleInputChange(e, "exactPageUrls", index)}
                      disabled={webUrls[index] && webUrls[index].trim() !== ""}
                      variant="outlined"
                      margin="normal"
                    />
                  </Grid>
                ))}
                <Grid item xs={12}>
                  <Button
                    variant="contained"
                    color="primary"
                    fullWidth
                    onClick={() => addUrlField("exactPageUrls")}
                  >
                    Add URL
                  </Button>
                </Grid>
              </Grid>

              {/* Ad Image */}
              <Grid item xs={12}>
                <Input
                  type="file"
                  name="adImage"
                  onChange={(e) => handleInputChange(e, "adImage")}
                />
              </Grid>

              {/* Date Range */}
              <Grid container spacing={3} item xs={12}>
                <Grid item xs={12}>
                  <Typography variant="h6">Select Date Range</Typography>
                </Grid>
                <Grid item xs={12}>
                  <DatePicker
                    selected={startDate}
                    onChange={(date) => handleStartDateChange(date)}
                    selectsStart
                    startDate={startDate}
                    endDate={endDate}
                    placeholderText="Start Date"
                  />
                </Grid>
                <Grid item xs={12}>
                  <DatePicker
                    selected={endDate}
                    onChange={(date) => handleEndDateChange(date)}
                    selectsEnd
                    startDate={startDate}
                    endDate={endDate}
                    placeholderText="End Date"
                  />
                </Grid>
              </Grid>

              {/* Save Button */}
              <Grid item xs={12}>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={handleSaveClick}
                  fullWidth
                >
                  Save
                </Button>
              </Grid>
            </Grid>
          </form>
        </CardContent>
      </Card>
      {showPopup && (
        <div
          style={{
            position: "fixed",
            top: "50%",
            left: "50%",
           // transform: "translate(-50%, -50%)",
            padding: "16px",
            background: "#fff",
            boxShadow: "0 0 20px rgba(5, 5, 5, 5)",
            borderRadius: "16px",
            textAlign: "center",
          }}
        >
          <Typography variant="h2" gutterBottom>
            Data Saved Successfully!
          </Typography>
          <Button
            variant="contained"
            color="primary"
            onClick={closePopup}
            style={{ marginTop: "5px" }}
          >
            Close
          </Button>
        </div>
      )}
    </div>
  );
};

export default Register;
