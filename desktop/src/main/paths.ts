import { app } from 'electron';
import * as path from 'path';
import * as os from 'os';

/**
 * 跨平台解析用户数据目录、运行时目录、业务代码目录。
 * 与 docs/桌面客户端打包方案.md §3.2 保持一致。
 */

export interface ResolvedPaths {
  installDir: string;       // app 父目录
  resourcesDir: string;      // process.resourcesPath
  userData: string;          // app.getPath('userData')
  runtimeDir: string;        // userData/runtime
  dataDir: string;           // userData/data  ← SAU_DATA_DIR
  logsDir: string;           // userData/logs
  appCodeDir: string;        // userData/app-code
  runtimeSeed: string;       // resources/runtime-seed（只读）
}

let cached: ResolvedPaths | null = null;

export function resolvePaths(): ResolvedPaths {
  if (cached) return cached;
  const userData = app.getPath('userData');
  const resourcesDir = process.resourcesPath;
  const installDir = path.dirname(resourcesDir);
  cached = {
    installDir,
    resourcesDir,
    userData,
    runtimeDir: path.join(userData, 'runtime'),
    dataDir: path.join(userData, 'data'),
    logsDir: path.join(userData, 'logs'),
    appCodeDir: path.join(userData, 'app-code'),
    runtimeSeed: path.join(resourcesDir, 'runtime-seed'),
  };
  return cached;
}

export function pickPort(): number {
  return 5409;
}

export function ts(): string {
  return new Date().toISOString().replace('T', ' ').slice(0, 19);
}

export function dumpPaths(): string {
  const p = resolvePaths();
  return [
    `installDir   = ${p.installDir}`,
    `resourcesDir = ${p.resourcesDir}`,
    `userData     = ${p.userData}`,
    `runtimeDir   = ${p.runtimeDir}`,
    `runtimeSeed  = ${p.runtimeSeed}`,
    `os.tmpdir()  = ${os.tmpdir()}`,
  ].join('\n');
}