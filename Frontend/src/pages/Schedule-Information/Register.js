import React, { useState } from "react";
import {
  Button,
  Card,
  CardHeader,
  CardContent,
  Grid,
  TextField,
  Typography,
} from "@mui/material";
import { format } from "date-fns";
import "react-datepicker/dist/react-datepicker.css";
import { DateTimePicker, MuiPickersUtilsProvider } from "@material-ui/pickers";
import DateFnsUtils from "@date-io/date-fns";
import "./style.css";

const Register = () => {
  const [webUrls, setWebUrls] = useState([""]);
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [showSuccessPopup, setShowSuccessPopup] = useState(false);
  const [showErrorPopup, setShowErrorPopup] = useState(false);
  const [CampaignName, setCampaignName] = useState("");
  const [IntervalTime, setIntervalTime] = useState();
  const [Images, setImages] = useState([""]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [new_image_path, setnew_image_path] = useState([]);
  const [isFocused, setIsFocused] = useState(false);

  const handleTimeChange = (e) => {
    setIntervalTime(e.target.value);
  };

  const handleTextChange = (e) => {
    setCampaignName(e.target.value);
  };

  const handleInputChange = (e, name, index) => {
    const { value } = e.target;

    if (name === "webUrls") {
      const newWebUrls = [...webUrls];
      newWebUrls[index] = value;
      setWebUrls(newWebUrls);
    }
  };

  const addDays = (date, days) => {
    const result = new Date(date);
    result.setDate(date.getDate() + days);
    return result;
  };

  const handleStartDateChange = (newDate) => {
    setStartDate(newDate);
  };

  const handleEndDateChange = (newDate) => {
    if (newDate <= startDate) {
      setEndDate(addDays(new Date(startDate), 1));
    } else {
      setEndDate(newDate);
    }
  };

  const handleSaveClick = async () => {
    try {
      const campaignData = {
        CampaignName: CampaignName,
        StartDate: startDate ? format(startDate, "yyyy-MM-dd HH:mm:ss") : null,
        EndDate: endDate ? format(endDate, "yyyy-MM-dd HH:mm:ss") : null,
        IntervalTime: parseInt(IntervalTime),
        Websites: webUrls.filter((url) => url.trim() !== ""),
        Images: Images.filter((imageName) => imageName.trim() !== ""),
        new_image_path: new_image_path,
      };

      const campaignResponse = await fetch(
        "http://127.0.0.1:5000/campaign_details",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(campaignData),
        }
      );

      if (!campaignResponse.ok) {
        throw new Error(`HTTP error! Status: ${campaignResponse.status}`);
      }

      const campaignResult = await campaignResponse.json();
      console.log("Campaign data saved successfully:", campaignResult);


      const campaignId = campaignResult.CampaignID;

      if (selectedFile) {
        const formData = new FormData();
        formData.append("image", selectedFile);
        formData.append("campaign_id", campaignId);

        const uploadResponse = await fetch("http://127.0.0.1:5000/upload", {
          method: "POST",
          body: formData,
        });

        if (uploadResponse.ok) {
          const uploadResult = await uploadResponse.json();
          console.log("Image uploaded successfully. Result:", uploadResult);
          const imagePath = uploadResult.file_path;

          await savePathToDB(imagePath, campaignId);
          setShowSuccessPopup(true);
          setnew_image_path(imagePath);
          console.log("All API calls completed successfully!");
         
        } else {
          console.error("Image upload failed");
        }
      }
    } catch (error) {
      console.error("Error during save operation:", error);
      setShowErrorPopup(true);
    }
  };

  const savePathToDB = async (path, campaignId) => {
    try {
      const response = await fetch("http://127.0.0.1:5000/save_image_path", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ new_image_path: path, campaign_id: campaignId }),
      });

      if (!response.ok) {
        const errorResponse = await response.json();
        console.error("Error response from server:", errorResponse);
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Image path saved in the database:", data);
    } catch (error) {
      console.error("Error saving image path in the database:", error);
    }
  };

  const closeSuccessPopup = () => {
    setShowSuccessPopup(false);
    window.location.reload();
  };

  const closeErrorPopup = () => {
    setShowErrorPopup(false);
  };

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  return (
    <React.Fragment>
      <div className="container">
        <Card
          className="card"
          style={{ backgroundColor: "#E3F2FD", color: "#1976D2" }}
        >
          <Typography variant="h2" className="header" gutterBottom>
            Advertisement Scheduling
          </Typography>
          <CardHeader />
          <CardContent>
            <form className="form">
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Campaign Name"
                    placeholder="Campaign Name"
                    onChange={handleTextChange}
                    type="text"
                    value={CampaignName}
                    variant="standard"
                    required
                    margin="normal"
                    InputLabelProps={{
                      shrink: CampaignName !== "",
                    }}
                    onFocus={() => setIsFocused(true)}
                    onBlur={() => setIsFocused(false)}
                  />
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="h6" gutterBottom>
                    Select Date Range
                  </Typography>
                  <MuiPickersUtilsProvider utils={DateFnsUtils}>
                    <Grid container spacing={2}>
                      <Grid item xs={12}>
                        <DateTimePicker
                          fullWidth
                          label="Start Date"
                          placeholder="Start Date"
                          value={startDate}
                          onChange={handleStartDateChange}
                          format="yyyy-MM-dd HH:mm:ss"
                          disablePast
                        />
                      </Grid>
                      <Grid item xs={12}>
                        <DateTimePicker
                          fullWidth
                          label="End Date"
                          value={endDate}
                          onChange={handleEndDateChange}
                          format="yyyy-MM-dd HH:mm:ss"
                          minDate={startDate}
                          disablePast
                        />
                      </Grid>
                    </Grid>
                  </MuiPickersUtilsProvider>
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Interval Time"
                    placeholder="Interval Time"
                    onChange={(e) => handleTimeChange(e)}
                    type="number"
                    inputProps={{ min: "0" }}
                    value={IntervalTime}
                    autoComplete="given-name"
                    variant="standard"
                    required
                  />
                </Grid>
                <Grid container spacing={0} item xs={12}>
                  {webUrls.map((url, index) => (
                    <Grid item xs={12} key={index}>
                      <TextField
                        fullWidth
                        label={`Website`}
                        placeholder={`Website`}
                        type="url"
                        value={url}
                        onChange={(e) => handleInputChange(e, "webUrls", index)}
                        margin="normal"
                        autoComplete="given-name"
                        variant="standard"
                        required
                      />
                    </Grid>
                  ))}
                </Grid>
                <Grid container spacing={1} item xs={12}>
                  <Grid item xs={12}>
                    <input
                      className="button"
                      type="file"
                      onChange={handleFileChange}
                      accept="image/*"
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
        {showSuccessPopup && (
          <div className="popup">
            <Typography variant="h2" gutterBottom>
              Data Saved Successfully!
            </Typography>
            <Button
              variant="contained"
              color="primary"
              onClick={closeSuccessPopup}
              style={{ marginTop: "2px" }}
            >
              Close
            </Button>
          </div>
        )}
        {showErrorPopup && (
          <div className="popup">
            <Typography variant="h2" gutterBottom>
              Campaign Already Exists
            </Typography>
            <Typography variant="body1">
              The campaign with the same name already exists. Please choose a different name.
            </Typography>
            <Button
              variant="contained"
              color="primary"
              onClick={closeErrorPopup}
              style={{ marginTop: "2px" }}
            >
              Close
            </Button>
          </div>
        )}
      </div>
    </React.Fragment>
  );
};

export default Register;



    {/* <Grid item xs={12}>
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={() => addUrlField("webUrls")}
                  >
                    Add URL
                  </Button>
                </Grid> */}
{
  /* Exact Page URLs */
}
{
  /* <Grid container spacing={2}>
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
              </Grid> */
}