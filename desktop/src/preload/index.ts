import { contextBridge, ipcRenderer } from 'electron';

// P0 最小能力集；P3 扩展 restartBackend/pickPath/checkUpdate/exportDiagnostics
contextBridge.exposeInMainWorld('qfsShell', {
  platform: process.platform,
  shellVersion: '1.3.0-alpha.1',
  ping: () => ipcRenderer.invoke('qfs:ping'),
});