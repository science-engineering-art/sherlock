import { useState } from 'react';
import axios from 'axios';
import { DocumentDto } from './DocumentIl';
import './QueryBar.css'
import ConfigurationModal from "./ConfigurationModal";
import CustomizedDialogs from "./SettingsModal";
import SettingsModal from "./SettingsModal";

export type QueryBarProps = {
  setDocumentDtos: (item: DocumentDto[]) => void;  
  setShowResults: (show: boolean) => void
}

function QueryBar(props: QueryBarProps) {

  const [query, setQuery] = useState(sessionStorage['query']);

  return (
      <div className="container">
        <div className="search">
            <input
            type="text"
            className="searchTerm"
            placeholder="What are you looking for?"
            onChange={(e) => {
              setQuery(e.target.value);
              props.setShowResults(false);
            }}
            />
            <button
            type="submit"
            className="searchButton"
            onClick={async () => {
              sessionStorage[ 'query'] = query

              var url = 'http://localhost:8000/search?' +
                'model='+encodeURIComponent(sessionStorage['model'])+
                '&dataset=' + encodeURIComponent(sessionStorage['dataset']) +
                '&query=' + encodeURIComponent(sessionStorage['query']) + 
                '&pag=' + encodeURIComponent(sessionStorage['pag']);
              if (sessionStorage['model'] === 'clustering')
                 url = 'http://localhost:8000/clustering?' +
                  'dataset=' + encodeURIComponent(sessionStorage['dataset']) +
                  '&query=' + encodeURIComponent(sessionStorage['query']) + 
                  '&cluster=' + encodeURIComponent(sessionStorage['pag']);

              await axios.get(url)
                .then((resp) => {
                  props.setDocumentDtos(resp.data.results);
                  props.setShowResults(true);})
                .catch((err) => console.log(err.data));
            }}
            >
            <i className="fa fa-search"></i>
            </button>
            <SettingsModal></SettingsModal>
        </div>
      </div>
  );
}

export default QueryBar;
