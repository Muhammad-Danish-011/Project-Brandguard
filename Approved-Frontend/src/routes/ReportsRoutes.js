
// project import
import ScrapingReport from "../pages/Report/Reports";
import ScreeningReport from "../pages/Report/ScreenshotDetails";
import DetailPage from "../pages/Report/ScreenshotDetails";
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
