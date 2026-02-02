import { FileText, Menu, X } from 'lucide-react';
import { useState } from 'react';

const Sidebar = ({ activeTool, setActiveTool }) => {
    const [isCollapsed, setIsCollapsed] = useState(false);

    const tools = [
        { id: 'proposal-generator', name: 'Proposal Generator', icon: FileText },
    ];

    return (
        <>
            {/* Mobile Toggle */}
            <button
                onClick={() => setIsCollapsed(!isCollapsed)}
                className="fixed top-4 left-4 z-50 md:hidden bg-indigo-600/20 backdrop-blur-xl p-2.5 rounded-xl border border-indigo-500/30 hover:bg-indigo-600/30 transition-all"
            >
                {isCollapsed ? <Menu className="w-5 h-5 text-indigo-300" /> : <X className="w-5 h-5 text-indigo-300" />}
            </button>

            {/* Sidebar */}
            <div
                className={`fixed left-0 top-0 h-full bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 border-r border-indigo-500/10 transition-transform duration-300 z-40 ${isCollapsed ? '-translate-x-full md:translate-x-0' : 'translate-x-0'
                    } w-72 flex flex-col shadow-2xl shadow-indigo-950/50`}
            >
                {/* Logo/Brand */}
                <div className="p-8 border-b border-indigo-500/10">
                    <div className="flex items-center gap-3 mb-2">
                        <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 shadow-lg shadow-indigo-500/50 flex items-center justify-center">
                            <span className="text-white font-black text-lg">A</span>
                        </div>
                        <div>
                            <h1 className="text-xl font-black bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
                                AutomateX
                            </h1>
                        </div>
                    </div>
                    <p className="text-xs text-slate-500 font-medium ml-[52px]">AI Automation Suite</p>
                </div>

                {/* Navigation */}
                <nav className="flex-1 p-6 space-y-2">
                    <p className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-4 px-2">Tools</p>
                    {tools.map((tool) => {
                        const Icon = tool.icon;
                        const isActive = activeTool === tool.id;

                        return (
                            <button
                                key={tool.id}
                                onClick={() => setActiveTool(tool.id)}
                                className={`w-full flex items-center gap-4 px-4 py-4 rounded-2xl transition-all font-medium ${isActive
                                        ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-lg shadow-indigo-500/30'
                                        : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-200 border border-transparent hover:border-slate-700'
                                    }`}
                            >
                                <Icon className="w-5 h-5" />
                                <span className="text-sm">{tool.name}</span>
                            </button>
                        );
                    })}
                </nav>

                {/* Footer */}
                <div className="p-6 border-t border-indigo-500/10">
                    <div className="bg-gradient-to-r from-indigo-500/10 to-purple-500/10 rounded-2xl p-4 border border-indigo-500/20">
                        <p className="text-xs text-slate-400 font-medium mb-1">Version</p>
                        <p className="text-sm font-bold text-indigo-300">1.0.0 Beta</p>
                    </div>
                </div>
            </div>
        </>
    );
};

export default Sidebar;
