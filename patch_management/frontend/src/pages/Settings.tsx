import React from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  TextField,
  Button,
  Switch,
  FormControlLabel,
  Divider,
  Alert
} from '@mui/material';
import { Save as SaveIcon } from '@mui/icons-material';

const Settings = () => {
  // Mock data - in real app, this would come from Redux store
  const settings = {
    scanInterval: 24,
    emailNotifications: true,
    emailAddress: 'admin@example.com',
    smtpServer: 'smtp.example.com',
    smtpPort: 587,
    smtpUsername: 'admin@example.com',
    smtpPassword: '********',
    retentionDays: 30,
    maxConcurrentScans: 5
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Settings
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Scan Settings
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Scan Interval (hours)"
                  type="number"
                  value={settings.scanInterval}
                  InputProps={{ inputProps: { min: 1, max: 168 } }}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Max Concurrent Scans"
                  type="number"
                  value={settings.maxConcurrentScans}
                  InputProps={{ inputProps: { min: 1, max: 10 } }}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Data Retention (days)"
                  type="number"
                  value={settings.retentionDays}
                  InputProps={{ inputProps: { min: 1, max: 365 } }}
                />
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Email Notifications
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.emailNotifications}
                      color="primary"
                    />
                  }
                  label="Enable Email Notifications"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Email Address"
                  type="email"
                  value={settings.emailAddress}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="SMTP Server"
                  value={settings.smtpServer}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="SMTP Port"
                  type="number"
                  value={settings.smtpPort}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="SMTP Username"
                  value={settings.smtpUsername}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="SMTP Password"
                  type="password"
                  value={settings.smtpPassword}
                />
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              System Information
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="API Version"
                  value="1.0.0"
                  disabled
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="UI Version"
                  value="1.0.0"
                  disabled
                />
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
            <Button
              variant="contained"
              color="primary"
              startIcon={<SaveIcon />}
            >
              Save Settings
            </Button>
          </Box>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Settings; 