// assets
import { LineChartOutlined, BarChartOutlined, PieChartOutlined } from '@ant-design/icons';

// icons
const icons = {
    LineChartOutlined,
    BarChartOutlined,
    PieChartOutlined
};

// ==============================|| MENU ITEMS - DASHBOARD ||============================== //

const Report= {
  id: 'group-dashboard',
  title: 'Reports',
  type: 'group',
  children: [
    {
      id: 'Scraping-Report',
      title: 'Reporting',
      type: 'item',
      url: '/Scraping-Report',
      icon: icons.LineChartOutlined,
      breadcrumbs: false
    },
    // {
    //   id: 'Screenshots-Report',
    //   title: 'Screenshots Report',
    //   type: 'item',
    //   url: '/Screenshots-Report',
    //   icon: icons.BarChartOutlined,
    //   breadcrumbs: false
    // }

  ]
};

export default Report;
