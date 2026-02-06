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
        <div className="w-full max-w-5xl mx-auto space-y-8 animate-fade-in pb-12">
            {/* Header */}
            <div className="text-center space-y-4 pt-4">
                <div className="inline-flex items-center justify-center p-3 bg-indigo-50 rounded-2xl ring-1 ring-indigo-100 mb-2">
                    <Sparkles className="w-6 h-6 text-indigo-600" />
                </div>
                <div className="space-y-2">
                    <h1 className="text-4xl md:text-5xl font-bold tracking-tight text-slate-900">
                        Proposal Generator
                    </h1>
                    <p className="text-slate-500 text-lg max-w-xl mx-auto">
                        Transform job descriptions into <span className="text-indigo-600 font-semibold">winning proposals</span> in seconds.
                    </p>
                </div>
            </div>

            {/* Input Section */}
            <div className="bg-white rounded-3xl p-1 shadow-xl shadow-slate-200/50 border border-slate-100">
                <div className="bg-slate-50/50 rounded-[20px] p-6 md:p-8 border border-slate-100">
                    <form onSubmit={handleGenerate} className="space-y-6">
                        {/* Label */}
                        <div className="flex items-center justify-between px-1">
                            <label className="text-xs font-bold text-slate-500 uppercase tracking-wider flex items-center gap-2">
                                <div className="w-1.5 h-1.5 rounded-full bg-indigo-500"></div>
                                Job Description
                            </label>
                            <span className="text-xs text-slate-400 font-medium bg-white px-2 py-1 rounded-md border border-slate-100 shadow-sm">
                                {jobDescription.length} characters
                            </span>
                        </div>

                        {/* Textarea */}
                        <div className="relative group">
                            <textarea
                                placeholder="Paste the complete job description here...&#10;&#10;Example: Seeking a Senior Full-Stack Developer to architect and build a high-performance SaaS platform..."
                                value={jobDescription}
                                onChange={(e) => setJobDescription(e.target.value)}
                                className="w-full h-64 bg-white border-2 border-slate-100 group-hover:border-slate-200 rounded-2xl px-6 py-5 text-slate-700 placeholder:text-slate-400 focus:outline-none focus:border-indigo-500/50 focus:ring-4 focus:ring-indigo-500/10 transition-all resize-none font-sans text-base leading-relaxed shadow-sm"
                                required
                            />
                            <div className="absolute bottom-4 right-4 pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity">
                                <div className="bg-slate-900 text-white text-xs font-bold px-2 py-1 rounded-md shadow-lg">
                                    Ready to Paste
                                </div>
                            </div>
                        </div>

                        {/* Submit Button */}
                        <button
                            type="submit"
                            disabled={loading || !jobDescription}
                            className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl px-8 py-4 flex items-center justify-center gap-3 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-indigo-500/30 hover:shadow-indigo-500/40 hover:-translate-y-0.5 active:translate-y-0 text-base"
                        >
                            {loading ? (
                                <>
                                    <Loader2 className="w-5 h-5 animate-spin" />
                                    <span>Crafting Your Proposal...</span>
                                </>
                            ) : (
                                <>
                                    <Sparkles className="w-5 h-5" />
                                    <span>Generate Winning Proposal</span>
                                </>
                            )}
                        </button>
                    </form>
                </div>
            </div>

            {/* Error Message */}
            {error && (
                <div className="bg-red-50 border border-red-100 text-red-600 px-6 py-4 rounded-xl flex items-center gap-3 animate-fade-in shadow-sm">
                    <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0" />
                    <p className="text-sm font-medium">{error}</p>
                </div>
            )}

            {/* Job Insights Dashboard */}
            {jobDetails && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 animate-fade-in-up">
                    {/* Role Card */}
                    <div className="bg-white border border-slate-100 rounded-2xl p-6 hover:shadow-lg hover:shadow-slate-200/50 transition-all group">
                        <div className="flex flex-col h-full justify-between space-y-6">
                            <div className="space-y-4">
                                <div className="flex items-center gap-3">
                                    <div className="p-2.5 bg-indigo-50 rounded-xl text-indigo-600">
                                        <Briefcase className="w-5 h-5" />
                                    </div>
                                    <h3 className="font-bold text-slate-400 text-xs uppercase tracking-wider">Role</h3>
                                </div>
                                <p className="text-xl font-bold text-slate-900 leading-tight group-hover:text-indigo-600 transition-colors">
                                    {jobDetails.role || "N/A"}
                                </p>
                            </div>
                            <div className="flex items-center gap-2 text-slate-500 text-sm pt-4 border-t border-slate-50">
                                <Building2 className="w-4 h-4" />
                                <span className="font-medium">{jobDetails.company_name || "Unknown Company"}</span>
                            </div>
                        </div>
                    </div>

                    {/* Requirements Card */}
                    <div className="bg-white border border-slate-100 rounded-2xl p-6 hover:shadow-lg hover:shadow-slate-200/50 transition-all space-y-6">
                        <div className="space-y-2">
                            <div className="flex items-center gap-3 mb-3">
                                <div className="p-2.5 bg-purple-50 rounded-xl text-purple-600">
                                    <Clock className="w-5 h-5" />
                                </div>
                                <span className="font-bold text-slate-400 text-xs uppercase tracking-wider">Experience</span>
                            </div>
                            <p className="text-slate-700 font-semibold pl-1">{jobDetails.experience || "Not specified"}</p>
                        </div>

                        <div className="space-y-3">
                            <div className="flex items-center gap-3">
                                <div className="p-2.5 bg-pink-50 rounded-xl text-pink-600">
                                    <Zap className="w-5 h-5" />
                                </div>
                                <span className="font-bold text-slate-400 text-xs uppercase tracking-wider">Skills Required</span>
                            </div>
                            <div className="flex flex-wrap gap-2">
                                {jobDetails.skills && jobDetails.skills.length > 0 ? (
                                    jobDetails.skills.map((skill, i) => (
                                        <span key={i} className="px-3 py-1 bg-slate-50 rounded-lg text-xs font-semibold text-slate-600 border border-slate-200">
                                            {skill}
                                        </span>
                                    ))
                                ) : (
                                    <span className="text-slate-400 text-sm italic">No specific skills extracted</span>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Proposal Result */}
            {generatedEmail && (
                <div className="bg-white rounded-3xl shadow-xl shadow-slate-200/50 border border-slate-100 overflow-hidden animate-fade-in-up">
                    <div className="flex items-center justify-between px-8 py-5 border-b border-slate-100 bg-slate-50/50">
                        <h3 className="text-lg font-bold text-slate-800 flex items-center gap-2">
                            <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                            Your Proposal
                        </h3>
                        <div className="flex gap-2">
                            <button
                                onClick={() => setIsEditing(!isEditing)}
                                className={`flex items-center gap-2 text-sm font-semibold px-4 py-2 rounded-lg transition-all border ${isEditing
                                    ? 'bg-indigo-50 text-indigo-700 border-indigo-200'
                                    : 'bg-white text-slate-600 border-slate-200 hover:border-slate-300 hover:bg-slate-50'
                                    }`}
                            >
                                {isEditing ? <Eye className="w-4 h-4" /> : <Edit2 className="w-4 h-4" />}
                                {isEditing ? 'Preview' : 'Edit'}
                            </button>
                            <button
                                onClick={handleCopy}
                                className={`flex items-center gap-2 text-sm font-semibold px-4 py-2 rounded-lg transition-all border ${copied
                                    ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                                    : 'bg-indigo-600 text-white border-transparent hover:bg-indigo-700 shadow-sm'
                                    }`}
                            >
                                {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                                {copied ? 'Copied!' : 'Copy Text'}
                            </button>
                        </div>
                    </div>

                    <div className="p-8 md:p-10">
                        {isEditing ? (
                            <textarea
                                value={generatedEmail}
                                onChange={(e) => setGeneratedEmail(e.target.value)}
                                className="w-full h-[500px] bg-slate-50 border border-slate-200 rounded-xl p-6 text-slate-700 font-mono text-sm focus:outline-none focus:border-indigo-500/50 focus:ring-2 focus:ring-indigo-500/10 resize-none leading-relaxed"
                            />
                        ) : (
                            <div className="prose prose-slate prose-lg max-w-none prose-p:leading-loose prose-headings:text-slate-900 prose-headings:font-bold prose-a:text-indigo-600 prose-strong:text-slate-900">
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
