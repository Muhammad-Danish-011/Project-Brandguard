import React, { useState, useEffect } from "react";
import {
  Button,
  Card,
  CardHeader,
  CardBody,
  FormGroup,
  Form,
  Input,
  Row,
  Col,
} from "reactstrap";
import PanelHeader from "components/PanelHeader/PanelHeader.js";
import axios from "axios";


function UserPage() {
  const [formData, setFormData] = useState({
    company: "",
    username: "",
    email: "",
    firstName: "",
    lastName: "",
    address: "",
    city: "",
    country: "",
    postalCode: "",
    aboutMe: "",
  });

  const resetFormData = () => {
    setFormData({
      company: "",
      user_name: "",
      email: "",
      first_name: "",
      last_name: "",
      address: "",
      city: "",
      country: "",
      postal_code: "",
      about_me: "",
    });
  };

  const closePopup = () => {
    setShowPopup(false);
    setSaveSuccess(false);
    resetFormData();
  };

  const [saveSuccess, setSaveSuccess] = useState(false);
  const [showPopup, setShowPopup] = useState(false);


  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
  };

  useEffect(() => {
    if (saveSuccess) {
      console.log("Data saved successfully!");
    }
  }, [saveSuccess]);

  const handleSaveClick = () => {
    axios
      .post("http://localhost:8081/UserInformations/add", formData)
      .then((response) => {
        console.log(response.data);
        
        setSaveSuccess(true);
        setShowPopup(true);
      })
      .catch((error) => {
        console.error("Error saving data:", error);
        setSaveSuccess(true);
      });

    
    setTimeout(() => {
      setSaveSuccess(true);
    }, 1000);
  };



  return (
    <>
      <PanelHeader size="sm" />
      <div className="content">
        <Row>
          <Col md="8">
            <Card >
              <CardHeader>
                <h5 className="title">User Information </h5>
              </CardHeader>
              <CardBody>
                <Form>
                <Row>
    <Col md="12">
      <FormGroup>
        <label>Web URL</label>
        <Input
          cols="80"
          placeholder="Web URL"
          type="url"
          name="web_url"
          value={formData.web_url}
          onChange={handleInputChange}
          disabled={formData.exact_page_url && formData.exact_page_url.trim() !== ""}
        />
      </FormGroup>
    </Col>
  </Row>

  {/* New Row for Exact Page URL */}
  <Row>
    <Col md="12">
      <FormGroup>
        <label>Exact Page URL</label>
        <Input
          cols="80"
          placeholder="Exact Page URL"
          type="url"
          name="exact_page_url"
          value={formData.exact_page_url}
          onChange={handleInputChange}
          disabled={formData.web_url && formData.web_url.trim() !== ""}

          />
      </FormGroup>
    </Col>
  </Row>

  <Row>
    <Col md="12">
      <FormGroup>
        <label>Choose Ad Image</label>
        <Input
          type="file"  
          name="ad_image"
          onChange={handleInputChange}
        />
      </FormGroup>
    </Col>
  </Row>

 
  <Row>
    <Col md="12">
      <FormGroup>
        <label>Time Duration for Ad (in days)</label>
        <Input
          cols="80"
          placeholder="Time Duration"
          type="positive number"
          name="time_duration"
          value={formData.time_duration}
          onChange={handleInputChange}
        />
      </FormGroup>
    </Col>
  </Row>
                  
                        <Button
                          className="btn-neutral btn-icon btn-round"
                          onClick={()=>{
                            handleSaveClick();
                          }}
                        >
                          Save
                        </Button>
                     
                </Form>
              </CardBody>
            </Card>
          </Col>
        </Row>
      </div>
      {showPopup && (
        <div className="popup">
          <div className="popup-content">
            <p>Data Saved Successfully!</p>
            <button  className="btn-neutral btn-icon btn-round" onClick={closePopup}>Close</button>
          </div>
        </div>
      )}
      
    </>
  );
}

export default UserPage;
