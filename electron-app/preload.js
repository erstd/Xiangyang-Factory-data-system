const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  // 可以在这里暴露需要的 Electron API
  platform: process.platform
});
