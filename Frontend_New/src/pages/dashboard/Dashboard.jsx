import React, { useEffect, useState } from 'react'
import Layout from '../../layouts/Layout'
import { Button, Col, Flex, Row, Space, Table, Typography } from 'antd'
import axios from 'axios';
import { useNavigate } from 'react-router-dom';


const columns = (navigate) => [
  {
    title: 'Campaign Id',
    dataIndex: 'CampaignID',
    key: 'CampaignID',
  },
  {
    title: 'Campaign Name',
    dataIndex: 'CampaignName',
    key: 'CampaignName',
  },
  {
    title: 'Start Date',
    dataIndex: 'StartDate',
    key: 'StartDate',
  },
  {
    title: 'End Date',
    dataIndex: 'EndDate',
    key: 'EndDate',
  },
  {
    title: 'Website',
    dataIndex: 'WebsiteURL',
    key: 'WebsiteURL',
    render: (value) => value.join('')
  },
  {
    title: 'Found Status (Screenshot)',
    dataIndex: 'Found_Status_Screenshot',
    key: 'Found_Status_Screenshot',
  },
  {
    title: 'Found Status (Scraping)',
    dataIndex: 'Found_Status_Scraping',
    key: 'Found_Status_Scraping',
  },
  {
    title: 'Action',
    dataIndex: 'action',
    key: 'action',
    render: (_, record) => <Button onClick={() => navigate(`/campaigns/${record.CampaignID}?details=screenshot`)}>View Details</Button>
  },
];

const Dashboard = () => {

  const [campaignsData, setCampaignsData] = useState([])

  const navigate = useNavigate()

  const fetchCampaignsData = () => {
    axios.get(process.env.REACT_APP_API_BASEURL+'/general_report')
      .then((response) => response?.data)
      .then((response) => {
        setCampaignsData(response)
      })
      .catch((error) => {
        console.log(error)
      })
  }

  useEffect(() => {
    fetchCampaignsData()
  }, [])

  return (
    <>
      <Layout>
        <Row gutter={[24, 24]}>
          <Col span={9}>
            <div style={{ border: '1px solid gray', borderRadius: '15px', padding: '24px'}}>
              <Typography.Title level={2} style={{ marginTop: '0' }}>Total Campaigns</Typography.Title>
              <Typography.Title level={3} style={{ marginBottom: '0' }}>{campaignsData.length}</Typography.Title>
            </div>
          </Col>
          <Col span={15}>
          </Col>
        </Row>
        <div style={{ marginTop: '48px' }}>
          <Flex align='center' gap={24}><Typography.Title level={1}>Campaigns</Typography.Title><Button onClick={() => navigate('/campaigns')}>View All</Button></Flex>
          <Table dataSource={campaignsData.slice(0, 3)} columns={columns(navigate)} pagination={false} />
        </div>
      </Layout>
    </>
  )
}

export default Dashboard