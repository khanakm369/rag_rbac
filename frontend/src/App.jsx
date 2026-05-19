import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import './App.css'
import Signin from './components/Signin'
import Signup from './components/Signup'
import Home from './components/Home'
import Promt from './components/Promt'
function App() {
  return (
  <>

      <nav>
        <Link to="/signin">
          <button>Sign In</button>
        </Link>

        <Link to="/signup">
          <button>Sign Up</button>
        </Link>

        
      </nav>

      <Routes>
        <Route path="/signin" element={<Signin />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/" element={<Home/>} />
        <Route path="/promt" element={<Promt />} />
      </Routes>

    </>
  )
}

export default App