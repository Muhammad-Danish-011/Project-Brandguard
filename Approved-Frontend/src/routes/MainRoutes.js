import { lazy } from "react";

// project import
import Loadable from "components/Loadable";
import MainLayout from "layout/MainLayout";
import Register from "pages/Schedule-Information/Register.js";
import ScrapingReport from "../pages/Report/Scraping-Report";
import ScreeningReport from "../pages/Report/Screenshots-Report";
// render - dashboard
const DashboardDefault = Loadable(lazy(() => import("pages/dashboard")));

// render - utilities

//const Register = Loadable(lazy(() => import('../../src/pages/Schedule-Information/Register.js')));

// ==============================|| MAIN ROUTING ||============================== //

const MainRoutes = {
  path: "/",
  element: <MainLayout />,
  children: [
    {
      path: "/",
      element: <DashboardDefault />,
    },
    {
      path: "/Schedule-Information/Register",
      element: <Register />,
    },
    {
      path: "/Scraping-Report",
      element: <ScrapingReport/>,
    },
    {
      path: "/Screenshots-Report",
      element: <ScreeningReport />,
    },

    {
      path: "dashboard",
      children: [
        {
          path: "default",
          element: <DashboardDefault />,
        },
      ],
    },
  ],
};

export default MainRoutes;
