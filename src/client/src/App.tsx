import { useState } from 'react';
import './styles/globals.css';
import axios from 'axios';

function App() {
  const [query, setQuery] = useState('');

  return (
    <div id='wrapper' className='sm:text-center space-x-10'>
      <h1 id='name-engine' className='text-center font-mono font-bold h-30 text-9xl my-20'>Moogle!🔍</h1>
      <input 
        className="border-4 placeholder:italic placeholder:text-slate-400 block bg-white xl:w-11/12 border-slate-300 rounded-3xl py-2 pl-9 pr-3 shadow-sm focus:outline-none focus:border-sky-500 focus:ring-sky-500 focus:ring-1" 
        placeholder="Search for anything..." 
        type="text" 
        name="search"
        onChange={(e) => setQuery(e.target.value)}
      />
      <button 
        id='button-search' 
        className='w-1/12 border-black-300 mt-4 bg-blue-500 hover:bg-blue-600 active:bg-blue-700 focus:outline-none focus:ring focus:ring-blue-300 rounded-sm'
        onClick={async () => {
          await axios.get('http://localhost:8000/search?query='+encodeURIComponent(query))
            .then((resp) => console.log(resp.data))
            .catch((resp) => console.log('Error: '));
        }}
      >
        Search
      </button>
    </div>
  )
}

export default App;
