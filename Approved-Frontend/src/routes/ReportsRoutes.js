
// project import
import ScrapingReport from "../pages/Report/Scraping-Report";
import ScreeningReport from "../pages/Report/Screenshots-Report";
// ==============================|| MAIN ROUTING ||============================== //

const ReportsRoutes = {
  path: "/",
 // element: <Reports />,
  children: [
    {
      path: "/Scraping-Report",
      element: <ScrapingReport/>,
    },
    {
      path: "/Screenshots-Report",
      element: <ScreeningReport />,
    },
   
  ],
};

export default ReportsRoutes;
