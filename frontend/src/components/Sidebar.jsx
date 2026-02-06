import { FileText, Menu, X, Video, BarChart3, Youtube } from 'lucide-react';
import { useState } from 'react';

const Sidebar = ({ activeTool, setActiveTool }) => {
    const [isCollapsed, setIsCollapsed] = useState(false);

    const tools = [
        { id: 'proposal-generator', name: 'Proposal Generator', icon: FileText },
        { id: 'ugc-video-generator', name: 'UGC Video Generator', icon: Video },
        { id: 'youtube-title-generator', name: 'YouTube Titles', icon: Youtube },
        { id: 'data-analytics', name: 'Data Analytics', icon: BarChart3 },
    ];

    return (
        <>
            {/* Mobile Toggle */}
            <button
                onClick={() => setIsCollapsed(!isCollapsed)}
                className="fixed top-4 left-4 z-50 md:hidden bg-white/80 backdrop-blur-xl p-2.5 rounded-xl border border-slate-200 shadow-lg text-slate-500 hover:text-indigo-600 transition-all"
            >
                {isCollapsed ? <Menu className="w-5 h-5" /> : <X className="w-5 h-5" />}
            </button>

            {/* Sidebar */}
            <div
                className={`fixed left-0 top-0 h-full bg-white/70 backdrop-blur-2xl border-r border-slate-100 transition-transform duration-300 z-40 ${isCollapsed ? '-translate-x-full md:translate-x-0' : 'translate-x-0'
                    } w-72 flex flex-col shadow-2xl shadow-indigo-100/50`}
            >
                {/* Logo/Brand */}
                <div className="p-8 border-b border-slate-100/50">
                    <div className="flex items-center gap-3 mb-2">
                        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-600 via-indigo-500 to-purple-600 shadow-lg shadow-indigo-500/20 flex items-center justify-center text-white">
                            <span className="font-black text-lg">A</span>
                        </div>
                        <div>
                            <h1 className="text-xl font-bold text-slate-900 tracking-tight">
                                AutomateX
                            </h1>
                        </div>
                    </div>
                    <p className="text-xs text-slate-400 font-medium ml-[52px]">AI Automation Suite</p>
                </div>

                {/* Navigation */}
                <nav className="flex-1 p-6 space-y-2">
                    <p className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-4 px-2">Tools</p>
                    {tools.map((tool) => {
                        const Icon = tool.icon;
                        const isActive = activeTool === tool.id;

                        return (
                            <button
                                key={tool.id}
                                onClick={() => setActiveTool(tool.id)}
                                className={`w-full flex items-center gap-4 px-4 py-3.5 rounded-xl transition-all font-medium duration-200 ${isActive
                                    ? 'bg-indigo-50 text-indigo-600 shadow-sm ring-1 ring-indigo-100'
                                    : 'text-slate-500 hover:bg-slate-50 hover:text-slate-900'
                                    }`}
                            >
                                <Icon className={`w-5 h-5 ${isActive ? 'text-indigo-600' : 'text-slate-400 group-hover:text-slate-600'}`} />
                                <span className="text-sm">{tool.name}</span>
                            </button>
                        );
                    })}
                </nav>

                {/* Footer */}
                <div className="p-6 border-t border-slate-100/50">
                    <div className="bg-slate-50 rounded-xl p-4 border border-slate-100 flex items-center justify-between">
                        <div>
                            <p className="text-xs text-slate-400 font-medium mb-0.5">Version</p>
                            <p className="text-sm font-bold text-slate-700">1.0.0 Beta</p>
                        </div>
                        <div className="w-2 h-2 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.4)]"></div>
                    </div>
                </div>
            </div>
        </>
    );
};

export default Sidebar;
