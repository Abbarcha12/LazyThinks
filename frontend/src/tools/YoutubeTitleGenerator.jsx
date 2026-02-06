import { useState } from 'react';
import axios from 'axios';
import { Youtube, Copy, Check, Loader2, Sparkles, AlertCircle, TrendingUp, Award, Hash, Target, Lightbulb, RefreshCw, Bot, ShieldCheck, Palette, Image as ImageIcon } from 'lucide-react';
import AgentConversationViewer from '../components/AgentConversationViewer';

const YoutubeTitleGenerator = () => {
    const [formData, setFormData] = useState({
        video_concept: '',
        niche: '',
        keywords: '',
        tone: 'engaging',
        num_variations: 7
    });

    const [titles, setTitles] = useState([]);
    const [recommendedTitle, setRecommendedTitle] = useState('');
    const [seoTips, setSeoTips] = useState([]);

    // Multi-Agent State
    const [useMultiAgent, setUseMultiAgent] = useState(false);
    const [multiAgentResults, setMultiAgentResults] = useState(null);
    const [agentProgress, setAgentProgress] = useState('');

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [copiedIndex, setCopiedIndex] = useState(null);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: name === 'num_variations' ? parseInt(value) : value
        }));
    };

    const handleGenerate = async (e) => {
        e.preventDefault();
        if (!formData.video_concept || !formData.niche || !formData.keywords) return;

        setLoading(true);
        setError('');
        setTitles([]);
        setRecommendedTitle('');
        setSeoTips([]);
        setMultiAgentResults(null);
        setAgentProgress('');

        try {
            // Parse keywords (comma-separated)
            const keywordsArray = formData.keywords.split(',').map(k => k.trim()).filter(k => k);

            if (keywordsArray.length === 0) {
                setError('Please provide at least one keyword');
                setLoading(false);
                return;
            }

            // Step 1: Generate initial titles
            setAgentProgress('Generating initial variations...');
            const response = await axios.post('http://localhost:8000/api/youtube/generate-titles', {
                video_concept: formData.video_concept,
                niche: formData.niche,
                keywords: keywordsArray,
                tone: formData.tone,
                num_variations: formData.num_variations
            });

            const generatedTitles = response.data.titles;
            setTitles(generatedTitles);
            setRecommendedTitle(response.data.recommended_title);
            setSeoTips(response.data.seo_tips);

            // Step 2: If Multi-Agent enabled, validate titles
            if (useMultiAgent) {
                setAgentProgress('Agents validating titles (Researching & Analyzing)...');

                const validationResponse = await axios.post('http://localhost:8000/api/youtube/validate-titles-multiagent', {
                    video_concept: formData.video_concept,
                    niche: formData.niche,
                    keywords: keywordsArray,
                    titles_to_validate: generatedTitles.map(t => t.title),
                    max_research_depth: 20
                });

                setMultiAgentResults(validationResponse.data);

                // Update titles with validation data if approved
                if (validationResponse.data.validated_titles) {
                    // Start with validated titles (sorted by rank)
                    const enhancedTitles = validationResponse.data.validated_titles.map(vt => {
                        // Find original if exists to keep metadata
                        const original = generatedTitles.find(t => t.title === vt.title) || {};
                        return {
                            ...original, // Keep formula_used from original if matches
                            title: vt.title, // Might be an improved alternative
                            seo_score: vt.final_score || original.seo_score || 70,
                            ctr_potential: vt.predicted_ctr > 7 ? 'high' : vt.predicted_ctr > 4 ? 'medium' : 'low',
                            validation: vt, // Attach full validation data
                            formula_used: original.formula_used || 'optimized_alternative',
                            length_status: vt.title.length >= 50 && vt.title.length <= 60 ? 'optimal' : 'acceptable',
                            character_count: vt.title.length,
                            includes_power_words: original.includes_power_words || [],
                            includes_brackets: vt.title.includes('[') || vt.title.includes('(')
                        };
                    });
                    setTitles(enhancedTitles);

                    if (validationResponse.data.top_recommendation) {
                        setRecommendedTitle(validationResponse.data.top_recommendation.title);
                    }
                }
            }

        } catch (err) {
            console.error(err);
            setError(err.response?.data?.detail || err.message || 'Failed to generate titles');
        } finally {
            setLoading(false);
            setAgentProgress('');
        }
    };

    const handleCopy = (title, index) => {
        navigator.clipboard.writeText(title);
        setCopiedIndex(index);
        setTimeout(() => setCopiedIndex(null), 2000);
    };

    const getCharacterCountColor = (status) => {
        switch (status) {
            case 'optimal': return 'text-emerald-600 bg-emerald-50 border-emerald-200';
            case 'good': return 'text-blue-600 bg-blue-50 border-blue-200';
            case 'acceptable': return 'text-amber-600 bg-amber-50 border-amber-200';
            case 'too_short': return 'text-orange-600 bg-orange-50 border-orange-200';
            case 'too_long': return 'text-red-600 bg-red-50 border-red-200';
            default: return 'text-slate-600 bg-slate-50 border-slate-200';
        }
    };

    const getCTRBadge = (ctr) => {
        switch (ctr) {
            case 'high': return 'bg-emerald-100 text-emerald-700 border-emerald-200';
            case 'medium': return 'bg-blue-100 text-blue-700 border-blue-200';
            case 'low': return 'bg-slate-100 text-slate-600 border-slate-200';
            default: return 'bg-slate-100 text-slate-600 border-slate-200';
        }
    };

    const getSEOScoreColor = (score) => {
        if (score >= 70) return 'text-emerald-600';
        if (score >= 50) return 'text-blue-600';
        if (score >= 30) return 'text-amber-600';
        return 'text-red-600';
    };

    return (
        <div className="w-full max-w-6xl mx-auto space-y-12 animate-fade-in pb-24 font-inter text-slate-800">
            {/* Header */}
            <div className="text-center space-y-4 pt-8">
                <div className="inline-flex items-center justify-center p-4 bg-white rounded-2xl shadow-xl shadow-indigo-100 ring-1 ring-slate-100 mb-4 animate-float">
                    <Sparkles className="w-8 h-8 text-indigo-600" />
                </div>
                <div className="space-y-2">
                    <h1 className="text-4xl md:text-6xl font-black tracking-tight text-slate-900 leading-tight">
                        Viral Video <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-violet-600">Copilot</span>
                    </h1>
                    <p className="text-slate-500 text-lg md:text-xl max-w-2xl mx-auto font-medium">
                        Generate high-CTR titles & thumbnails with AI magic.
                    </p>
                </div>
            </div>

            {/* Magic Input Card */}
            <div className="bg-white/80 backdrop-blur-xl rounded-[2.5rem] p-8 md:p-12 shadow-2xl shadow-indigo-200/40 border border-white ring-1 ring-indigo-50 relative overflow-hidden group transition-all hover:shadow-indigo-200/50">
                {/* Decorative gradients */}
                <div className="absolute -top-24 -right-24 w-64 h-64 bg-indigo-500/10 rounded-full blur-3xl group-hover:bg-indigo-500/20 transition-all duration-1000 pointer-events-none"></div>
                <div className="absolute -bottom-24 -left-24 w-64 h-64 bg-violet-500/10 rounded-full blur-3xl group-hover:bg-violet-500/20 transition-all duration-1000 pointer-events-none"></div>

                <form onSubmit={handleGenerate} className="relative space-y-8">
                    {/* Main Input */}
                    <div className="space-y-4">
                        <label className="text-sm font-bold text-slate-400 uppercase tracking-widest pl-1">
                            What is your video about?
                        </label>
                        <input
                            type="text"
                            name="video_concept"
                            value={formData.video_concept}
                            onChange={handleInputChange}
                            placeholder="e.g., How to learn Python in 30 days without burnout"
                            className="w-full bg-slate-50/50 border-2 border-slate-100 hover:border-indigo-200 hover:bg-white rounded-2xl px-6 py-5 text-xl md:text-2xl font-semibold text-slate-800 placeholder:text-slate-300 focus:outline-none focus:border-indigo-500/50 focus:ring-4 focus:ring-indigo-500/10 transition-all shadow-inner"
                            required
                        />
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                        {/* Target Audience */}
                        <div className="space-y-3">
                            <label className="text-xs font-bold text-slate-400 uppercase tracking-widest pl-1">
                                Who is watching?
                            </label>
                            <input
                                type="text"
                                name="niche"
                                value={formData.niche}
                                onChange={handleInputChange}
                                placeholder="e.g., Beginner Developers"
                                className="w-full bg-slate-50/50 border-2 border-slate-100 hover:border-indigo-200 hover:bg-white rounded-xl px-5 py-4 text-lg font-medium text-slate-700 placeholder:text-slate-300 focus:outline-none focus:border-indigo-500/50 focus:ring-4 focus:ring-indigo-500/10 transition-all"
                                required
                            />
                        </div>

                        {/* Keywords */}
                        <div className="space-y-3">
                            <label className="text-xs font-bold text-slate-400 uppercase tracking-widest pl-1">
                                Keywords (SEO)
                            </label>
                            <input
                                type="text"
                                name="keywords"
                                value={formData.keywords}
                                onChange={handleInputChange}
                                placeholder="e.g., Python, Coding, Tutorial"
                                className="w-full bg-slate-50/50 border-2 border-slate-100 hover:border-indigo-200 hover:bg-white rounded-xl px-5 py-4 text-lg font-medium text-slate-700 placeholder:text-slate-300 focus:outline-none focus:border-indigo-500/50 focus:ring-4 focus:ring-indigo-500/10 transition-all"
                                required
                            />
                        </div>
                    </div>

                    <div className="flex flex-col md:flex-row items-center gap-6 pt-4">
                        {/* Power Mode Toggle */}
                        <div className={`flex-1 w-full bg-gradient-to-br transition-all duration-300 cursor-pointer rounded-2xl p-1 ${useMultiAgent ? 'from-indigo-500 to-violet-600 shadow-lg shadow-indigo-500/25' : 'from-slate-100 to-slate-200'}`}
                            onClick={() => setUseMultiAgent(!useMultiAgent)}
                        >
                            <div className="bg-white/95 backdrop-blur-sm rounded-xl p-4 flex items-center justify-between h-full hover:bg-white transition-colors">
                                <div className="flex items-center gap-4">
                                    <div className={`p-3 rounded-lg transition-colors ${useMultiAgent ? 'bg-indigo-100 text-indigo-600' : 'bg-slate-100 text-slate-400'}`}>
                                        <Bot className="w-6 h-6" />
                                    </div>
                                    <div>
                                        <h3 className={`font-bold text-base ${useMultiAgent ? 'text-indigo-900' : 'text-slate-500'}`}>
                                            Validator Agents
                                        </h3>
                                        <p className="text-xs text-slate-400 font-medium">Research & Design Co-pilots</p>
                                    </div>
                                </div>
                                <div className={`w-12 h-6 rounded-full p-1 transition-colors ${useMultiAgent ? 'bg-indigo-600' : 'bg-slate-300'}`}>
                                    <div className={`w-4 h-4 rounded-full bg-white shadow-sm transition-transform ${useMultiAgent ? 'translate-x-6' : 'translate-x-0'}`}></div>
                                </div>
                            </div>
                        </div>

                        {/* Generate Button */}
                        <button
                            type="submit"
                            disabled={loading || !formData.video_concept}
                            className="w-full md:w-auto flex-1 bg-slate-900 hover:bg-slate-800 text-white font-bold rounded-2xl px-8 py-5 flex items-center justify-center gap-3 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-xl shadow-slate-900/20 hover:shadow-slate-900/30 hover:-translate-y-1 active:translate-y-0 text-lg group/btn"
                        >
                            {loading ? (
                                <>
                                    <Loader2 className="w-6 h-6 animate-spin" />
                                    <span>Crafting Magic...</span>
                                </>
                            ) : (
                                <>
                                    <span>Generate Ideas</span>
                                    <Sparkles className="w-5 h-5 text-yellow-300 group-hover/btn:animate-pulse" />
                                </>
                            )}
                        </button>
                    </div>
                </form>
            </div>

            {/* Agent Progress */}
            {(loading || agentProgress) && (
                <div className="max-w-4xl mx-auto">
                    {useMultiAgent ? (
                        <AgentConversationViewer
                            conversationLog={useMultiAgent ? (multiAgentResults?.conversation_log || []) : []}
                            totalTime={multiAgentResults?.total_duration || 0}
                        />
                    ) : (
                        <div className="text-center p-8 animate-pulse text-slate-400 font-medium bg-white rounded-2xl border border-dashed border-slate-200">
                            <Bot className="w-8 h-8 mx-auto mb-3 opacity-50" />
                            <p>{agentProgress}</p>
                        </div>
                    )}
                </div>
            )}


            {/* Results Section */}
            {titles.length > 0 && (
                <div className="space-y-8 animate-fade-in-up delay-100">

                    {/* Hero Card: Winner & Thumbnails */}
                    {recommendedTitle && (
                        <div className="relative overflow-hidden bg-slate-900 rounded-[2.5rem] shadow-2xl shadow-indigo-900/20 border border-slate-800 min-h-[500px] flex flex-col md:flex-row">
                            {/* Background Effects */}
                            <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-indigo-600/20 rounded-full blur-[100px] pointer-events-none"></div>
                            <div className="absolute bottom-0 left-0 w-[300px] h-[300px] bg-violet-600/20 rounded-full blur-[100px] pointer-events-none"></div>

                            {/* Left: Title Strategy */}
                            <div className="relative p-8 md:p-12 flex-1 flex flex-col justify-center space-y-8 z-10 text-white">
                                <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-bold uppercase tracking-wider w-fit shadow-lg shadow-emerald-500/5">
                                    <Award className="w-4 h-4" />
                                    Top Recommendation
                                </div>

                                <div className="space-y-4">
                                    <h2 className="text-3xl md:text-4xl lg:text-5xl font-black text-white leading-tight">
                                        "{recommendedTitle}"
                                    </h2>
                                    <div className="flex flex-wrap gap-3">
                                        {formData.keywords.split(',').map((k, i) => (
                                            <span key={i} className="px-3 py-1 rounded-lg bg-slate-800/50 border border-white/10 text-slate-400 text-xs font-medium">
                                                #{k.trim()}
                                            </span>
                                        ))}
                                    </div>
                                </div>

                                <div className="flex gap-4 pt-4">
                                    <button
                                        onClick={() => handleCopy(recommendedTitle, 'hero')}
                                        className="bg-white text-slate-900 px-6 py-3 rounded-xl font-bold flex items-center gap-2 hover:bg-indigo-50 transition-colors shadow-lg shadow-white/10"
                                    >
                                        {copiedIndex === 'hero' ? <Check className="w-5 h-5 text-emerald-600" /> : <Copy className="w-5 h-5" />}
                                        {copiedIndex === 'hero' ? 'Copied!' : 'Copy Title'}
                                    </button>
                                </div>
                            </div>

                            {/* Right: Visual Concepts */}
                            <div className="relative md:w-[45%] bg-slate-950/50 border-l border-white/5 p-8 flex flex-col">
                                <div className="mb-6 flex items-center justify-between">
                                    <h3 className="text-white font-bold flex items-center gap-2">
                                        <Palette className="w-5 h-5 text-indigo-400" />
                                        <span>Visual Concepts</span>
                                    </h3>
                                    {multiAgentResults?.thumbnail_data && (
                                        <span className="text-xs font-mono text-slate-500 bg-slate-900 px-2 py-1 rounded border border-white/5">
                                            3 Variants
                                        </span>
                                    )}
                                </div>

                                <div className="flex-1 overflow-y-auto pr-2 space-y-6 custom-scrollbar">
                                    {multiAgentResults?.thumbnail_data ? (
                                        (multiAgentResults.thumbnail_data.image_urls || (multiAgentResults.thumbnail_data.image_url ? [multiAgentResults.thumbnail_data.image_url] : [])).map((url, idx) => (
                                            <div key={idx} className="group relative aspect-video bg-slate-900 rounded-xl overflow-hidden border border-white/10 shadow-lg hover:border-indigo-500/50 transition-all">
                                                <img
                                                    src={`http://localhost:8000${url}`}
                                                    alt={`Thumbnail Variant ${idx + 1}`}
                                                    className="w-full h-full object-cover opacity-90 group-hover:opacity-100 transition-opacity"
                                                />
                                                <div className="absolute inset-0 bg-gradient-to-t from-slate-900/90 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex items-end p-4">
                                                    <a
                                                        href={`http://localhost:8000${url}`}
                                                        target="_blank"
                                                        rel="noopener noreferrer"
                                                        className="w-full bg-white/10 backdrop-blur border border-white/20 text-white text-center py-2 rounded-lg text-xs font-bold hover:bg-white hover:text-slate-900 transition-colors"
                                                    >
                                                        View Full Size
                                                    </a>
                                                </div>
                                                <div className="absolute top-2 left-2 bg-black/60 backdrop-blur px-2 py-0.5 rounded text-[10px] font-bold text-white border border-white/10 shadow-sm">
                                                    V{idx + 1}
                                                </div>
                                            </div>
                                        ))
                                    ) : (
                                        <div className="h-full flex flex-col items-center justify-center text-slate-600 border-2 border-dashed border-slate-800 rounded-xl bg-slate-900/50 p-8 text-center">
                                            <ImageIcon className="w-12 h-12 mb-4 opacity-30" />
                                            <p className="text-sm font-medium">Generating Visuals...</p>
                                            <p className="text-xs opacity-50 mt-1">AI Artist is at work</p>
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Variations Grid */}
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {titles.filter(t => t.title !== recommendedTitle).map((item, index) => (
                            <div key={index} className="bg-white rounded-2xl p-6 border border-slate-100 shadow-sm hover:shadow-xl hover:shadow-indigo-100/50 hover:border-indigo-100 transition-all group duration-300">
                                <div className="flex justify-between items-start mb-4">
                                    <span className="text-[10px] font-bold uppercase tracking-wider text-slate-500 bg-slate-100 px-2 py-1 rounded group-hover:bg-indigo-50 group-hover:text-indigo-600 transition-colors">
                                        {item.formula_used?.replace(/_/g, ' ') || 'Alternative'}
                                    </span>
                                    {item.validation && (
                                        <div className={`w-2.5 h-2.5 rounded-full ${item.validation.final_score > 80 ? 'bg-emerald-500 shadow-lg shadow-emerald-500/50' : 'bg-amber-500'}`}></div>
                                    )}
                                </div>

                                <h3 className="text-lg font-bold text-slate-800 mb-6 leading-relaxed group-hover:text-indigo-900 transition-colors line-clamp-3">
                                    {item.title}
                                </h3>

                                <div className="flex items-center justify-between mt-auto pt-4 border-t border-slate-50 group-hover:border-indigo-50 transition-colors">
                                    <div className="flex items-center gap-3">
                                        <div className="flex items-center gap-1">
                                            <Target className="w-3 h-3 text-slate-400" />
                                            <span className={`text-xs font-bold ${getSEOScoreColor(item.seo_score)}`}>
                                                {Math.round(item.seo_score)}
                                            </span>
                                        </div>
                                        <div className="w-1 h-1 rounded-full bg-slate-300"></div>
                                        <span className="text-xs text-slate-400">
                                            {item.character_count} chars
                                        </span>
                                    </div>
                                    <button
                                        onClick={() => handleCopy(item.title, index)}
                                        className="text-slate-300 hover:text-indigo-600 transition-colors p-1"
                                        title="Copy to clipboard"
                                    >
                                        {copiedIndex === index ? <Check className="w-4 h-4 text-emerald-600" /> : <Copy className="w-4 h-4" />}
                                    </button>
                                </div>
                            </div>
                        ))}

                        <button
                            onClick={handleGenerate}
                            disabled={loading}
                            className="bg-slate-50 hover:bg-indigo-50 text-slate-500 hover:text-indigo-600 font-semibold rounded-2xl p-6 flex flex-col items-center justify-center gap-3 transition-all border-2 border-dashed border-slate-200 hover:border-indigo-200 group"
                        >
                            <div className="p-3 bg-white rounded-full shadow-sm group-hover:scale-110 transition-transform">
                                <RefreshCw className="w-5 h-5" />
                            </div>
                            <span>Generate More</span>
                        </button>
                    </div>

                    {/* SEO Tips */}
                    {seoTips.length > 0 && (
                        <div className="bg-gradient-to-br from-indigo-50/50 to-violet-50/50 rounded-2xl p-8 border border-indigo-100/50">
                            <h3 className="text-sm font-bold text-indigo-900 uppercase tracking-wider mb-6 flex items-center gap-2">
                                <Lightbulb className="w-4 h-4" />
                                Viral Optimization Tips
                            </h3>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                {seoTips.map((tip, index) => (
                                    <div key={index} className="flex items-start gap-3 bg-white/60 p-4 rounded-xl border border-white/50 shadow-sm">
                                        <div className="min-w-[4px] h-[4px] mt-2 rounded-full bg-indigo-400"></div>
                                        <p className="text-sm text-slate-700 leading-relaxed">{tip}</p>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default YoutubeTitleGenerator;
