// 临时版本：使用 localStorage 存储数据
// 用于在没有配置 Supabase 时测试功能

// 模拟延迟
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms))

// 生成唯一ID
const generateId = () => Date.now().toString(36) + Math.random().toString(36).substring(2)

/**
 * 保存祝福
 */
export async function saveGreeting(data) {
  await delay(500) // 模拟网络延迟

  try {
    const greetings = JSON.parse(localStorage.getItem('greetings') || '[]')

    const newGreeting = {
      id: generateId(),
      template_id: data.templateId,
      message: data.message,
      sender_name: data.senderName || '匿名',
      recipient_name: data.recipientName || '所有人',
      background_style: data.backgroundStyle || 'default',
      created_at: new Date().toISOString()
    }

    greetings.unshift(newGreeting)
    localStorage.setItem('greetings', JSON.stringify(greetings))

    return {
      success: true,
      id: newGreeting.id,
      data: newGreeting
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
export async function getGreetings(limit = 100) {
  await delay(300)

  try {
    const greetings = JSON.parse(localStorage.getItem('greetings') || '[]')

    // 如果没有数据，添加一些示例数据
    if (greetings.length === 0) {
      const sampleGreetings = [
        {
          id: generateId(),
          template_id: 1,
          message: '龙马精神迎新春，马到成功行大运！愿大家在新的一年里身体健康，万事如意！',
          sender_name: '小明',
          recipient_name: '所有人',
          background_style: 'default',
          created_at: new Date(Date.now() - 3600000).toISOString()
        },
        {
          id: generateId(),
          template_id: 2,
          message: '马年大吉！祝您和家人新春快乐，阖家幸福，财源广进！',
          sender_name: '小红',
          recipient_name: '亲朋好友',
          background_style: 'default',
          created_at: new Date(Date.now() - 7200000).toISOString()
        },
        {
          id: generateId(),
          template_id: 3,
          message: '新春佳节到，祝福送上门：一祝身体棒，二祝心情好，三祝财运旺！',
          sender_name: '老王',
          recipient_name: '所有朋友',
          background_style: 'default',
          created_at: new Date(Date.now() - 10800000).toISOString()
        }
      ]

      localStorage.setItem('greetings', JSON.stringify(sampleGreetings))

      return {
        success: true,
        data: sampleGreetings.slice(0, limit)
      }
    }

    return {
      success: true,
      data: greetings.slice(0, limit)
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
export async function uploadPhoto(data) {
  await delay(800) // 模拟上传延迟

  try {
    const photos = JSON.parse(localStorage.getItem('photos') || '[]')

    // 将图片转换为 base64 存储（仅用于测试）
    const reader = new FileReader()

    const imageUrl = await new Promise((resolve, reject) => {
      reader.onload = (e) => resolve(e.target.result)
      reader.onerror = reject
      reader.readAsDataURL(data.file)
    })

    const newPhoto = {
      id: generateId(),
      image_url: imageUrl,
      uploader_name: data.uploaderName || '匿名',
      message: data.message || '',
      is_public: data.isPublic !== false,
      created_at: new Date().toISOString()
    }

    photos.unshift(newPhoto)
    localStorage.setItem('photos', JSON.stringify(photos))

    return {
      success: true,
      id: newPhoto.id,
      data: newPhoto
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
export async function getPhotos(limit = 100, onlyPublic = true) {
  await delay(300)

  try {
    let photos = JSON.parse(localStorage.getItem('photos') || '[]')

    // 如果没有数据，添加示例数据（使用占位图）
    if (photos.length === 0) {
      const samplePhotos = [
        {
          id: generateId(),
          image_url: 'https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=600',
          uploader_name: '美食家小张',
          message: '今年的年夜饭真丰盛！家人团聚，其乐融融 🧧',
          is_public: true,
          created_at: new Date(Date.now() - 3600000).toISOString()
        },
        {
          id: generateId(),
          image_url: 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=600',
          uploader_name: '厨神老李',
          message: '亲手做的年夜饭，满满的都是爱 ❤️',
          is_public: true,
          created_at: new Date(Date.now() - 7200000).toISOString()
        },
        {
          id: generateId(),
          image_url: 'https://images.unsplash.com/photo-1466637574441-749b8f19452f?w=600',
          uploader_name: '幸福一家人',
          message: '团团圆圆过大年，热热闹闹吃年饭 🏮',
          is_public: true,
          created_at: new Date(Date.now() - 10800000).toISOString()
        }
      ]

      localStorage.setItem('photos', JSON.stringify(samplePhotos))
      photos = samplePhotos
    }

    if (onlyPublic) {
      photos = photos.filter(p => p.is_public)
    }

    return {
      success: true,
      data: photos.slice(0, limit)
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
export async function getStats() {
  await delay(200)

  try {
    const greetings = JSON.parse(localStorage.getItem('greetings') || '[]')
    const photos = JSON.parse(localStorage.getItem('photos') || '[]')

    return {
      success: true,
      data: {
        greetingsCount: greetings.length,
        photosCount: photos.length
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

export default {
  saveGreeting,
  getGreetings,
  uploadPhoto,
  getPhotos,
  getStats
}
