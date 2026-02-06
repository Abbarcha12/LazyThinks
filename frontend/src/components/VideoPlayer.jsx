import React, { useRef, useState } from 'react';
import { Play, Pause, Download, Maximize2, Volume2, VolumeX, RefreshCw } from 'lucide-react';

export default function VideoPlayer({ videoUrl, thumbnailUrl, onRegenerate }) {
    const videoRef = useRef(null);
    const [playing, setPlaying] = useState(false);
    const [muted, setMuted] = useState(false);
    const [progress, setProgress] = useState(0);

    const togglePlay = () => {
        if (videoRef.current) {
            if (playing) {
                videoRef.current.pause();
            } else {
                videoRef.current.play();
            }
            setPlaying(!playing);
        }
    };

    const handleTimeUpdate = () => {
        if (videoRef.current) {
            const progress = (videoRef.current.currentTime / videoRef.current.duration) * 100;
            setProgress(progress);
        }
    };

    const toggleMute = () => {
        if (videoRef.current) {
            videoRef.current.muted = !muted;
            setMuted(!muted);
        }
    }

    return (
        <div className="w-full max-w-sm mx-auto bg-black rounded-[32px] overflow-hidden shadow-2xl relative group aspect-[9/16]">
            <video
                ref={videoRef}
                src={videoUrl}
                poster={thumbnailUrl}
                className="w-full h-full object-cover"
                onTimeUpdate={handleTimeUpdate}
                onEnded={() => setPlaying(false)}
                onClick={togglePlay}
                loop
                playsInline
            />

            {/* Overlay Gradient */}
            <div className={`absolute inset-0 bg-gradient-to-b from-black/40 via-transparent to-black/60 pointer-events-none transition-opacity duration-300 ${playing ? 'opacity-0 group-hover:opacity-100' : 'opacity-100'}`}></div>

            {/* Play/Pause Button (Center) */}
            {!playing && (
                <button
                    onClick={togglePlay}
                    className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-16 h-16 bg-white/20 backdrop-blur-md rounded-full flex items-center justify-center hover:scale-110 transition-all z-10"
                >
                    <Play className="w-6 h-6 text-white fill-current ml-1" />
                </button>
            )}

            {/* Controls */}
            <div className={`absolute bottom-0 left-0 w-full p-6 transition-opacity duration-300 ${playing ? 'opacity-0 group-hover:opacity-100' : 'opacity-100'}`}>
                {/* Progress Bar */}
                <div className="w-full h-1 bg-white/30 rounded-full mb-4 overflow-hidden cursor-pointer" onClick={(e) => {
                    const rect = e.currentTarget.getBoundingClientRect();
                    const percent = (e.clientX - rect.left) / rect.width;
                    if (videoRef.current) {
                        videoRef.current.currentTime = percent * videoRef.current.duration;
                    }
                }}>
                    <div className="h-full bg-purple-500 rounded-full" style={{ width: `${progress}%` }}></div>
                </div>

                <div className="flex items-center justify-between text-white">
                    <div className="flex items-center gap-4">
                        <button onClick={togglePlay} className="hover:text-purple-400 transition-colors">
                            {playing ? <Pause className="w-5 h-5 fill-current" /> : <Play className="w-5 h-5 fill-current" />}
                        </button>
                        <button onClick={toggleMute} className="hover:text-purple-400 transition-colors">
                            {muted ? <VolumeX className="w-5 h-5" /> : <Volume2 className="w-5 h-5" />}
                        </button>
                    </div>

                    <div className="flex items-center gap-3">
                        {onRegenerate && (
                            <button
                                onClick={onRegenerate}
                                className="p-2 hover:bg-white/10 rounded-full transition-colors"
                                title="Regenerate"
                            >
                                <RefreshCw className="w-4 h-4" />
                            </button>
                        )}
                        <a
                            href={videoUrl}
                            download
                            className="bg-white text-black px-4 py-2 rounded-full text-xs font-bold flex items-center gap-2 hover:bg-purple-400 hover:text-white transition-all"
                        >
                            <Download className="w-3 h-3" />
                            Download
                        </a>
                    </div>
                </div>
            </div>
        </div>
    );
}
