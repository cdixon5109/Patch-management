import React from 'react';
import {
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  LinearProgress,
} from '@mui/material';
import {
  Storage as ServerIcon,
  Security as PatchIcon,
  Warning as CriticalIcon,
  Error as HighIcon,
  Info as MediumIcon,
} from '@mui/icons-material';
import { useSelector } from 'react-redux';
import { RootState } from '../../app/store';

export default function Dashboard() {
  const { servers, patches } = useSelector((state: RootState) => ({
    servers: state.servers.servers,
    patches: state.patches.patches,
  }));

  const totalServers = servers.length;
  const totalPatches = patches.length;
  const criticalPatches = patches.filter(p => p.severity === 'CRITICAL').length;
  const highPatches = patches.filter(p => p.severity === 'HIGH').length;
  const mediumPatches = patches.filter(p => p.severity === 'MEDIUM').length;

  const StatCard = ({ title, value, icon, color }: { title: string; value: number; icon: React.ReactNode; color: string }) => (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Box display="flex" alignItems="center" mb={2}>
          <Box
            sx={{
              backgroundColor: `${color}20`,
              borderRadius: '50%',
              p: 1,
              mr: 2,
            }}
          >
            {icon}
          </Box>
          <Typography variant="h6" component="div">
            {title}
          </Typography>
        </Box>
        <Typography variant="h4" component="div">
          {value}
        </Typography>
      </CardContent>
    </Card>
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
            value={totalServers}
            icon={<ServerIcon sx={{ color: '#2196f3' }} />}
            color="#2196f3"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Patches"
            value={totalPatches}
            icon={<PatchIcon sx={{ color: '#4caf50' }} />}
            color="#4caf50"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Critical Patches"
            value={criticalPatches}
            icon={<CriticalIcon sx={{ color: '#f44336' }} />}
            color="#f44336"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="High Patches"
            value={highPatches}
            icon={<HighIcon sx={{ color: '#ff9800' }} />}
            color="#ff9800"
          />
        </Grid>
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Patch Distribution
            </Typography>
            <Box sx={{ width: '100%', mb: 2 }}>
              <Box display="flex" alignItems="center" mb={1}>
                <CriticalIcon sx={{ color: '#f44336', mr: 1 }} />
                <Typography variant="body2" sx={{ flexGrow: 1 }}>
                  Critical
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {criticalPatches}
                </Typography>
              </Box>
              <LinearProgress
                variant="determinate"
                value={(criticalPatches / totalPatches) * 100}
                sx={{
                  height: 10,
                  borderRadius: 5,
                  backgroundColor: '#f4433620',
                  '& .MuiLinearProgress-bar': {
                    backgroundColor: '#f44336',
                  },
                }}
              />
            </Box>
            <Box sx={{ width: '100%', mb: 2 }}>
              <Box display="flex" alignItems="center" mb={1}>
                <HighIcon sx={{ color: '#ff9800', mr: 1 }} />
                <Typography variant="body2" sx={{ flexGrow: 1 }}>
                  High
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {highPatches}
                </Typography>
              </Box>
              <LinearProgress
                variant="determinate"
                value={(highPatches / totalPatches) * 100}
                sx={{
                  height: 10,
                  borderRadius: 5,
                  backgroundColor: '#ff980020',
                  '& .MuiLinearProgress-bar': {
                    backgroundColor: '#ff9800',
                  },
                }}
              />
            </Box>
            <Box sx={{ width: '100%' }}>
              <Box display="flex" alignItems="center" mb={1}>
                <MediumIcon sx={{ color: '#2196f3', mr: 1 }} />
                <Typography variant="body2" sx={{ flexGrow: 1 }}>
                  Medium
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {mediumPatches}
                </Typography>
              </Box>
              <LinearProgress
                variant="determinate"
                value={(mediumPatches / totalPatches) * 100}
                sx={{
                  height: 10,
                  borderRadius: 5,
                  backgroundColor: '#2196f320',
                  '& .MuiLinearProgress-bar': {
                    backgroundColor: '#2196f3',
                  },
                }}
              />
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
} 