// src/services/supabase.js
// ✅ 已修复：兼容 CommonJS 环境，不使用 import.meta.env

// 🔧 修改 1：使用 require 替代 import（兼容 CommonJS）
const { createClient } = require('@supabase/supabase-js')

// 🔧 修改 2：从配置文件读取环境变量（替代 import.meta.env）
const env = require('../config/env.js')

// 从环境变量获取配置
const supabaseUrl = env.SUPABASE_URL
const supabaseAnonKey = env.SUPABASE_ANON_KEY

// 创建 Supabase 客户端
const supabase = createClient(supabaseUrl, supabaseAnonKey)

// 表名常量
const TABLES = {
  GREETINGS: 'greetings',
  PHOTOS: 'photos'
}

/**
 * 保存祝福
 */
async function saveGreeting(data) {
  try {
    const { data: result, error } = await supabase
      .from(TABLES.GREETINGS)
      .insert([
        {
          template_id: data.templateId,
          message: data.message,
          sender_name: data.senderName || '匿名',
          recipient_name: data.recipientName || '所有人',
          background_style: data.backgroundStyle || 'default'
        }
      ])
      .select()

    if (error) throw error

    return {
      success: true,
      id: result[0].id,
      data: result[0]
    }
  } catch (error) {
    console.error('保存祝福失败:', error)
    return {
      success: false,
      error: error.message
    }
  }
}

/**
 * 获取祝福列表
 */
async function getGreetings(limit = 100) {
  try {
    const { data, error } = await supabase
      .from(TABLES.GREETINGS)
      .select('*')
      .order('created_at', { ascending: false })
      .limit(limit)

    if (error) throw error

    return {
      success: true,
      data: data || []
    }
  } catch (error) {
    console.error('获取祝福列表失败:', error)
    return {
      success: false,
      error: error.message
    }
  }
}

/**
 * 上传年夜饭照片
 */
async function uploadPhoto(data) {
  try {
    // 1. 上传图片文件到 Supabase Storage
    let fileUrl = ''
    let filePath = ''

    if (data.file) {
      const fileName = `photo_${Date.now()}_${Math.random().toString(36).substring(7)}.jpg`
      const { data: uploadData, error: uploadError } = await supabase.storage
        .from('dinner-photos')
        .upload(fileName, data.file)

      if (uploadError) throw uploadError

      filePath = uploadData.path

      // 获取公开 URL
      const { data: { publicUrl } } = supabase.storage
        .from('dinner-photos')
        .getPublicUrl(fileName)

      fileUrl = publicUrl
    }

    // 2. 保存照片信息到数据库
    const { data: result, error } = await supabase
      .from(TABLES.PHOTOS)
      .insert([
        {
          image_url: fileUrl,
          image_path: filePath,
          uploader_name: data.uploaderName || '匿名',
          message: data.message || '',
          is_public: data.isPublic !== false
        }
      ])
      .select()

    if (error) throw error

    return {
      success: true,
      id: result[0].id,
      data: result[0]
    }
  } catch (error) {
    console.error('保存照片信息失败:', error)
    return {
      success: false,
      error: error.message
    }
  }
}

/**
 * 获取年夜饭照片列表
 */
async function getPhotos(limit = 100, onlyPublic = true) {
  try {
    let query = supabase
      .from(TABLES.PHOTOS)
      .select('*')
      .order('created_at', { ascending: false })
      .limit(limit)

    if (onlyPublic) {
      query = query.eq('is_public', true)
    }

    const { data, error } = await query

    if (error) throw error

    return {
      success: true,
      data: data || []
    }
  } catch (error) {
    console.error('获取照片列表失败:', error)
    return {
      success: false,
      error: error.message
    }
  }
}

/**
 * 获取统计数据
 */
async function getStats() {
  try {
    const [greetingsResult, photosResult] = await Promise.all([
      supabase.from(TABLES.GREETINGS).select('*', { count: 'exact', head: true }),
      supabase.from(TABLES.PHOTOS).select('*', { count: 'exact', head: true })
    ])

    return {
      success: true,
      data: {
        greetingsCount: greetingsResult.count || 0,
        photosCount: photosResult.count || 0
      }
    }
  } catch (error) {
    console.error('获取统计数据失败:', error)
    return {
      success: false,
      error: error.message
    }
  }
}

// 🔧 修改 3：使用 CommonJS 导出（替代 export）
module.exports = {
  supabase,
  saveGreeting,
  getGreetings,
  uploadPhoto,
  getPhotos,
  getStats
}
