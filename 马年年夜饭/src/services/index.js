// 服务配置 - 使用 localStorage 进行测试
// 如需使用 Supabase，请在各个视图文件中直接导入 supabase.js

console.log('🧪 使用本地存储模式（用于测试）')

// 导出 localStorage 服务
export * from './local-storage.js'
export { default } from './local-storage.js'
