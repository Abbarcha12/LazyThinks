import React, { useState, useEffect } from 'react';
import { Loader2, CheckCircle2, AlertCircle, Film, Image as ImageIcon, Mic, Scissors, Wand2, RefreshCw } from 'lucide-react';
import axios from 'axios';

export default function VideoProgressTracker({ taskId, onComplete, onError, onRetry }) {
    const [status, setStatus] = useState({
        progress: 0,
        status: 'Initializing...',
        step: 'starting',
        message: 'Starting video generation...'
    });
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!taskId) return;

        const pollStatus = async () => {
            try {
                const response = await axios.get(`http://localhost:8000/api/ugc/video-status/${taskId}`);
                const data = response.data;

                if (data.status === 'failed') {
                    setError(data.message || 'Video generation failed');
                    if (onError) onError(data.message);
                    return; // Stop polling
                }

                setStatus({
                    progress: data.progress || 0,
                    status: data.status,
                    message: data.message,
                    step: data.details?.step || 'processing'
                });

                if (data.status === 'completed') {
                    if (onComplete) onComplete(data.result);
                    return; // Stop polling
                }

                // Continue polling if not complete or failed
                timeoutId = setTimeout(pollStatus, 2000);
            } catch (err) {
                console.error("Error polling status:", err);
                // Don't error out immediately on network glitch, maybe retry
                timeoutId = setTimeout(pollStatus, 3000);
            }
        };

        let timeoutId = setTimeout(pollStatus, 1000);

        return () => clearTimeout(timeoutId);
    }, [taskId]);

    // Steps for visual visualization
    const steps = [
        { id: 'images', label: 'Generating Images', icon: ImageIcon, threshold: 10 },
        { id: 'voice', label: 'Generating Voice', icon: Mic, threshold: 35 },
        { id: 'videos', label: 'Creating Clips', icon: Film, threshold: 45 },
        { id: 'stitching', label: 'Stitching Video', icon: Scissors, threshold: 90 },
        { id: 'thumbnail', label: 'Final Polish', icon: Wand2, threshold: 95 }
    ];

    const getCurrentStepIndex = () => {
        // Find the last step that we've passed or are currently in
        for (let i = steps.length - 1; i >= 0; i--) {
            if (status.progress >= steps[i].threshold) return i;
        }
        return -1;
    };

    const currentStepIndex = getCurrentStepIndex();

    if (error) {
        return (
            <div className="bg-red-50 border border-red-100 rounded-2xl p-6 animate-in fade-in">
                <div className="flex items-center gap-3 text-red-600 mb-2">
                    <AlertCircle className="w-6 h-6" />
                    <h3 className="font-bold">Generation Failed</h3>
                </div>
                <p className="text-red-500 text-sm mb-4">{error}</p>
                {onRetry && (
                    <button
                        onClick={onRetry}
                        className="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-6 rounded-xl transition-colors flex items-center gap-2 shadow-lg shadow-red-500/20"
                    >
                        <RefreshCw className="w-4 h-4" />
                        Retry Generation
                    </button>
                )}
            </div>
        );
    }

    return (
        <div className="bg-white border border-slate-200 rounded-2xl p-8 shadow-lg shadow-purple-500/5 animate-in fade-in space-y-6">
            <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-3">
                    <div className="relative">
                        <div className="w-10 h-10 rounded-full bg-purple-100 flex items-center justify-center">
                            <Loader2 className="w-5 h-5 text-purple-600 animate-spin" />
                        </div>
                    </div>
                    <div>
                        <h3 className="text-lg font-bold text-slate-900">Generating Your Video</h3>
                        <p className="text-sm text-slate-500 animate-pulse">{status.message}</p>
                    </div>
                </div>
                <span className="text-2xl font-black text-purple-600">{Math.round(status.progress)}%</span>
            </div>

            {/* Progress Bar */}
            <div className="h-3 w-full bg-slate-100 rounded-full overflow-hidden">
                <div
                    className="h-full bg-gradient-to-r from-purple-500 to-pink-500 transition-all duration-500 ease-out rounded-full"
                    style={{ width: `${status.progress}%` }}
                />
            </div>

            {/* Steps Visualization */}
            <div className="grid grid-cols-5 gap-2 relative">
                {/* Connecting Line */}
                <div className="absolute top-4 left-0 w-full h-0.5 bg-slate-100 -z-10" />

                {steps.map((step, idx) => {
                    const isCompleted = currentStepIndex > idx;
                    const isCurrent = currentStepIndex === idx;
                    const isActive = isCompleted || isCurrent;
                    const Icon = step.icon;

                    return (
                        <div key={step.id} className="flex flex-col items-center gap-2">
                            <div className={`w-8 h-8 rounded-full flex items-center justify-center transition-all duration-500 ${isActive
                                ? 'bg-purple-600 text-white shadow-lg shadow-purple-500/30 scale-110'
                                : 'bg-slate-100 text-slate-400'
                                }`}>
                                {isCompleted ? <CheckCircle2 className="w-5 h-5" /> : <Icon className="w-4 h-4" />}
                            </div>
                            <span className={`text-[10px] font-bold text-center transition-colors duration-300 ${isActive ? 'text-purple-700' : 'text-slate-400'
                                }`}>
                                {step.label}
                            </span>
                        </div>
                    );
                })}
            </div>

            <div className="bg-slate-50 rounded-xl p-4 border border-slate-100 flex items-start gap-3">
                <InfoIcon className="w-5 h-5 text-slate-400 flex-shrink-0 mt-0.5" />
                <p className="text-xs text-slate-500 leading-relaxed">
                    This process usually takes <span className="font-bold text-slate-700">5-10 minutes</span>.
                    We're generating unique images for each shot, animating them into videos, synthesizing voiceover, and editing it all together with transitions.
                </p>
            </div>
        </div>
    );
}

function InfoIcon({ className }) {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className={className}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z" />
        </svg>
    )
}
