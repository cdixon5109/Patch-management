import React from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Typography,
  Box,
  Chip,
  IconButton,
  Tooltip,
  Button
} from '@mui/material';
import {
  Security as PatchIcon,
  Warning as CriticalIcon,
  Error as HighIcon,
  Info as MediumIcon,
  LowPriority as LowIcon,
  Refresh as RefreshIcon,
  CheckCircle as ApplyIcon
} from '@mui/icons-material';

const PatchList = () => {
  // Mock data - in real app, this would come from Redux store
  const patches = [
    {
      id: 1,
      package: 'kernel',
      currentVersion: '5.14.0-284.11.1.el9_2',
      availableVersion: '5.14.0-284.18.1.el9_2',
      severity: 'CRITICAL',
      status: 'PENDING',
      server: 'server1.example.com',
      description: 'Kernel security update'
    },
    {
      id: 2,
      package: 'openssl',
      currentVersion: '3.0.1-43.el9_0',
      availableVersion: '3.0.1-47.el9_0',
      severity: 'HIGH',
      status: 'PENDING',
      server: 'server1.example.com',
      description: 'OpenSSL security update'
    },
    {
      id: 3,
      package: 'systemd',
      currentVersion: '250-12.el9_2.1',
      availableVersion: '250-12.el9_2.3',
      severity: 'MEDIUM',
      status: 'PENDING',
      server: 'server2.example.com',
      description: 'Systemd bug fix update'
    }
  ];

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'CRITICAL':
        return <CriticalIcon color="error" />;
      case 'HIGH':
        return <HighIcon color="warning" />;
      case 'MEDIUM':
        return <MediumIcon color="info" />;
      case 'LOW':
        return <LowIcon color="success" />;
      default:
        return <PatchIcon />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'PENDING':
        return 'warning';
      case 'APPLIED':
        return 'success';
      case 'FAILED':
        return 'error';
      default:
        return 'default';
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h4">Patches</Typography>
        <Box>
          <Tooltip title="Refresh">
            <IconButton color="primary">
              <RefreshIcon />
            </IconButton>
          </Tooltip>
        </Box>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Package</TableCell>
              <TableCell>Current Version</TableCell>
              <TableCell>Available Version</TableCell>
              <TableCell>Severity</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Server</TableCell>
              <TableCell>Description</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {patches.map((patch) => (
              <TableRow key={patch.id}>
                <TableCell>{patch.package}</TableCell>
                <TableCell>{patch.currentVersion}</TableCell>
                <TableCell>{patch.availableVersion}</TableCell>
                <TableCell>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    {getSeverityIcon(patch.severity)}
                    <Typography>{patch.severity}</Typography>
                  </Box>
                </TableCell>
                <TableCell>
                  <Chip
                    label={patch.status}
                    color={getStatusColor(patch.status)}
                    size="small"
                  />
                </TableCell>
                <TableCell>{patch.server}</TableCell>
                <TableCell>{patch.description}</TableCell>
                <TableCell>
                  <Button
                    variant="contained"
                    color="primary"
                    size="small"
                    startIcon={<ApplyIcon />}
                    disabled={patch.status === 'APPLIED'}
                  >
                    Apply
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default PatchList; 