import { useState } from 'react';
import axios from 'axios';
import { Send, Copy, Check, Loader2, Sparkles, AlertCircle, Edit2, Eye, Briefcase, Building2, Clock, Zap } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

const ProposalGenerator = () => {
    const [jobDescription, setJobDescription] = useState('');
    const [generatedEmail, setGeneratedEmail] = useState('');
    const [jobDetails, setJobDetails] = useState(null);

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [copied, setCopied] = useState(false);
    const [isEditing, setIsEditing] = useState(false);

    const handleGenerate = async (e) => {
        e.preventDefault();
        if (!jobDescription) return;

        setLoading(true);
        setError('');
        setGeneratedEmail('');
        setJobDetails(null);
        setIsEditing(false);

        try {
            const response = await axios.post('http://localhost:8000/submit', {
                job_description: jobDescription
            });

            if (response.data.status === 'success') {
                setGeneratedEmail(response.data.email);
                setJobDetails(response.data.job_details);
            } else {
                setError(response.data.message || 'Failed to generate proposal.');
            }
        } catch (err) {
            setError(err.message || 'Something went wrong.');
        } finally {
            setLoading(false);
        }
    };

    const handleCopy = () => {
        if (!generatedEmail) return;
        navigator.clipboard.writeText(generatedEmail);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    return (
        <div className="w-full max-w-5xl mx-auto space-y-10 py-12 px-4">
            {/* Header */}
            <div className="text-center space-y-6">
                <div className="inline-flex items-center justify-center p-4 bg-gradient-to-br from-indigo-500/10 via-purple-500/10 to-pink-500/10 rounded-3xl ring-1 ring-indigo-500/20 shadow-2xl backdrop-blur-xl mb-2">
                    <Sparkles className="w-10 h-10 text-indigo-400" />
                </div>
                <div className="space-y-3">
                    <h1 className="text-5xl md:text-6xl font-black tracking-tight">
                        <span className="bg-gradient-to-r from-indigo-300 via-purple-300 to-pink-300 bg-clip-text text-transparent">
                            Proposal Generator
                        </span>
                    </h1>
                    <p className="text-slate-400 text-xl max-w-2xl mx-auto font-light">
                        Transform job descriptions into{' '}
                        <span className="text-indigo-400 font-semibold">winning proposals</span> in seconds
                    </p>
                </div>
            </div>

            {/* Input Section */}
            <div className="bg-gradient-to-br from-slate-900/50 to-slate-800/30 backdrop-blur-2xl border border-indigo-500/10 rounded-3xl p-8 shadow-2xl shadow-indigo-950/50">
                <form onSubmit={handleGenerate} className="space-y-6">
                    {/* Label */}
                    <div className="flex items-center justify-between">
                        <label className="text-sm font-bold text-indigo-300 uppercase tracking-wider flex items-center gap-2">
                            <div className="w-1.5 h-1.5 rounded-full bg-indigo-400"></div>
                            Job Description
                        </label>
                        <span className="text-xs text-slate-500 font-medium">
                            {jobDescription.length} characters
                        </span>
                    </div>

                    {/* Textarea */}
                    <textarea
                        placeholder="Paste the complete job description here...

Example: Seeking a Senior Full-Stack Developer to architect and build a high-performance SaaS platform. Must have expertise in Node.js, React, MongoDB, and cloud infrastructure..."
                        value={jobDescription}
                        onChange={(e) => setJobDescription(e.target.value)}
                        className="w-full h-64 bg-slate-950/50 border border-indigo-500/20 rounded-2xl px-6 py-5 text-slate-200 placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-transparent transition-all resize-none font-sans text-base leading-relaxed"
                        required
                    />

                    {/* Submit Button */}
                    <button
                        type="submit"
                        disabled={loading || !jobDescription}
                        className="w-full bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 hover:from-indigo-500 hover:via-purple-500 hover:to-pink-500 text-white font-bold rounded-2xl px-10 py-5 flex items-center justify-center gap-3 transition-all disabled:opacity-40 disabled:cursor-not-allowed shadow-2xl shadow-indigo-500/30 hover:shadow-indigo-500/50 hover:scale-[1.02] active:scale-[0.98] text-lg"
                    >
                        {loading ? (
                            <>
                                <Loader2 className="w-6 h-6 animate-spin" />
                                Crafting Your Proposal...
                            </>
                        ) : (
                            <>
                                <Sparkles className="w-6 h-6" />
                                Generate Winning Proposal
                            </>
                        )}
                    </button>
                </form>
            </div>

            {/* Error Message */}
            {error && (
                <div className="bg-red-500/10 border border-red-500/30 text-red-200 px-8 py-5 rounded-2xl flex items-center gap-4 animate-fade-in backdrop-blur-xl">
                    <AlertCircle className="w-6 h-6 text-red-400 flex-shrink-0" />
                    <p className="text-base">{error}</p>
                </div>
            )}

            {/* Job Insights Dashboard */}
            {jobDetails && (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 animate-fade-in-up">
                    {/* Role Card */}
                    <div className="bg-gradient-to-br from-slate-900/50 to-slate-800/30 backdrop-blur-2xl border border-indigo-500/20 rounded-3xl p-8 flex flex-col justify-between hover:border-indigo-500/40 hover:shadow-2xl hover:shadow-indigo-500/10 transition-all group">
                        <div className="space-y-5">
                            <div className="flex items-center gap-3 text-indigo-400">
                                <div className="p-3 bg-gradient-to-br from-indigo-500/20 to-purple-500/20 rounded-2xl ring-1 ring-indigo-400/30">
                                    <Briefcase className="w-6 h-6" />
                                </div>
                                <h3 className="font-bold text-slate-300 text-lg uppercase tracking-wide">Role</h3>
                            </div>
                            <p className="text-2xl font-black bg-gradient-to-r from-white to-indigo-200 bg-clip-text text-transparent">
                                {jobDetails.role || "N/A"}
                            </p>
                        </div>
                        <div className="mt-8 flex items-center gap-3 text-slate-500 text-sm pt-6 border-t border-indigo-500/10">
                            <Building2 className="w-5 h-5" />
                            <span className="font-medium">{jobDetails.company_name || "Unknown Company"}</span>
                        </div>
                    </div>

                    {/* Requirements Card */}
                    <div className="bg-gradient-to-br from-slate-900/50 to-slate-800/30 backdrop-blur-2xl border border-purple-500/20 rounded-3xl p-8 space-y-8 hover:border-purple-500/40 hover:shadow-2xl hover:shadow-purple-500/10 transition-all">
                        <div className="space-y-3">
                            <div className="flex items-center gap-3 text-purple-400">
                                <div className="p-3 bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-2xl ring-1 ring-purple-400/30">
                                    <Clock className="w-5 h-5" />
                                </div>
                                <span className="font-bold text-sm uppercase tracking-wide text-slate-300">Experience</span>
                            </div>
                            <p className="text-slate-200 text-lg font-semibold">{jobDetails.experience || "Not specified"}</p>
                        </div>

                        <div className="space-y-4">
                            <div className="flex items-center gap-3 text-pink-400">
                                <div className="p-3 bg-gradient-to-br from-pink-500/20 to-orange-500/20 rounded-2xl ring-1 ring-pink-400/30">
                                    <Zap className="w-5 h-5" />
                                </div>
                                <span className="font-bold text-sm uppercase tracking-wide text-slate-300">Skills Required</span>
                            </div>
                            <div className="flex flex-wrap gap-2">
                                {jobDetails.skills && jobDetails.skills.length > 0 ? (
                                    jobDetails.skills.map((skill, i) => (
                                        <span key={i} className="px-4 py-2 bg-gradient-to-r from-indigo-500/10 to-purple-500/10 rounded-xl text-sm text-indigo-200 border border-indigo-500/30 font-medium hover:border-indigo-400/50 hover:bg-indigo-500/20 transition-all">
                                            {skill}
                                        </span>
                                    ))
                                ) : (
                                    <span className="text-slate-500 text-sm">No specific skills extracted</span>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Proposal Result */}
            {generatedEmail && (
                <div className="bg-gradient-to-br from-slate-900/50 to-slate-800/30 backdrop-blur-2xl border border-indigo-500/20 rounded-3xl overflow-hidden shadow-2xl shadow-indigo-950/50 animate-fade-in-up">
                    <div className="flex items-center justify-between px-8 py-6 border-b border-indigo-500/10 bg-gradient-to-r from-indigo-500/5 to-purple-500/5">
                        <h3 className="text-xl font-black bg-gradient-to-r from-indigo-300 to-purple-300 bg-clip-text text-transparent">Your Winning Proposal</h3>
                        <div className="flex gap-3">
                            <button
                                onClick={() => setIsEditing(!isEditing)}
                                className={`flex items-center gap-2 text-sm font-semibold px-4 py-2.5 rounded-xl transition-all ${isEditing
                                        ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-lg shadow-indigo-500/30'
                                        : 'bg-slate-800/50 text-slate-400 hover:text-slate-200 hover:bg-slate-700/50 border border-slate-700'
                                    }`}
                            >
                                {isEditing ? <Eye className="w-4 h-4" /> : <Edit2 className="w-4 h-4" />}
                                {isEditing ? 'Preview' : 'Edit'}
                            </button>
                            <button
                                onClick={handleCopy}
                                className="text-slate-300 hover:text-white transition-all flex items-center gap-2 text-sm font-semibold bg-slate-800/50 px-4 py-2.5 rounded-xl hover:bg-emerald-600/20 border border-slate-700 hover:border-emerald-500/50"
                            >
                                {copied ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
                                {copied ? 'Copied!' : 'Copy'}
                            </button>
                        </div>
                    </div>

                    <div className="p-10">
                        {isEditing ? (
                            <textarea
                                value={generatedEmail}
                                onChange={(e) => setGeneratedEmail(e.target.value)}
                                className="w-full h-96 bg-slate-950/50 border border-indigo-500/20 rounded-2xl p-6 text-slate-300 font-mono text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/30 resize-none leading-loose"
                            />
                        ) : (
                            <div className="prose prose-invert prose-lg max-w-none prose-p:text-slate-300 prose-p:leading-relaxed prose-headings:text-indigo-200 prose-headings:font-black prose-li:text-slate-300 prose-strong:text-indigo-300 prose-strong:font-bold">
                                <ReactMarkdown>{generatedEmail}</ReactMarkdown>
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

export default ProposalGenerator;
