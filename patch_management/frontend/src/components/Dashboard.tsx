import React from 'react';
import { Box, Grid, Paper, Typography } from '@mui/material';
import { useAppSelector } from '../store';
import ServerList from './ServerList';
import PatchList from './PatchList';
import PatchDetails from './PatchDetails';

const Dashboard: React.FC = () => {
  const { selectedServer } = useAppSelector((state) => state.servers);
  const { selectedPatch } = useAppSelector((state) => state.patches);

  return (
    <Box sx={{ flexGrow: 1, p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Patch Management Dashboard
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2, height: '100%' }}>
            <ServerList />
          </Paper>
        </Grid>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2, height: '100%' }}>
            {selectedServer ? (
              <PatchList serverId={selectedServer.id} />
            ) : (
              <Typography>Select a server to view patches</Typography>
            )}
          </Paper>
        </Grid>
        {selectedPatch && (
          <Grid item xs={12}>
            <Paper sx={{ p: 2 }}>
              <PatchDetails patch={selectedPatch} />
            </Paper>
          </Grid>
        )}
      </Grid>
    </Box>
  );
};

export default Dashboard; 