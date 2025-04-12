import React from 'react';
import { Grid, Paper, Typography, Box } from '@mui/material';
import {
  Storage as ServerIcon,
  Security as PatchIcon,
  Warning as CriticalIcon,
  Error as HighIcon,
  Info as MediumIcon,
  LowPriority as LowIcon
} from '@mui/icons-material';

const Dashboard = () => {
  // Mock data - in real app, this would come from Redux store
  const stats = {
    totalServers: 12,
    onlineServers: 10,
    totalPatches: 45,
    criticalPatches: 5,
    highPatches: 10,
    mediumPatches: 20,
    lowPatches: 10
  };

  const StatCard = ({ title, value, icon: Icon, color }: any) => (
    <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <Icon sx={{ fontSize: 40, color }} />
      <Typography variant="h4" component="div" sx={{ mt: 1 }}>
        {value}
      </Typography>
      <Typography color="text.secondary">{title}</Typography>
    </Paper>
  );

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Servers"
            value={stats.totalServers}
            icon={ServerIcon}
            color="primary"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Online Servers"
            value={stats.onlineServers}
            icon={ServerIcon}
            color="success"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Patches"
            value={stats.totalPatches}
            icon={PatchIcon}
            color="info"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Critical Patches"
            value={stats.criticalPatches}
            icon={CriticalIcon}
            color="error"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="High Patches"
            value={stats.highPatches}
            icon={HighIcon}
            color="warning"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Medium Patches"
            value={stats.mediumPatches}
            icon={MediumIcon}
            color="info"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Low Patches"
            value={stats.lowPatches}
            icon={LowIcon}
            color="success"
          />
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard; 