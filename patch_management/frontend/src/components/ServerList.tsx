import React, { useEffect } from 'react';
import { useAppDispatch, useAppSelector } from '../store';
import { fetchServersStart, selectServer } from '../features/servers/serversSlice';
import { List, ListItem, ListItemText, ListItemButton, CircularProgress, Typography } from '@mui/material';

const ServerList: React.FC = () => {
  const dispatch = useAppDispatch();
  const { servers, loading, error, selectedServer } = useAppSelector((state) => state.servers);

  useEffect(() => {
    dispatch(fetchServersStart());
  }, [dispatch]);

  if (loading) {
    return <CircularProgress />;
  }

  if (error) {
    return <Typography color="error">{error}</Typography>;
  }

  return (
    <List>
      {servers.map((server) => (
        <ListItem key={server.id} disablePadding>
          <ListItemButton
            selected={selectedServer?.id === server.id}
            onClick={() => dispatch(selectServer(server))}
          >
            <ListItemText
              primary={server.name}
              secondary={`Status: ${server.status} | IP: ${server.ipAddress}`}
            />
          </ListItemButton>
        </ListItem>
      ))}
    </List>
  );
};

export default ServerList; 