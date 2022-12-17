import './styles/globals.css';
import NavBar from './components/NavBar';
import QueryBar from './components/QueryBar';
import { DocumentDto } from './components/DocumentIl';
import Loading from './components/Loading';
import { DocumentDtos } from './components/DocumentDtos';
import { useState } from 'react';

function App() {
  const [documentDtos, setDocumentDtos] = useState([] as DocumentDto[]);
  const [showResults, setShowResults] = useState(false);

  return (
    <div id='app' className='sm:text-center space-x-10'>
      <NavBar />
      <QueryBar 
        setDocumentDtos={function (item: DocumentDto[]): void { 
          setDocumentDtos(item); 
        } } 
        setShowResults={function (show: boolean): void {
          setShowResults(show);
        } }
      />
      {/*\!showResults && <Loading />*/}
      {showResults && <DocumentDtos items={documentDtos}/>}
    </div>
  )
}

export default App;
