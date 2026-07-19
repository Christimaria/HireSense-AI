import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './pages/Home';
import ResumeReview from './pages/ResumeReview';
import Interview from './pages/Interview';
import Roadmap from './pages/Roadmap';

function App() {
  return (
    <Router>
      <div className="flex flex-col min-h-screen">
        <Navbar />
        <main className="flex-grow bg-slate-950">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/resume" element={<ResumeReview />} />
            <Route path="/interview" element={<Interview />} />
            <Route path="/roadmap" element={<Roadmap />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
