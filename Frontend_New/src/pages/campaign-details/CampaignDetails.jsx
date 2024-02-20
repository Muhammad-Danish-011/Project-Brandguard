import { Button, Col, Image, Radio, Row, Space, Table, Typography } from 'antd'
import React, { useEffect, useState } from 'react'
import { useLocation, useNavigate, useParams } from 'react-router-dom'
import useSWR from 'swr';
import Layout from '../../layouts/Layout';
import axios from 'axios';
import RadialPlot from '../../components/RadialPlot/RadialPlot';
import { ReactComponent as DateIcon } from '../../assets/cards/calendar-day_9586284.svg'
import { ReactComponent as ScrapingIcon } from '../../assets/cards/icons8-web-scraper.svg'
import { ReactComponent as ScreenshotIcon } from '../../assets/cards/screenshot_scissors_cut_icon_207353.svg'
import screenshotImage from '../../assets/cards/4306405.webp'


const fetcher = (url) => fetch(url).then((res) => res.json());

const extractFolderAndFile = (filePath) => {
  const parts = filePath.split(/[\\\/]/); // Split by directory separator
  const fileName = parts.pop(); // Get the last part (file name)
  const folderName = parts.pop(); // Get the second last part (folder name)
  return { folderName, fileName };
};

const screenshotColumns = [
  {
    title: 'Capture Time',
    dataIndex: 'Capture_DateTime',
    key: 'Capture_DateTime',
  },
  {
    title: 'Website Screenshot',
    dataIndex: 'FilePath',
    key: 'FilePath',
    render: (value) => {

      const image = <Image height={100} src={process.env.REACT_APP_API_BASEURL+`/image?folder=${encodeURIComponent(extractFolderAndFile(value).folderName)}&file=${encodeURIComponent(extractFolderAndFile(value).fileName)}`}/>
      return image
    }
  },
  {
    title: 'Found Status',
    dataIndex: 'Found_Status',
    key: 'Found_Status',
  },
  {
    title: 'Ad Position',
    dataIndex: 'Ad_Position',
    key: 'Ad_Position',
  }
]

const scrapingColumns = [
  {
    title: 'Capture Time',
    dataIndex: 'DateTime',
    key: 'DateTime',
  },
  {
    title: 'Found Status',
    dataIndex: 'Found_Status',
    key: 'Found_Status',
  }
]

const svgStyles = { 
  position: 'absolute', 
  height: '150px', 
  width: '140px', 
  top: '16', 
  right: '30', 
  opacity: 0.2  
}


