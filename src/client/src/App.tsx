import './styles/globals.css';
import NavBar from './components/NavBar';
import QueryBar from './components/QueryBar';
import { DocumentDto } from './components/DocumentIl';
import Loading from './components/Loading';
import { DocumentDtos } from './components/DocumentDtos';
import { useState } from 'react';
import Pagination from '@mui/material/Pagination';
import * as React from 'react';
import Typography from '@mui/material/Typography';
import Stack from '@mui/material/Stack';
import axios from 'axios';


function App() {
  const [documentDtos, setDocumentDtos] = useState([] as DocumentDto[]);
  const [showResults, setShowResults] = useState(false);
  const [page, setPage] = React.useState(() => {
    if (typeof(sessionStorage['pag']) == 'undefined'){
      sessionStorage['pag'] = 1;
    }
    return sessionStorage['pag']
  });
  const [model, setModel] = React.useState(() =>{
    if (typeof(sessionStorage['model']) == 'undefined'){
      sessionStorage['model'] = 'vector';
    }
    return sessionStorage['model']
  });
  const [dataset, setDataset] = React.useState(() =>{
    if (typeof(sessionStorage['dataset']) == 'undefined'){
      sessionStorage['dataset'] = 'cranfield';
    }
    return sessionStorage['dataset']
  });

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
      {showResults && <DocumentDtos items={documentDtos} setItems={setDocumentDtos}/>}

      <Stack spacing={2}>
        <Pagination 
          count={100} 
          page={page} 
          onChange={async (_, value) => {
              setPage(value);
              await axios.get('http://localhost:8000/search?' +
                'model='+encodeURIComponent(model)+
                '&dataset=' + encodeURIComponent(dataset) +
                '&query=' + encodeURIComponent(sessionStorage['query']) + 
                '&pag=' + encodeURIComponent(value))
                .then((resp) => {
                  setDocumentDtos(resp.data.results);
                  setShowResults(true);
                })
                .catch((err) => console.log(err.data));
            }} 
        />
      </Stack>
      
    </div>
  )
}

export default App;


