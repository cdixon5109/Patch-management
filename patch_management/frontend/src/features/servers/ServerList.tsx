import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
  Box,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  Chip,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  Refresh as RefreshIcon,
  Security as PatchIcon,
  Computer as ServerIcon,
} from '@mui/icons-material';
import { RootState } from '../../app/store';
import { fetchServers } from './serversSlice';

export default function ServerList() {
  const dispatch = useDispatch();
  const { servers, loading, error } = useSelector((state: RootState) => state.servers);

  useEffect(() => {
    dispatch(fetchServers());
  }, [dispatch]);

  const handleRefresh = () => {
    dispatch(fetchServers());
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Servers</Typography>
        <Tooltip title="Refresh">
          <IconButton onClick={handleRefresh}>
            <RefreshIcon />
          </IconButton>
        </Tooltip>
      </Box>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>IP Address</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>OS</TableCell>
              <TableCell>Last Checked</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {servers.map((server) => (
              <TableRow key={server.id}>
                <TableCell>
                  <Box display="flex" alignItems="center">
                    <ServerIcon sx={{ mr: 1 }} />
                    {server.name}
                  </Box>
                </TableCell>
                <TableCell>{server.ip_address}</TableCell>
                <TableCell>
                  <Chip
                    label={server.status}
                    color={
                      server.status === 'ONLINE'
                        ? 'success'
                        : server.status === 'OFFLINE'
                        ? 'error'
                        : 'warning'
                    }
                  />
                </TableCell>
                <TableCell>{server.os_version}</TableCell>
                <TableCell>
                  {new Date(server.last_checked).toLocaleString()}
                </TableCell>
                <TableCell>
                  <Tooltip title="View Patches">
                    <IconButton
                      onClick={() => window.location.href = `/patches?server=${server.id}`}
                    >
                      <PatchIcon />
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
} 