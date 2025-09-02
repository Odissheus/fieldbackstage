import React, { useEffect, useRef, useState } from 'react'
import { Layout } from '../components/Layout'
import { apiFetch } from '../modules/api'

type ProductLine = { id: string; name: string }

export const CapturePage: React.FC = () => {
  const [lines, setLines] = useState<ProductLine[]>([])
  const [lineId, setLineId] = useState('')
  const [text, setText] = useState('')
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null)
  const [photoBlob, setPhotoBlob] = useState<Blob | null>(null)
  const [isRecording, setIsRecording] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [location, setLocation] = useState<{ lat: number; lng: number } | null>(null)
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const chunksRef = useRef<BlobPart[]>([])

  useEffect(() => { 
    apiFetch('/product-lines').then(setLines).catch(()=>{})
    
    // Get user location for territory context
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setLocation({
            lat: position.coords.latitude,
            lng: position.coords.longitude
          })
        },
        (error) => console.warn('Location not available:', error)
      )
    }
  }, [])

  const startRec = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const mr = new MediaRecorder(stream)
      mediaRecorderRef.current = mr
      chunksRef.current = []
      
      mr.ondataavailable = e => { if (e.data.size > 0) chunksRef.current.push(e.data) }
      mr.onstop = () => {
        setAudioBlob(new Blob(chunksRef.current, { type: 'audio/webm' }))
        setIsRecording(false)
        // Stop all tracks to release microphone
        stream.getTracks().forEach(track => track.stop())
      }
      
      mr.start()
      setIsRecording(true)
    } catch (error) {
      alert('Errore accesso microfono. Controlla permessi.')
      console.error('Audio recording error:', error)
    }
  }
  
  const stopRec = () => {
    mediaRecorderRef.current?.stop()
    setIsRecording(false)
  }

  const onPickPhoto = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0]
    if (f) setPhotoBlob(f)
  }

  const uploadToPresigned = async (blob: Blob, filename: string, mime: string): Promise<string> => {
    const presign = await apiFetch('/upload/presign', { method: 'POST', body: JSON.stringify({ filename, mime }) })
    await fetch(presign.url, { method: 'PUT', headers: { 'Content-Type': mime }, body: blob })
    return presign.fields.key
  }

  const submitInsight = async () => {
    if (!lineId) return alert('Seleziona una linea')
    
    setIsSubmitting(true)
    
    try {
      let audioUrl: string | undefined
      let photoUrl: string | undefined
      
      // Upload audio if present
      if (audioBlob) {
        const key = await uploadToPresigned(audioBlob, 'note.webm', 'audio/webm')
        audioUrl = key
      }
      
      // Upload photo if present
      if (photoBlob) {
        const key = await uploadToPresigned(photoBlob, 'photo.jpg', photoBlob.type || 'image/jpeg')
        photoUrl = key
      }
      
      // Include location if available
      const payload = {
        productLineId: lineId,
        territoryId: null,
        type: 'INSIGHT',
        text,
        audioUrl,
        photoUrl,
        metadata: location ? { location } : undefined
      }
      
      await apiFetch('/insights', { 
        method: 'POST', 
        body: JSON.stringify(payload) 
      })
      
      // Reset form
      setText('')
      setAudioBlob(null)
      setPhotoBlob(null)
      setLineId('')
      
      // Success feedback
      alert('✅ Insight inviato! Verrà elaborato automaticamente con AI.')
      
    } catch (error) {
      console.error('Submit error:', error)
      alert('❌ Errore invio. Riprova.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <Layout>
      <div className="min-h-screen bg-gray-50 p-4">
        <div className="max-w-md mx-auto space-y-6">
          {/* Header */}
          <div className="text-center">
            <h1 className="text-2xl font-bold text-gray-900 mb-2">📱 Nuovo Insight</h1>
            <p className="text-gray-600 text-sm">Raccogli feedback dal territorio</p>
          </div>

          {/* Form Card */}
          <div className="bg-white rounded-xl shadow-lg p-6 space-y-6">
            
            {/* Linea di Prodotto */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                🏷️ Linea di Prodotto
              </label>
              <select 
                className="w-full border-2 border-gray-200 rounded-lg px-4 py-3 text-lg focus:border-blue-500 focus:ring-0" 
                value={lineId} 
                onChange={e=>setLineId(e.target.value)}
              >
                <option value="">Seleziona linea...</option>
                {lines.map(l => <option key={l.id} value={l.id}>{l.name}</option>)}
              </select>
            </div>

            {/* Nota Testuale */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                ✍️ Note dal Campo
              </label>
              <textarea 
                className="w-full border-2 border-gray-200 rounded-lg px-4 py-3 text-lg focus:border-blue-500 focus:ring-0 resize-none" 
                rows={4} 
                placeholder="Descrivi il feedback del cliente, osservazioni, obiezioni..."
                value={text} 
                onChange={e=>setText(e.target.value)} 
              />
            </div>

            {/* Audio Recording */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                🎤 Registrazione Vocale
              </label>
              <div className="flex gap-3">
                <button 
                  className={`flex-1 rounded-lg px-4 py-3 font-medium text-lg transition-colors flex items-center justify-center gap-2 ${
                    isRecording 
                      ? 'bg-red-600 text-white animate-pulse' 
                      : 'bg-red-500 hover:bg-red-600 text-white'
                  }`}
                  onClick={startRec}
                  disabled={isRecording}
                >
                  <span className={`w-3 h-3 rounded-full ${isRecording ? 'bg-white animate-pulse' : 'bg-white'}`}></span>
                  {isRecording ? 'Registrando...' : 'Registra'}
                </button>
                <button 
                  className="flex-1 bg-gray-500 hover:bg-gray-600 text-white rounded-lg px-4 py-3 font-medium text-lg transition-colors disabled:opacity-50" 
                  onClick={stopRec}
                  disabled={!isRecording}
                >
                  ⏹️ Stop
                </button>
              </div>
              {audioBlob && (
                <div className="mt-3 p-3 bg-green-50 border border-green-200 rounded-lg">
                  <div className="flex items-center gap-2">
                    <span className="text-green-600">✅</span>
                    <span className="text-green-700 font-medium">
                      Audio registrato ({Math.round(audioBlob.size/1024)} KB)
                    </span>
                  </div>
                </div>
              )}
            </div>

            {/* Photo Upload */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                📷 Foto Competitive Intelligence
              </label>
              <div className="relative">
                <input 
                  type="file" 
                  accept="image/*" 
                  capture="environment"
                  onChange={onPickPhoto}
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                />
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-400 transition-colors">
                  <div className="text-4xl mb-2">📸</div>
                  <div className="text-gray-600 font-medium">Tocca per scattare foto</div>
                  <div className="text-gray-400 text-sm mt-1">Materiali competitori, prezzi, ecc.</div>
                </div>
              </div>
              {photoBlob && (
                <div className="mt-3 p-3 bg-green-50 border border-green-200 rounded-lg">
                  <div className="flex items-center gap-2">
                    <span className="text-green-600">✅</span>
                    <span className="text-green-700 font-medium">Foto selezionata</span>
                  </div>
                </div>
              )}
            </div>

            {/* Submit Button */}
            <button 
              className="w-full bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-6 py-4 font-bold text-lg transition-colors shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
              onClick={submitInsight}
              disabled={!lineId || isSubmitting}
            >
              {isSubmitting ? (
                <div className="flex items-center justify-center gap-2">
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  Invio in corso...
                </div>
              ) : (
                '🚀 Invia Insight'
              )}
            </button>

            {!lineId && !isSubmitting && (
              <p className="text-center text-red-500 text-sm">
                ⚠️ Seleziona una linea di prodotto per continuare
              </p>
            )}

            {location && (
              <div className="text-center text-green-600 text-sm">
                📍 Posizione rilevata per contesto territoriale
              </div>
            )}
          </div>

          {/* Help Text */}
          <div className="text-center text-gray-500 text-sm space-y-1">
            <p>💡 I tuoi insight verranno elaborati automaticamente con AI</p>
            <p>🔒 Tutti i dati sono protetti e anonimi</p>
          </div>
        </div>
      </div>
    </Layout>
  )
}

