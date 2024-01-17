
import Dashboard from "views/Dashboard.js";

import TableList from "views/TableList.js";

import UserPage from "views/UserPage.js";

var dashRoutes = [
  {
    path: "/dashboard",
    name: "Dashboard",
    icon: "design_app",
    component: <Dashboard />,
    layout: "/admin",
  },
  {
    path: "/user-page",
    name: "scheduling information",
    icon: "users_single-02",
    component: <UserPage />,
    layout: "/admin",
  },
  {
    path: "/extended-tables",
    name: "report",
    icon: "files_paper",
    component: <TableList />,
    layout: "/admin",
  },


 
];
export default dashRoutes;
