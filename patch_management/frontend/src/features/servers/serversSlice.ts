import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

interface Server {
  id: number;
  name: string;
  ip_address: string;
  status: 'ONLINE' | 'OFFLINE' | 'MAINTENANCE';
  os_version: string;
  last_checked: string;
}

interface ServersState {
  servers: Server[];
  loading: boolean;
  error: string | null;
}

const initialState: ServersState = {
  servers: [],
  loading: false,
  error: null,
};

export const fetchServers = createAsyncThunk(
  'servers/fetchServers',
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch('/api/servers');
      if (!response.ok) {
        throw new Error('Failed to fetch servers');
      }
      return await response.json();
    } catch (error) {
      return rejectWithValue(error instanceof Error ? error.message : 'An error occurred');
    }
  }
);

const serversSlice = createSlice({
  name: 'servers',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchServers.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchServers.fulfilled, (state, action) => {
        state.loading = false;
        state.servers = action.payload;
      })
      .addCase(fetchServers.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

export default serversSlice.reducer; 