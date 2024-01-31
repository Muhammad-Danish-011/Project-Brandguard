
// project import
import ScrapingReport from "../pages/Report/Scraping-Report";
import ScreeningReport from "../pages/Report/Details";
import DetailPage from "../pages/Report/Details";
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
    {
      path: "/details/:campaignId" ,
      element: <DetailPage />
    }
   
  ],
};

export default ReportsRoutes;
