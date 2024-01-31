import React, { useState } from "react";
import {
  Button,
  Card,
  CardHeader,
  CardContent,
  Grid,
  // Input,
  TextField,
  Typography,
} from "@mui/material";
import { format } from "date-fns";
// import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { DateTimePicker, MuiPickersUtilsProvider } from "@material-ui/pickers";
import DateFnsUtils from "@date-io/date-fns";
// import { result } from "lodash";
import "./style.css";

// import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';



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

  // const addUrlField = (name) => {
  //   if (name === "webUrls") {
  //     setWebUrls([...webUrls, ""]);
  //   } else if (name === "exactPageUrls") {
  //     setExactPageUrls([...exactPageUrls, ""]);
  //   }
  // };

  const handleStartDateChange = (newDate) => {
    setStartDate(newDate);
  };

  const handleEndDateChange = (newDate) => {
    setEndDate(newDate);
  };

  const handleSaveClick = async () => {
    try {
      // 1. Prepare data to send to the campaign_details API
      const campaignData = {
        CampaignName: CampaignName,
        StartDate: startDate ? format(startDate, "yyyy-MM-dd HH:mm:ss") : null,
        EndDate: endDate ? format(endDate, "yyyy-MM-dd HH:mm:ss") : null,
        IntervalTime: parseInt(IntervalTime),
        Websites: webUrls.filter((url) => url.trim() !== ""),
        Images: Images.filter((imageName) => imageName.trim() !== ""),
        new_image_path: new_image_path,
      };
  
      // Make API call to save campaign details
      const campaignResponse = await fetch("http://127.0.0.1:5000/campaign_details", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(campaignData),
      });
  
      if (!campaignResponse.ok) {
        throw new Error(`HTTP error! Status: ${campaignResponse.status}`);
      }
  
      const campaignResult = await campaignResponse.json();
      console.log("Campaign data saved successfully:", campaignResult);
  
      // 2. Upload image and save image path to the database
      if (selectedFile) {
        const formData = new FormData();
        formData.append("image", selectedFile);
  
        const uploadResponse = await fetch("http://127.0.0.1:5000/upload", {
          method: "POST",
          body: formData,
        });
  
        if (uploadResponse.ok) {
          const uploadResult = await uploadResponse.json();
          console.log("Image uploaded successfully. Result:", uploadResult);
          const imagePath = uploadResult.file_path;
          await savePathToDB(imagePath);
          setShowPopup(true);
          setnew_image_path(imagePath);
        } else {
          console.error("Image upload failed");
        }
      }
  
      console.log("All API calls completed successfully!");
    } catch (error) {
      console.error("Error during save operation:", error);
    }
  };
  
      // Make API call to save image path
     

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


  return (
    <React.Fragment>
    <div className="container">
      <Card className="card" >
        <Typography variant="h2" className="header" gutterBottom>AD Scheduling</Typography>
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
                  // autoComplete="given-name"
                  variant="standard"
                  required
                  // InputLabelProps={{
                  //   shrink: true,
                  // }}
                />
              </Grid>
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom>Select Date Range</Typography>
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
                        disablePast
                      />
                    </Grid>
                   
                  </Grid>
                </MuiPickersUtilsProvider>

              </Grid>
              {/* <Grid container spacing={2} item xs={12}> */}
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
              {/* </Grid> */}
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
                      // disabled={
                      //   exactPageUrls[index] !== "" &&
                      //   exactPageUrls[index].trim() !== ""
                      // }
                      margin="normal"
                      autoComplete="given-name"
                     variant="standard"
                     required
                      
                    />
                  </Grid>
                ))}
                {/* <Grid item xs={12}>
                  <Button 
                    variant="contained"
                    color="primary"
                    onClick={() => addUrlField("webUrls")}
                  >
                    Add URL
                  </Button>
                </Grid> */}
               
              </Grid>
              <Grid container spacing={1} item xs={12}>
                <Grid item xs={12}>
                  <input className="button"
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
      {showPopup && (
        <div className="popup">
          <Typography variant="h2" gutterBottom>
            Data Saved Successfully!
          </Typography>
          <Button
            variant="contained"
            color="primary"
            onClick={closePopup}
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
