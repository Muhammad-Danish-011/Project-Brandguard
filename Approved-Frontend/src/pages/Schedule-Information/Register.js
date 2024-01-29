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
import { format } from "date-fns";
// import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { DateTimePicker, MuiPickersUtilsProvider } from "@material-ui/pickers";
import DateFnsUtils from "@date-io/date-fns";
// import { result } from "lodash";

const Register = () => {
  const [webUrls, setWebUrls] = useState([""]);
  const [exactPageUrls, setExactPageUrls] = useState([""]);
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [showPopup, setShowPopup] = useState(false);
  const [CampaignName, setCampaignName] = useState(" ");
  const [IntervalTime, setIntervalTime] = useState();
  const [Images, setImages] = useState([""]);
  const [selectedFile, setSelectedFile] = useState(null);

  const [new_image_path, setnew_image_path] = useState([]);

  
 

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
    } else if (name === "exactPageUrls") {
      const newExactPageUrls = [...exactPageUrls];
      newExactPageUrls[index] = value;
      setExactPageUrls(newExactPageUrls);
      const newImages = [...Images];
      newImages[index] = adImageFile ? adImageFile.name : ""; // Update with file name or handle as needed
      setImages(newImages);
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
  // Prepare data to send to the API
  const dataToSend = {
    CampaignName: CampaignName,
    StartDate: startDate ? format(startDate, "yyyy-MM-dd HH:mm:ss") : null,
    EndDate: endDate ? format(endDate, "yyyy-MM-dd HH:mm:ss") : null,
    IntervalTime: parseInt(IntervalTime),
    Websites: webUrls.filter((url) => url.trim() !== ""), // Remove empty URLs
    Images: Images.filter((imageName) => imageName.trim() !== ""),
    new_image_path: new_image_path,
    // Status: "Active",
    // Add other data properties as needed
  };

  // Make API call to save campaign details
  fetch("http://127.0.0.1:5000/campaign_details", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(dataToSend),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      // Handle success
      console.log("Data saved successfully:", data);

      if (data.new_image && data.new_image.length > 0) {
        setShowPopup(true);
        setnew_image_path(data.new_image_path[0]);

      }
      }  )
      .catch((error) => {
        // Handle error
        console.error("Error saving data:", error);
      });

      // Make API call to save image path
     
};

const savePathToDB = (path) => {
  fetch("http://127.0.0.1:5000/save_image_path", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ new_image_path: path }), // Use 'new_image_path' as the key
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      // Handle success
      console.log("Image path saved in the database:", data);
    })
    .catch((error) => {
      // Handle error
      console.error("Error saving image path in the database:", error);
    });
    
     
}

  
  const closePopup = () => {
    setShowPopup(false);
  };

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };
// store the image locally in storage _____________________________________________________
  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please select an image");
      return;
    }

    const formData = new FormData();
    formData.append("image", selectedFile);

    try {
      const response = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData,
        // Add headers if needed, e.g., for authorization or content type
      });

      if (response.ok) {
        // Handle successful upload
        const result = await response.json();
        console.log("Image uploaded successfully. Result:", result);
        savePathToDB([result.file_path])
      } else {
        // Handle upload error
        console.error("Image upload failed");
      }
    } catch (error) {
      console.error("Error during image upload:", error);
    }
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
            <Grid container spacing={2} item xs={12}>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Campaign Name"
                  onChange={handleTextChange}
                  type="text"
                  placeholder="Campaign Name"
                  value={CampaignName}
                />
              </Grid>
              {/* Date Range */}
              <Grid item xs={12}>
                <Typography variant="h6">Select Date Range</Typography>
                <MuiPickersUtilsProvider utils={DateFnsUtils}>
                  <Grid container spacing={2}>
                    <Grid item xs={12}>
                      <DateTimePicker
                        fullWidth
                        label="Start Date"
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
                        disablePast
                      />
                    </Grid>
                  </Grid>
                </MuiPickersUtilsProvider>
              </Grid>

              {/* Interval Time */}
              <Grid container spacing={-1} item xs={12}>
                <TextField
                  fullWidth
                  label="Interval Time"
                  onChange={(e) => handleTimeChange(e)}
                  type="number"
                  inputProps={{ min: "0" }}
                  value={IntervalTime}
                  placeholder="Interval Time"
                />
              </Grid>
              {/* Web URLs */}
              <Grid container spacing={2} item xs={12}>
                {webUrls.map((url, index) => (
                  <Grid item xs={12} key={index}>
                    <TextField
                      fullWidth
                      label={`Web URL ${index + 1}`}
                      placeholder="Web URL"
                      type="url"
                      value={url}
                      onChange={(e) => handleInputChange(e, "webUrls", index)}
                      disabled={
                        exactPageUrls[index] !== "" &&
                        exactPageUrls[index].trim() !== ""
                      }
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
              {/* Ad Image */}
              <Grid item xs={12}>
                <input
                  type="file"
                  onChange={handleFileChange}
                  accept="image/*"
                />
                </Grid>
                <Grid item xs={12}>
                <Button
                 variant="contained"
                 color="primary"
                 fullWidth
                  onClick={handleUpload}
                 
                >
                  Upload Image
                </Button>
              </Grid>
              {/* Ad Image */}
              <Grid item xs={12}>
                <Input
                  type="text"
                  name="adImage"
                  onChange={(e) => handleInputChange(e, "adImage")}
                />
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
