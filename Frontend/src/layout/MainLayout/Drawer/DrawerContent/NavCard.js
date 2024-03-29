// material-ui
import {  Stack, Typography } from '@mui/material';

// project import
import MainCard from 'components/MainCard';

// assets

// ==============================|| DRAWER CONTENT - NAVIGATION CARD ||============================== //

const NavCard = () => (
  <MainCard sx={{ bgcolor: 'grey.50', m: 3 }}>
    <Stack alignItems="center" spacing={2.5}>
     
      <Stack alignItems="center">
        <Typography variant="h5"></Typography>
        <Typography variant="h6" color="secondary">
         
        </Typography>
      </Stack>
     
    </Stack>
  </MainCard>
);

export default NavCard;
