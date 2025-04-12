import { configureStore } from '@reduxjs/toolkit';
import authReducer from '../features/auth/authSlice';
import serversReducer from '../features/servers/serversSlice';
import patchesReducer from '../features/patches/patchesSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    servers: serversReducer,
    patches: patchesReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch; 