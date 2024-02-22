import React, { useState } from 'react'
import Layout from '../../layouts/Layout'
import { Button, DatePicker, Flex, Form, Input, InputNumber, Modal, Result, Space, Typography, Upload, message } from 'antd'
import { UploadOutlined, ex } from '@ant-design/icons'
import axios from 'axios'
import moment from 'moment'
import { useNavigate } from 'react-router-dom'

const CreateCampaign = () => {

  const [imageName, setImageName] = useState('')
  const [loading, setLoading] = useState(false)

  const [modal, modalContextHolder] = Modal.useModal();
  const [messageApi, contextHolder] = message.useMessage()
  const [form] = Form.useForm()
  const navigate = useNavigate()

  const showSuccessMessage = () => {
    modal.success({
      title: 'Success',
      content: 'Campaign successfully created.',
      okText: 'Go to campaigns',
      maskClosable: true,
      onOk: () => navigate('/campaigns')
    })
    // messageApi.open({
    //   type: 'success',
    //   content: 'Campaign successfully created',
    //   // duration: 0,
    // })
  }

  const showErrorMessage = () => {
    messageApi.open({
      type: 'error',
      content: 'Error while creating campaign',
      // duration: 0,
    })
  }

  const sendCampaignDetails = async (data) => {
    return axios.post(process.env.REACT_APP_API_BASEURL+'/campaign_details', data)
  }

  const sendImage = async (data) => {

    const { image, campaign_id } = data

    const formData = new FormData()
    formData.append('image', image)
    formData.append('campaign_id', campaign_id)

    return axios.post(process.env.REACT_APP_API_BASEURL+'/upload', formData)
  }

  const sendImageDetails = async (data) => {
    return axios.post(process.env.REACT_APP_API_BASEURL+'/save_image_path', data)
  }

  const getFile = (e) => {
    const file = e.file.originFileObj
    setImageName(e.file.name)
    return file
  }

  const handleFormSubmit = (values) => {
    const { StartDate: sd, EndDate: ed, Websites, ImageFile, ...rest } = values

    const formateDate = (s) => `${s.$y}-${s.$M+1}-${s.$D} ${s.$H}:${s.$m}:${s.$s}`

    setLoading(true)
    sendCampaignDetails({ StartDate: formateDate(sd), EndDate: formateDate(ed), Websites: [Websites], Images: [], ...rest })
      .then((response) => {
        const { CampaignID } = response?.data
        console.log(response)

        sendImage({ image: ImageFile, campaign_id: CampaignID })
          .then((response) => {
            const { file_path } = response?.data
            console.log(response)

            sendImageDetails({ new_image_path: file_path, campaign_id: CampaignID })
              .then((response) => {
                console.log(response)

                form.resetFields()
                setImageName('')
                showSuccessMessage()

              })
              .catch((error) => {
                console.log(error)
                showErrorMessage()
              })
              .finally(() => setLoading(false))

          })
          .catch((error) => {
            console.log(error)
            setLoading(false)
            showErrorMessage()
          })

      })
      .catch((error) => {
        console.log(error)
        setLoading(false)
        showErrorMessage()
      })
  }

  const disableStartDate = (current) => {
    // Disable dates in the past (including today)
    return current && current < Date.now();
  };

  const disableEndDate = (current) => {
    const startDate = form.getFieldValue('StartDate')
    // If no start date is selected, don't disable any dates
    if (!startDate) {
      return false;
    }

    return current && current < startDate;
  }

  return (
    <>
      {contextHolder}
      <Layout>
        <Typography.Title level={1} style={{ margin: '0 auto 70px 0' }}>Create Campaign</Typography.Title>
        <Form
          form={form}
          labelCol={{ span: 3 }}
          wrapperCol={{ span: 6 }}
          layout="horizontal"
          size='large'
          onFinish={handleFormSubmit}
        >
          <Form.Item label='Campaign Name' name='CampaignName' rules={[{ required: true }]}>
            <Input placeholder="Loreal Shampoo Advertisement" />
          </Form.Item>
          <Form.Item label='Start Date:' name='StartDate' rules={[{ required: true }]}>
            <DatePicker showTime={{ defaultOpenValue: moment() }} disabledDate={disableStartDate} format='YYYY-MM-DD HH:mm:ss' style={{ width: '100%' }}/>
          </Form.Item>
          <Form.Item label='End Date:' name='EndDate' rules={[{ required: true }]}>
            <DatePicker showTime={{ defaultOpenValue: moment(form.getFieldValue('StartDate')) }} disabledDate={disableEndDate} format='YYYY-MM-DD HH:mm:ss' style={{ width: '100%' }}/>
          </Form.Item>
          <Form.Item label='Interval' name='IntervalTime' rules={[{ required: true }]}>
            <InputNumber placeholder='3 (in Minutes)' style={{ width: '100%' }}/>
          </Form.Item>
          <Form.Item label='Website URL' name='Websites' rules={[{ required: true }]}>
            <Input placeholder='https://www.google.com/' />
          </Form.Item>
          <Form.Item label="Reference Image" name='ImageFile' valuePropName='file' getValueFromEvent={getFile}
            rules={[{ required: true }]}
          >
            <Upload
              customRequest={() => {}}
              listType="picture"
              maxCount={1}
              showUploadList={false}
              >
              <Space style={{ alignItems: 'flex-start' }}>
                <Button icon={<UploadOutlined />}>Upload</Button>
                <Typography.Text>{imageName}</Typography.Text>
              </Space>
            </Upload>
          </Form.Item>
          <Form.Item wrapperCol={{ offset: 3 }}>
            <Button loading={loading} type='primary' htmlType='submit'>Submit</Button>
          </Form.Item>
        </Form>

        {modalContextHolder}
      </Layout>
    </>
  )
}

export default CreateCampaign