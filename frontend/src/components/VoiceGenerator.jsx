import { useState, useEffect, useRef } from 'react';
import { Mic, Play, Download, Loader2, Volume2, Pause, Zap, Award, Upload, Sparkles } from 'lucide-react';
import axios from 'axios';

function VoiceGenerator({ voiceScript }) {
    const [engine, setEngine] = useState('edge'); // 'edge', 'elevenlabs', or 'xtts'
    const [voices, setVoices] = useState([]);
    const [selectedVoice, setSelectedVoice] = useState(null);
    const [loading, setLoading] = useState(false);
    const [generating, setGenerating] = useState(false);
    const [audioUrl, setAudioUrl] = useState(null);
    const [error, setError] = useState(null);
    const [playing, setPlaying] = useState(false);
    const [audioElement, setAudioElement] = useState(null);
    // XTTS Voice Cloning
    const [referenceAudio, setReferenceAudio] = useState(null);
    const fileInputRef = useRef(null);
    const [languageFilter, setLanguageFilter] = useState('en'); // 'en' or 'ur'

    useEffect(() => {
        if (engine !== 'xtts') {
            fetchVoices();
        }
    }, [engine]);

    const fetchVoices = async () => {
        setLoading(true);
        setVoices([]);
        setSelectedVoice(null);
        setError(null);

        try {
            const endpoint = engine === 'edge'
                ? 'http://localhost:8000/api/voices/edge/list'
                : 'http://localhost:8000/api/voices/list';

            const response = await axios.get(endpoint);
            if (response.data.status === 'success') {
                setVoices(response.data.voices);
                // Pre-select first voice
                if (response.data.voices.length > 0) {
                    // Start with Christopher for Edge as it's very popular
                    const defaultVoice = engine === 'edge'
                        ? (response.data.voices.find(v => v.voice_id.includes('Christopher'))?.voice_id || response.data.voices[0].voice_id)
                        : response.data.voices[0].id;

                    setSelectedVoice(defaultVoice);
                }
            } else {
                setError(response.data.message);
            }
        } catch (err) {
            if (engine === 'elevenlabs') {
                setError('Failed to load ElevenLabs voices. Check API Key.');
            } else {
                setError('Failed to load voices. Backend might be down.');
            }
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const generateVoice = async () => {
        // XTTS requires reference audio, not voice selection
        if (engine === 'xtts' && !referenceAudio) {
            setError('Please upload a reference audio file for voice cloning.');
            return;
        }
        if (engine !== 'xtts' && !selectedVoice) {
            setError('Please select a voice');
            return;
        }

        setGenerating(true);
        setError(null);
        setAudioUrl(null);

        try {
            let response;

            if (engine === 'xtts') {
                // Use FormData for file upload
                const formData = new FormData();
                formData.append('text', voiceScript.full_text);
                formData.append('reference_audio', referenceAudio);
                formData.append('language', 'en');

                response = await axios.post('http://localhost:8000/api/voices/xtts/generate', formData, {
                    headers: { 'Content-Type': 'multipart/form-data' }
                });
            } else {
                const endpoint = engine === 'edge'
                    ? 'http://localhost:8000/api/voices/edge/generate'
                    : 'http://localhost:8000/api/voices/generate';

                const payload = {
                    text: voiceScript.full_text,
                    voice_id: selectedVoice
                };

                response = await axios.post(endpoint, payload);
            }

            if (response.data.status === 'success') {
                const url = `http://localhost:8000${response.data.audio_url}`;
                setAudioUrl(url);

                // Create audio element
                const audio = new Audio(url);
                setAudioElement(audio);

                audio.onended = () => setPlaying(false);
            } else {
                setError(response.data.message);
            }
        } catch (err) {
            setError(err.response?.data?.message || 'Failed to generate voice');
            console.error(err);
        } finally {
            setGenerating(false);
        }
    };

    const togglePlayback = () => {
        if (!audioElement) return;

        if (playing) {
            audioElement.pause();
            setPlaying(false);
        } else {
            audioElement.play();
            setPlaying(true);
        }
    };

    const downloadAudio = () => {
        if (!audioUrl) return;
        const link = document.createElement('a');
        link.href = audioUrl;
        link.download = `voice-${Date.now()}.mp3`;
        link.click();
    };

    return (
        <div className="bg-purple-50/50 border border-purple-100 rounded-3xl p-8">
            <div className="flex items-center justify-between mb-6">
                <h3 className="text-xl font-bold text-purple-700 flex items-center gap-2">
                    <Mic className="w-5 h-5" />
                    Voice Generation
                </h3>

                {/* Engine Toggle */}
                <div className="bg-white p-1 rounded-xl border border-purple-100 flex shadow-sm">
                    <button
                        onClick={() => setEngine('edge')}
                        className={`px-3 py-1.5 rounded-lg text-xs font-bold flex items-center gap-1.5 transition-all ${engine === 'edge'
                            ? 'bg-purple-100 text-purple-700 shadow-sm'
                            : 'text-slate-500 hover:bg-slate-50'
                            }`}
                        title="Unlimited free generations"
                    >
                        <Zap className="w-3 h-3" />
                        Free (Fast)
                    </button>
                    <button
                        onClick={() => setEngine('xtts')}
                        className={`px-3 py-1.5 rounded-lg text-xs font-bold flex items-center gap-1.5 transition-all ${engine === 'xtts'
                            ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-sm'
                            : 'text-slate-500 hover:bg-slate-50'
                            }`}
                        title="Clone any voice from a sample (Local AI)"
                    >
                        <Sparkles className="w-3 h-3" />
                        Clone
                    </button>
                </div>
            </div>

            {error && (
                <div className="bg-red-50 border border-red-100 text-red-600 rounded-xl p-4 mb-6 animate-in slide-in-from-top-2">
                    <p className="text-sm font-medium">{error}</p>
                    {error.includes('ELEVENLABS_API_KEY') && (
                        <p className="text-xs mt-2 text-red-500">
                            Add <code className="bg-red-100 px-2 py-0.5 rounded text-red-700">ELEVENLABS_API_KEY="your_key"</code> to backend/.env file
                        </p>
                    )}
                </div>
            )}

            <div className="space-y-6">
                {/* XTTS Clone Voice UI */}
                {engine === 'xtts' && (
                    <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl p-6 border border-purple-200 mb-6">
                        <h4 className="text-sm font-bold text-purple-700 mb-3 flex items-center gap-2">
                            <Sparkles className="w-4 h-4" />
                            Voice Cloning (Local AI)
                        </h4>
                        <p className="text-xs text-slate-500 mb-4">
                            Upload a 3-10 second audio sample of the voice you want to clone. The AI will generate speech in that voice.
                        </p>
                        <input
                            type="file"
                            ref={fileInputRef}
                            accept="audio/*"
                            onChange={(e) => setReferenceAudio(e.target.files[0])}
                            className="hidden"
                        />
                        <button
                            onClick={() => fileInputRef.current?.click()}
                            className={`w-full py-4 px-6 rounded-xl border-2 border-dashed transition-all flex items-center justify-center gap-3 ${referenceAudio
                                ? 'border-purple-400 bg-purple-100 text-purple-700'
                                : 'border-slate-300 bg-white text-slate-500 hover:border-purple-300 hover:bg-purple-50'
                                }`}
                        >
                            <Upload className="w-5 h-5" />
                            {referenceAudio ? (
                                <span className="font-medium">{referenceAudio.name}</span>
                            ) : (
                                <span>Upload Reference Audio (MP3, WAV)</span>
                            )}
                        </button>
                        {referenceAudio && (
                            <button
                                onClick={() => setReferenceAudio(null)}
                                className="text-xs text-red-500 hover:underline mt-2"
                            >
                                Remove file
                            </button>
                        )}
                    </div>
                )}

                {/* Voice Selector (for non-XTTS engines) */}
                {engine !== 'xtts' && (
                    <div>
                        <label className="block text-sm font-bold text-purple-700 mb-3 flex items-center justify-between">
                            <span>Select Voice</span>
                            <span className="text-xs font-normal text-purple-400">
                                {engine === 'edge' ? 'Powered by Microsoft Edge (Free)' : 'Powered by ElevenLabs (Premium)'}
                            </span>
                        </label>

                        {engine === 'edge' && (
                            <div className="flex bg-slate-100 p-1 rounded-lg w-fit mb-3">
                                <button
                                    onClick={() => setLanguageFilter('en')}
                                    className={`px-3 py-1.5 rounded-md text-xs font-bold transition-all ${languageFilter === 'en'
                                        ? 'bg-white text-purple-700 shadow-sm'
                                        : 'text-slate-500 hover:text-slate-700'
                                        }`}
                                >
                                    English
                                </button>
                                <button
                                    onClick={() => setLanguageFilter('ur')}
                                    className={`px-3 py-1.5 rounded-md text-xs font-bold transition-all ${languageFilter === 'ur'
                                        ? 'bg-white text-purple-700 shadow-sm'
                                        : 'text-slate-500 hover:text-slate-700'
                                        }`}
                                >
                                    Urdu 🇵🇰
                                </button>
                            </div>
                        )}

                        {loading ? (
                            <div className="flex items-center gap-2 text-slate-500 h-24 bg-white rounded-xl border border-slate-200 justify-center">
                                <Loader2 className="w-4 h-4 animate-spin" />
                                Loading voices...
                            </div>
                        ) : voices.length > 0 ? (
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 max-h-[300px] overflow-y-auto pr-1 custom-scrollbar">
                                {voices
                                    .filter(voice => {
                                        if (engine !== 'edge') return true;
                                        const isUrdu = voice.voice_id.startsWith('ur');
                                        return languageFilter === 'ur' ? isUrdu : !isUrdu;
                                    })
                                    .slice(0, 20)
                                    .map((voice) => {
                                        const voiceId = engine === 'edge' ? voice.voice_id : voice.id;
                                        const isSelected = selectedVoice === voiceId;

                                        return (
                                            <button
                                                key={voiceId}
                                                onClick={() => setSelectedVoice(voiceId)}
                                                className={`p-3 rounded-xl border-2 transition-all text-left relative ${isSelected
                                                    ? 'border-purple-600 bg-purple-50 ring-1 ring-purple-600'
                                                    : 'border-slate-200 bg-white hover:border-purple-300 hover:bg-purple-50/50'
                                                    }`}
                                            >
                                                <div className="flex items-center justify-between mb-1">
                                                    <p className={`text-sm font-bold truncate ${isSelected ? 'text-purple-900' : 'text-slate-700'}`}>
                                                        {voice.name.replace('Neural', '')}
                                                    </p>
                                                    {engine === 'edge' && voice.name.includes('Neural') && (
                                                        <Zap className="w-3 h-3 text-amber-500 fill-amber-500" />
                                                    )}
                                                </div>
                                                {voice.labels && voice.labels.accent && (
                                                    <p className={`text-xs ${isSelected ? 'text-purple-700' : 'text-slate-500'}`}>{voice.labels.accent}</p>
                                                )}
                                                {engine === 'edge' && (
                                                    <p className={`text-[10px] ${isSelected ? 'text-purple-600' : 'text-slate-400'}`}>
                                                        {voice.voice_id.split('-')[1]} • {voice.name.includes('Female') ? 'Female' : 'Male'}
                                                    </p>
                                                )}
                                            </button>
                                        );
                                    })}
                            </div>
                        ) : (
                            <div className="text-center py-8 bg-white rounded-xl border border-slate-200 border-dashed">
                                <p className="text-slate-500 text-sm">No voices found.</p>
                                {engine === 'elevenlabs' && (
                                    <button onClick={() => setEngine('edge')} className="text-purple-600 text-sm font-bold mt-2 hover:underline">
                                        Try Free Voices instead?
                                    </button>
                                )}
                            </div>
                        )}
                    </div>
                )}

                {/* Generate Button */}
                <div>
                    <button
                        onClick={generateVoice}
                        disabled={generating || (engine !== 'xtts' && !selectedVoice) || (engine === 'xtts' && !referenceAudio) || loading}
                        className="w-full bg-purple-600 hover:bg-purple-700 text-white font-bold py-4 px-6 rounded-2xl transition-all shadow-lg shadow-purple-500/30 hover:shadow-purple-500/40 hover:scale-[1.005] active:scale-100 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center gap-3"
                    >
                        {generating ? (
                            <>
                                <Loader2 className="w-5 h-5 animate-spin" />
                                {engine === 'xtts' ? 'Cloning Voice...' : 'Generating Audio...'}
                            </>
                        ) : (
                            <>
                                {engine === 'xtts' ? <Sparkles className="w-5 h-5" /> : <Volume2 className="w-5 h-5" />}
                                {engine === 'xtts' ? 'Clone Voice' : engine === 'edge' ? 'Generate (Free)' : 'Generate (Premium)'}
                            </>
                        )}
                    </button>
                    {engine === 'edge' && (
                        <p className="text-center text-xs text-slate-400 mt-3 flex items-center justify-center gap-1">
                            <Zap className="w-3 h-3 text-amber-500" />
                            Generates instantly • Unlimited usage
                        </p>
                    )}
                </div>

                {/* Audio Player */}
                {audioUrl && (
                    <div className="bg-white rounded-2xl p-6 border border-purple-100 shadow-sm animate-in fade-in slide-in-from-top-4">
                        <div className="flex items-center justify-between">
                            <div className="flex items-center gap-4">
                                <button
                                    onClick={togglePlayback}
                                    className="w-12 h-12 rounded-full bg-purple-600 text-white flex items-center justify-center hover:bg-purple-700 transition-colors shadow-lg shadow-purple-500/30 active:scale-95"
                                >
                                    {playing ? (
                                        <Pause className="w-5 h-5" />
                                    ) : (
                                        <Play className="w-5 h-5 ml-0.5" />
                                    )}
                                </button>
                                <div>
                                    <p className="text-sm font-bold text-slate-900">Voice Generated!</p>
                                    <p className="text-xs text-slate-500 flex items-center gap-1">
                                        {voices.find(v => (engine === 'edge' ? v.voice_id : v.id) === selectedVoice)?.name.replace('Neural', '') || 'Selected voice'}
                                        <span className="w-1 h-1 rounded-full bg-slate-300"></span>
                                        {voiceScript.full_text.split(' ').length} words
                                    </p>
                                </div>
                            </div>
                            <button
                                onClick={downloadAudio}
                                className="bg-slate-50 hover:bg-slate-100 border border-slate-200 text-slate-600 px-4 py-2 rounded-xl transition-all flex items-center gap-2 font-medium text-sm"
                            >
                                <Download className="w-4 h-4" />
                                Download MP3
                            </button>
                        </div>
                    </div>
                )}

                {/* Script Preview */}
                <details className="group">
                    <summary className="cursor-pointer text-sm font-bold text-purple-700 hover:text-purple-800 transition-colors select-none">
                        Full Voice Script (Click to expand)
                    </summary>
                    <div className="mt-3 bg-white rounded-xl p-4 border border-slate-200 shadow-sm animate-in fade-in">
                        <p className="text-xs text-slate-600 leading-relaxed whitespace-pre-wrap font-mono selection:bg-purple-100 selection:text-purple-900">
                            {voiceScript.full_text}
                        </p>
                    </div>
                </details>
            </div>
        </div>
    );
}

export default VoiceGenerator;
