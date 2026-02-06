import { useState } from 'react';
import { Sparkles, Video, Copy, Download, Loader2, Play, Info, LayoutGrid, BookOpen, Mic, Clapperboard, MonitorPlay } from 'lucide-react';
import axios from 'axios';
import VoiceGenerator from '../components/VoiceGenerator';
import VideoProgressTracker from '../components/VideoProgressTracker';
import VideoPlayer from '../components/VideoPlayer';

function UGCVideoGenerator() {
    const [formData, setFormData] = useState({
        idea: '',
        niche: '',
        tone: 'casual',
        platform: 'instagram',
        length: 30,
        language: 'english'
    });
    const [activeTab, setActiveTab] = useState('script');

    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);
    const [copiedText, setCopiedText] = useState('');
    const [showGuide, setShowGuide] = useState(false);

    // Video Generation State
    const [videoTaskId, setVideoTaskId] = useState(null);
    const [videoResult, setVideoResult] = useState(null);
    const [generatingVideo, setGeneratingVideo] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            const response = await axios.post('http://localhost:8000/api/ugc/generate-script', formData);

            if (response.data.status === 'success') {
                setResult(response.data.data);
            } else {
                setError(response.data.message || 'Failed to generate script');
            }
        } catch (err) {
            setError(err.response?.data?.message || 'An error occurred');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const generateCompleteVideo = async () => {
        if (!result) return;
        setGeneratingVideo(true);
        setError(null);
        setActiveTab('video'); // Switch to video tab

        try {
            const response = await axios.post('http://localhost:8000/api/ugc/generate-video', result);
            if (response.data.status === 'success') {
                setVideoTaskId(response.data.task_id);
            } else {
                setError(response.data.message || 'Failed to start video generation');
                setGeneratingVideo(false);
            }
        } catch (err) {
            setError(err.response?.data?.message || 'Error starting video generation');
            setGeneratingVideo(false);
        }
    };

    const handleVideoComplete = (data) => {
        setVideoResult(data);
        setGeneratingVideo(false);
        setVideoTaskId(null);
    };

    const copyToClipboard = (text, label) => {
        navigator.clipboard.writeText(text);
        setCopiedText(label);
        setTimeout(() => setCopiedText(''), 2000);
    };

    const downloadJSON = () => {
        const dataStr = JSON.stringify(result, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `ugc-script-${Date.now()}.json`;
        link.click();
    };

    return (
        <div className="w-full max-w-6xl mx-auto space-y-8 animate-fade-in pb-12 pt-4">
            {/* Header */}
            <div className="flex items-center gap-6 mb-8">
                <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-purple-600 to-pink-600 flex items-center justify-center shadow-lg shadow-purple-500/20">
                    <Video className="w-8 h-8 text-white" />
                </div>
                <div>
                    <h1 className="text-4xl font-black text-slate-900 tracking-tight">
                        UGC Video Generator
                    </h1>
                    <p className="text-slate-500 text-lg mt-1">AI-powered shot-by-shot script generation for authentic UGC videos</p>
                </div>
            </div>

            {/* Info Banner */}
            <div className="bg-purple-50 border border-purple-100 rounded-2xl p-6">
                <div className="flex items-start gap-3">
                    <Info className="w-5 h-5 text-purple-600 mt-0.5 flex-shrink-0" />
                    <div className="text-sm text-slate-600 leading-relaxed">
                        <strong className="text-purple-700">How it works:</strong> Enter your product idea → Get complete shot-by-shot script →
                        Copy prompts → Use with HeyGen/Runway for video + ElevenLabs for voice → Edit in CapCut
                    </div>
                </div>
            </div>

            {/* Input Form */}
            <div className="bg-white rounded-3xl p-1 shadow-xl shadow-slate-200/50 border border-slate-100">
                <div className="bg-slate-50/50 rounded-[20px] p-6 md:p-8">
                    <form onSubmit={handleSubmit}>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                            {/* Idea */}
                            <div className="md:col-span-2">
                                <label className="block text-sm font-bold text-slate-700 mb-2">
                                    Product / Idea
                                </label>
                                <input
                                    type="text"
                                    value={formData.idea}
                                    onChange={(e) => setFormData({ ...formData, idea: e.target.value })}
                                    placeholder="e.g., wireless earbuds for runners, skincare serum for acne, productivity app"
                                    className="w-full bg-white border border-slate-200 rounded-xl px-4 py-3 text-slate-900 placeholder-slate-400 focus:outline-none focus:border-purple-500/50 focus:ring-4 focus:ring-purple-500/10 transition-all shadow-sm"
                                    required
                                />
                            </div>

                            {/* Niche */}
                            <div>
                                <label className="block text-sm font-bold text-slate-700 mb-2">
                                    Target Niche
                                </label>
                                <input
                                    type="text"
                                    value={formData.niche}
                                    onChange={(e) => setFormData({ ...formData, niche: e.target.value })}
                                    placeholder="e.g., Gen Z beauty enthusiasts, remote workers"
                                    className="w-full bg-white border border-slate-200 rounded-xl px-4 py-3 text-slate-900 placeholder-slate-400 focus:outline-none focus:border-purple-500/50 focus:ring-4 focus:ring-purple-500/10 transition-all shadow-sm"
                                    required
                                />
                            </div>

                            {/* Language */}
                            <div>
                                <label className="block text-sm font-bold text-slate-700 mb-2">
                                    Language
                                </label>
                                <select
                                    value={formData.language}
                                    onChange={(e) => setFormData({ ...formData, language: e.target.value })}
                                    className="w-full bg-white border border-slate-200 rounded-xl px-4 py-3 text-slate-900 focus:outline-none focus:border-purple-500/50 focus:ring-4 focus:ring-purple-500/10 transition-all shadow-sm"
                                >
                                    <option value="english">English</option>
                                    <option value="urdu">Urdu</option>
                                </select>
                            </div>

                            {/* Tone */}
                            <div>
                                <label className="block text-sm font-bold text-slate-700 mb-2">
                                    Tone
                                </label>
                                <select
                                    value={formData.tone}
                                    onChange={(e) => setFormData({ ...formData, tone: e.target.value })}
                                    className="w-full bg-white border border-slate-200 rounded-xl px-4 py-3 text-slate-900 focus:outline-none focus:border-purple-500/50 focus:ring-4 focus:ring-purple-500/10 transition-all shadow-sm"
                                >
                                    <option value="casual">Casual & Relatable</option>
                                    <option value="energetic">Energetic & Upbeat</option>
                                    <option value="professional">Professional & Expert</option>
                                    <option value="humorous">Humorous & Fun</option>
                                    <option value="emotional">Emotional & Inspiring</option>
                                </select>
                            </div>

                            {/* Platform */}
                            <div>
                                <label className="block text-sm font-bold text-slate-700 mb-2">
                                    Platform
                                </label>
                                <select
                                    value={formData.platform}
                                    onChange={(e) => setFormData({ ...formData, platform: e.target.value })}
                                    className="w-full bg-white border border-slate-200 rounded-xl px-4 py-3 text-slate-900 focus:outline-none focus:border-purple-500/50 focus:ring-4 focus:ring-purple-500/10 transition-all shadow-sm"
                                >
                                    <option value="instagram">Instagram Reels</option>
                                    <option value="tiktok">TikTok</option>
                                    <option value="youtube_shorts">YouTube Shorts</option>
                                </select>
                            </div>

                            {/* Length */}
                            <div>
                                <label className="block text-sm font-bold text-slate-700 mb-2">
                                    Video Length
                                </label>
                                <select
                                    value={formData.length}
                                    onChange={(e) => setFormData({ ...formData, length: parseInt(e.target.value) })}
                                    className="w-full bg-white border border-slate-200 rounded-xl px-4 py-3 text-slate-900 focus:outline-none focus:border-purple-500/50 focus:ring-4 focus:ring-purple-500/10 transition-all shadow-sm"
                                >
                                    <option value={15}>15 seconds</option>
                                    <option value={30}>30 seconds</option>
                                    <option value={45}>45 seconds</option>
                                    <option value={60}>60 seconds</option>
                                </select>
                            </div>
                        </div>

                        {/* Submit Button */}
                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full mt-8 bg-purple-600 hover:bg-purple-700 text-white font-bold py-4 px-6 rounded-xl transition-all shadow-lg shadow-purple-500/30 hover:shadow-purple-500/40 hover:-translate-y-0.5 active:translate-y-0 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center gap-3"
                        >
                            {loading ? (
                                <>
                                    <Loader2 className="w-5 h-5 animate-spin" />
                                    <span>Generating Script...</span>
                                </>
                            ) : (
                                <>
                                    <Sparkles className="w-5 h-5" />
                                    <span>Generate UGC Script</span>
                                </>
                            )}
                        </button>
                    </form>
                </div>
            </div>

            {/* Error */}
            {error && (
                <div className="bg-red-50 border border-red-100 text-red-600 px-6 py-4 rounded-xl flex items-center gap-3 animate-fade-in shadow-sm">
                    <p className="font-medium">{error}</p>
                </div>
            )}

            {/* Results */}
            {result && (
                <div className="space-y-8 animate-fade-in-up">
                    {/* Copy Notification */}
                    {copiedText && (
                        <div className="fixed top-8 right-8 bg-emerald-600 text-white px-6 py-4 rounded-xl shadow-2xl shadow-emerald-500/30 z-50 flex items-center gap-3 animate-in slide-in-from-top">
                            <Copy className="w-5 h-5" />
                            <span className="font-bold">Copied {copiedText}!</span>
                        </div>
                    )}

                    {/* Action Buttons */}
                    <div className="flex justify-between items-center">
                        <h2 className="text-3xl font-black text-slate-900">Your UGC Script</h2>
                        <div className="flex gap-3">
                            <button
                                onClick={downloadJSON}
                                className="bg-purple-50 border border-purple-200 text-purple-700 hover:bg-purple-100 px-5 py-2.5 rounded-xl transition-all flex items-center gap-2 font-medium"
                            >
                                <Download className="w-4 h-4" />
                                Download JSON
                            </button>
                        </div>
                    </div>

                    {/* Concept Banner */}
                    <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
                        <div className="flex items-center gap-3 mb-4">
                            <div className="w-10 h-10 rounded-lg bg-purple-100 flex items-center justify-center">
                                <Play className="w-5 h-5 text-purple-600" />
                            </div>
                            <div>
                                <h3 className="text-lg font-bold text-slate-900 leading-tight">Video Concept</h3>
                                <p className="text-sm text-slate-500">Key elements of your script</p>
                            </div>
                        </div>

                        <div className="flex flex-wrap gap-4">
                            <div className="flex-1 min-w-[200px] bg-slate-50 rounded-xl p-3 border border-slate-100">
                                <p className="text-[10px] text-purple-600 uppercase font-black mb-1">Hook</p>
                                <p className="text-sm text-slate-700 font-medium leading-snug">{result.video_concept.hook}</p>
                            </div>
                            <div className="flex-1 min-w-[200px] bg-slate-50 rounded-xl p-3 border border-slate-100">
                                <p className="text-[10px] text-orange-600 uppercase font-black mb-1">Problem</p>
                                <p className="text-sm text-slate-700 font-medium leading-snug">{result.video_concept.problem}</p>
                            </div>
                            <div className="flex-1 min-w-[200px] bg-slate-50 rounded-xl p-3 border border-slate-100">
                                <p className="text-[10px] text-blue-600 uppercase font-black mb-1">Solution</p>
                                <p className="text-sm text-slate-700 font-medium leading-snug">{result.video_concept.solution}</p>
                            </div>
                            <div className="flex-1 min-w-[200px] bg-slate-50 rounded-xl p-3 border border-slate-100">
                                <p className="text-[10px] text-emerald-600 uppercase font-black mb-1">CTA</p>
                                <p className="text-sm text-slate-700 font-medium leading-snug">{result.video_concept.cta}</p>
                            </div>
                        </div>
                    </div>

                    {/* Tabs Navigation */}
                    <div className="border-b border-slate-200">
                        <div className="flex gap-8">
                            <button
                                onClick={() => setActiveTab('script')}
                                className={`pb-4 text-sm font-bold flex items-center gap-2 transition-all border-b-2 ${activeTab === 'script'
                                    ? 'border-purple-600 text-purple-700'
                                    : 'border-transparent text-slate-500 hover:text-slate-700'
                                    }`}
                            >
                                <LayoutGrid className="w-4 h-4" />
                                Script
                            </button>
                            <button
                                onClick={() => setActiveTab('voice')}
                                className={`pb-4 text-sm font-bold flex items-center gap-2 transition-all border-b-2 ${activeTab === 'voice'
                                    ? 'border-pink-600 text-pink-700'
                                    : 'border-transparent text-slate-500 hover:text-slate-700'
                                    }`}
                            >
                                <Mic className="w-4 h-4" />
                                Voice
                            </button>
                            <button
                                onClick={() => setActiveTab('video')}
                                className={`pb-4 text-sm font-bold flex items-center gap-2 transition-all border-b-2 ${activeTab === 'video'
                                    ? 'border-indigo-600 text-indigo-700'
                                    : 'border-transparent text-slate-500 hover:text-slate-700'
                                    }`}
                            >
                                <Clapperboard className="w-4 h-4" />
                                Video
                            </button>
                        </div>
                    </div>

                    {/* Tab Content */}
                    <div className="min-h-[400px]">
                        {/* Script Tab (Storyboard + Guide) */}
                        {activeTab === 'script' && (
                            <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
                                {/* Collapsible Production Guide */}
                                <div className="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm">
                                    <button
                                        onClick={() => setShowGuide(!showGuide)}
                                        className="w-full flex items-center justify-between p-6 bg-slate-50 hover:bg-slate-100 transition-colors"
                                    >
                                        <div className="flex items-center gap-3">
                                            <div className="w-8 h-8 rounded-full bg-cyan-100 flex items-center justify-center">
                                                <Info className="w-4 h-4 text-cyan-700" />
                                            </div>
                                            <div className="text-left">
                                                <h3 className="text-base font-bold text-slate-900">Production Guide</h3>
                                                <p className="text-xs text-slate-500">Step-by-step instructions (Click to {showGuide ? 'hide' : 'expand'})</p>
                                            </div>
                                        </div>
                                        <span className="text-slate-400">
                                            {showGuide ? 'Hide' : 'Show'}
                                        </span>
                                    </button>

                                    {showGuide && (
                                        <div className="p-8 border-t border-slate-200 bg-cyan-50/30">
                                            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                                                <div className="space-y-6">
                                                    <div>
                                                        <h4 className="text-sm font-bold text-cyan-900 mb-2">1. Character Setup</h4>
                                                        <p className="text-sm text-slate-700 leading-relaxed">{result.production_notes.character_description}</p>
                                                    </div>
                                                    <div>
                                                        <h4 className="text-sm font-bold text-cyan-900 mb-2">2. Visuals</h4>
                                                        <p className="text-xs text-slate-600 mb-2">Copy "Image Prompt" from shots below → Generate in Midjourney/DALL-E.</p>
                                                        <p className="text-xs text-slate-600">Then use "Video Prompt" with the image in HeyGen/Runway.</p>
                                                    </div>
                                                </div>
                                                <div className="space-y-6">
                                                    <div>
                                                        <h4 className="text-sm font-bold text-cyan-900 mb-2">3. Audio</h4>
                                                        <p className="text-sm text-slate-700 mb-2">Download the generated audio above or use ElevenLabs manually.</p>
                                                        <button
                                                            onClick={() => copyToClipboard(result.voice_script.full_text, 'Voice Script')}
                                                            className="text-xs bg-white border border-cyan-200 text-cyan-700 px-3 py-1.5 rounded-lg hover:bg-cyan-50 transition-all flex items-center gap-2 w-fit"
                                                        >
                                                            <Copy className="w-3 h-3" /> Copy Full Script
                                                        </button>
                                                    </div>
                                                    <div>
                                                        <h4 className="text-sm font-bold text-cyan-900 mb-2">4. Editing</h4>
                                                        <p className="text-xs text-slate-600">Sync clips to audio in CapCut. Add auto-captions. Export 9:16.</p>
                                                    </div>
                                                </div>
                                            </div>

                                            {result.production_notes.tips && result.production_notes.tips.length > 0 && (
                                                <div className="mt-8 pt-6 border-t border-cyan-100">
                                                    <h4 className="text-sm font-bold text-cyan-900 mb-3">💡 Pro Tips</h4>
                                                    <ul className="grid grid-cols-1 md:grid-cols-2 gap-2">
                                                        {result.production_notes.tips.map((tip, idx) => (
                                                            <li key={idx} className="text-xs text-cyan-800 flex items-start gap-2">
                                                                <span className="text-cyan-400 mt-0.5">•</span> {tip}
                                                            </li>
                                                        ))}
                                                    </ul>
                                                </div>
                                            )}
                                        </div>
                                    )}
                                </div>

                                {/* Storyboard Grid */}
                                <div>
                                    <div className="flex items-center justify-between mb-6">
                                        <h3 className="text-2xl font-black text-slate-900">Storyboard</h3>
                                        <span className="text-sm text-slate-500 font-medium">{result.shots.length} Shots</span>
                                    </div>
                                    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                                        {result.shots.map((shot) => (
                                            <ShotCard
                                                key={shot.shot_number}
                                                shot={shot}
                                                onCopy={copyToClipboard}
                                            />
                                        ))}
                                    </div>
                                </div>
                            </div>
                        )}

                        {activeTab === 'voice' && (
                            <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
                                <VoiceGenerator voiceScript={result.voice_script} />
                            </div>
                        )}

                        {activeTab === 'video' && (
                            <div className="animate-in fade-in slide-in-from-bottom-4 duration-500 min-h-[400px]">
                                {!videoTaskId && !videoResult ? (
                                    <div className="bg-indigo-50 border border-indigo-100 rounded-3xl p-12 text-center">
                                        <div className="w-20 h-20 bg-indigo-100 rounded-full flex items-center justify-center mx-auto mb-6">
                                            <Sparkles className="w-10 h-10 text-indigo-600" />
                                        </div>
                                        <h3 className="text-2xl font-black text-indigo-900 mb-4">Generate Complete AI Video</h3>
                                        <p className="text-slate-600 max-w-lg mx-auto mb-8 text-lg">
                                            Turn your script into a fully edited video with AI-generated visuals, voiceover, and motion — automatically.
                                        </p>

                                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-3xl mx-auto mb-10 text-left">
                                            <div className="bg-white p-4 rounded-xl border border-indigo-100 shadow-sm">
                                                <span className="text-2xl mb-2 block">🖼️</span>
                                                <p className="font-bold text-indigo-900 text-sm">Visuals</p>
                                                <p className="text-xs text-slate-500">AI images for each shot</p>
                                            </div>
                                            <div className="bg-white p-4 rounded-xl border border-indigo-100 shadow-sm">
                                                <span className="text-2xl mb-2 block">🎥</span>
                                                <p className="font-bold text-indigo-900 text-sm">Motion</p>
                                                <p className="text-xs text-slate-500">Video clips from images</p>
                                            </div>
                                            <div className="bg-white p-4 rounded-xl border border-indigo-100 shadow-sm">
                                                <span className="text-2xl mb-2 block">✂️</span>
                                                <p className="font-bold text-indigo-900 text-sm">Editing</p>
                                                <p className="text-xs text-slate-500">Stitched with audio</p>
                                            </div>
                                        </div>

                                        <button
                                            onClick={generateCompleteVideo}
                                            disabled={generatingVideo}
                                            className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-4 px-10 rounded-2xl transition-all shadow-xl shadow-indigo-500/30 hover:scale-105 active:scale-100 flex items-center gap-3 mx-auto text-lg"
                                        >
                                            {generatingVideo ? (
                                                <Loader2 className="w-6 h-6 animate-spin" />
                                            ) : (
                                                <MonitorPlay className="w-6 h-6" />
                                            )}
                                            Generate Full Video
                                        </button>
                                        <p className="text-xs text-indigo-400 mt-4 font-medium">Est. cost: $0.52 • Est. time: 5-10 mins</p>
                                    </div>
                                ) : videoTaskId ? (
                                    <VideoProgressTracker
                                        taskId={videoTaskId}
                                        onComplete={handleVideoComplete}
                                        onError={(msg) => setError(msg)}
                                        onRetry={() => {
                                            setVideoTaskId(null);
                                            setVideoResult(null);
                                            generateCompleteVideo();
                                        }}
                                    />
                                ) : (
                                    <div className="space-y-8 text-center animate-in zoom-in duration-500">
                                        <div className="bg-emerald-50 border border-emerald-100 rounded-3xl p-8 mb-8">
                                            <h3 className="text-2xl font-black text-emerald-800 mb-2">Video Generation Complete! 🎉</h3>
                                            <p className="text-emerald-600">Your unique UGC video is ready to download.</p>
                                        </div>

                                        <div className="flex justify-center">
                                            <VideoPlayer
                                                videoUrl={`http://localhost:8000${videoResult.video_url}`}
                                                thumbnailUrl={`http://localhost:8000${videoResult.thumbnail_url}`}
                                                onRegenerate={() => {
                                                    setVideoResult(null);
                                                    setVideoTaskId(null);
                                                }}
                                            />
                                        </div>

                                        <div className="flex justify-center gap-4">
                                            <button
                                                onClick={() => {
                                                    setVideoResult(null);
                                                    setVideoTaskId(null);
                                                }}
                                                className="text-slate-500 hover:text-indigo-600 font-medium text-sm flex items-center gap-2 transition-colors"
                                            >
                                                <Sparkles className="w-4 h-4" />
                                                Generate Another Version
                                            </button>
                                        </div>
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
}

function ShotCard({ shot, onCopy }) {
    const typeColors = {
        hook: 'from-pink-500 to-rose-500',
        problem: 'from-orange-500 to-red-500',
        solution: 'from-cyan-500 to-blue-500',
        proof: 'from-green-500 to-emerald-500',
        'b-roll': 'from-purple-500 to-violet-500',
        cta: 'from-yellow-500 to-amber-500',
    };

    const badgeColors = {
        hook: 'bg-pink-100 text-pink-700',
        problem: 'bg-orange-100 text-orange-700',
        solution: 'bg-cyan-100 text-cyan-700',
        proof: 'bg-emerald-100 text-emerald-700',
        'b-roll': 'bg-purple-100 text-purple-700',
        cta: 'bg-yellow-100 text-yellow-700',
    };

    // Fallback
    const bgColor = typeColors[shot.type.toLowerCase()] || 'from-slate-500 to-slate-600';
    const badgeColor = badgeColors[shot.type.toLowerCase()] || 'bg-slate-100 text-slate-700';

    return (
        <div className="bg-white rounded-2xl border border-slate-200 shadow-lg shadow-slate-200/50 hover:shadow-xl hover:shadow-slate-200/80 transition-all flex flex-col h-full overflow-hidden group">
            {/* Header / Scene Info */}
            <div className="p-5 border-b border-slate-100 bg-slate-50/50">
                <div className="flex items-start justify-between mb-3">
                    <div className={`px-2.5 py-1 rounded-lg text-[10px] font-black uppercase tracking-wider ${badgeColor}`}>
                        {shot.type}
                    </div>
                    <div className="text-xs font-bold text-slate-400">
                        {shot.duration}s
                    </div>
                </div>

                <div className="flex gap-3">
                    <div className={`flex-shrink-0 w-8 h-8 rounded-lg bg-gradient-to-br ${bgColor} flex items-center justify-center text-white font-black text-sm shadow-md`}>
                        {shot.shot_number}
                    </div>
                    <div>
                        <p className="text-xs font-bold text-slate-500 uppercase tracking-wide mb-0.5">Scene</p>
                        <p className="text-sm text-slate-800 font-medium leading-snug line-clamp-3">{shot.scene}</p>
                    </div>
                </div>
            </div>

            {/* Prompts Section (Middle) */}
            <div className="p-5 space-y-4 flex-grow bg-white">
                {/* Visual Prompts */}
                <div>
                    <div className="flex items-center justify-between mb-2">
                        <span className="text-[10px] font-bold text-indigo-500 uppercase tracking-wider flex items-center gap-1">
                            Image Prompt
                        </span>
                        <button
                            onClick={() => onCopy(shot.image_prompt, 'Image Prompt')}
                            className="text-[10px] font-bold bg-indigo-50 text-indigo-600 px-2 py-1 rounded hover:bg-indigo-100 transition-colors"
                        >
                            COPY
                        </button>
                    </div>
                    <div className="bg-indigo-50/30 rounded-lg p-3 border border-indigo-50 group-hover:border-indigo-100 transition-all">
                        <p className="text-xs text-slate-600 font-mono leading-relaxed line-clamp-4 hover:line-clamp-none transition-all cursor-default" title={shot.image_prompt}>
                            {shot.image_prompt}
                        </p>
                    </div>
                </div>

                {/* Video Prompt */}
                <div>
                    <div className="flex items-center justify-between mb-2">
                        <span className="text-[10px] font-bold text-pink-500 uppercase tracking-wider flex items-center gap-1">
                            Video Prompt
                        </span>
                        <button
                            onClick={() => onCopy(shot.video_prompt, 'Video Prompt')}
                            className="text-[10px] font-bold bg-pink-50 text-pink-600 px-2 py-1 rounded hover:bg-pink-100 transition-colors"
                        >
                            COPY
                        </button>
                    </div>
                    <div className="bg-pink-50/30 rounded-lg p-3 border border-pink-50 group-hover:border-pink-100 transition-all">
                        <p className="text-xs text-slate-600 font-mono leading-relaxed line-clamp-4 hover:line-clamp-none transition-all cursor-default" title={shot.video_prompt}>
                            {shot.video_prompt}
                        </p>
                    </div>
                </div>
            </div>

            {/* Script Footer (Bottom) */}
            <div className="p-5 bg-slate-50 border-t border-slate-100">
                <div className="flex items-center justify-between mb-2">
                    <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                        Voiceover
                    </span>
                    <button onClick={() => onCopy(shot.script, 'Script')}>
                        <Copy className="w-3 h-3 text-slate-400 hover:text-purple-600 transition-colors" />
                    </button>
                </div>
                <p className="text-sm text-slate-900 italic font-medium leading-relaxed">
                    "{shot.script}"
                </p>
            </div>
        </div>
    );
}

export default UGCVideoGenerator;
