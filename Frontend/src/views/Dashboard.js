
import React from "react";

import { Line, Bar } from "react-chartjs-2";

import {
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  CardTitle,
  Row,
  Col,

} from "reactstrap";

import PanelHeader from "components/PanelHeader/PanelHeader.js";

import {
  dashboardPanelChart,

  dashboard24HoursPerformanceChart,
} from "variables/charts.js";

function Dashboard() {
  return (
    <>
    
   
      <PanelHeader
        size="lg"
        content={
          <Line
            data={dashboardPanelChart.data}
            options={dashboardPanelChart.options}
          />
        } 
      />
      <>
      <br/><br/><br/><br/>
      </>
      <div className="content">
        <Row>
          <Col xs={12} md={15}>
            <Card className="card-chart">
              <CardHeader>
                <h5 className="card-category">REPORT ANALYSIS</h5>
                <CardTitle tag="h4" className="card-title"> Performance</CardTitle>
              </CardHeader>
              <CardBody>
                <div className="chart-area">
                  <Bar
                    data={dashboard24HoursPerformanceChart.data}
                    options={dashboard24HoursPerformanceChart.options}
                  />
                </div>
              </CardBody>
              <CardFooter>
                <div className="stats">
                  <i className="now-ui-icons ui-2_time-alarm" /> Previous days
                </div>
              </CardFooter>
            </Card>
          </Col>
        </Row>
      
      </div>
    </>
  );
}

export default Dashboard;
