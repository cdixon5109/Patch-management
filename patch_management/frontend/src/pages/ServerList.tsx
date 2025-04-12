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
  Tooltip
} from '@mui/material';
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
  Add as AddIcon,
  Refresh as RefreshIcon
} from '@mui/icons-material';

const ServerList = () => {
  // Mock data - in real app, this would come from Redux store
  const servers = [
    {
      id: 1,
      hostname: 'server1.example.com',
      ip: '192.168.1.101',
      os: 'Rocky Linux 9',
      status: 'online',
      lastScan: '2024-02-20 10:30:00',
      patches: {
        critical: 2,
        high: 3,
        medium: 5,
        low: 2
      }
    },
    {
      id: 2,
      hostname: 'server2.example.com',
      ip: '192.168.1.102',
      os: 'Rocky Linux 9',
      status: 'offline',
      lastScan: '2024-02-19 15:45:00',
      patches: {
        critical: 1,
        high: 2,
        medium: 3,
        low: 1
      }
    }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'online':
        return 'success';
      case 'offline':
        return 'error';
      case 'maintenance':
        return 'warning';
      default:
        return 'default';
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h4">Servers</Typography>
        <Box>
          <Tooltip title="Add Server">
            <IconButton color="primary">
              <AddIcon />
            </IconButton>
          </Tooltip>
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
              <TableCell>Hostname</TableCell>
              <TableCell>IP Address</TableCell>
              <TableCell>OS</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Last Scan</TableCell>
              <TableCell>Patches</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {servers.map((server) => (
              <TableRow key={server.id}>
                <TableCell>{server.hostname}</TableCell>
                <TableCell>{server.ip}</TableCell>
                <TableCell>{server.os}</TableCell>
                <TableCell>
                  <Chip
                    label={server.status}
                    color={getStatusColor(server.status)}
                    size="small"
                  />
                </TableCell>
                <TableCell>{server.lastScan}</TableCell>
                <TableCell>
                  <Box sx={{ display: 'flex', gap: 1 }}>
                    <Chip
                      label={`C: ${server.patches.critical}`}
                      color="error"
                      size="small"
                    />
                    <Chip
                      label={`H: ${server.patches.high}`}
                      color="warning"
                      size="small"
                    />
                    <Chip
                      label={`M: ${server.patches.medium}`}
                      color="info"
                      size="small"
                    />
                    <Chip
                      label={`L: ${server.patches.low}`}
                      color="success"
                      size="small"
                    />
                  </Box>
                </TableCell>
                <TableCell>
                  <Tooltip title="Edit">
                    <IconButton size="small">
                      <EditIcon />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Delete">
                    <IconButton size="small" color="error">
                      <DeleteIcon />
                    </IconButton>
                  </Tooltip>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default ServerList; 