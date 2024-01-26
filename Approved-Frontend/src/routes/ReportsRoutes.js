
// project import
import Report1 from "../pages/Report/Scraping-Report";
import Report2 from "../pages/Report/Screenshots-Report";

//const Register = Loadable(lazy(() => import('../../src/pages/Schedule-Information/Register.js')));

// ==============================|| MAIN ROUTING ||============================== //

const Reports = {
  path: "/",
  element: <Reports />,
  children: [
    {
      path: "/",
      element: <Report1 />,
    },
    {
      path: "/",
      element: <Report2 />,
    },
   
  ],
};

export default Reports;
