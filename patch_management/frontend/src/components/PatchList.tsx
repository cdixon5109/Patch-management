import React, { useEffect } from 'react';
import { useAppDispatch, useAppSelector } from '../store';
import { fetchPatchesStart, selectPatch } from '../features/patches/patchesSlice';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  CircularProgress,
  Typography,
} from '@mui/material';

interface PatchListProps {
  serverId: string;
}

const PatchList: React.FC<PatchListProps> = ({ serverId }) => {
  const dispatch = useAppDispatch();
  const { patches, loading, error, selectedPatch } = useAppSelector((state) => state.patches);

  useEffect(() => {
    dispatch(fetchPatchesStart());
  }, [dispatch, serverId]);

  const serverPatches = patches.filter((patch) => patch.serverId === serverId);

  if (loading) {
    return <CircularProgress />;
  }

  if (error) {
    return <Typography color="error">{error}</Typography>;
  }

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Name</TableCell>
            <TableCell>Version</TableCell>
            <TableCell>Severity</TableCell>
            <TableCell>Status</TableCell>
            <TableCell>Release Date</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {serverPatches.map((patch) => (
            <TableRow
              key={patch.id}
              hover
              selected={selectedPatch?.id === patch.id}
              onClick={() => dispatch(selectPatch(patch))}
            >
              <TableCell>{patch.name}</TableCell>
              <TableCell>{patch.version}</TableCell>
              <TableCell>{patch.severity}</TableCell>
              <TableCell>{patch.status}</TableCell>
              <TableCell>{patch.releaseDate}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default PatchList; 