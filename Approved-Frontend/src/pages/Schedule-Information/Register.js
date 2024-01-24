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
  const [formData, setFormData] = useState({
    webUrl: "",
    exactPageUrl: "",
    adImage: null,
    startDate: null,
    endDate: null,
  });

  const [showPopup, setShowPopup] = useState(false);

  const handleInputChange = (e, name) => {
    const { value, files } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: name === "adImage" ? files[0] : value,
    }));
  };
  const handleStartDateChange = (newDate) => {
    setFormData((prevFormData) => ({
      ...prevFormData,
      startDate: newDate,
    }));
  };

  const handleEndDateChange = (newDate) => {
    setFormData((prevFormData) => ({
      ...prevFormData,
      endDate: newDate,
    }));
  };
  const handleSaveClick = () => {
    // Your save logic goes here
    // You can implement your save logic, API calls, etc.
    // For now, let's just show the popup
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
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Web URL"
                  placeholder="Web URL"
                  type="url"
                  name="webUrl"
                  value={formData.webUrl}
                  onChange={(e) => handleInputChange(e, "webUrl")}
                  disabled={
                    formData.exactPageUrl && formData.exactPageUrl.trim() !== ""
                  }
                  variant="outlined"
                  margin="normal"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Exact Page URL"
                  placeholder="Exact Page URL"
                  type="url"
                  name="exactPageUrl"
                  value={formData.exactPageUrl}
                  onChange={(e) => handleInputChange(e, "exactPageUrl")}
                  disabled={formData.webUrl && formData.webUrl.trim() !== ""}
                  variant="outlined"
                  margin="normal"
                />
              </Grid>
              <Grid item xs={12}>
                <Input
                  type="file"
                  name="adImage"
                  onChange={(e) => handleInputChange(e, "adImage")}
                />
              </Grid>
              <Grid container spacing={3} item xs={12}>
                <Grid item xs={12}>
                  <Typography variant="h6">Select Date Range</Typography>
                </Grid>
                <Grid item xs={12}>
                  {/* Start Date Picker */}
                  <DatePicker
                   
                    selected={formData.startDate}
                    onChange={(date) => handleStartDateChange(date, "startDate")}
                    selectsStart
                    startDate={formData.startDate}
                    endDate={formData.endDate}
                    placeholderText="Start Date"
                    
                  />
                </Grid>
                <Grid item xs={12}>
                  {/* End Date Picker */}
                  <DatePicker
                    selected={formData.endDate}
                    onChange={(date) => handleEndDateChange(date, "endDate")}
                    
                    selectsEnd
                    startDate={formData.startDate}
                    endDate={formData.endDate}
                    placeholderText="End Date"
                  />
                </Grid>
              </Grid>
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
            transform: "translate(-50%, -50%)",
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
            style={{ marginTop: "10px" }}
          >
            Close
          </Button>
        </div>
      )}
    </div>
  );
};

export default Register;
