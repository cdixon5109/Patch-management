import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';

interface Patch {
  id: number;
  package_name: string;
  current_version: string;
  available_version: string;
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  status: 'PENDING' | 'APPLIED' | 'FAILED';
  server_id: number;
}

interface PatchesState {
  patches: Patch[];
  loading: boolean;
  error: string | null;
}

const initialState: PatchesState = {
  patches: [],
  loading: false,
  error: null,
};

interface ThunkAPI {
  rejectWithValue: (value: string) => unknown;
}

export const fetchPatches = createAsyncThunk<Patch[], number, { rejectValue: string }>(
  'patches/fetchPatches',
  async (serverId: number, { rejectWithValue }: ThunkAPI) => {
    try {
      const response = await fetch(`/api/servers/${serverId}/patches`);
      if (!response.ok) {
        throw new Error('Failed to fetch patches');
      }
      return await response.json();
    } catch (error) {
      return rejectWithValue(error instanceof Error ? error.message : 'An error occurred');
    }
  }
);

export const applyPatch = createAsyncThunk<Patch, { serverId: number; patchId: number }, { rejectValue: string }>(
  'patches/applyPatch',
  async ({ serverId, patchId }: { serverId: number; patchId: number }, { rejectWithValue }: ThunkAPI) => {
    try {
      const response = await fetch(`/api/servers/${serverId}/patches/${patchId}/apply`, {
        method: 'POST',
      });
      if (!response.ok) {
        throw new Error('Failed to apply patch');
      }
      return await response.json();
    } catch (error) {
      return rejectWithValue(error instanceof Error ? error.message : 'An error occurred');
    }
  }
);

const patchesSlice = createSlice({
  name: 'patches',
  initialState,
  reducers: {},
  extraReducers: (builder: any) => {
    builder
      .addCase(fetchPatches.pending, (state: PatchesState) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchPatches.fulfilled, (state: PatchesState, action: PayloadAction<Patch[]>) => {
        state.loading = false;
        state.patches = action.payload;
      })
      .addCase(fetchPatches.rejected, (state: PatchesState, action: PayloadAction<string | undefined>) => {
        state.loading = false;
        state.error = action.payload || 'An error occurred';
      })
      .addCase(applyPatch.pending, (state: PatchesState) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(applyPatch.fulfilled, (state: PatchesState, action: PayloadAction<Patch>) => {
        state.loading = false;
        const index = state.patches.findIndex(p => p.id === action.payload.id);
        if (index !== -1) {
          state.patches[index] = action.payload;
        }
      })
      .addCase(applyPatch.rejected, (state: PatchesState, action: PayloadAction<string | undefined>) => {
        state.loading = false;
        state.error = action.payload || 'An error occurred';
      });
  },
});

export default patchesSlice.reducer; 