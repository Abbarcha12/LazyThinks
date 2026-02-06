import { useState } from 'react';
import Sidebar from './components/Sidebar';
import ProposalGenerator from './tools/ProposalGenerator';
import UGCVideoGenerator from './tools/UGCVideoGenerator';
import DataAnalytics from './tools/DataAnalytics';
import YoutubeTitleGenerator from './tools/YoutubeTitleGenerator';

function App() {
  const [activeTool, setActiveTool] = useState('proposal-generator');

  const renderTool = () => {
    switch (activeTool) {
      case 'proposal-generator':
        return <ProposalGenerator />;
      case 'ugc-video-generator':
        return <UGCVideoGenerator />;
      case 'youtube-title-generator':
        return <YoutubeTitleGenerator />;
      case 'data-analytics':
        return <DataAnalytics />;
      default:
        return <ProposalGenerator />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex relative overflow-hidden font-sans">
      {/* Background Gradients */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden -z-10 pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-indigo-200/40 rounded-full blur-[128px]"></div>
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-purple-200/40 rounded-full blur-[128px]"></div>
      </div>

      {/* Sidebar */}
      <Sidebar activeTool={activeTool} setActiveTool={setActiveTool} />

      {/* Main Content */}
      <div className="flex-1 md:ml-72 overflow-y-auto h-screen">
        <div className="mx-auto max-w-7xl px-4 py-8 md:px-8">
          {renderTool()}
        </div>
      </div>
    </div>
  );
}

export default App;
