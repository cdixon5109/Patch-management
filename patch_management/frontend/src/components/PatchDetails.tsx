import React from 'react';
import { useAppDispatch } from '../store';
import { updatePatchStatus } from '../features/patches/patchesSlice';
import {
  Card,
  CardContent,
  Typography,
  Button,
  Grid,
  Chip,
} from '@mui/material';

interface PatchDetailsProps {
  patch: {
    id: string;
    name: string;
    version: string;
    releaseDate: string;
    description: string;
    severity: 'critical' | 'high' | 'medium' | 'low';
    status: 'pending' | 'applied' | 'failed';
  };
}

const PatchDetails: React.FC<PatchDetailsProps> = ({ patch }) => {
  const dispatch = useAppDispatch();

  const handleApplyPatch = () => {
    dispatch(updatePatchStatus({ id: patch.id, status: 'applied' }));
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'error';
      case 'high':
        return 'warning';
      case 'medium':
        return 'info';
      case 'low':
        return 'success';
      default:
        return 'default';
    }
  };

  return (
    <Card>
      <CardContent>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <Typography variant="h5" component="div">
              {patch.name}
            </Typography>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Typography color="text.secondary">Version</Typography>
            <Typography variant="body1">{patch.version}</Typography>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Typography color="text.secondary">Release Date</Typography>
            <Typography variant="body1">{patch.releaseDate}</Typography>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Typography color="text.secondary">Severity</Typography>
            <Chip
              label={patch.severity}
              color={getSeverityColor(patch.severity) as any}
              size="small"
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <Typography color="text.secondary">Status</Typography>
            <Chip
              label={patch.status}
              color={patch.status === 'applied' ? 'success' : 'default'}
              size="small"
            />
          </Grid>
          <Grid item xs={12}>
            <Typography color="text.secondary">Description</Typography>
            <Typography variant="body1">{patch.description}</Typography>
          </Grid>
          {patch.status === 'pending' && (
            <Grid item xs={12}>
              <Button
                variant="contained"
                color="primary"
                onClick={handleApplyPatch}
              >
                Apply Patch
              </Button>
            </Grid>
          )}
        </Grid>
      </CardContent>
    </Card>
  );
};

export default PatchDetails; 