import React, { useState, useEffect } from 'react';
import { Search, Trophy, CheckCircle, ChevronDown, ChevronRight, MessageSquare, Clock, Palette, Sparkles, Activity, FileText } from 'lucide-react';

const AgentConversationViewer = ({ conversationLog, totalTime }) => {
    const [showLogs, setShowLogs] = useState(false);
    const [currentStep, setCurrentStep] = useState(0);
    const [expandedMessages, setExpandedMessages] = useState({});

    // Determine current step based on logs
    useEffect(() => {
        if (!conversationLog) return;

        const types = conversationLog.map(m => m.type);
        if (types.includes('THUMBNAIL_COMPLETE')) setCurrentStep(4);
        else if (types.includes('FINAL_DECISION')) setCurrentStep(3);
        else if (types.includes('COMPETITOR_ANALYSIS_COMPLETE')) setCurrentStep(2);
        else if (types.includes('RESEARCH_COMPLETE')) setCurrentStep(1);
        else setCurrentStep(0);
    }, [conversationLog]);

    if (!conversationLog || conversationLog.length === 0) return null;

    const steps = [
        { id: 'research', label: 'Market Research', icon: Search, color: 'text-blue-500', bg: 'bg-blue-50', border: 'border-blue-200' },
        { id: 'competitor', label: 'Competitor Analysis', icon: Trophy, color: 'text-orange-500', bg: 'bg-orange-50', border: 'border-orange-200' },
        { id: 'validator', label: 'Quality Check', icon: CheckCircle, color: 'text-green-500', bg: 'bg-green-50', border: 'border-green-200' },
        { id: 'thumbnail', label: 'Visual Design', icon: Palette, color: 'text-purple-500', bg: 'bg-purple-50', border: 'border-purple-200' }
    ];

    const toggleMessage = (id) => {
        setExpandedMessages(prev => ({ ...prev, [id]: !prev[id] }));
    };

    const getAgentIcon = (agentName) => {
        switch (agentName.toLowerCase()) {
            case 'research': return <Search className="w-4 h-4 text-blue-500" />;
            case 'competitor': return <Trophy className="w-4 h-4 text-orange-500" />;
            case 'validator': return <CheckCircle className="w-4 h-4 text-green-500" />;
            case 'thumbnail': return <Palette className="w-4 h-4 text-purple-500" />;
            default: return <MessageSquare className="w-4 h-4 text-slate-500" />;
        }
    };

    const getAgentColor = (agentName) => {
        switch (agentName.toLowerCase()) {
            case 'research': return 'bg-blue-50 border-blue-200 text-blue-700';
            case 'competitor': return 'bg-orange-50 border-orange-200 text-orange-700';
            case 'validator': return 'bg-green-50 border-green-200 text-green-700';
            case 'thumbnail': return 'bg-purple-50 border-purple-200 text-purple-700';
            default: return 'bg-slate-50 border-slate-200 text-slate-700';
        }
    };

    const getMessageSummary = (type, content) => {
        switch (type) {
            case 'RESEARCH_COMPLETE':
                return `Found ${content.raw_research?.videos_found || 0} relevant videos and analyzed patterns.`;
            case 'ANALYSIS_COMPLETE':
                return `Analyzed titles and generated ${content.alternative_titles?.length || 0} alternatives.`;
            case 'FINAL_DECISION':
                return `Approved ${content.approved_count || 0} titles with ${(content.total_confidence || 0) * 100}% confidence.`;
            case 'THUMBNAIL_COMPLETE':
                const imgCount = content.image_urls?.length || (content.image_path ? 1 : 0);
                return `Designed viral thumbnail concept${imgCount > 0 ? ` and generated ${imgCount} variant${imgCount > 1 ? 's' : ''}` : ''}.`;
            default:
                return 'Agent communication...';
        }
    };

    return (
        <div className="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm animate-fade-in-up">
            {/* Header / Stepper Section */}
            <div className="p-6 border-b border-slate-100 bg-gradient-to-b from-slate-50/50 to-white">
                <div className="flex justify-between items-center mb-6">
                    <h3 className="font-bold text-slate-700 flex items-center gap-2">
                        <Sparkles className="w-5 h-5 text-indigo-500" />
                        AI Workflow
                    </h3>
                    <div className="flex items-center gap-3">
                        {totalTime > 0 && (
                            <div className="text-xs font-semibold text-slate-500 bg-white px-3 py-1 rounded-full border border-slate-200 flex items-center gap-1 shadow-sm">
                                <Clock className="w-3 h-3" />
                                {totalTime}s
                            </div>
                        )}
                        <button
                            onClick={() => setShowLogs(!showLogs)}
                            className="text-xs font-semibold text-indigo-600 hover:text-indigo-700 hover:bg-indigo-50 px-3 py-1 rounded-full transition-colors flex items-center gap-1"
                        >
                            <FileText className="w-3 h-3" />
                            {showLogs ? 'Hide Logs' : 'View Logs'}
                        </button>
                    </div>
                </div>

                {/* Visual Stepper */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {steps.map((step, idx) => {
                        const isActive = idx === currentStep;
                        const isCompleted = idx < currentStep;
                        const isPending = idx > currentStep;
                        const finalStep = currentStep === 4; // All done

                        return (
                            <div key={step.id}
                                className={`relative p-4 rounded-xl border transition-all duration-500 ${isCompleted || finalStep ? `${step.bg} ${step.border}` :
                                        isActive ? 'bg-white border-indigo-200 ring-2 ring-indigo-50 ring-offset-1 shadow-lg scale-[1.02]' :
                                            'bg-slate-50 border-slate-100 opacity-60 grayscale'
                                    }`}
                            >
                                <div className="flex items-center gap-3 mb-2">
                                    <div className={`p-2 rounded-lg ${isCompleted || finalStep ? 'bg-white/60' : isActive ? 'bg-indigo-100 text-indigo-600' : 'bg-slate-200 text-slate-400'
                                        }`}>
                                        <step.icon className={`w-4 h-4 ${isCompleted || finalStep ? step.color : 'currentColor'
                                            }`} />
                                    </div>
                                    {(isActive && !finalStep) && (
                                        <div className="absolute top-2 right-2">
                                            <span className="relative flex h-2.5 w-2.5">
                                                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span>
                                                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-indigo-500"></span>
                                            </span>
                                        </div>
                                    )}
                                    {(isCompleted || finalStep) && <CheckCircle className={`w-4 h-4 ml-auto ${step.color}`} />}
                                </div>
                                <p className={`text-xs font-bold uppercase tracking-wider mb-0.5 ${isCompleted || finalStep ? step.color : isActive ? 'text-indigo-600' : 'text-slate-400'
                                    }`}>
                                    Step {idx + 1}
                                </p>
                                <p className={`text-sm font-semibold ${isCompleted || finalStep ? 'text-slate-700' : isActive ? 'text-indigo-900' : 'text-slate-500'
                                    }`}>
                                    {step.label}
                                </p>
                            </div>
                        );
                    })}
                </div>
            </div>

            {/* Collapsible Logs */}
            {showLogs && (
                <div className="bg-slate-50 border-t border-slate-200 animate-fade-in-down">
                    <div className="p-6 space-y-4 max-h-[400px] overflow-y-auto custom-scrollbar">
                        {conversationLog.map((msg, index) => {
                            const isExpanded = expandedMessages[msg.id];
                            return (
                                <div key={msg.id} className="relative pl-8 md:pl-0">
                                    {index !== conversationLog.length - 1 && (
                                        <div className="absolute left-4 md:left-[23px] top-10 bottom-[-20px] w-0.5 bg-slate-200 md:block hidden"></div>
                                    )}
                                    <div className="flex gap-4">
                                        <div className={`w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0 border-2 bg-white z-10 hidden md:flex ${msg.sender === 'research' ? 'border-blue-100 text-blue-500' :
                                                msg.sender === 'competitor' ? 'border-orange-100 text-orange-500' :
                                                    msg.sender === 'validator' ? 'border-green-100 text-green-500' :
                                                        msg.sender === 'thumbnail' ? 'border-purple-100 text-purple-500' : 'border-slate-100'
                                            }`}>
                                            {getAgentIcon(msg.sender)}
                                        </div>
                                        <div className="flex-1 min-w-0">
                                            <div className={`rounded-2xl border transition-all ${isExpanded ? 'shadow-md' : 'shadow-sm'} ${getAgentColor(msg.sender).split(' ')[0] + ' ' + getAgentColor(msg.sender).split(' ')[1]
                                                } bg-opacity-30`}>
                                                <button onClick={() => toggleMessage(msg.id)} className="w-full flex items-center justify-between p-4 text-left">
                                                    <div className="flex items-center gap-3">
                                                        <span className={`text-xs font-bold px-2 py-0.5 rounded uppercase tracking-wider ${getAgentColor(msg.sender)}`}>
                                                            {msg.sender}
                                                        </span>
                                                        <span className="text-sm font-medium text-slate-600 truncate">{getMessageSummary(msg.type, msg.content)}</span>
                                                    </div>
                                                    {isExpanded ? <ChevronDown className="w-4 h-4 text-slate-400" /> : <ChevronRight className="w-4 h-4 text-slate-400" />}
                                                </button>
                                                {isExpanded && (
                                                    <div className="p-4 pt-0 border-t border-dashed border-slate-200/50 mt-1">
                                                        <div className="mt-4 bg-white rounded-xl p-4 border border-slate-100 text-xs font-mono text-slate-600 overflow-x-auto">
                                                            <pre>{JSON.stringify(msg.content, null, 2)}</pre>
                                                        </div>
                                                    </div>
                                                )}
                                            </div>
                                            <div className="mt-1 text-[10px] text-slate-400 font-medium pl-2">
                                                {new Date(msg.timestamp).toLocaleTimeString()} • {msg.type}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                </div>
            )}
        </div>
    );
};

export default AgentConversationViewer;
