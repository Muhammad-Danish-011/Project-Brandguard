import axios from 'axios'
import React, { useEffect, useState } from 'react'
import Layout from '../../layouts/Layout'
import { Button, Col, Flex, Row, Space, Table, Typography } from 'antd'
import { useNavigate } from 'react-router-dom'


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
]

const Campaigns = () => {

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
        <Typography.Title level={1} style={{ marginTop: '0' }}>Campaigns</Typography.Title>
        <Table dataSource={campaignsData} columns={columns(navigate)} style={{ marginTop: '36px' }}/>
      </Layout>
    </>
  )
}

export default Campaigns