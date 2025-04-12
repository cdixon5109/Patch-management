import { configureStore } from '@reduxjs/toolkit';
import { TypedUseSelectorHook, useDispatch, useSelector } from 'react-redux';
import authReducer from './features/auth/authSlice';
import serversReducer from './features/servers/serversSlice';
import patchesReducer from './features/patches/patchesSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    servers: serversReducer,
    patches: patchesReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

export const useAppDispatch = () => useDispatch<AppDispatch>();
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector; 