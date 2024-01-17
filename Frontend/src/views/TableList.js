import React, { useState, useEffect } from "react";
import {
  Card,
  CardBody,
  CardHeader,
  CardTitle,
  Table,
  Row,
  Col,
} from "reactstrap";
import PanelHeader from "components/PanelHeader/PanelHeader.js";

function RegularTables() {
  const [tableData, setTableData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://localhost:8081/UserInformation/all");
        const data = await response.json();
        setTableData(data);
        console.log(data, "====");
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  return (
    <>
      <PanelHeader size="sm" />
      <div className="content">
        <Row>
          <Col xs={12}>
            <Card>
              <CardHeader>
                <CardTitle tag="h4">User Information Table</CardTitle>
              </CardHeader>
              <CardBody>
                <Table responsive>
                  <thead className="text-primary">
                    <tr>
                      <th>ID</th>
                      <th>User Name</th>
                      <th>First Name</th>
                      <th>Last Name</th>
                      <th>Company</th>
                      <th>address</th>
                      <th>email</th>
                      <th>city</th>
                      <th>country</th>
                      <th>postal_code</th>
                      <th>about_me</th>
                
                    </tr>
                  </thead>
                  <tbody>
                    {tableData.map((userData) => (
                      <tr key={userData.id}>
                        <td>{userData.id}</td>
                        <td>{userData.user_name}</td>
                        <td>{userData.first_name}</td>
                        <td>{userData.last_name}</td>
                        <td>{userData.address}</td>
                        <td>{userData.email}</td>
                        <td>{userData.city}</td>
                        <td>{userData.country}</td>
                        <td>{userData.postal_code}</td>
                        <td>{userData.about_me}</td>
                      
                      </tr>
                    ))}
                  </tbody>
                </Table>
              </CardBody>
            </Card>
          </Col>
        </Row>
      </div>
    </>
  );
}

export default RegularTables;