const CampaignDetails = () => {

  const { campaignId } = useParams()
  const navigate = useNavigate()
  
  const { search } = useLocation()
  const searchParams = new URLSearchParams(search)
  const details = searchParams.get('details')

  const [campaignData, setCampaignData] = useState({})
  const [showScreenshotDetails, setShowScreenshotDetails] = useState(true)

  const { data: screenshotData, error: screenshotError, isLoading: screenshotIsLoading, mutate: mutateScreenshot } = useSWR(
    process.env.REACT_APP_API_BASEURL+'/screenshot_report/'+campaignId,
    fetcher
  );

  const { data: scrapingData, error: scrapingError, isLoading: scrapingIsLoading, mutate: mutateScraping } = useSWR(
    process.env.REACT_APP_API_BASEURL+'/scraping_report/'+campaignId,
    fetcher
  );

  const handleTabChange = (e) => {
    navigate(`/campaigns/${campaignId}?details=${e.target.value}`)
  }

  useEffect(() => {    
    if(details === 'screenshot') {
      mutateScreenshot()
      setShowScreenshotDetails(true)
    }
    else if(details === 'scraping') {
      mutateScraping()
      setShowScreenshotDetails(false)
    }

  }, [search])

  const fetchCampaignsData = async () => {
    return axios.get(process.env.REACT_APP_API_BASEURL+'/general_report')
      .then((response) => response?.data)
      .catch((error) => error?.response?.data)
  }

  useEffect(() => {
    fetchCampaignsData()
      .then((response) => {
        const campaign = response.find((item) => item.CampaignID == campaignId)
        setCampaignData(campaign)
      })
      .catch((error) => {
        console.log(error)
      })
  }, [])

  return (
    <>
      <Layout>
        <Space direction='vertical'>
          <Typography.Title level={1}>{screenshotData?.CampaignName}</Typography.Title>
          <Space><Typography.Text strong>Website URL:</Typography.Text><Typography.Text>{screenshotData?.WebsiteURL.join('')}</Typography.Text></Space>
        </Space>
        <Row gutter={[36, 36]} style={{ marginTop: '48px' }}>
          <Col span={12}>
            <div style={{ borderRadius: '20px', height: '185px', padding: '36px', paddingTop: '24px',
              boxShadow: 'rgba(0, 0, 0, 0.35) 0px 5px 15px', position: 'relative',  overflow: 'hidden'
            }}>
              <Typography.Title level={2} style={{ marginTop: '0' }}>Campaign Start Date</Typography.Title>
              <Typography.Text style={{ fontSize: '20px' }}>{campaignData?.StartDate}</Typography.Text>
              <DateIcon style={{...svgStyles, height: '130px', width: '130px', top: 25}} />
            </div>
          </Col>
          <Col span={12}>
            <div style={{ borderRadius: '20px', height: '185px', padding: '36px', paddingTop: '24px',
              boxShadow: 'rgba(0, 0, 0, 0.35) 0px 5px 15px', position: 'relative',  overflow: 'hidden'
            }}>
              <Typography.Title level={2} style={{ marginTop: '0' }}>Campaign End Date</Typography.Title>
              <Typography.Text style={{ fontSize: '20px' }}>{campaignData?.EndDate}</Typography.Text>
              <DateIcon style={{...svgStyles, height: '130px', width: '130px', top: 25}} />
            </div>
          </Col>
          <Col span={12}>
            <div style={{ borderRadius: '20px', height: '185px', padding: '36px', paddingTop: '24px',
              boxShadow: 'rgba(0, 0, 0, 0.35) 0px 5px 15px', position: 'relative',  overflow: 'hidden'
            }}>
              <Typography.Title level={2} style={{ marginTop: '0' }}>Screenshot Details</Typography.Title>
              <Space direction='vertical'>
                <Space>
                  <Typography.Text strong style={{ fontSize: '20px' }}>Attempts:</Typography.Text>
                  <Typography.Text style={{ fontSize: '20px' }}>{campaignData?.Screenshot_Attempts}</Typography.Text>
                </Space>
                <Space>
                  <Typography.Text strong style={{ fontSize: '20px' }}>Found Rate:</Typography.Text>
                  <Typography.Text style={{ fontSize: '20px' }}>{campaignData?.Found_Status_Screenshot}</Typography.Text>
                </Space>
              </Space>
              <img src={screenshotImage} style={{...svgStyles, height: '130px', width: '130px', top: 25, right: 30}}/>
            </div>
          </Col>
          <Col span={12}>
            <div style={{ borderRadius: '20px', height: '185px', padding: '36px', paddingTop: '24px',
              boxShadow: 'rgba(0, 0, 0, 0.35) 0px 5px 15px', position: 'relative',  overflow: 'hidden'
            }}>
              <Typography.Title level={2} style={{ marginTop: '0' }}>Scraping Details</Typography.Title>
              <Space direction='vertical'>
                <Space>
                  <Typography.Text strong style={{ fontSize: '20px' }}>Attempts:</Typography.Text>
                  <Typography.Text style={{ fontSize: '20px' }}>{campaignData?.Scraping_Attempts}</Typography.Text>
                </Space>
                <Space>
                  <Typography.Text strong style={{ fontSize: '20px' }}>Found Rate:</Typography.Text>
                  <Typography.Text style={{ fontSize: '20px' }}>{campaignData?.Found_Status_Scraping}</Typography.Text>
                </Space>
              </Space>
              <ScrapingIcon style={{...svgStyles, height: '150px', width: '150px', top: 16}}/>
            </div>
          </Col>
        </Row>
        {/* <RadialPlot/> */}
        <div style={{ marginTop: '60px' }}>
          <Radio.Group defaultValue={details} buttonStyle="solid" onChange={handleTabChange}>
            <Radio.Button value="screenshot">Screenshot Details</Radio.Button>
            <Radio.Button value="scraping">Scraping Details</Radio.Button>
          </Radio.Group>
        </div>

        <div style={{ marginTop: '48px' }}>
        <Typography.Text italic>
          Showing {showScreenshotDetails ? 'screenshot' : 'scraping'} approach details
        </Typography.Text>
        <Table style={{ marginTop: '24px', borderRadius: '20px', padding: '12px 20px', boxShadow: 'rgba(0, 0, 0, 0.35) 0px 5px 15px' }}
          loading={showScreenshotDetails ? screenshotIsLoading : scrapingIsLoading}
          columns={showScreenshotDetails ? screenshotColumns : scrapingColumns}
          dataSource={showScreenshotDetails ? screenshotData?.AdPositions : scrapingData?.ScrapeImageStatus}
        />
        </div>
      </Layout>
    </>
  )
}

export default CampaignDetails