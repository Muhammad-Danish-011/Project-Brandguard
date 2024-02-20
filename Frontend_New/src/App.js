import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './App.css';
import Dashboard from './pages/dashboard/Dashboard';
import Campaigns from './pages/campaigns/Campaigns';
import CampaignDetails from './pages/campaign-details/CampaignDetails';
import CreateCampaign from './pages/create-campaign/CreateCampaign';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Dashboard/>}/>
        <Route path='/campaigns' element={<Campaigns/>}/>
        <Route path='/campaigns/create' element={<CreateCampaign/>}/>
        <Route path='/campaigns/:campaignId' element={<CampaignDetails/>}/>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
