import { useState } from 'react';
import '../styles/globals.css';
import axios from 'axios';
import { DocumentDto } from './DocumentIl';

export type QueryBarProps = {
  setDocumentDtos: (item: DocumentDto[]) => void;  
  setShowResults: (show: boolean) => void
}

function QueryBar(props: QueryBarProps) {

  const [query, setQuery] = useState('');

  return (
    <div className='sm:text-center space-x-10'>
      <input 
        className="border-4 placeholder:italic placeholder:text-slate-400 
          block bg-white xl:w-11/12 border-slate-300 rounded-3xl py-2 pl-9 
          pr-3 shadow-sm focus:outline-none focus:border-sky-500 
          focus:ring-sky-500 focus:ring-1" 
        placeholder="Search for anything..." 
        type="text"
        onChange={(e) => {
          setQuery(e.target.value);
          props.setShowResults(false);
        }}
      />
      <button 
        id='button-search' 
        className='w-1/12 border-black-300 mt-4 bg-blue-500 hover:bg-blue-600 
        active:bg-blue-700 focus:outline-none focus:ring focus:ring-blue-300 
        rounded-sm'
        onClick={async () => {
          await axios.get('http://localhost:8000/search?query=' +
            encodeURIComponent(query))
            .then((resp) => { 
              props.setDocumentDtos(resp.data.results);
              props.setShowResults(true);})
            .catch((err) => console.log(err.data));
        }}
      >
        Search
      </button>
    </div>
  );
}

export default QueryBar;
