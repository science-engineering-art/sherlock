import './styles/globals.css';
import NavBar from './components/NavBar';
import QueryBar from './components/QueryBar';
import { SearchItem } from './components/SearchItem';
import { SearchResult } from './components/SearchResult';
import { useState } from 'react';

function App() {
  const [searchItems, setSearchItems] = useState([] as SearchItem[]);
  const [showResults, setShowResults] = useState(false);

  return (
    <div id='app' className='sm:text-center space-x-10'>
      <NavBar />
      <QueryBar 
        setSearchItems={function (item: SearchItem[]): void { 
          setSearchItems(item); 
        } } 
        setShowResults={function (show: boolean): void {
          setShowResults(show);
        } }
      />
      {showResults && <SearchResult items={searchItems}/>}
    </div>
  )
}

export default App;
