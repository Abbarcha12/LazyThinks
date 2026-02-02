import { useState } from 'react';
import Sidebar from './components/Sidebar';
import ProposalGenerator from './tools/ProposalGenerator';

function App() {
  const [activeTool, setActiveTool] = useState('proposal-generator');

  const renderTool = () => {
    switch (activeTool) {
      case 'proposal-generator':
        return <ProposalGenerator />;
      default:
        return <ProposalGenerator />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white selection:bg-cyan-500/30 flex relative overflow-hidden font-sans">
      {/* Background Gradients */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden -z-10 pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-purple-600/20 rounded-full blur-[128px]"></div>
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-cyan-600/20 rounded-full blur-[128px]"></div>
      </div>

      {/* Sidebar */}
      <Sidebar activeTool={activeTool} setActiveTool={setActiveTool} />

      {/* Main Content */}
      <div className="flex-1 md:ml-64 overflow-y-auto">
        <div className="container mx-auto px-4">
          {renderTool()}
        </div>
      </div>
    </div>
  );
}

export default App;
