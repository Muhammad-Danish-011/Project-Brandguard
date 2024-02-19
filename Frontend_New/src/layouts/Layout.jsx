import React, { useState } from 'react';
import {
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  UploadOutlined,
  UserOutlined,
  VideoCameraOutlined,
} from '@ant-design/icons';
import { Layout as AntLayout, Menu, Button, theme, Flex } from 'antd';
import logo from '../assets/brandguard_logo_black.png'
import { useLocation, useNavigate } from 'react-router-dom';
const { Header, Sider, Content, Footer } = AntLayout;


const pathMappings = new Map()
pathMappings.set('/', 'dashboard')
pathMappings.set('/campaigns', 'campaigns')

const Layout = ({ children }) => {

  const [collapsed, setCollapsed] = useState(false);
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

  const { pathname } = useLocation()

  const navigate = useNavigate()

  return (
    <AntLayout>
      <Sider trigger={null} collapsible collapsed={collapsed} theme='light' width={260}>
        <Flex style={{ height: '64px' }} justify={collapsed ? 'center' : 'flex-start'} align='center'>
          {collapsed? <strong>BG</strong> : <img src={logo} alt='logo' style={{ width: '180px', marginLeft: '24px' }} />}
        </Flex>
        <Menu
          theme="light"
          mode="vertical"
          defaultSelectedKeys={[pathMappings.get(pathname)]}
          items={[
            {
              key: 'dashboard',
              icon: <UserOutlined />,
              label: 'Dashboard',
              onClick: () => navigate('/')
            },
            {
              key: 'create-campaign',
              icon: <VideoCameraOutlined />,
              label: 'Create Campaign',
            },
            {
              key: 'campaigns',
              icon: <UploadOutlined />,
              label: 'Campaigns',
              onClick: () => navigate('/campaigns')
            },
          ]}
        />
      </Sider>
      <AntLayout>
        <Header
          style={{
            padding: 0,
            background: colorBgContainer,
          }}
        >
          <Button
            type="text"
            icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
            onClick={() => setCollapsed(!collapsed)}
            style={{
              fontSize: '16px',
              width: 64,
              height: 64,
            }}
          />
        </Header>
        <Content
          style={{
            margin: '24px 24px 0',
            padding: 48,
            minHeight: 1000,
            background: colorBgContainer,
            borderRadius: 15,
          }}
        >
          {children}
        </Content>
        <Footer style={{ textAlign: 'center' }}>
          BrandGuard © {new Date().getFullYear()}
        </Footer>
      </AntLayout>
    </AntLayout>
  )
}

export default Layout